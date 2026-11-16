"""Ani hareket momentumu: ani yükselişe LONG / ani düşüşe SHORT — günde tek işlem, 10x, futures, 1 yıl.

Tetik (1 saatlik mumlar, hacimde ilk MO_COINS futures coini): son 4 saatte ≥ X% hareket (X = 5/8/12) ve isteğe bağlı
hacim patlaması (son 4 saatin hacmi ≥ 2× önceki 7 günün 4 saatlik ortalaması). Gün içinde (TR saatiyle) İLK tetik alınır,
o gün başka işlem açılmaz. Yön: devam (yükselişe long / düşüşe short) — kıyas için ters yön (sönmeye karşı işlem) de ölçülür.
Giriş: tetik mumunun kapanışı (piyasa). Stop: 1.5 × ATR(1s) veya 2.5 × ATR(1s). Hedef 1.5R (yarısı, stop girişe) / 3R, en çok 24 saat.
10x izole: fiyat stoptan önce %9.5 ters giderse tasfiye (marjin biter). Komisyon %0.1 + kayma + funding dahil.
Marjin: bakiyenin %10 / %20'si. Eğitim %70 → karar TEST'te (n≥40, ort>0, PF>1.05, eğitimde ort>0).
"""
from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime, timedelta, timezone

os.environ.setdefault("EX_COINS", os.environ.get("MO_COINS", "150"))
os.environ.setdefault("EX_DAYS", "365")
os.environ.setdefault("EX_MET_DAYS", "2")

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
import extreme as X  # noqa: E402
import telegram  # noqa: E402
import tf30  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEV = 10
LIQ = 1 / LEV - 0.005
HOLD = 24
THS = (0.05, 0.08, 0.12)


def events(data, rank, btc):
    rows = []
    for s, (k, market) in data.items():
        if market != "fut":
            continue
        o, h, l, c = (k[q].values.astype(float) for q in "ohlc")
        qv = k["qv"].values.astype(float)
        t = k["t"].values
        n = len(c)
        if n < 400:
            continue
        a = X.atr(h, l, c)
        r4 = c / np.r_[np.full(4, np.nan), c[:-4]] - 1
        v4 = pd.Series(qv).rolling(4).sum().values
        v7 = pd.Series(qv).rolling(168).sum().shift(4).values / 42
        rv = v4 / np.maximum(v7, 1e-9)
        fu = np.nan_to_num(k["funding"].values.astype(float)) if "funding" in k else np.zeros(n)
        tier = X.tier_of(rank.get(s, 999))
        cost = X.FEE + 2 * X.SLIP[tier]
        for th in THS:
            hit = np.abs(r4) >= th
            prev = np.r_[False, hit[:-1]]
            for i in np.flatnonzero(hit & ~prev):
                if i < 200 or i >= n - 2:
                    continue
                mv = 1 if r4[i] > 0 else -1
                for side in ("devam", "ters"):
                    d = mv if side == "devam" else -mv
                    for sm in (1.5, 2.5):
                        e = c[i]
                        stop = e - d * sm * a[i]
                        r = X.sim(o, h, l, c, i, d, e, stop, "mkt", cost, float(fu[i]), hold=HOLD)
                        if not r.get("filled"):
                            continue
                        liq = r["mae"] >= LIQ
                        roe = -1.0 if liq else LEV * r["R"] * r["risk"]
                        rows.append({"sym": s, "t": int(t[i]), "t_exit": int(t[min(r["start"] + r["bars"] - 1, n - 1)]), "th": th, "side": side,
                                     "sm": sm, "dir": d, "rv": float(rv[i]), "btc_ok": bool(np.sign(btc.get(int(t[i]), 0)) == d),
                                     "R": r["R"], "roe": max(roe, -1.0), "liq": liq, "move": float(r4[i] * 100), "tier": tier})
    return pd.DataFrame(rows)


def one_per_day(D):
    D = D.sort_values(["t", "move"], key=lambda col: col if col.name == "t" else -col.abs())
    day = (D["t"] // 1000 + 3 * 3600) // 86400
    return D[~day.duplicated()]


def analyze(E, split):
    res = {}
    for th in THS:
        for side in ("devam", "ters"):
            for sm in (1.5, 2.5):
                for vf in (False, True):
                    for bf in (False, True):
                        D = E[(E["th"] == th) & (E["side"] == side) & (E["sm"] == sm)]
                        if vf:
                            D = D[D["rv"] >= 2]
                        if bf:
                            D = D[D["btc_ok"]]
                        D = one_per_day(D)
                        T = D.to_dict("records")
                        tr, te = [x for x in T if x["t"] < split], [x for x in T if x["t"] >= split]
                        key = f"{th}|{side}|{sm}|{int(vf)}|{int(bf)}"
                        desc = (f"4 saatte %{int(th*100)}+ hareket → {'aynı yöne (yükselişe LONG / düşüşe SHORT)' if side == 'devam' else 'ters yöne'}"
                                f", stop {sm} ATR{', hacim ≥2x' if vf else ''}{', BTC aynı yönde' if bf else ''}")
                        res[key] = {"desc": desc, "side": side, "train": tf30.tstats(tr), "test": tf30.tstats(te), "liq": int(sum(x["liq"] for x in T)),
                                    "per_day": round(len(T) / 365, 2),
                                    "r10": {"eğitim": tf30.replay(tr, 300, 0.10, 1), "TEST": tf30.replay(te, 300, 0.10, 1), "yıl": tf30.replay(T, 300, 0.10, 1)},
                                    "r20": {"yıl": tf30.replay(T, 300, 0.20, 1), "TEST": tf30.replay(te, 300, 0.20, 1)}}
    cand = [k for k, v in res.items() if v["side"] == "devam" and v["train"].get("n", 0) >= 60]
    pick = max(cand, key=lambda k: res[k]["train"]["avg_roe"]) if cand else None
    te = res[pick]["test"] if pick else {}
    adopted = bool(pick and te.get("n", 0) >= 40 and te["avg_roe"] > 0 and (te.get("pf") or 0) > 1.05 and res[pick]["train"]["avg_roe"] > 0)
    return {"rules": res, "pick": pick, "adopted": adopted}


def to_md(r):
    d = datetime.fromtimestamp(r["time"] / 1000, timezone.utc) + timedelta(hours=3)
    sp = datetime.fromtimestamp(r["split"] / 1000, timezone.utc)
    fs = tf30.fs2
    L = [f"# Ani hareket momentumu — günde 1 işlem, 10x futures ({d:%d.%m.%Y})", "",
         f"{r['coins']} futures coini, son 365 gün, 1s mum. Eğitim → {sp:%d.%m.%Y} → TEST. 10x izole (%9.5 ters harekette tasfiye), "
         "komisyon + kayma + funding dahil. Getiriler marjine göre (işlem başı).", "",
         "## Aynı yöne (yükselişe LONG / düşüşe SHORT) — tüm varyantlar", "",
         "| Kural | günde | Eğitim | TEST | Tasfiye | 300$, %10 marjin: eğitim / TEST / yıl | %20 marjin yıl |", "|---|---|---|---|---|---|---|"]
    rows = sorted(r["rules"].items(), key=lambda kv: -(kv[1]["train"].get("avg_roe") or -99))
    for side in ("devam", "ters"):
        if side == "ters":
            L += ["", "## Kıyas: ters yöne (yükselişe SHORT / düşüşe LONG) — en iyi 8", "", "| Kural | günde | Eğitim | TEST | Tasfiye | 300$, %10: eğitim / TEST / yıl | %20 yıl |", "|---|---|---|---|---|---|---|"]
        cnt = 0
        for k, v in rows:
            if v["side"] != side or not v["train"].get("n"):
                continue
            a = v["r10"]
            L.append(f"| {v['desc']} | {v['per_day']} | {fs(v['train'])} | {fs(v['test'])} | {v['liq']} | %{a['eğitim']['ret']:+} / %{a['TEST']['ret']:+} / %{a['yıl']['ret']:+} (düşüş %{a['yıl']['mdd']}) | %{v['r20']['yıl']['ret']:+} (düşüş %{v['r20']['yıl']['mdd']}) |")
            cnt += 1
            if (side == "devam" and cnt >= 24) or (side == "ters" and cnt >= 8):
                break
    p = r["pick"]
    if p:
        v = r["rules"][p]
        L += ["", f"**Eğitimde en iyi (aynı yön):** {v['desc']} → " + ("✅ TEST'te DOĞRULANDI" if r["adopted"] else "❌ TEST'te tutmadı"),
              f"- Eğitim: {fs(v['train'])}", f"- TEST: {fs(v['test'])}"]
    L += ["", "_Simülasyondur, yatırım tavsiyesi değildir._"]
    return "\n".join(L)


def main():
    t0 = time.time()
    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    data, rank = X.load_all(today)
    bk = data["BTCUSDT"][0]
    bc = bk["c"].values.astype(float)
    btc = dict(zip(bk["t"].values.astype(int), bc / np.r_[np.full(24, np.nan), bc[:-24]] - 1))
    E = events(data, rank, btc)
    start = int((today - timedelta(days=365)).timestamp() * 1000)
    E = E[E["t"] >= start]
    split = int(start + 0.7 * (today.timestamp() * 1000 - start))
    r = analyze(E, split)
    r.update(time=int(time.time() * 1000), split=split, coins=sum(1 for v in data.values() if v[1] == "fut"))
    json.dump(r, open(os.path.join(ROOT, "state", "momentum.json"), "w"), ensure_ascii=False, default=float)
    md = to_md(r)
    open(os.path.join(ROOT, "docs", "arastirma", f"ani-hareket-10x-{(today + timedelta(hours=3)):%Y-%m-%d}.md"), "w", encoding="utf-8").write(md)
    print(md)
    import notify
    chat = os.environ.get("TELEGRAM_CHAT_ID") or json.load(open(os.path.join(ROOT, "state", "futures.json"))).get("chat_id")
    telegram.send(chat, notify.md_to_tg(md))
    print(f"toplam {time.time()-t0:.0f} sn")


if __name__ == "__main__":
    main()
