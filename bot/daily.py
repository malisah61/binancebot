"""Günlük formasyon araştırması + güncel tarama.

1) Güvenilirlik: 40 coinin 2023'ten bugüne günlük (futures) mumlarında her formasyon olayı tespit edilir.
   Her olay için: 3/7/14 gün sonraki yöne göre getiri, isabet oranı ve formasyonun kendi stop/hedefiyle
   işlem sonucu (R). Zaman bazlı ayrım: ilk %70 eğitim, son %30 TEST. Karşılaştırma tabanı: aynı coinlerde
   rastgele bir günde aynı yönde girmek.
2) Güncel tarama: hacimce ilk 40 coinde son 10 günün formasyonları, destek/direnç, alıcı bölgesi,
   yıllık aralıktaki konum, trend yapısı. Formasyonun geçmiş güvenilirliği yanına yazılır.
Çıktı: state/daily_patterns.json, docs/gunluk/formasyon-YYYY-MM-DD.md, Telegram özeti.
"""
from __future__ import annotations

import io
import json
import os
import sys
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
import binance  # noqa: E402
import patterns as P  # noqa: E402
import research  # noqa: E402
import telegram  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, "data", "cache", "d1")
BASE = "https://data.binance.vision/data/futures/um"
START = datetime(2023, 1, 1, tzinfo=timezone.utc)
HORIZ = (3, 7, 14)


def load_hist(sym, today):
    jobs = []
    m = START
    cur = datetime(today.year, today.month, 1, tzinfo=timezone.utc)
    while m < cur:
        ym = m.strftime("%Y-%m")
        jobs.append((f"{BASE}/monthly/klines/{sym}/1d/{sym}-1d-{ym}.zip", f"{CACHE}/{sym}/{ym}.zip", False))
        m = (m + timedelta(days=32)).replace(day=1)
    d = cur
    while d < today:
        ds = d.strftime("%Y-%m-%d")
        jobs.append((f"{BASE}/daily/klines/{sym}/1d/{sym}-1d-{ds}.zip", f"{CACHE}/{sym}/d{ds}.zip", (today - d).days <= 3))
        d += timedelta(days=1)
    frames = []
    for url, path, recent in jobs:
        p = research.fetch(url, path, recent)
        if p:
            try:
                frames.append(research.read_zip_csv(p, research.KCOLS))
            except Exception:
                pass
    if not frames:
        return None
    k = pd.concat(frames).rename(columns={"open_time": "t", "open": "o", "high": "h", "low": "l", "close": "c", "volume": "v",
                                         "quote_volume": "qv", "taker_buy_quote_volume": "tq"})
    k = k[["t", "o", "h", "l", "c", "v", "qv", "tq"]].apply(pd.to_numeric, errors="coerce").dropna()
    k["t"] = k["t"].astype(np.int64)
    k.loc[k["t"] > 1e14, "t"] //= 1000
    return k.drop_duplicates("t").sort_values("t").reset_index(drop=True)


def study(data):
    rows, base = [], []
    rng = np.random.default_rng(7)
    for sym, k in data.items():
        o, h, l, c = (k[x].values.astype(float) for x in "ohlc")
        t = k["t"].values
        if len(c) < 120:
            continue
        ev, A = P.detect(o, h, l, c)
        fwd = {H: np.r_[c[H:] / c[:-H] - 1, np.full(H, np.nan)] for H in HORIZ}
        for i in range(30, len(c) - 1):
            base.append({"t": t[i], **{f"f{H}": fwd[H][i] for H in HORIZ}})
        for e in ev:
            i = e["i"]
            if i >= len(c) - 1:
                continue
            r = P.trade(h, l, c, i, e["dir"], e["stop"], e["target"])
            # kıyas: aynı stop/hedef mesafesi ve yönle rastgele bir günde girseydin (formasyonun katkısını ayırmak için)
            rr = []
            for _ in range(3):
                j = int(rng.integers(30, len(c) - 2))
                sp, tg = e["stop"] / c[i], e["target"] / c[i]
                x = P.trade(h, l, c, j, e["dir"], c[j] * sp, c[j] * tg)
                if x:
                    rr.append(x[0])
            rows.append({"sym": sym, "t": t[i], "type": e["type"], "dir": e["dir"], **{f"f{H}": fwd[H][i] * e["dir"] for H in HORIZ},
                         "R": r[0] if r else np.nan, "days": r[1] if r else np.nan, "out": r[2] if r else None,
                         "R_rand": float(np.mean(rr)) if rr else np.nan})
    E, B = pd.DataFrame(rows), pd.DataFrame(base)
    split = np.quantile(B["t"], 0.7)
    out = {"split": int(split), "base": {}, "types": {}}
    for part, cond in (("train", lambda x: x["t"] < split), ("test", lambda x: x["t"] >= split)):
        b = B[cond(B)]
        out["base"][part] = {f"f{H}": round(float(b[f"f{H}"].mean()) * 100, 2) for H in HORIZ}
    for typ, g in E.groupby("type"):
        st = {"name": P.NAMES[typ], "dir": int(g["dir"].iloc[0])}
        for part, cond in (("train", lambda x: x["t"] < split), ("test", lambda x: x["t"] >= split)):
            x = g[cond(g)]
            bdir = {H: out["base"][part][f"f{H}"] * st["dir"] for H in HORIZ}  # rastgele günde aynı yön
            rr = x["R"].dropna()
            st[part] = {"n": int(len(x)),
                        **{f"hit{H}": round(float((x[f"f{H}"] > 0).mean() * 100), 1) if len(x) else None for H in HORIZ},
                        **{f"ret{H}": round(float(x[f"f{H}"].mean() * 100), 2) if len(x) else None for H in HORIZ},
                        **{f"edge{H}": round(float(x[f"f{H}"].mean() * 100 - bdir[H]), 2) if len(x) else None for H in HORIZ},
                        "trade_n": int(len(rr)), "avg_R": round(float(rr.mean()), 3) if len(rr) else None,
                        "win": round(float((rr > 0).mean() * 100), 1) if len(rr) else None,
                        "pf": round(float(rr[rr > 0].sum() / -rr[rr < 0].sum()), 2) if (rr < 0).any() else None,
                        "rand_R": round(float(x["R_rand"].mean()), 3) if x["R_rand"].notna().any() else None}
            st[part]["edge_R"] = round(st[part]["avg_R"] - st[part]["rand_R"], 3) if st[part]["avg_R"] is not None and st[part]["rand_R"] is not None else None
        tr, te = st["train"], st["test"]
        ok = lambda p: p["n"] >= 20 and (p["avg_R"] or -9) > 0.1 and (p["edge_R"] or -9) > 0.1 and (p["edge7"] or -9) > 0
        st["verdict"] = ("güvenilir" if ok(tr) and ok(te) else
                         "az örnek" if tr["n"] < 20 or te["n"] < 20 else
                         "zayıf/karışık" if ((tr["edge_R"] or -9) > 0) != ((te["edge_R"] or -9) > 0) else
                         "işe yaramıyor" if (te["edge_R"] or -9) <= 0 else "zayıf/karışık")
        out["types"][typ] = st
    return out


def scan(stats, n=40):
    out = []
    tick = binance.top_usdt(n)
    for x in tick:
        s = x["symbol"]
        try:
            k = pd.DataFrame(binance.klines(s, "1d", 1000))
        except Exception as e:
            print("hata", s, e)
            continue
        k = k[k["t"] + 86_400_000 <= time.time() * 1000].reset_index(drop=True)  # yalnız kapanmış günler
        if len(k) < 60:
            continue
        o, h, l, c, v = (k[x].values.astype(float) for x in "ohlcv")
        ev, A = P.detect(o, h, l, c)
        recent = [e for e in ev if e["i"] >= len(c) - 10]
        lv = P.levels(h, l, c, v, k["tq"].values.astype(float), k["qv"].values.astype(float))
        tr = P.trend_state(h, l, c)
        items = []
        for e in recent:
            stt = stats["types"].get(e["type"], {})
            items.append({"type": e["type"], "name": P.NAMES[e["type"]], "dir": e["dir"], "days_ago": int(len(c) - 1 - e["i"]),
                          "date": datetime.fromtimestamp(k["t"].iloc[e["i"]] / 1000, timezone.utc).strftime("%d.%m"),
                          "stop": e["stop"], "target": e["target"], "info": e.get("info", ""),
                          "verdict": stt.get("verdict"), "test": stt.get("test")})
        out.append({"symbol": s, "price": float(c[-1]), "atr_pct": round(float(A[-1] / c[-1] * 100), 2), "events": items, "levels": lv, "trend": tr})
    return out


def fmt(x):
    return f"{x:,.2f}" if x >= 100 else f"{x:.4f}" if x >= 1 else f"{x:.6g}"


def report(stats, sc, today):
    L = [f"# 📐 Günlük Formasyon Raporu — {today.strftime('%d.%m.%Y')}", "",
         f"Geçmiş: {stats['n_coins']} coin, 2023'ten bugüne günlük mumlar. Eğitim/TEST ayrımı {datetime.fromtimestamp(stats['split'] / 1000, timezone.utc).strftime('%d.%m.%Y')}.",
         f"Taban (rastgele gün, 7 gün sonra): eğitim %{stats['base']['train']['f7']}, test %{stats['base']['test']['f7']}", "",
         "## Formasyonlar kriptoda işe yarıyor mu?", "",
         "| Formasyon | Yön | Eğitim n / 7g isabet / ort R (rastgele) | TEST n / 7g isabet / ort R (rastgele) / PF | Karar |", "|---|---|---|---|---|"]
    for typ, s in sorted(stats["types"].items(), key=lambda kv: -((kv[1]["test"]["avg_R"] or -9))):
        tr, te = s["train"], s["test"]
        L.append(f"| {s['name']} | {'↑' if s['dir'] > 0 else '↓'} | {tr['n']} / %{tr['hit7']} / {tr['avg_R']} ({tr['rand_R']}) | {te['n']} / %{te['hit7']} / {te['avg_R']} ({te['rand_R']}) / {te['pf']} | {s['verdict']} |")
    L += ["", "İsabet: 7 gün sonra fiyat beklenen yönde mi. Ort R: formasyonun kendi stop/hedefiyle işlemin ortalama sonucu (komisyon dahil; R = risk birimi).",
          "Parantez: aynı stop/hedef mesafesiyle RASTGELE bir günde girseydin. Formasyonun gerçek katkısı = ort R − rastgele. 'Güvenilir' için hem eğitimde hem testte bu fark > 0,1R olmalı.", "",
          "## Bugünün tablosu (ilk 40 coin)", ""]
    act = [x for x in sc if x["events"]]
    for x in sorted(act, key=lambda x: min(e["days_ago"] for e in x["events"])):
        lv, tr = x["levels"], x["trend"]
        evs = "; ".join(f"{'🟢' if e['dir'] > 0 else '🔴'} {e['name']} ({e['date']}{', geçmişte ' + e['verdict'] if e.get('verdict') else ''})" for e in x["events"])
        L.append(f"- **{x['symbol'].replace('USDT', '')}** {fmt(x['price'])} — {evs}. Trend: {tr['structure']}, "
                 f"{'EMA200 üstü' if tr['above200'] else 'EMA200 altı'}. Yıllık aralığın %{int(lv['range_pos'] * 100)}'inde "
                 f"(tepeden %{lv['from_hi']}). Destek {', '.join(fmt(s) for s in lv['support'][:2]) or '-'} · direnç {', '.join(fmt(s) for s in lv['resistance'][:2]) or '-'}"
                 + (f" · alıcı bölgesi {fmt(lv['accumulation']['price'])}" if lv.get("accumulation") else ""))
    L += ["", "Simülasyon/araştırmadır, yatırım tavsiyesi değildir."]
    return "\n".join(L)


def main():
    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    syms = [x["symbol"] for x in binance.top_usdt(55)]
    with ThreadPoolExecutor(16) as ex:
        hist = dict(zip(syms, ex.map(lambda s: load_hist(s, today), syms)))
    data = {s: k for s, k in hist.items() if k is not None and len(k) >= 200}
    data = dict(list(data.items())[:40])
    print(f"{len(data)} coin günlük geçmişi")
    stats = study(data)
    stats["n_coins"] = len(data)
    sc = scan(stats)
    os.makedirs(os.path.join(ROOT, "state"), exist_ok=True)
    json.dump({"time": int(time.time() * 1000), "stats": stats, "scan": sc}, open(os.path.join(ROOT, "state", "daily_patterns.json"), "w"), ensure_ascii=False, default=float)
    md = report(stats, sc, today)
    path = f"docs/gunluk/formasyon-{(today + timedelta(hours=3)).strftime('%Y-%m-%d')}.md"
    os.makedirs(os.path.join(ROOT, "docs", "gunluk"), exist_ok=True)
    open(os.path.join(ROOT, path), "w", encoding="utf-8").write(md)
    print(md)
    chat = os.environ.get("TELEGRAM_CHAT_ID") or (json.load(open(os.path.join(ROOT, "state", "futures.json"))).get("chat_id") if os.path.exists(os.path.join(ROOT, "state", "futures.json")) else None)
    import notify
    telegram.send(chat, notify.md_to_tg(md))


if __name__ == "__main__":
    main()
