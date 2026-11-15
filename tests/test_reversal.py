"""Ağsız dipten dönüş testi: sentetik 1s veri (bazı coinlerde dipten sıçrama ekli)."""
import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "bot"))
import numpy as np, pandas as pd
import reversal as RV

def series(seed, n=3600, pumps=0):
    rnd = np.random.default_rng(seed); r = rnd.normal(-0.0002, 0.012, n)
    for p in range(pumps):  # dip sonrası güçlü dönüş; öncesinde hacim ve agresif alım artışı (öncü işaret)
        at = rnd.integers(900, n - 200); r[at:at + 30] += 0.012
    c = 10 * np.exp(np.cumsum(r)); o = np.r_[10, c[:-1]]
    h = np.maximum(o, c) * (1 + np.abs(rnd.normal(0, 0.004, n))); l = np.minimum(o, c) * (1 - np.abs(rnd.normal(0, 0.004, n)))
    v = np.abs(rnd.normal(1e5, 2e4, n)); tq = v * c * np.clip(0.5 + r * 8, 0.1, 0.9)
    t = (int(time.time() * 1000) // 3600000 - n) * 3600000 + np.arange(n) * 3600000
    return pd.DataFrame({"t": t, "o": o, "h": h, "l": l, "c": c, "v": v, "qv": v * c, "tq": tq})
data = {f"S{i}USDT": series(i, pumps=4) for i in range(30)}
data["BTCUSDT"] = series(999)
bm = RV.btc_map(data["BTCUSDT"])
rows = []
for s, k in data.items():
    for e in RV.triggers(k, bm):
        e["sym"] = s; rows.append(e)
E = pd.DataFrame(rows); split = float(np.quantile(E["t"], 0.7))
print("tetik", len(E), "başarılı %", round(E["pump"].mean() * 100, 1), "ort R", round(E["R"].mean(), 3))
cmp_ = RV.compare(E, split)
for c in cmp_[:6]: print(c["name"], c["train"], c["test"]["d"], c["stable"])
rules = RV.mine(E, split, [f for f in RV.LIVE_FEATS if f in E])
te = E[E["t"] >= split]
for r in rules:
    m = RV.apply_rule(te, r["conds"]); print(RV.rule_text(r["conds"]), r["train"], RV.trade_stats(te[m], 3))
print("DİPTEN DÖNÜŞ TESTİ GEÇTİ")
