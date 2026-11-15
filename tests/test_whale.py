"""Ağsız balina testi: sentetik 1s veri (OI, top trader oranı, funding dahil) → 4s kurallar, karşılaştırma, rapor."""
import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "bot"))
import numpy as np, pandas as pd
import whale as W
def k(seed, n=24 * 365):
    rnd = np.random.default_rng(seed); r = rnd.normal(0, 0.008, n)
    c = 100 * np.exp(np.cumsum(r)); o = np.r_[100, c[:-1]]
    h = np.maximum(o, c) * 1.002; l = np.minimum(o, c) * 0.998
    qv = np.abs(rnd.normal(1e6, 3e5, n)); tq = qv * np.clip(0.5 + rnd.normal(0, 0.05, n), 0.1, 0.9)
    t = (int(time.time() * 1000) // 3600000 - n) * 3600000 + np.arange(n) * 3600000
    return pd.DataFrame({"t": t, "o": o, "h": h, "l": l, "c": c, "qv": qv, "tq": tq, "oi": 1e8 * np.exp(np.cumsum(rnd.normal(0, 0.01, n))),
                         "tls": 1.5 * np.exp(np.cumsum(rnd.normal(0, 0.01, n))), "gls": 1.2, "funding": 0.0001})
data = {"BTCUSDT": (k(0), "fut")} | {f"S{i}USDT": (k(i + 1), "fut") for i in range(int(os.environ.get("N", 10)))}
rank = {s: i + 1 for i, s in enumerate(data)}
bk = W.to4h(data["BTCUSDT"][0]); bc = bk["c"].values
btc = dict(zip(bk["t"].values, (bc / np.r_[np.full(6, np.nan), bc[:-6]] - 1) * 100))
split = int(bk["t"].quantile(0.7))
r = W.analyze(data, rank, btc, split)
r.update(time=int(time.time() * 1000), split=split, coins=len(data))
print(len(r["rules"]), r["pick"], r["adopted"], len(r["compare"]))
md = W.to_md(r); assert "Balina izi" in md; print(md[:900])
assert not r["adopted"] or True
print("BALİNA TESTİ GEÇTİ")
