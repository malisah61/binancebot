"""V5 kantitatif model — vektörel (tüm mumlar için tek seferde) Python sürümü.

app/www/analysis.js ile aynı bileşenler ve ağırlıklar. Araştırma (geriye dönük test)
ve canlı bot bunu kullanır. Bileşen puanları -1..+1, skor = 50 + 50 * ağırlıklı ortalama.

Girdi DataFrame sütunları: t,o,h,l,c,v,qv,tq  (+ isteğe bağlı oi, gls, tls, funding)
"""
from __future__ import annotations

import numpy as np
import pandas as pd

WEIGHTS = {"trend": 20, "momentum": 18, "oi": 15, "volume": 10, "deriv": 10, "book": 10, "smc": 10, "vwap": 5}
NAMES = {"trend": "Trend", "momentum": "Momentum", "oi": "Open Interest", "volume": "Hacim",
         "deriv": "Funding+L/S", "book": "Emir defteri", "smc": "FVG+Likidite avı", "vwap": "VWAP"}
TF_MS = {"15m": 900_000, "30m": 1_800_000, "1h": 3_600_000, "2h": 7_200_000, "4h": 14_400_000, "1d": 86_400_000}


def ema(s, n):
    return s.ewm(span=n, adjust=False).mean()


def rma(s, n):
    return s.ewm(alpha=1.0 / n, adjust=False).mean()


def clip(x, a=-1.0, b=1.0):
    return np.clip(x, a, b)


def resample(df, ms):
    g = df["t"] // ms
    agg = df.groupby(g).agg(t=("t", "first"), o=("o", "first"), h=("h", "max"), l=("l", "min"), c=("c", "last"),
                            v=("v", "sum"), qv=("qv", "sum"), tq=("tq", "sum"), n=("t", "size"))
    return agg.reset_index(drop=True)


def decision(score):
    s = np.asarray(score)
    return np.select([s >= 70, s >= 58, s >= 43, s >= 30], ["GÜÇLÜ LONG", "LONG", "NEUTRAL", "SHORT"], "GÜÇLÜ SHORT")


def _fvg_component(o, h, l, c, atr, look=60):
    """Her mum için: altındaki/üstündeki doldurulmamış FVG etkisi (JS ile aynı kural)."""
    n = len(c)
    out = np.zeros(n)
    near_bull = np.zeros(n, bool)
    near_bear = np.zeros(n, bool)
    active = []  # [type, bottom, top, created_i]
    for i in range(n):
        # mevcut mumla dolanları kapat (oluştuğu mumdan sonra)
        keep = []
        for f in active:
            if i > f[3]:
                if f[0] == 1 and l[i] <= f[1]:
                    continue
                if f[0] == -1 and h[i] >= f[2]:
                    continue
            if i - f[3] < look:
                keep.append(f)
        active = keep
        if i >= 2:
            if l[i] > h[i - 2]:
                active.append([1, h[i - 2], l[i], i])
            elif h[i] < l[i - 2]:
                active.append([-1, h[i], l[i - 2], i])
        p, A = c[i], atr[i]
        s = 0.0
        bull = [f for f in active if f[0] == 1 and f[2] <= p * 1.001 and p - f[2] < 2 * A]
        bear = [f for f in active if f[0] == -1 and f[1] >= p * 0.999 and f[1] - p < 2 * A]
        if bull:
            s += 0.3; near_bull[i] = True
        if bear:
            s -= 0.3; near_bear[i] = True
        for f in active:
            if f[1] <= p <= f[2]:
                s += 0.2 if f[0] == 1 else -0.2
                break
        out[i] = s
    return out, near_bull, near_bear


def compute(df: pd.DataFrame, tf: str, weights: dict | None = None) -> pd.DataFrame:
    """Her mum için bileşen puanları, ham göstergeler, skor ve karar."""
    W = dict(WEIGHTS, **(weights or {}))
    d = df.reset_index(drop=True)
    o, h, l, c, v, qv, tq = (d[x].astype(float) for x in ("o", "h", "l", "c", "v", "qv", "tq"))
    tf_ms = TF_MS[tf]
    R = pd.DataFrame({"t": d["t"], "c": c})

    tr = pd.concat([h - l, (h - c.shift(1)).abs(), (l - c.shift(1)).abs()], axis=1).max(axis=1).fillna(h - l)
    atr = rma(tr, 14)
    R["atr"] = atr
    R["atr_pct"] = atr / c * 100

    # ---- TREND
    e20, e50, e200 = ema(c, 20), ema(c, 50), ema(c, 200)
    t1 = (np.sign(c - e50) + np.sign(c - e200) + np.sign(e20 - e50) + np.sign(e50 - e50.shift(5))) / 4
    hk = resample(d, tf_ms * 4)
    hk = hk[hk["n"] == 4].copy()  # yalnızca tamamlanmış üst periyot mumları
    c4 = hk["c"]
    a4, b4 = ema(c4, 21), ema(c4, 55)
    hk["t4"] = (np.sign(c4 - a4) + np.sign(a4 - b4) + np.sign(a4 - a4.shift(3))) / 3
    hk.loc[hk.index[:60], "t4"] = np.nan
    hk["avail"] = hk["t"] + tf_ms * 4  # bu zamandan sonra bilinir
    bar_end = d["t"] + tf_ms
    t4 = pd.merge_asof(pd.DataFrame({"e": bar_end}), hk[["avail", "t4"]].rename(columns={"avail": "e"}),
                       on="e", direction="backward")["t4"]
    R["trend"] = np.where(t4.isna(), t1, 0.6 * t1 + 0.4 * t4.fillna(0))
    R["f_ema_order"] = np.select([(e20 > e50) & (e50 > e200), (e20 < e50) & (e50 < e200)], [1, -1], 0)
    R["f_htf"] = t4
    R["f_ema200"] = np.sign(c - e200)

    # ---- MOMENTUM
    dlt = c.diff().fillna(0)
    rs = rma(dlt.clip(lower=0), 14) / rma((-dlt).clip(lower=0), 14).replace(0, 1e-12)
    rsi = 100 - 100 / (1 + rs)
    rP = np.select([rsi > 78, rsi > 65, rsi >= 50, rsi >= 40, rsi >= 25], [-0.6, 0.3, 0.7, -0.4, -0.6], 0.4)
    rP = rP + np.where(rsi > rsi.shift(3), 0.3, -0.3)
    m = ema(c, 12) - ema(c, 26)
    mh = m - ema(m, 9)
    mP = np.where(mh > 0, 0.5, -0.5) + np.where(mh > mh.shift(1), 0.5, -0.5)
    up = (mh > 0) & (mh.shift(1) <= 0)
    dn = (mh < 0) & (mh.shift(1) >= 0)
    bonus = np.zeros(len(c))
    for lag in (2, 1, 0):  # en yakın kesişim kazanır
        bonus = np.where(up.shift(lag, fill_value=False), 0.3, np.where(dn.shift(lag, fill_value=False), -0.3, bonus))
    mP = mP + bonus
    sm20, sd20 = c.rolling(20).mean(), c.rolling(20).std(ddof=0)
    z = (c - sm20) / sd20.replace(0, np.nan)
    zP = np.where(z.abs() > 2.5, -np.sign(z) * 0.6, clip(z / 2) * 0.5)
    R["momentum"] = clip(0.35 * clip(rP) + 0.45 * clip(mP) + 0.2 * np.nan_to_num(zP))
    R["f_rsi"], R["f_macd"], R["f_z"] = rsi, np.sign(mh), z
    bw = 4 * sd20 / sm20
    R["f_squeeze"] = (bw < bw.rolling(120).quantile(0.2)).astype(float)

    # ---- OPEN INTEREST + REJİM
    if "oi" in d and d["oi"].notna().any():
        oi = d["oi"].astype(float)
        dOI = oi / oi.shift(6) - 1
        dP = c / c.shift(6) - 1
        mag = clip(dOI.abs() / 0.05, 0.2, 1)
        reg = np.select([dOI.abs() < 0.005, (dP >= 0) & (dOI > 0), (dP < 0) & (dOI > 0), (dP >= 0) & (dOI < 0)],
                        [0, 1, 2, 3], 4)
        s = np.select([reg == 0, reg == 1, reg == 2, reg == 3], [0, mag, -mag, 0.5 * mag], -0.5 * mag)
        R["oi"] = np.where(dOI.isna(), np.nan, s)
        R["f_oi_chg"] = dOI * 100
        R["f_regime"] = np.where(dOI.isna(), np.nan, reg)  # 0 nötr,1 long baskı,2 short baskı,3 squeeze,4 tasfiye
    else:
        R["oi"] = np.nan

    # ---- HACİM
    vAvg = v.shift(1).rolling(20).mean()
    rvol = v / vAvg
    taker = tq.rolling(6).sum() / qv.rolling(6).sum().replace(0, np.nan)
    obv = (np.sign(c.diff().fillna(0)) * v).cumsum()
    x = np.arange(20.0)
    xm = x - x.mean()

    def _slope(y):
        sc = np.mean(np.abs(np.diff(y))) or 1e-12
        return float(np.dot(xm, y - y.mean()) / np.dot(xm, xm) / sc)
    so = obv.rolling(20).apply(_slope, raw=True)
    rv = np.maximum(rvol, v.rolling(3).mean() / vAvg)
    rvP = np.where(rv > 1.5, np.sign(c - c.shift(3)) * clip((rv - 1) / 2, 0, 1), 0)
    R["volume"] = clip(0.4 * clip((taker - 0.5) * 10) + 0.3 * np.tanh(so * 3) + 0.3 * np.nan_to_num(rvP))
    R["f_rvol"], R["f_taker"], R["f_obv"] = rvol, taker, np.sign(so)

    # ---- FUNDING + L/S
    parts = []
    if "funding" in d and d["funding"].notna().any():
        f = d["funding"].astype(float)
        parts.append(pd.Series(np.where(f.isna(), np.nan, np.select([f > 0.0005, f > 0.0002, f < -0.0003, f < 0], [-1, -0.5, 0.8, 0.3], 0))))
        R["f_funding"] = f * 100
    if "gls" in d and d["gls"].notna().any():
        g = d["gls"].astype(float)
        parts.append(pd.Series(np.where(g.isna(), np.nan, np.select([g > 2.5, g > 1.8, g < 0.7, g < 1], [-0.8, -0.4, 0.6, 0.3], 0))))
        R["f_gls"] = g
    if "tls" in d and d["tls"].notna().any():
        tt = d["tls"].astype(float)
        parts.append(pd.Series(np.where(tt.isna(), np.nan, np.select([tt > 1.3, tt < 0.8], [0.6, -0.6], clip((tt - 1) * 1.5)))))
        R["f_tls"] = tt
    R["deriv"] = pd.concat(parts, axis=1).mean(axis=1) if parts else np.nan

    R["book"] = np.nan  # geçmiş emir defteri verisi yok

    # ---- FVG + LİKİDİTE AVI
    ph = h.shift(1).rolling(20).max()
    pl = l.shift(1).rolling(20).min()
    bsl = ((h > ph) & (c < ph)).astype(float)
    ssl = ((l < pl) & (c > pl)).astype(float)
    sweep = (0.7 * ssl.rolling(3, min_periods=1).sum() - 0.7 * bsl.rolling(3, min_periods=1).sum())
    fvg, nb, nr = _fvg_component(o.values, h.values, l.values, c.values, atr.values)
    R["smc"] = clip(sweep + fvg)
    R["f_sweep"] = np.sign(sweep)
    R["f_ssl1"], R["f_bsl1"] = ssl, bsl          # bu mumda likidite avı
    R["f_ssl3"] = ssl.rolling(3, min_periods=1).sum()
    R["f_bsl3"] = bsl.rolling(3, min_periods=1).sum()
    R["f_fvg"] = np.where(nb & ~nr, 1, np.where(nr & ~nb, -1, 0))

    # ---- VWAP (~24 saat)
    nV = max(20, round(86_400_000 / tf_ms))
    tp = (h + l + c) / 3
    vwap = (tp * v).rolling(nV, min_periods=20).sum() / v.rolling(nV, min_periods=20).sum()
    R["vwap"] = np.tanh((c - vwap) / atr / 2)
    R["f_vwap"] = np.sign(c - vwap)
    R["f_vwap_atr"] = (c - vwap) / atr          # VWAP'tan uzaklık (ATR cinsinden)

    # ---- YAPI: son dip/tepe ve fiyatın bu aralıktaki konumu ("dipten % kaç yükseldi")
    R["f_lo48"], R["f_hi48"] = l.rolling(48, min_periods=20).min(), h.rolling(48, min_periods=20).max()
    R["f_lo12"], R["f_hi12"] = l.rolling(12, min_periods=6).min(), h.rolling(12, min_periods=6).max()
    rng = (R["f_hi48"] - R["f_lo48"]).replace(0, np.nan)
    R["f_pos"] = (c - R["f_lo48"]) / rng                     # 0 = dipte, 1 = tepede
    R["f_from_lo"] = (c / R["f_lo48"] - 1) * 100             # dipten yükseliş %
    R["f_from_hi"] = (c / R["f_hi48"] - 1) * 100             # tepeden düşüş % (negatif)

    # ---- SKOR
    keys = list(WEIGHTS)
    comp = R[keys].astype(float)
    w = np.array([W[k] for k in keys], float)
    mask = comp.notna().values
    num = np.nansum(comp.values * w, axis=1)
    den = (mask * w).sum(axis=1)
    R["score"] = np.round(50 + 50 * num / np.where(den == 0, np.nan, den), 1)
    R["decision"] = decision(R["score"].fillna(50))
    R.loc[R.index[:210], "score"] = np.nan  # ısınma (EMA200)
    return R


# ---------------------------------------------------------------- stratejiler
# Ortak strateji tanımı (araştırma, canlı bot ve uygulama aynı kuralı kullanır)
DEFAULT_STRATEGY = {"type": "trend", "lt": 58, "st": 42.99, "max_ext": None, "htf": False,
                    "sl": 1.5, "tp1": 1.5, "tp2": 3.0, "max_new": 99}


def signals(R, score, st):
    """Her mum için +1 / -1 / 0 ve sinyal gücü."""
    typ = st.get("type", "trend")
    z = R["f_z"].values.astype(float)
    rsi = R["f_rsi"].values.astype(float)
    htf = np.nan_to_num(R["f_htf"].values.astype(float))
    ext = np.nan_to_num(R["f_vwap_atr"].values.astype(float))
    sc = np.nan_to_num(np.asarray(score, float), nan=50)
    valid = ~np.isnan(np.asarray(score, float))
    if typ == "trend":
        d = np.where(sc >= st["lt"], 1, np.where(sc <= st["st"], -1, 0))
        if st.get("max_ext") is not None:
            d = np.where(np.abs(ext) > st["max_ext"], 0, d)  # aşırı uzamış fiyatı kovalama
        strength = np.abs(sc - 50)
    elif typ == "meanrev":
        zt, hi, lo = st["z"], st["rsi_hi"], st["rsi_lo"]
        d = np.where((z <= -zt) & (rsi <= lo), 1, np.where((z >= zt) & (rsi >= hi), -1, 0))
        if st.get("need_sweep"):
            d = np.where((d > 0) & (R["f_ssl3"].values > 0), 1, np.where((d < 0) & (R["f_bsl3"].values > 0), -1, 0))
        strength = np.nan_to_num(np.abs(z))
    elif typ == "pullback":  # yön trendden; tepede long / dipte short açılmaz
        d = np.where(sc >= st["lt"], 1, np.where(sc <= st["st"], -1, 0))
        pos = np.nan_to_num(R["f_pos"].values.astype(float), nan=0.5)
        mp = st.get("max_pos", 0.6)
        d = np.where((d > 0) & (pos > mp), 0, np.where((d < 0) & (pos < 1 - mp), 0, d))
        strength = np.abs(sc - 50)
    elif typ == "rules":  # kazanan işlemlerin ortak noktalarından çıkarılan kurallar (mine15)
        import mine15
        d = np.where(sc >= st.get("lt", 55), 1, np.where(sc <= st.get("st", 45), -1, 0))
        d = mine15.rule_signals(R, d, st["conds"])
        strength = np.abs(sc - 50)
    else:  # sweep
        d = np.where(R["f_ssl1"].values > 0, 1, np.where(R["f_bsl1"].values > 0, -1, 0))
        strength = np.nan_to_num(np.abs(ext))
    if st.get("htf") == "with":
        d = np.where(d * np.sign(htf) > 0, d, 0)
    elif st.get("htf") == "against":
        d = np.where(d * np.sign(htf) < 0, d, 0)
    d = np.where(valid & np.isfinite(z), d, 0)
    return d.astype(int), strength


def pullback_levels(R, d, st):
    """Geri çekilme stratejisi için her sinyal mumunda limit emir seviyeleri.
    Dönen: entry, sl, tp1, tp2 dizileri ve geçerli (risk/ödül uygun) sinyal maskesi."""
    c = R["c"].values.astype(float)
    A = R["atr"].values.astype(float)
    lo, hi = R["f_lo48"].values.astype(float), R["f_hi48"].values.astype(float)
    lo_s = R["f_lo12" if st.get("stop_lb", 12) == 12 else "f_lo48"].values.astype(float)
    hi_s = R["f_hi12" if st.get("stop_lb", 12) == 12 else "f_hi48"].values.astype(float)
    if st.get("entry") == "fib":  # dip-tepe aralığının f geri çekilmesi (fiyat zaten altındaysa mevcut fiyat)
        f = st.get("fib", 0.5)
        e_long = np.minimum(c, hi - f * (hi - lo))
        e_short = np.maximum(c, lo + f * (hi - lo))
    else:  # mevcut fiyatın k ATR altı/üstü
        k = st.get("k", 0.5)
        e_long, e_short = c - k * A, c + k * A
    buf = st.get("buf", 0.3)
    sl_long = np.minimum(lo_s - buf * A, e_long - 0.8 * A)    # yapısal stop: son dibin altı (en az 0.8 ATR)
    sl_short = np.maximum(hi_s + buf * A, e_short + 0.8 * A)
    entry = np.where(d > 0, e_long, e_short)
    sl = np.where(d > 0, sl_long, sl_short)
    risk = np.abs(entry - sl)
    tp1 = entry + d * risk * st.get("tp1", 1.5)
    tp2 = entry + d * risk * st.get("tp2", 2.5)
    ok = (d != 0) & np.isfinite(entry) & np.isfinite(sl) & (risk <= st.get("max_risk", 3.0) * A) & (risk > 0)
    return entry, sl, tp1, tp2, ok


def order_levels(R, d, st):
    """Limit emirli stratejiler için seviyeler (pullback: yapısal; rules+limit: ATR tabanlı)."""
    if st.get("type") == "pullback":
        return pullback_levels(R, d, st)
    c = R["c"].values.astype(float)
    A = R["atr"].values.astype(float)
    k = st.get("limit", 0.5)
    e = c - d * k * A
    sl = e - d * st.get("sl", 1.0) * A
    t1 = e + d * st.get("tp1", 1.5) * A
    t2 = e + d * st.get("tp2", 2.5) * A
    ok = (d != 0) & np.isfinite(e) & np.isfinite(A) & (A > 0)
    return e, sl, t1, t2, ok


def uses_limit(st):
    return st.get("type") == "pullback" or st.get("limit") is not None


def strategy_name(st):
    t = st.get("type")
    ex = f"SL{st.get('sl')}/TP{st.get('tp1')}-{st.get('tp2')}"
    h = {"with": " +üst trend yönünde", "against": " +üst trende karşı"}.get(st.get("htf"), "")
    if t == "trend":
        e = f", VWAP'tan ≤{st['max_ext']} ATR" if st.get("max_ext") is not None else ""
        return f"Trend takibi (skor ≥{st['lt']} / ≤{round(st['st'])}{e}){h}, {ex}"
    if t == "meanrev":
        return f"Ortalamaya dönüş (|Z|≥{st['z']}, RSI {st['rsi_lo']}/{st['rsi_hi']}{', likidite avı şart' if st.get('need_sweep') else ''}){h}, {ex}"
    if t == "pullback":
        ent = f"{st.get('fib', 0.5)} Fibonacci geri çekilmesine" if st.get("entry") == "fib" else f"fiyatın {st.get('k', 0.5)} ATR gerisine"
        return (f"Geri çekilmede limit giriş (skor ≥{st['lt']} / ≤{round(st['st'])}, dip-tepe aralığının en fazla %{int(st.get('max_pos', 0.6) * 100)}'inde, "
                f"{ent} limit emir, {st.get('expire', 6)} mum geçerli, stop son {st.get('stop_lb', 12)} mumun dibinin/tepesinin ötesi, "
                f"hedef {st.get('tp1', 1.5)}R / {st.get('tp2', 2.5)}R){h}")
    if t == "rules":
        import mine15
        lim = f", fiyatın {st['limit']} ATR gerisine limit emirle giriş ({st.get('expire', 6)} mum geçerli)" if st.get("limit") is not None else ""
        return f"Kazanan ortak noktaları kuralı (skor ≥{st.get('lt', 55)} / ≤{st.get('st', 45)} VE {mine15.rule_text(st['conds'])}){lim}{h}, {ex}"
    return f"Likidite avı tersine dönüş{h}, {ex}"
