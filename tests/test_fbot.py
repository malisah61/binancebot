"""Ağsız canlı bot testi: sentetik mumlarla iki çalıştırma."""
import os, sys, tempfile, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "bot"))
import numpy as np
import binance, fbot

NOW = [int(time.time() * 1000)]
fbot.now_ms = lambda: NOW[0]
def series(seed, tf_ms, n, drift):
    rnd = np.random.default_rng(seed); end = NOW[0] - NOW[0] % tf_ms; t0 = end - n * tf_ms
    r = rnd.normal(drift, 0.004 * (tf_ms / 900_000) ** 0.5, n); c = 100 * np.exp(np.cumsum(r)); o = np.r_[100, c[:-1]]
    h = np.maximum(o, c) * 1.002; l = np.minimum(o, c) * 0.998; v = np.abs(rnd.normal(1000, 200, n))
    return [{"t": int(t0 + i * tf_ms), "o": o[i], "h": h[i], "l": l[i], "c": c[i], "v": v[i], "qv": v[i] * c[i], "tb": v[i] * 0.55, "tq": v[i] * c[i] * (0.6 if drift > 0 else 0.4)} for i in range(n)]
syms = [f"C{i}USDT" for i in range(12)]
MS = {"15m": 900_000, "1h": 3_600_000, "4h": 14_400_000}
binance.top_usdt = lambda n: [{"symbol": s} for s in syms]
binance.klines = lambda s, tf, limit: series(int(s[1:-4]), MS[tf], limit, 0.0015 if int(s[1:-4]) % 2 else -0.0015)
fbot.STATE = os.environ.get("OUT") or tempfile.mkdtemp()
fbot.telegram.send = lambda chat, txt: print("[TG]", txt[:1500])
fbot.main()
st = fbot.load("futures.json", None)
n_open = sum(len(a["positions"]) for a in st["accounts"].values())
print("açık pozisyon:", n_open)
assert n_open > 0
# 2. çalıştırma: 3 saat sonra, fiyatlar sert hareket etsin
NOW[0] += 3 * 3600_000
binance.klines = lambda s, tf, limit: series(int(s[1:-4]), MS[tf], limit, -0.004 if int(s[1:-4]) % 2 else 0.004)
fbot.main()
st = fbot.load("futures.json", None)
print("kapanan:", sum(len(a["closed"]) for a in st["accounts"].values()))
assert sum(len(a["closed"]) for a in st["accounts"].values()) > 0
print("CANLI BOT TESTİ GEÇTİ")
