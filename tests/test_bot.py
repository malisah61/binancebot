"""Ağ olmadan sentetik veriyle analiz + bot testi:  python tests/test_bot.py"""
import os
import sys
import tempfile
import random

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "bot"))
import numpy as np  # noqa: E402
import analysis  # noqa: E402
import binance  # noqa: E402
import bot  # noqa: E402


def fake_klines(seed, n=1000, drift=0.0):
    rnd = np.random.default_rng(seed)
    p, out, t = 100.0, [], 1_700_000_000_000 - (1_700_000_000_000 % 3_600_000)
    for i in range(n):
        r = rnd.normal(drift, 0.006)
        o, c = p, p * (1 + r)
        h, l = max(o, c) * (1 + abs(rnd.normal(0, 0.003))), min(o, c) * (1 - abs(rnd.normal(0, 0.003)))
        v = abs(rnd.normal(1000, 300))
        tb = v * min(max(0.5 + r * 20 + rnd.normal(0, 0.05), 0.05), 0.95)
        out.append({"t": t + i * 3_600_000, "o": o, "h": h, "l": l, "c": c, "v": v, "qv": v * c, "tb": tb, "tq": tb * c})
        p = c
    return out


def test_analysis():
    up = analysis.analyze(fake_klines(2, drift=0.002))
    dn = analysis.analyze(fake_klines(2, drift=-0.002))
    print("yükselen skor", up["score"], up["label"], "| düşen skor", dn["score"], dn["label"])
    assert up["score"] > 60 > 40 > dn["score"], (up["score"], dn["score"])
    assert up["plan"]["stop"] < up["price"] < up["plan"]["tp1"] < up["plan"]["tp2"] or up["plan"]["tp1"] >= up["plan"]["tp2"]
    book = {"bids": [[up["price"] * 0.99, 100]], "asks": [[up["price"] * 1.01, 10]]}
    trades = [{"p": up["price"], "q": random.uniform(1, 200), "m": i % 3 == 0} for i in range(300)]
    d = analysis.analyze(fake_klines(1, drift=0.002), book, trades)
    names = [c["name"] for c in d["components"]]
    assert "Emir defteri (±%2)" in names and "Büyük işlemler" in names
    for c in d["components"]:
        assert -1 <= c["score"] <= 1, c


def test_bot_run():
    syms = [f"C{i}USDT" for i in range(20)]
    data = {s: fake_klines(i, drift=(0.003 if i < 6 else -0.001)) for i, s in enumerate(syms)}
    binance.top_usdt = lambda n=100: [{"symbol": s, "quoteVolume": "50000000"} for s in syms]
    binance.klines = lambda s, i="1h", limit=1000: data[s][-limit:]
    binance.depth = lambda s, limit=500: {"bids": [[data[s][-1]["c"] * 0.995, 1000]], "asks": [[data[s][-1]["c"] * 1.005, 500]]}
    binance.agg_trades = lambda s, limit=1000: [{"p": data[s][-1]["c"], "q": random.uniform(1, 100), "m": random.random() < 0.4} for _ in range(400)]
    binance.prices = lambda: {s: d[-1]["c"] for s, d in data.items()}
    bot.STATE = tempfile.mkdtemp()
    bot.main()
    pf = bot.load("portfolio.json", None)
    print("açık pozisyon:", list(pf["positions"]))
    assert pf["positions"], "yükselen coinlerde pozisyon açılmalıydı"
    # fiyatları çökert: stop tetiklenmeli
    for s in pf["positions"]:
        last = data[s][-1]
        crash = dict(last, t=last["t"] + 3_600_000 * 2, o=last["c"], h=last["c"], l=last["c"] * 0.8, c=last["c"] * 0.82)
        data[s] = data[s] + [crash]
    import time
    real = time.time
    time.time = lambda: real() + 0  # aynı saat
    bot.now_ms = lambda: data[syms[0]][-1]["t"] + 10 * 3_600_000
    pf_before = set(pf["positions"])
    for s in pf_before:  # giriş zamanını crash mumundan önceye çek
        pf["positions"][s]["time"] = data[s][-2]["t"]
        pf["positions"][s]["checked"] = data[s][-2]["t"]
    bot.save("portfolio.json", pf)
    bot.main()
    pf = bot.load("portfolio.json", None)
    print("kapanan:", [(c["symbol"], c["pct"]) for c in pf["closed"]])
    assert not (pf_before & set(pf["positions"])), "çöküşte stop çalışmalıydı"
    assert len(pf["closed"]) >= len(pf_before)


if __name__ == "__main__":
    test_analysis()
    test_bot_run()
    print("TÜM TESTLER GEÇTİ")
