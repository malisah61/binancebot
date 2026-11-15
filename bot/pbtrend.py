"""Canlı sinyal: trend yönünde geri çekilmede limit giriş (1 yıllık testte 4s/3s/2s'de eğitim+TEST'te doğrulandı).

Kurulumlar (BTC aynı zaman diliminde aynı trendde olmalı; yalnız hacimde ilk 150 coin — büyük + orta):
  4s: son 20 mumluk salınımın %50 geri çekilmesine limit
  3s: son 20 mumluk salınımın %50 geri çekilmesine limit   (3s mumu 1s mumlardan kurulur)
  2s: EMA20'ye limit
Trend: kapanış > EMA200, EMA50 > EMA200, EMA50 son 5 mumda yükseliyor (düşüş trendi tersi); son 3 mumda yeni 20 mumluk
tepe/dip ve fiyat EMA20'nin trend tarafında. Stop: giriş − 1 ATR ve son 10 mumun dibinin 0.3 ATR altı (uzak olan);
hedef 1.5R (yarısı, stop girişe) / 3R; limit 6 mum içinde dolmazsa iptal; en çok 7 gün (4s) / 6 gün (3s) / 4 gün (2s).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

SETUPS = {
    "4h": {"entry": "f50", "ms": 4 * 3_600_000, "hold": 42, "desc": "4s trend · %50 geri çekilme"},
    "3h": {"entry": "f50", "ms": 3 * 3_600_000, "hold": 48, "desc": "3s trend · %50 geri çekilme"},
    "2h": {"entry": "ema20", "ms": 2 * 3_600_000, "hold": 48, "desc": "2s trend · EMA20 geri çekilme"},
}
MAX_RANK = 150


def bars(k1h, ms, now):
    """1 saatlik mumlardan kapanmış üst periyot mumları."""
    k = k1h[k1h["t"] + 3_600_000 <= now]
    g = k.groupby(k["t"] // ms)
    d = g.agg(t=("t", "first"), o=("o", "first"), h=("h", "max"), l=("l", "min"), c=("c", "last"), n=("t", "size")).reset_index(drop=True)
    d = d[d["n"] == ms // 3_600_000].reset_index(drop=True)
    return d[d["t"] + ms <= now].reset_index(drop=True)


def _atr(h, l, c, n=14):
    pc = np.r_[c[0], c[:-1]]
    tr = np.maximum(h - l, np.maximum(np.abs(h - pc), np.abs(l - pc)))
    return pd.Series(tr).ewm(alpha=1 / n, adjust=False).mean().values


def trend_state(c):
    e20, e50, e200 = (pd.Series(c).ewm(span=n, adjust=False).mean().values for n in (20, 50, 200))
    p50 = np.r_[np.full(5, np.nan), e50[:-5]]
    up = (c > e200) & (e50 > e200) & (e50 > p50)
    dn = (c < e200) & (e50 < e200) & (e50 < p50)
    return e20, up, dn


def signal(d, btc_dir, setup):
    """Son kapanmış mumda kurulum var mı → (yön, plan) veya None. d: üst periyot mumları (≥260)."""
    if len(d) < 260:
        return None
    o, h, l, c = (d[q].values.astype(float) for q in "ohlc")
    i = len(c) - 1
    a = _atr(h, l, c)
    e20, up, dn = trend_state(c)
    hh, ll = pd.Series(h).rolling(20).max().values, pd.Series(l).rolling(20).min().values
    for dirn, ok in ((1, up[i]), (-1, dn[i])):
        if not ok or btc_dir != dirn:
            continue
        fresh = h[i - 2:i + 1].max() >= hh[i] if dirn == 1 else l[i - 2:i + 1].min() <= ll[i]
        side = c[i] > e20[i] if dirn == 1 else c[i] < e20[i]
        if not (fresh and side):
            continue
        if setup["entry"] == "ema20":
            lv = e20[i]
        else:
            lv = hh[i] - 0.5 * (hh[i] - ll[i]) if dirn == 1 else ll[i] + 0.5 * (hh[i] - ll[i])
        if (dirn == 1 and lv >= c[i]) or (dirn == -1 and lv <= c[i]):
            continue
        ll10, hh10 = l[max(0, i - 9):i + 1].min(), h[max(0, i - 9):i + 1].max()
        stop = min(lv - a[i], ll10 - 0.3 * a[i]) if dirn == 1 else max(lv + a[i], hh10 + 0.3 * a[i])
        risk = abs(lv - stop)
        t_close = int(d["t"].iloc[i]) + setup["ms"]
        return dirn, {"entry": float(lv), "sl": float(stop), "tp1": float(lv + dirn * 1.5 * risk), "tp2": float(lv + dirn * 3 * risk),
                      "expire_t": t_close + 6 * setup["ms"], "until_ms": setup["hold"] * setup["ms"], "score": 0.0, "bar_t": int(d["t"].iloc[i])}
    return None


def btc_direction(btc1h, ms, now):
    d = bars(btc1h, ms, now)
    if len(d) < 210:
        return 0
    c = d["c"].values.astype(float)
    _, up, dn = trend_state(c)
    return 1 if up[-1] else (-1 if dn[-1] else 0)
