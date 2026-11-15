"""Ağsız uç hareket testi: (1) simülatör birim kontrolleri, (2) rastgele yürüyüşte hiçbir şey benimsenmemeli,
(3) sert düşüşlerden sonra tepki eklenmiş veride long-tepki varyantı öne çıkmalı."""
import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "bot"))
import numpy as np, pandas as pd
import extreme as X

# (1) simülatör: long, stop 9, giriş 10 → hedef1 11.5, hedef2 13
o = np.array([10, 10, 10.5, 11.6, 12.5, 13.2]); h = o + 0.1; l = o - 0.1; c = o.copy()
r = X.sim(o, h, l, c, 0, 1, 10.0, 9.0, "mkt", 0.0)
assert abs(r["R"] - 2.25) < 1e-9, r
o = np.array([10, 10, 9.5, 8.5, 8]); h = o + 0.05; l = o - 0.05; c = o.copy()
r = X.sim(o, h, l, c, 0, 1, 10.0, 9.0, "mkt", 0.0)
assert r["R"] < -1.4 and r["R"] > -1.6, r      # boşlukla açılış stop altından → açılıştan çıkış (8.5)
r = X.sim(o, h, l, c, 0, -1, 10.0, 11.0, "mkt", 0.0)
assert r["R"] > 1.5, r                           # short kazanır
r = X.sim(o, h, l, c, 0, 1, 7.0, 6.0, "lim", 0.0)
assert not r["filled"]                           # limit dolmadı
st = X.stats([{"R": 1, "risk": 0.25, "mae": 0.3}, {"R": -1, "risk": 0.05, "mae": 0.05}])
assert st["x5"]["liq"] == 1 and st["x3"]["liq"] == 0, st   # 5x'te %19.5 ters harekette tasfiye
print("simülatör tamam")

def series(seed, n=3000, drift=0.0, bounce=False):
    rnd = np.random.default_rng(seed); r = rnd.normal(drift, 0.02, n)
    if bounce:
        for at in rnd.integers(800, n - 100, 12):
            r[at:at + 4] -= 0.05; r[at + 5:at + 15] += 0.025
    c = 10 * np.exp(np.cumsum(r)); o = np.r_[10, c[:-1]]
    h = np.maximum(o, c) * (1 + np.abs(rnd.normal(0, 0.006, n))); l = np.minimum(o, c) * (1 - np.abs(rnd.normal(0, 0.006, n)))
    v = np.abs(rnd.normal(1e5, 2e4, n)); t = (int(time.time() * 1000) // 3600000 - n) * 3600000 + np.arange(n) * 3600000
    return pd.DataFrame({"t": t, "o": o, "h": h, "l": l, "c": c, "v": v, "qv": v * c, "tq": v * c * 0.5})

N = int(os.environ.get("N", 40))
for label, bounce in (("rastgele", False), ("tepkili", True)):
    data = {f"S{i}USDT": (series(i, bounce=bounce), "fut") for i in range(N)}
    rank = {s: 10 + i * 6 for i, s in enumerate(data)}
    E, split, G, picks, cmps = X.analyze(data, rank)
    ad = [g for g in G if g["adopt"]]
    print(label, "olay", len(E), "seçimler", {k: (v["name"], v["th"], v["tiers"], v["train"]["avg_R"], v["test"].get("avg_R"), v["adopted"]) for k, v in picks.items()},
          "testi geçen kombinasyon", len(ad))
    if label == "rastgele":
        assert not any(p["adopted"] for p in picks.values()), "rastgele yürüyüşte benimsenme olmamalı"
    else:
        assert picks["crash"]["name"].startswith("L"), picks["crash"]
md = X.to_md({"time": int(time.time()*1000), "coins": N, "split": int(split), "n_events": {"crash": 1, "ctpump": 1}, "grid": G,
              "picks": picks, "compare": cmps, "scan": [], "ledger": None})
assert "Sert düşüş" in md
print("UÇ HAREKET TESTİ GEÇTİ")
