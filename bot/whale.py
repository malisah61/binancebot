"""Balina izi araştırması (4 saatlik grafik, 1 yıl, hacme göre ilk WH_COINS futures coini).

Balina göstergeleri (Binance futures arşivinden, sinyal anında bilinen):
  tls_chg : Top trader (en büyük %20 hesap) long/short POZİSYON oranının 24 saatlik değişimi
  oi24    : Açık pozisyon (OI) 24 saatlik değişimi — yeni büyük pozisyon açılıyor mu
  taker_z : Son 24 saatteki agresif alım oranının önceki 7 güne göre z-puanı (büyük piyasa emirleri)
  rvol    : Son 24 saatin hacmi / önceki 7 günün günlük ortalaması
  rel     : Coinin 24s getirisi − BTC'nin 24s getirisi ("farklı hareket")
Konum: 30 günlük aralıkta dibe yakın (alt %15/%25) → LONG adayı; tepeye yakın (üst %15/%25) → SHORT adayı.
Kurallar: yalnız konum (balinasız, kıyas için) + 5 balina koşulu × 2 konum eşiği × 2 giriş (piyasa / 0.5 ATR limit).
Stop yapısal (son 24 saatin dibi/tepesi ± 0.5 ATR), hedef 1.5R (yarısı, stop girişe) ve 3R, en çok 7 gün, 3x.
Eğitim ilk %70, karar TEST'te (n≥40, ort getiri>0, PF>1.05, eğitimde ort>0). Gerçek hesap kurallarıyla yeniden oynatılır.
"""
from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime, timedelta, timezone

os.environ.setdefault("EX_COINS", os.environ.get("WH_COINS", "80"))
os.environ.setdefault("EX_DAYS", "365")
os.environ.setdefault("EX_MET_DAYS", "365")

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
import extreme as X  # noqa: E402
import telegram  # noqa: E402
import tf30  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H4 = 4 * 3_600_000
DAYS = int(os.environ["EX_DAYS"])
HOLD = 42          # 7 gün
LEV = 3
WHALE = {
    "konum": "Yalnız konum (balina şartı yok — kıyas)",
    "tls": "Top trader pozisyon oranı yön değiştiriyor (24s ≥%5)",
    "oi_taker": "OI artıyor (≥%3) + agresif alım/satım patlaması (z≥1)",
    "rvol_taker": "Hacim patlaması (≥2x) + agresif alım/satım (z≥1)",
    "tls_oi": "Top trader yönü + OI artışı birlikte",
    "rel": "BTC'den farklı hareket (24s ≥%3 ayrışma) + hacim ≥1.5x",
}
FEATS = {"tls_chg": "Top trader L/S değişimi 24s", "oi24": "OI değişimi 24s %", "taker_z": "Agresif alım z-puanı",
         "rvol": "Hacim patlaması (x)", "rel": "BTC'ye göre ayrışma 24s %", "pos": "30g aralıkta konum", "fund": "Funding"}


def to4h(k):
    g = k.assign(b=k["t"] // H4 * H4).groupby("b")
    agg = {"o": ("o", "first"), "h": ("h", "max"), "l": ("l", "min"), "c": ("c", "last"), "qv": ("qv", "sum"), "tq": ("tq", "sum"), "n": ("c", "size")}
    for col, how in (("oi", "last"), ("tls", "last"), ("gls", "last"), ("funding", "mean")):
        if col in k:
            agg[col] = (col, how)
    d = g.agg(**agg).reset_index().rename(columns={"b": "t"})
    return d[d["n"] == 4].drop(columns="n").reset_index(drop=True)


def features(d, btc):
    c, h, l = (d[q].values.astype(float) for q in "chl")
    a = X.atr(h, l, c)
    lo30, hi30 = X.roll_min(l, 180), X.roll_max(h, 180)
    f = pd.DataFrame({"t": d["t"].values})
    f["pos"] = (c - lo30) / np.maximum(hi30 - lo30, 1e-12)
    qv, tq = d["qv"].values.astype(float), d["tq"].values.astype(float)
    v6 = pd.Series(qv).rolling(6).sum().values
    v42 = pd.Series(qv).rolling(42).sum().shift(6).values / 7
    f["rvol"] = v6 / np.maximum(v42, 1e-9)
    tk = pd.Series(tq).rolling(6).sum() / pd.Series(qv).rolling(6).sum().clip(lower=1e-9)
    tk_bar = pd.Series(tq / np.maximum(qv, 1e-9))
    m, s = tk_bar.rolling(42).mean().shift(6), tk_bar.rolling(42).std().shift(6)
    f["taker_z"] = ((tk - m) / s.clip(lower=1e-4)).values
    for col, name in (("oi", "oi24"), ("tls", "tls_chg")):
        x = d[col].values.astype(float) if col in d else np.full(len(c), np.nan)
        f[name] = (x / np.r_[np.full(6, np.nan), x[:-6]] - 1) * (100 if name == "oi24" else 1)
    ret24 = (c / np.r_[np.full(6, np.nan), c[:-6]] - 1) * 100
    f["rel"] = ret24 - np.array([btc.get(t, np.nan) for t in d["t"].values])
    f["fund"] = d["funding"].values.astype(float) if "funding" in d else np.nan
    return f, a, c, h, l, d["o"].values.astype(float)


def whale_ok(name, f, d):
    """d=+1 (dipte long) için balina şartı; d=-1 için ayna."""
    z, oi, tl, rv, rel = (f[q].values for q in ("taker_z", "oi24", "tls_chg", "rvol", "rel"))
    if name == "konum":
        return np.ones(len(f), bool)
    if name == "tls":
        return d * tl >= 0.05
    if name == "oi_taker":
        return (oi >= 3) & (d * z >= 1)
    if name == "rvol_taker":
        return (rv >= 2) & (d * z >= 1)
    if name == "tls_oi":
        return (d * tl >= 0.05) & (oi >= 3)
    if name == "rel":
        return (d * rel >= 3) & (rv >= 1.5)


def run(data, rank, btc):
    rows, samples = {}, []
    for s, (k, market) in data.items():
        if market != "fut" or "oi" not in k or k["oi"].notna().sum() < 1000:
            continue
        d = to4h(k)
        if len(d) < 400:
            continue
        f, a, c, h, l, o = features(d, btc)
        t = d["t"].values
        tier = X.tier_of(rank.get(s, 999))
        cost = X.FEE + 2 * X.SLIP[tier]
        fu = np.nan_to_num(f["fund"].values.astype(float))
        lo6, hi6 = X.roll_min(l, 6), X.roll_max(h, 6)
        pos = f["pos"].values
        for dirn in (1, -1):
            for P in (0.15, 0.25):
                near = (pos <= P) if dirn == 1 else (pos >= 1 - P)
                for w in WHALE:
                    sig = near & whale_ok(w, f, dirn) & ~np.isnan(pos)
                    sig[:200] = False
                    for entry in ("mkt", "lim"):
                        key = f"{'L' if dirn == 1 else 'S'}|{w}|{P}|{entry}"
                        last = -10 ** 9
                        for i in np.flatnonzero(sig):
                            if i - last < 12 or i >= len(c) - 2:
                                continue
                            last = i
                            if entry == "mkt":
                                e = c[i]
                            else:
                                e = c[i] - dirn * 0.5 * a[i]
                            stop = (min(lo6[i], e - a[i]) - 0.5 * a[i]) if dirn == 1 else (max(hi6[i], e + a[i]) + 0.5 * a[i])
                            r = X.sim(o, h, l, c, i, dirn, e, stop, entry, cost, fu[i] * 4, hold=HOLD, wait=3)
                            if not r.get("filled"):
                                continue
                            tr = {"sym": s, "t": int(t[min(r["start"], len(t) - 1)]), "t_exit": int(t[min(r["start"] + r["bars"] - 1, len(t) - 1)]),
                                  "dir": dirn, "R": r["R"], "roe": LEV * r["R"] * r["risk"], "liq": False}
                            rows.setdefault(key, []).append(tr)
                            if w == "konum" and entry == "mkt" and P == 0.25:
                                samples.append({**{q: (float(f[q].iloc[i]) if f[q].iloc[i] == f[q].iloc[i] else np.nan) for q in FEATS},
                                                "t": int(t[i]), "dir": dirn, "win": r["R"] > 0, "R": r["R"]})
    return rows, pd.DataFrame(samples)


def compare(S, split):
    out = []
    for dirn in (1, -1):
        D = S[S["dir"] == dirn]
        for q, nm in FEATS.items():
            row = {"dir": "LONG (dipte)" if dirn == 1 else "SHORT (tepede)", "f": q, "name": nm}
            ok = True
            for part, P in (("train", D[D["t"] < split]), ("test", D[D["t"] >= split])):
                wv, lv = P.loc[P["win"], q].dropna(), P.loc[~P["win"], q].dropna()
                if len(wv) < 15 or len(lv) < 15:
                    ok = False
                    break
                sd = np.sqrt((wv.var() + lv.var()) / 2) or 1e-9
                row[part] = {"win": round(float(wv.median()), 3), "loss": round(float(lv.median()), 3), "d": round(float((wv.mean() - lv.mean()) / sd), 2)}
            if ok:
                row["stable"] = bool(np.sign(row["train"]["d"]) == np.sign(row["test"]["d"]) and min(abs(row["train"]["d"]), abs(row["test"]["d"])) >= 0.15)
                out.append(row)
    return out


def analyze(data, rank, btc, split):
    rows, S = run(data, rank, btc)
    res = {}
    for key, T in rows.items():
        dirn, w, P, entry = key.split("|")
        tr, te = [x for x in T if x["t"] < split], [x for x in T if x["t"] >= split]
        res[key] = {"desc": f"{'LONG dibe yakın' if dirn == 'L' else 'SHORT tepeye yakın'} (%{int(float(P)*100)}) · {WHALE[w]} · {'piyasa' if entry == 'mkt' else '0.5 ATR limit'}",
                    "w": w, "train": tf30.tstats(tr), "test": tf30.tstats(te), "replay_test": tf30.replay(te), "replay_all": tf30.replay(T)}
    cand = [k for k, v in res.items() if v["train"].get("n", 0) >= 100]
    pick = max(cand, key=lambda k: res[k]["train"]["avg_roe"]) if cand else None
    te = res[pick]["test"] if pick else {}
    adopted = bool(pick and te.get("n", 0) >= 40 and te["avg_roe"] > 0 and (te.get("pf") or 0) > 1.05 and res[pick]["train"]["avg_roe"] > 0)
    return {"rules": res, "pick": pick, "adopted": adopted, "compare": compare(S, split) if len(S) else []}


def to_md(r):
    d = datetime.fromtimestamp(r["time"] / 1000, timezone.utc) + timedelta(hours=3)
    sp = datetime.fromtimestamp(r["split"] / 1000, timezone.utc)
    fs = tf30.fs2
    L = [f"# Balina izi — 4 saatlik grafik, dip/tepe yakını ({d:%d.%m.%Y})", "",
         f"{r['coins']} futures coini (hacme göre), son {DAYS} gün. Eğitim → {sp:%d.%m.%Y} → TEST. 3x, komisyon + kayma + funding dahil.", "",
         "## Balina izi işe yarıyor mu? (dibe/tepeye yakın tüm durumlarda kazanan vs kaybeden; d = etki büyüklüğü, ✓ iki dönemde aynı yönde ≥0.15)", "",
         "| Yön | Gösterge | Kazanan (TEST medyan) | Kaybeden | d eğitim / TEST | |", "|---|---|---|---|---|---|"]
    for c in r["compare"]:
        L.append(f"| {c['dir']} | {c['name']} | {c['test']['win']} | {c['test']['loss']} | {c['train']['d']} / {c['test']['d']} | {'✓' if c['stable'] else ''} |")
    for dl, title in (("L", "LONG — dibe yakın"), ("S", "SHORT — tepeye yakın")):
        L += ["", f"## {title} (konum eşiği %25, piyasa girişi)", "", "| Balina şartı | Eğitim | TEST | Gerçek kurallarla TEST dönemi |", "|---|---|---|---|"]
        for w in WHALE:
            v = r["rules"].get(f"{dl}|{w}|0.25|mkt")
            if v:
                b = v["replay_test"]
                L.append(f"| {WHALE[w]} | {fs(v['train'])} | {fs(v['test'])} | %{b['ret']:+} (düşüş %{b['mdd']}) |")
    good = sorted([(k, v) for k, v in r["rules"].items() if v["test"].get("n", 0) >= 40 and v["test"]["avg_roe"] > 0 and (v["test"].get("pf") or 0) > 1.05
                   and (v["train"].get("avg_roe") or -1) > 0 and v["train"].get("n", 0) >= 60], key=lambda kv: -kv[1]["test"]["pf"])
    L += ["", "## Hem eğitimde hem TEST'te kârlı kurallar (bilgi amaçlı)", ""]
    L += [f"- {v['desc']} — eğitim {fs(v['train'])} · TEST {fs(v['test'])} · gerçek kurallarla TEST %{v['replay_test']['ret']:+}" for k, v in good[:10]] or ["- Yok."]
    p = r["pick"]
    if p:
        v = r["rules"][p]
        L += ["", f"**Eğitimde en iyi:** {v['desc']} → " + ("✅ TEST'te DOĞRULANDI" if r["adopted"] else "❌ TEST'te tutmadı"),
              f"- Eğitim: {fs(v['train'])}", f"- TEST: {fs(v['test'])}"]
    L += ["", "_Simülasyondur, yatırım tavsiyesi değildir._"]
    return "\n".join(L)


def main():
    t0 = time.time()
    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    data, rank = X.load_all(today)
    bk = to4h(data["BTCUSDT"][0])
    bc = bk["c"].values.astype(float)
    btc = dict(zip(bk["t"].values, (bc / np.r_[np.full(6, np.nan), bc[:-6]] - 1) * 100))
    start = int((today - timedelta(days=DAYS)).timestamp() * 1000)
    split = int(start + 0.7 * (today.timestamp() * 1000 - start))
    r = analyze(data, rank, btc, split)
    r.update(time=int(time.time() * 1000), split=split, coins=sum(1 for v in data.values() if v[1] == "fut"))
    json.dump(r, open(os.path.join(ROOT, "state", "whale.json"), "w"), ensure_ascii=False, default=float)
    md = to_md(r)
    os.makedirs(os.path.join(ROOT, "docs", "arastirma"), exist_ok=True)
    open(os.path.join(ROOT, "docs", "arastirma", f"balina-4s-{(today + timedelta(hours=3)):%Y-%m-%d}.md"), "w", encoding="utf-8").write(md)
    print(md)
    import notify
    chat = os.environ.get("TELEGRAM_CHAT_ID") or json.load(open(os.path.join(ROOT, "state", "futures.json"))).get("chat_id")
    telegram.send(chat, notify.md_to_tg(md))
    print(f"toplam {time.time()-t0:.0f} sn")


if __name__ == "__main__":
    main()
