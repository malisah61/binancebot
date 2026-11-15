"""Ağsız gerçek-hesap testi: sahte borsa ile (1) son mumda sert düşüş → doğru limit SHORT planı,
(2) seviye çoktan görüldüyse emir yok, (3) aynı olay ikinci kez işlenmez, (4) Actions'ta çalışmayı reddeder."""
import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "bot"))
import numpy as np, pandas as pd
import real, extreme as X

now = int(time.time() * 1000) // 3600000 * 3600000
def mk(seed, crash=False, touched=False, n=801):   # son satır = süren mum (atılır)
    rnd = np.random.default_rng(seed); r = rnd.normal(-0.0003, 0.006, n)
    if crash:
        end = n - 2 if touched else n - 1
        r[end - 2:end] = -0.07                     # 2 saatte ~%13 düşüş, %10 eşiği son kapanmış mumda geçilir
        if touched:
            r[end:] = 0.06                          # sonra sert tepki → %38.2 seviyesi görülmüş
    c = 100 * np.exp(np.cumsum(r)); o = np.r_[100, c[:-1]]
    h = np.maximum(o, c) * 1.002; l = np.minimum(o, c) * 0.998
    t = now - (n - 1) * 3600000 + np.arange(n) * 3600000
    return pd.DataFrame({"t": t, "o": o, "h": h, "l": l, "c": c, "qv": 1e6, "tq": 5e5})

data = {"BTCUSDT": mk(1), "AAAUSDT": mk(2, crash=True), "BBBUSDT": mk(3, crash=True, touched=True), "CCCUSDT": mk(4)}
real.klines = lambda R, s, n=800: data[s]
picks = {"crash": {"name": "S_f38", "th": 0.1, "tiers": ["büyük"], "regime": "tümü", "adopted": True}}
rank = {"BTCUSDT": 1, "AAAUSDT": 2, "BBBUSDT": 3, "CCCUSDT": 4}
done = {}
c, reg = real.candidates(None, picks, rank, done)
print(reg, [(x["sym"], x["dir"], {k: round(v, 3) for k, v in x["plan"].items() if k in ("entry", "sl", "tp1", "tp2")}) for x in c])
assert [x["sym"] for x in c] == ["AAAUSDT"], c
p = c[0]["plan"]; assert c[0]["dir"] == -1 and p["sl"] > p["entry"] > p["tp1"] > p["tp2"]
assert data["AAAUSDT"]["c"].iloc[-2] < p["entry"]          # limit, fiyatın üstünde (tepki bekler)
c2, _ = real.candidates(None, picks, rank, done)
assert not c2, "aynı olay ikinci kez işlenmemeli"
os.environ["GITHUB_ACTIONS"] = "true"
try:
    real.main(); raise AssertionError("Actions'ta çalışmamalıydı")
except SystemExit as e:
    assert "Actions" in str(e)
print("GERÇEK HESAP TESTİ GEÇTİ")
