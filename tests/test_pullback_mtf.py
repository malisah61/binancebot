"""Ağsız çoklu zaman dilimi geri çekilme testi (sentetik trendli veri)."""
import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "bot"))
import numpy as np, pandas as pd
import pullback_mtf as P
from datetime import datetime, timezone
today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
T0 = int(today.timestamp() * 1000)
def k(seed, n, ms, drift):
    rnd = np.random.default_rng(seed); r = rnd.normal(drift, 0.01, n) + 0.004 * np.sin(np.arange(n) / 150)
    c = 100 * np.exp(np.cumsum(r)); o = np.r_[100, c[:-1]]
    h = np.maximum(o, c) * 1.003; l = np.minimum(o, c) * 0.997; v = np.abs(rnd.normal(1e5, 2e4, n))
    t = T0 - n * ms + np.arange(n) * ms
    return pd.DataFrame({"t": t, "o": o, "h": h, "l": l, "c": c, "v": v, "qv": v * c, "tq": v * c * 0.5})
syms = ["BTCUSDT"] + [f"S{i}USDT" for i in range(int(os.environ.get("N", 6)))]
data = {s: (k(i, 24 * 365, 3600000, 0.0002 * (1 if i % 2 else -1)), "fut") for i, s in enumerate(syms)}
daily = {s: k(i + 50, 1095, 86400000, 0.002 * (1 if i % 2 else -1)) for i, s in enumerate(syms)}
r = P.analyze(data, daily, {s: i + 1 for i, s in enumerate(syms)}, today)
r.update(time=int(time.time() * 1000), coins=len(syms))
for tf, v in r["tfs"].items():
    print(tf, {k: v2["train"].get("n") for k, v2 in v["rules"].items()}, v["pick"], len(v["feat"]))
md = P.to_md(r); assert "Ortak göstergeler" in md
print(r["common"][:2])
print("ÇOKLU ZAMAN DİLİMİ TESTİ GEÇTİ")
