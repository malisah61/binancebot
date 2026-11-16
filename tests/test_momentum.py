"""Ağsız ani hareket testi (sentetik 1s veri)."""
import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "bot"))
import numpy as np, pandas as pd
import momentum as M
def k(seed, n=24 * 365):
    rnd = np.random.default_rng(seed); r = rnd.standard_t(3, n) * 0.008
    c = 100 * np.exp(np.cumsum(r)); o = np.r_[100, c[:-1]]
    h = np.maximum(o, c) * 1.003; l = np.minimum(o, c) * 0.997; qv = np.abs(rnd.normal(1e6, 3e5, n))
    t = (int(time.time() * 1000) // 3600000 - n) * 3600000 + np.arange(n) * 3600000
    return pd.DataFrame({"t": t, "o": o, "h": h, "l": l, "c": c, "qv": qv, "tq": qv / 2, "funding": 0.0001})
data = {"BTCUSDT": (k(0), "fut")} | {f"S{i}USDT": (k(i + 1), "fut") for i in range(8)}
rank = {s: i + 1 for i, s in enumerate(data)}
bk = data["BTCUSDT"][0]; bc = bk["c"].values
btc = dict(zip(bk["t"].values.astype(int), bc / np.r_[np.full(24, np.nan), bc[:-24]] - 1))
E = M.events(data, rank, btc); split = int(E["t"].quantile(0.7))
r = M.analyze(E, split); r.update(time=int(time.time() * 1000), split=split, coins=9)
print(len(E), len(r["rules"]), r["pick"], r["adopted"])
D = M.one_per_day(E[(E.th == 0.05) & (E.side == "devam") & (E.sm == 1.5)])
assert ((D["t"] // 1000 + 3 * 3600) // 86400).is_unique
print(M.to_md(r)[:700]); print("ANİ HAREKET TESTİ GEÇTİ")
