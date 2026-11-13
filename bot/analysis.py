"""Teknik analiz motoru.

Uygulamadaki (app/www/index.html) JavaScript motoruyla AYNI mantığı kullanır.
Her bileşen -1 (güçlü düşüş) ile +1 (güçlü yükseliş) arasında bir puan üretir,
ağırlıklı ortalama 0-100 arası skora çevrilir. Skor bir "olasılık" değil,
göstergelerin ne kadar aynı yönü gösterdiğinin ölçüsüdür.
"""
from __future__ import annotations

import math
import numpy as np

H4 = 4 * 3600 * 1000


# ---------------------------------------------------------------- temel
def ema(x, n):
    x = np.asarray(x, float)
    out = np.empty_like(x)
    a = 2.0 / (n + 1)
    out[0] = x[0]
    for i in range(1, len(x)):
        out[i] = a * x[i] + (1 - a) * out[i - 1]
    return out


def rma(x, n):  # Wilder ortalaması
    x = np.asarray(x, float)
    out = np.empty_like(x)
    out[0] = x[0]
    a = 1.0 / n
    for i in range(1, len(x)):
        out[i] = a * x[i] + (1 - a) * out[i - 1]
    return out


def sma(x, n):
    x = np.asarray(x, float)
    out = np.full_like(x, np.nan)
    c = np.cumsum(np.insert(x, 0, 0.0))
    out[n - 1:] = (c[n:] - c[:-n]) / n
    return out


def rolling_std(x, n):
    x = np.asarray(x, float)
    out = np.full_like(x, np.nan)
    for i in range(n - 1, len(x)):
        out[i] = x[i - n + 1:i + 1].std()
    return out


def rsi(c, n=14):
    d = np.diff(c, prepend=c[0])
    g = rma(np.clip(d, 0, None), n)
    l = rma(np.clip(-d, 0, None), n)
    rs = g / np.where(l == 0, 1e-12, l)
    return 100 - 100 / (1 + rs)


def macd(c, f=12, s=26, sig=9):
    m = ema(c, f) - ema(c, s)
    sg = ema(m, sig)
    return m, sg, m - sg


def true_range(h, l, c):
    pc = np.insert(c[:-1], 0, c[0])
    return np.maximum(h - l, np.maximum(abs(h - pc), abs(l - pc)))


def atr(h, l, c, n=14):
    return rma(true_range(h, l, c), n)


def adx(h, l, c, n=14):
    up = np.diff(h, prepend=h[0])
    dn = -np.diff(l, prepend=l[0])
    pdm = np.where((up > dn) & (up > 0), up, 0.0)
    ndm = np.where((dn > up) & (dn > 0), dn, 0.0)
    trs = rma(true_range(h, l, c), n)
    trs = np.where(trs == 0, 1e-12, trs)
    pdi = 100 * rma(pdm, n) / trs
    ndi = 100 * rma(ndm, n) / trs
    dx = 100 * abs(pdi - ndi) / np.where(pdi + ndi == 0, 1e-12, pdi + ndi)
    return rma(dx, n), pdi, ndi


def stoch_rsi(c, n=14, k=3, d=3):
    r = rsi(c, n)
    out = np.full_like(r, 50.0)
    for i in range(n - 1, len(r)):
        w = r[i - n + 1:i + 1]
        lo, hi = w.min(), w.max()
        out[i] = 100 * (r[i] - lo) / (hi - lo) if hi > lo else 50.0
    kk = sma(out, k)
    return kk, sma(np.nan_to_num(kk, nan=50.0), d)


def obv(c, v):
    s = np.sign(np.diff(c, prepend=c[0]))
    return np.cumsum(s * v)


def mfi(h, l, c, v, n=14):
    tp = (h + l + c) / 3
    mf = tp * v
    d = np.diff(tp, prepend=tp[0])
    pos = np.where(d > 0, mf, 0.0)
    neg = np.where(d < 0, mf, 0.0)
    ps, ns = pos[-n:].sum(), neg[-n:].sum()
    return 100.0 if ns == 0 else 100 - 100 / (1 + ps / ns)


def slope_norm(y, n=20):
    """Son n değerin doğrusal eğimi, ortalama mutlak değişime bölünmüş."""
    y = np.asarray(y[-n:], float)
    x = np.arange(len(y))
    b = np.polyfit(x, y, 1)[0]
    scale = np.mean(abs(np.diff(y))) or 1e-12
    return b / scale


# ---------------------------------------------------------------- yapı
def resample(k, ms=H4):
    """1s mumlarını 4s mumlarına birleştirir. k: dict listesi."""
    out, cur, key = [], None, None
    for c in k:
        g = c["t"] // ms
        if g != key:
            if cur:
                out.append(cur)
            key = g
            cur = dict(c)
        else:
            cur["h"] = max(cur["h"], c["h"])
            cur["l"] = min(cur["l"], c["l"])
            cur["c"] = c["c"]
            for f in ("v", "qv", "tb", "tq"):
                cur[f] += c[f]
    if cur:
        out.append(cur)
    return out


def pivots(h, l, k=5):
    hi, lo = [], []
    for i in range(k, len(h) - k):
        if h[i] == h[i - k:i + k + 1].max():
            hi.append((i, h[i]))
        if l[i] == l[i - k:i + k + 1].min():
            lo.append((i, l[i]))
    return hi, lo


def sr_levels(h, l, c, v, a):
    """Pivot kümeleri + hacim profili düğümleri -> destek/direnç."""
    ph, pl = pivots(h, l)
    pts = sorted([p for _, p in ph] + [p for _, p in pl])
    tol = max(a * 0.6, c[-1] * 0.002)
    clusters = []
    for p in pts:
        if clusters and p - clusters[-1]["last"] <= tol:
            cl = clusters[-1]
            cl["sum"] += p
            cl["n"] += 1
            cl["last"] = p
        else:
            clusters.append({"sum": p, "n": 1, "last": p})
    levels = [{"price": cl["sum"] / cl["n"], "touches": cl["n"], "src": "pivot"} for cl in clusters]

    # hacim profili (son 300 mum)
    m = min(300, len(c))
    lo, hi = l[-m:].min(), h[-m:].max()
    poc = None
    if hi > lo:
        bins = 40
        hist = np.zeros(bins)
        tp = (h[-m:] + l[-m:] + c[-m:]) / 3
        idx = np.clip(((tp - lo) / (hi - lo) * bins).astype(int), 0, bins - 1)
        np.add.at(hist, idx, v[-m:])
        centers = lo + (np.arange(bins) + 0.5) * (hi - lo) / bins
        poc = float(centers[hist.argmax()])
        top = hist.argsort()[-5:]
        for i in top:
            levels.append({"price": float(centers[i]), "touches": 2, "src": "hacim"})

    price = c[-1]
    sup = sorted([x for x in levels if x["price"] < price], key=lambda x: price - x["price"])
    res = sorted([x for x in levels if x["price"] > price], key=lambda x: x["price"] - price)
    return sup[:4], res[:4], poc


def fibonacci(h, l, n=150):
    hh, ll = h[-n:], l[-n:]
    ih, il = int(hh.argmax()), int(ll.argmin())
    hi, lo = float(hh[ih]), float(ll[il])
    up = ih > il  # dip önce, tepe sonra -> yükseliş dalgası
    rng = hi - lo
    ratios = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1, 1.272, 1.618]
    if up:
        lv = {r: hi - rng * r for r in ratios}
    else:
        lv = {r: lo + rng * r for r in ratios}
    return {"up": up, "high": hi, "low": lo, "levels": lv}


# ---------------------------------------------------------------- skor
def clip(x, a=-1.0, b=1.0):
    return max(a, min(b, x))


def analyze(k, book=None, trades=None):
    """k: 1s mum listesi (en az ~250). book: {'bids':[[p,q]],'asks':[[p,q]]}.
    trades: aggTrades listesi. Dönen: skor, bileşenler, seviyeler, plan."""
    o = np.array([x["o"] for x in k], float)
    h = np.array([x["h"] for x in k], float)
    l = np.array([x["l"] for x in k], float)
    c = np.array([x["c"] for x in k], float)
    v = np.array([x["v"] for x in k], float)
    qv = np.array([x["qv"] for x in k], float)
    tq = np.array([x["tq"] for x in k], float)
    price = float(c[-1])

    e20, e50, e200 = ema(c, 20), ema(c, 50), ema(c, 200)
    r = rsi(c)
    m, ms, mh = macd(c)
    a = atr(h, l, c)
    A = float(a[-1])
    ad, pdi, ndi = adx(h, l, c)
    sk, sd = stoch_rsi(c)
    ob = obv(c, v)
    mf = mfi(h, l, c, v)
    bm = sma(c, 20)
    bs = rolling_std(c, 20)
    bu, bl = bm + 2 * bs, bm - 2 * bs
    pb = (price - bl[-1]) / (bu[-1] - bl[-1]) if bu[-1] > bl[-1] else 0.5
    bw = (bu - bl) / bm
    vw = float((((h + l + c) / 3) * v)[-24:].sum() / max(v[-24:].sum(), 1e-12))

    comp = {}  # ad: (puan, ağırlık, açıklama)

    # 1) Trend (EMA 20/50/200)
    t = (np.sign(price - e50[-1]) + np.sign(price - e200[-1]) + np.sign(e20[-1] - e50[-1])
         + np.sign(e50[-1] - e50[-6])) / 4
    comp["Trend (EMA20/50/200)"] = (t, 2.0, f"Fiyat {'EMA200 üstünde' if price > e200[-1] else 'EMA200 altında'}, "
                                         f"EMA20 {'>' if e20[-1] > e50[-1] else '<'} EMA50")

    # 2) Üst zaman dilimi (4s)
    k4 = resample(k)
    if len(k4) >= 60:
        c4 = np.array([x["c"] for x in k4], float)
        e4a, e4b = ema(c4, 21), ema(c4, 55)
        t4 = (np.sign(c4[-1] - e4a[-1]) + np.sign(e4a[-1] - e4b[-1]) + np.sign(e4a[-1] - e4a[-4])) / 3
        comp["4s trend"] = (t4, 1.5, "4 saatlik EMA21/55 " + ("yükseliş" if t4 > 0 else "düşüş" if t4 < 0 else "yatay"))

    # 3) MACD
    s = (0.5 if mh[-1] > 0 else -0.5) + (0.5 if mh[-1] > mh[-2] else -0.5)
    cross = ""
    for i in range(1, 4):
        if mh[-i] > 0 >= mh[-i - 1]:
            s += 0.3; cross = " (yeni AL kesişimi)"; break
        if mh[-i] < 0 <= mh[-i - 1]:
            s -= 0.3; cross = " (yeni SAT kesişimi)"; break
    comp["MACD"] = (clip(s), 1.5, f"Histogram {mh[-1]:+.4g}, {'artıyor' if mh[-1] > mh[-2] else 'azalıyor'}{cross}")

    # 4) RSI
    R = float(r[-1])
    if R > 78: s = -0.6
    elif R > 65: s = 0.2
    elif R >= 50: s = 0.7
    elif R >= 40: s = -0.3
    elif R >= 28: s = -0.5
    else: s = 0.4  # aşırı satım tepkisi
    s += 0.3 if r[-1] > r[-4] else -0.3
    comp["RSI(14)"] = (clip(s), 1.0, f"RSI {R:.1f}" + (" aşırı alım" if R > 70 else " aşırı satım" if R < 30 else ""))

    # 5) ADX / DMI
    AD = float(ad[-1])
    s = (1 if pdi[-1] > ndi[-1] else -1) * min(AD / 40, 1) if AD > 18 else 0.0
    comp["ADX/DMI"] = (s, 1.0, f"ADX {AD:.0f} ({'güçlü trend' if AD > 25 else 'zayıf trend'}), +DI {pdi[-1]:.0f} / -DI {ndi[-1]:.0f}")

    # 6) Stoch RSI
    K, D, K1, D1 = sk[-1], sd[-1], sk[-2], sd[-2]
    s = 0.0
    if K > D and K1 <= D1 and K < 30: s = 1
    elif K < D and K1 >= D1 and K > 70: s = -1
    elif K > 85: s = -0.4
    elif K < 15: s = 0.4
    else: s = 0.3 if K > D else -0.3
    comp["Stoch RSI"] = (s, 0.5, f"K {K:.0f} / D {D:.0f}")

    # 7) Bollinger
    sq = bw[-1] < np.nanpercentile(bw[-120:], 20)
    s = 0.0
    if pb > 1: s = 0.3 if t > 0 else -0.3
    elif pb < 0: s = 0.3
    else: s = (pb - 0.5) * 0.8
    comp["Bollinger"] = (clip(s), 0.5, f"%B {pb:.2f}" + (" — sıkışma (sert hareket yakın)" if sq else ""))

    # 8) OBV
    so = slope_norm(ob, 20)
    comp["OBV (hacim akışı)"] = (math.tanh(so * 3), 1.0, "OBV " + ("yükseliyor: birikim" if so > 0 else "düşüyor: dağıtım"))

    # 9) MFI
    s = clip((mf - 50) / 30) if 20 < mf < 80 else (-0.5 if mf >= 80 else 0.5)
    comp["MFI(14)"] = (s, 0.5, f"MFI {mf:.0f}")

    # 10) VWAP
    d = (price - vw) / A if A else 0
    comp["VWAP (24 mum)"] = (math.tanh(d / 2), 0.5, f"Fiyat VWAP'ın {'üstünde' if price > vw else 'altında'} ({vw:.6g})")

    # 11) Alıcı/satıcı baskısı (taker buy oranı)
    tr = float(tq[-24:].sum() / max(qv[-24:].sum(), 1e-12))
    tr6 = float(tq[-6:].sum() / max(qv[-6:].sum(), 1e-12))
    comp["Alıcı/Satıcı baskısı"] = (clip((tr - 0.5) * 12 + (tr6 - 0.5) * 6), 1.5,
                                   f"Son 24 mum agresif alım %{tr*100:.1f}, son 6 mum %{tr6*100:.1f}")

    # 12) Hacim patlaması
    va = v[-23:-3].mean() if len(v) > 25 else v.mean()
    spike = float(v[-3:].mean() / max(va, 1e-12))
    ret3 = c[-1] / c[-4] - 1
    s = (1 if ret3 > 0 else -1) * clip((spike - 1.2) / 2, 0, 1) if spike > 1.2 else 0.0
    comp["Hacim patlaması"] = (s, 1.0, f"Hacim ortalamanın {spike:.1f} katı, son 3 mum {ret3*100:+.2f}%")

    # 13) Destek/Direnç konumu
    sup, res, poc = sr_levels(h, l, c, v, A)
    ns = sup[0]["price"] if sup else price - 3 * A
    nr = res[0]["price"] if res else price + 3 * A
    rr = (nr - price) / max(price - ns, A * 0.2)
    comp["Destek/Direnç"] = (clip(math.tanh(math.log(max(rr, 1e-3)))), 1.0,
                            f"En yakın destek {ns:.6g}, direnç {nr:.6g} (yer oranı {rr:.2f})")

    # 14) Fibonacci
    fb = fibonacci(h, l)
    lv = fb["levels"]
    s = 0.0
    if fb["up"]:
        if lv[0.618] <= price <= lv[0.5]:  # "altın bölge" geri çekilmesi
            s = 0.6 if mh[-1] > mh[-2] else 0.2
        elif price < lv[0.786]:
            s = -0.6
        elif price > lv[0.236]:
            s = 0.4
    else:
        if lv[0.5] <= price <= lv[0.618]:
            s = -0.6 if mh[-1] < mh[-2] else -0.2
        elif price > lv[0.786]:
            s = 0.6
        elif price < lv[0.236]:
            s = -0.4
    near = min(lv.items(), key=lambda kv: abs(kv[1] - price))
    comp["Fibonacci"] = (s, 0.5, f"{'Yükseliş' if fb['up'] else 'Düşüş'} dalgası, en yakın seviye {near[0]} = {near[1]:.6g}")

    # 15) Emir defteri dengesi (varsa)
    if book:
        lo_, hi_ = price * 0.98, price * 1.02
        bid = sum(float(p) * float(q) for p, q in book["bids"] if float(p) >= lo_)
        ask = sum(float(p) * float(q) for p, q in book["asks"] if float(p) <= hi_)
        imb = (bid - ask) / max(bid + ask, 1e-12)
        comp["Emir defteri (±%2)"] = (clip(imb * 2), 1.0, f"Alış duvarı {bid:,.0f}$ / Satış duvarı {ask:,.0f}$")

    # 16) Büyük işlemler (balina) (varsa)
    whales = None
    if trades:
        vals = np.array([float(x["p"]) * float(x["q"]) for x in trades])
        if len(vals) > 20:
            thr = max(np.percentile(vals, 95), 5000)
            buy = sum(val for x, val in zip(trades, vals) if val >= thr and not x["m"])
            sell = sum(val for x, val in zip(trades, vals) if val >= thr and x["m"])
            net = (buy - sell) / max(buy + sell, 1e-12)
            whales = {"buy": buy, "sell": sell, "threshold": thr}
            comp["Büyük işlemler"] = (clip(net * 1.5), 1.0, f"Büyük alım {buy:,.0f}$ / büyük satım {sell:,.0f}$ (eşik {thr:,.0f}$)")

    tw = sum(w for _, w, _ in comp.values())
    total = sum(s * w for s, w, _ in comp.values()) / tw
    score = round(float(50 + 50 * total), 1)
    agree = sum(1 for s, _, _ in comp.values() if s * total > 0.05) / len(comp)

    stop = price - 1.5 * A
    if sup and price - sup[0]["price"] < 1.5 * A:
        stop = min(stop, sup[0]["price"] - 0.3 * A)
    tp1 = nr if nr - price > A else price + 2 * A
    tp2 = price + 3.5 * A

    if score >= 65: label = "YÜKSELİŞ ihtimali yüksek"
    elif score >= 55: label = "Hafif yükseliş eğilimi"
    elif score > 45: label = "Nötr / kararsız"
    elif score > 35: label = "Hafif düşüş eğilimi"
    else: label = "DÜŞÜŞ ihtimali yüksek"

    return {
        "price": price, "score": score, "label": label, "agreement": round(agree, 2),
        "atr": A, "rsi": R, "adx": AD, "taker": tr, "spike": spike,
        "components": [{"name": n, "score": round(float(s), 2), "weight": w, "text": tx} for n, (s, w, tx) in comp.items()],
        "supports": sup, "resistances": res, "poc": poc, "fib": fb, "whales": whales,
        "plan": {"entry": price, "stop": stop, "tp1": tp1, "tp2": tp2},
        "change24": float(c[-1] / c[-25] - 1) if len(c) > 25 else 0.0,
    }
