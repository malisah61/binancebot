"""Ağsız günlük formasyon testi: elle kurulmuş OBO tespiti + rastgele veride çalışma."""
import os, sys, tempfile, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "bot"))
import numpy as np, pandas as pd
import patterns as P, daily, binance

# 1) elle OBO: yükseliş, sol omuz 110, dip 100, baş 120, dip 101, sağ omuz 111, sonra boyun kırılımı
path = [80, 90, 100, 110, 105, 100, 108, 120, 112, 101, 106, 111, 104, 99, 95, 92]
c = np.interp(np.arange(0, len(path) - 1, 0.25), np.arange(len(path)), path)
o = np.r_[c[0], c[:-1]]; h = np.maximum(o, c) + 0.3; l = np.minimum(o, c) - 0.3
ev, A = P.detect(o, h, l, c)
types = [e["type"] for e in ev]
print("tespit:", types)
assert "OBO" in types, "omuz-baş-omuz bulunmalıydı"
e = next(e for e in ev if e["type"] == "OBO"); print("OBO", e)
assert e["stop"] > c[e["i"]] > e["target"]

# 2) rastgele veride tüm akış
def series(seed, n=1100):
    rnd = np.random.default_rng(seed); r = rnd.normal(0, 0.035, n); c = 100 * np.exp(np.cumsum(r)); o = np.r_[100, c[:-1]]
    h = np.maximum(o, c) * (1 + np.abs(rnd.normal(0, 0.015, n))); l = np.minimum(o, c) * (1 - np.abs(rnd.normal(0, 0.015, n)))
    v = np.abs(rnd.normal(1e6, 2e5, n)); t = (int(time.time() * 1000) // 86400000 - n) * 86400000 + np.arange(n) * 86400000
    return pd.DataFrame({"t": t, "o": o, "h": h, "l": l, "c": c, "v": v, "qv": v * c, "tq": v * c * 0.5})
SEED = int(os.environ.get("SEED", 0))
data = {f"S{i}USDT": series(i + SEED * 100) for i in range(12)}
st = daily.study(data); st["n_coins"] = 12
for k, s in st["types"].items(): print(f"{s['name']:40} eğitim n{s['train']['n']} R{s['train']['avg_R']}  test n{s['test']['n']} R{s['test']['avg_R']} → {s['verdict']}")
guv = [k for k, s in st["types"].items() if s["verdict"] == "güvenilir"]
print("rastgele veride 'güvenilir' çıkan:", guv)
binance.top_usdt = lambda n: [{"symbol": s} for s in data]
binance.klines = lambda s, tf, limit: data[s].to_dict("records")
sc = daily.scan(st)
print(daily.report(st, sc, pd.Timestamp.now(tz="UTC"))[:1500])
print("GÜNLÜK FORMASYON TESTİ GEÇTİ")
