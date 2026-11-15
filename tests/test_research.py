"""Ağsız araştırma testi: sentetik 15dk mum + metrics + funding ile tüm akış."""
import os, sys, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "bot"))
import numpy as np, pandas as pd
from datetime import datetime, timedelta, timezone
import research

today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
start = int((today - timedelta(days=research.EVAL_DAYS + research.WARM_DAYS)).timestamp() * 1000)
raw = {}
for s in range(int(os.environ.get("N", 6))):
    rnd = np.random.default_rng(s)
    n = (research.EVAL_DAYS + research.WARM_DAYS) * 96
    r = rnd.normal(0, 0.004, n) + float(os.environ.get("DRIFT", 0.0015)) * np.sin(np.arange(n) / 300)  # trend dönemleri olan seri
    c = 100 * np.exp(np.cumsum(r)); o = np.r_[100, c[:-1]]
    h = np.maximum(o, c) * (1 + np.abs(rnd.normal(0, 0.002, n))); l = np.minimum(o, c) * (1 - np.abs(rnd.normal(0, 0.002, n)))
    v = np.abs(rnd.normal(1000, 300, n)); tq = v * c * np.clip(0.5 + r * 30, 0.05, 0.95)
    t = start + np.arange(n) * 900_000
    k = pd.DataFrame({"t": t, "o": o, "h": h, "l": l, "c": c, "v": v, "qv": v * c, "tq": tq})
    ts = t[::3] + 900_000
    met = pd.DataFrame({"ts": ts, "oi": 1e8 * np.exp(np.cumsum(rnd.normal(0, 0.003, len(ts)))), "gls": rnd.uniform(0.7, 2.8, len(ts)), "tls": rnd.uniform(0.7, 1.5, len(ts))})
    ft = np.arange(start - start % (8 * 3600_000), t[-1], 8 * 3600_000)
    fund = pd.DataFrame({"ts": ft, "funding": rnd.normal(0.0001, 0.0002, len(ft))})
    raw[f"S{s}USDT"] = (k, met, fund)
# Yeni filtreler: FVG/likidite onayı ve BTC trend yönü (v5.signals)
import v5
_R = pd.DataFrame({"t": [1, 2, 3, 4], "f_z": [0.1] * 4, "f_rsi": [50] * 4, "f_htf": [1, -1, 1, -1], "f_vwap_atr": [0.0] * 4,
                   "smc": [0.5, -0.5, -0.2, 0.3]})
_sc = np.array([70, 30, 70, 30], float)
_st = {"type": "trend", "lt": 58, "st": 42, "max_ext": None, "htf": None}
assert list(v5.signals(_R, _sc, _st)[0]) == [1, -1, 1, -1]
assert list(v5.signals(_R, _sc, {**_st, "smc": "with"})[0]) == [1, -1, 0, 0]
assert list(v5.signals(_R, _sc, {**_st, "btc": "with"})[0]) == [0, 0, 0, 0]       # BTC verisi yok → işlem yok
_R["f_btc"] = v5.btc_align(pd.DataFrame({"t": [1, 2, 3, 4], "trend": [0.5, 0.5, -0.5, np.nan]}), _R["t"].values)
assert list(v5.signals(_R, _sc, {**_st, "btc": "with"})[0]) == [1, 0, 0, 0]
assert "BTC trendi" in v5.strategy_name({**_st, "btc": "with", "sl": 1, "tp1": 1.5, "tp2": 2.5})
print("filtre testleri geçti")
research.STATE = os.environ.get("OUT") or tempfile.mkdtemp()
research.telegram.send = lambda chat, txt: print("[TG]\n" + txt[:600])
research.run(raw, today)
import json
m = json.load(open(os.path.join(research.STATE, "model.json")))
print({tf: (x["learned"], x["long_th"]) for tf, x in m["tfs"].items()})
print("ARAŞTIRMA TESTİ GEÇTİ")
