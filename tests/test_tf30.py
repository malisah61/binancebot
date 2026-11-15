"""Ağsız 30dk 1-yıl testi: rastgele yürüyüşte çalışır, filtreler uygulanır, hiçbir varyant benimsenmez (çoğunlukla)."""
import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "bot"))
os.environ.setdefault("EX30_DAYS", "120")
import numpy as np, pandas as pd
import tf30
from datetime import datetime, timezone
today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
def k(seed, n=(120 + 45) * 48):
    rnd = np.random.default_rng(seed); r = rnd.normal(0, 0.006, n)
    c = 100 * np.exp(np.cumsum(r)); o = np.r_[100, c[:-1]]
    h = np.maximum(o, c) * (1 + np.abs(rnd.normal(0, 0.002, n))); l = np.minimum(o, c) * (1 - np.abs(rnd.normal(0, 0.002, n)))
    v = np.abs(rnd.normal(1e5, 2e4, n)); t = int(today.timestamp() * 1000) - n * 1800000 + np.arange(n) * 1800000
    return pd.DataFrame({"t": t, "o": o, "h": h, "l": l, "c": c, "v": v, "qv": v * c, "tq": v * c * 0.5})
raw = {"BTCUSDT": (k(0), None, None)} | {f"S{i}USDT": (k(i + 1), None, None) for i in range(int(os.environ.get("N", 8)))}
r = tf30.analyze(raw, today)
for name, v in r["variants"].items():
    print(name, v["train"], v["test"].get("n"), v["replay_all"])
    if name == "short_only": assert v["train"].get("long", 0) == 0 and v["test"].get("long", 0) == 0
print("seçim", r["pick"], r["adopted"]); S = r["selective"]; print("seçici", len(S["rows"]), S["pick"], S["adopted"], {k: v["train"].get("n") for k, v in list(S["rows"].items())[:6]})
md = tf30.to_md(r); assert "Gerçek hesap kurallarıyla" in md
print("30DK TESTİ GEÇTİ")
