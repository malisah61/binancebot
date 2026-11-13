"""Kaldıraçlı vadeli işlem simülatörü (long + short).

Kurallar (uygulamadaki ATR planı ile aynı):
  SL = giriş ∓ 1.5×ATR, TP1 = ± 1.5×ATR (yarısı kapanır, stop girişe çekilir), TP2 = ± 3×ATR.
  En fazla `max_hold` mum tutulur, sonra kapanış fiyatından çıkılır.
  Aynı mumda hem stop hem hedef görülürse önce STOP sayılır (kötümser). TP2 aynı mumda TP1 ile
  birlikte görülürse tamamı TP2'den kapanır.
Kaldıraç: getiri marja göre (ROE) = kaldıraç × fiyat getirisi − komisyon − funding.
  Komisyon taker %0.05 (giriş + çıkış, nominal üzerinden). Likidasyon: fiyat 1/kaldıraç − %0.5 ters
  giderse (5x ≈ %19.5, 10x ≈ %9.5) ve bu seviye stoptan önce gelirse kalan marj tamamen kaybedilir.
Funding: pozisyon açıkken geçen her 8 saatlik ödeme anında long öder/short alır (oran pozitifse).
"""
from __future__ import annotations

import numpy as np

FEE = 0.0005
MMR = 0.005
H8 = 8 * 3600 * 1000


def _first(mask):
    return int(mask.argmax()) if mask.any() else 10 ** 9


def funding_marks(t, tf_ms, funding):
    """Her mum için: o mumun içinde 8 saatlik funding anı varsa oran, yoksa 0."""
    t = np.asarray(t, np.int64)
    has = (t // H8) != ((t + tf_ms) // H8)  # mum kapanışı yeni bir 8s dilimine geçiyor
    if funding is None:
        return np.zeros(len(t))
    f = np.nan_to_num(np.asarray(funding, float))
    return np.where(has, f, 0.0)


def simulate(t, h, l, c, atr, direction, lev, tf_ms, fmark=None, max_hold=100, start=0, snap=None, sl_m=1.5, tp1_m=1.5, tp2_m=3.0):
    """direction: her mum için +1 (long sinyali), -1 (short), 0. Bir coinde aynı anda tek pozisyon.
    Dönen: işlem listesi (dict)."""
    n = len(c)
    trades = []
    sig = np.flatnonzero(np.asarray(direction) != 0)
    sig = sig[sig >= start]
    liq_dist = 1.0 / lev - MMR
    if fmark is None:
        fmark = np.zeros(n)
    k = 0
    free_from = start
    while k < len(sig):
        i = sig[k]
        k += 1
        if i < free_from or i >= n - 2 or not np.isfinite(atr[i]) or atr[i] <= 0:
            continue
        d = int(direction[i])
        e, A = c[i], atr[i]
        sl, tp1, tp2 = e - d * sl_m * A, e + d * tp1_m * A, e + d * tp2_m * A
        liq = e * (1 - d * liq_dist)
        stop_is_liq = d * (liq - sl) > 0
        stop = liq if stop_is_liq else sl
        a, b = i + 1, min(n, i + 1 + max_hold)
        H, L = h[a:b], l[a:b]
        if d > 0:
            js, j1, j2 = _first(L <= stop), _first(H >= tp1), _first(H >= tp2)
        else:
            js, j1, j2 = _first(H >= stop), _first(L <= tp1), _first(L <= tp2)
        rem_path = []  # (bitiş indeksi, kalan oran) funding için
        if js <= j1 and js < 10 ** 9:  # stop önce
            j = js
            if stop_is_liq:
                pnl, reason, liq_hit = d * (stop / e - 1), "LİKİDASYON", True
            else:
                pnl, reason, liq_hit = d * (stop / e - 1), "SL", False
            fees = lev * FEE * 2
            rem_path = [(j, 1.0)]
        elif j1 < 10 ** 9:  # TP1 önce
            if j2 <= j1:
                j, pnl, reason = j1, d * ((tp1 + tp2) / 2 / e - 1), "TP2"
                rem_path = [(j1, 1.0)]
            else:
                H2, L2 = H[j1 + 1:], L[j1 + 1:]
                if d > 0:
                    jb, jt = _first(L2 <= e), _first(H2 >= tp2)
                else:
                    jb, jt = _first(H2 >= e), _first(L2 <= tp2)
                if jb <= jt and jb < 10 ** 9:
                    j, pnl, reason = j1 + 1 + jb, 0.5 * d * (tp1 / e - 1), "TP1→BE"
                elif jt < 10 ** 9:
                    j, pnl, reason = j1 + 1 + jt, d * ((tp1 + tp2) / 2 / e - 1), "TP2"
                else:
                    j = len(H) - 1
                    pnl, reason = 0.5 * d * (tp1 / e - 1) + 0.5 * d * (c[a + j] / e - 1), "SÜRE"
                rem_path = [(j1, 1.0), (j, 0.5)]
            liq_hit = False
            fees = lev * FEE * 2
        else:  # süre doldu
            j = len(H) - 1
            pnl, reason, liq_hit = d * (c[a + j] / e - 1), "SÜRE", False
            fees = lev * FEE * 2
            rem_path = [(j, 1.0)]
        # funding
        fund, prev = 0.0, 0
        for end, rem in rem_path:
            fund -= d * lev * rem * fmark[a + prev:a + end + 1].sum()
            prev = end + 1
        roe = -1.0 + fund - lev * FEE if liq_hit else lev * pnl - fees + fund
        risk = sl_m * A / e
        tr = {"i": int(i), "j": int(a + j), "dir": d, "entry": float(e), "reason": reason, "bars": int(j + 1),
              "ret": float(pnl), "R": float(pnl / risk) if not liq_hit else float(-liq_dist / risk),
              "roe": float(max(roe, -1.0 - lev * FEE)), "liq": liq_hit, "t": int(t[i]), "t_exit": int(t[a + j])}
        if snap is not None:
            tr["snap"] = {kk: (float(vv[i]) if np.isfinite(vv[i]) else None) for kk, vv in snap.items()}
        trades.append(tr)
        free_from = a + j + 1
    return trades


def stats(trades):
    n = len(trades)
    if not n:
        return {"n": 0}
    roe = np.array([x["roe"] for x in trades])
    Rm = np.array([x["R"] for x in trades])
    pos, neg = roe[roe > 0].sum(), -roe[roe < 0].sum()
    order = np.argsort([x["t_exit"] for x in trades])
    cum = np.cumsum(roe[order] * 100)  # her işleme 100$ marj
    dd = float((np.maximum.accumulate(np.maximum(cum, 0)) - cum).max())
    reasons = {}
    for x in trades:
        reasons[x["reason"]] = reasons.get(x["reason"], 0) + 1
    return {"n": n, "win": round(float((roe > 0).mean() * 100), 1), "avg_roe": round(float(roe.mean() * 100), 2),
            "med_roe": round(float(np.median(roe) * 100), 2), "pf": round(float(pos / neg), 2) if neg > 0 else None,
            "avg_R": round(float(Rm.mean()), 3), "net_100": round(float(roe.sum() * 100), 0), "max_dd_100": round(dd, 0),
            "liq": int(sum(x["liq"] for x in trades)), "avg_bars": round(float(np.mean([x["bars"] for x in trades])), 1),
            "reasons": reasons,
            "long": {"n": int(sum(1 for x in trades if x["dir"] > 0)),
                     "win": round(float(np.mean([x["roe"] > 0 for x in trades if x["dir"] > 0]) * 100), 1) if any(x["dir"] > 0 for x in trades) else None},
            "short": {"n": int(sum(1 for x in trades if x["dir"] < 0)),
                      "win": round(float(np.mean([x["roe"] > 0 for x in trades if x["dir"] < 0]) * 100), 1) if any(x["dir"] < 0 for x in trades) else None}}


def simulate_levels(t, o, h, l, c, orders, lev, tf_ms, fmark=None, max_hold=100):
    """Limit emirli işlemler. orders: [(i, dir, entry, sl, tp1, tp2, expire_bars, snap)] (i'ye göre sıralı).
    Emir i+1..i+expire mumlarında fiyat entry'ye değerse dolar (açılış daha iyiyse açılıştan).
    Doluş mumunda stop da görüldüyse kötümser: stop. Bir coinde aynı anda tek pozisyon/emir."""
    n = len(c)
    if fmark is None:
        fmark = np.zeros(n)
    liq_dist = 1.0 / lev - MMR
    trades, free_from = [], 0
    for (i, d, e, sl, tp1, tp2, exp, snap) in orders:
        if i < free_from or i >= n - 2:
            continue
        a, b = i + 1, min(n, i + 1 + exp)
        if d > 0:
            hit = np.flatnonzero(l[a:b] <= e)
        else:
            hit = np.flatnonzero(h[a:b] >= e)
        if not len(hit):
            free_from = b  # emir süresi doldu
            continue
        f = a + int(hit[0])
        fill = min(e, o[f]) if d > 0 else max(e, o[f])
        risk_px = abs(fill - sl)
        liq = fill * (1 - d * liq_dist)
        stop_is_liq = d * (liq - sl) > 0
        stop = liq if stop_is_liq else sl
        # doluş mumunda stop?
        if (d > 0 and l[f] <= stop) or (d < 0 and h[f] >= stop):
            j, pnl, reason = f, d * (stop / fill - 1), ("LİKİDASYON" if stop_is_liq else "SL")
            rem = [(f, 1.0)]
        else:
            H, L = h[f + 1:min(n, f + 1 + max_hold)], l[f + 1:min(n, f + 1 + max_hold)]
            if not len(H):
                break
            if d > 0:
                js, j1, j2 = _first(L <= stop), _first(H >= tp1), _first(H >= tp2)
            else:
                js, j1, j2 = _first(H >= stop), _first(L <= tp1), _first(L <= tp2)
            base = f + 1
            if js <= j1 and js < 10 ** 9:
                j, pnl, reason = base + js, d * (stop / fill - 1), ("LİKİDASYON" if stop_is_liq else "SL")
                rem = [(base + js, 1.0)]
            elif j1 < 10 ** 9:
                if j2 <= j1:
                    j, pnl, reason, rem = base + j1, d * ((tp1 + tp2) / 2 / fill - 1), "TP2", [(base + j1, 1.0)]
                else:
                    H2, L2 = H[j1 + 1:], L[j1 + 1:]
                    jb, jt = (_first(L2 <= fill), _first(H2 >= tp2)) if d > 0 else (_first(H2 >= fill), _first(L2 <= tp2))
                    if jb <= jt and jb < 10 ** 9:
                        j, pnl, reason = base + j1 + 1 + jb, 0.5 * d * (tp1 / fill - 1), "TP1→BE"
                    elif jt < 10 ** 9:
                        j, pnl, reason = base + j1 + 1 + jt, d * ((tp1 + tp2) / 2 / fill - 1), "TP2"
                    else:
                        j = base + len(H) - 1
                        pnl, reason = 0.5 * d * (tp1 / fill - 1) + 0.5 * d * (c[j] / fill - 1), "SÜRE"
                    rem = [(base + j1, 1.0), (j, 0.5)]
            else:
                j = base + len(H) - 1
                pnl, reason, rem = d * (c[j] / fill - 1), "SÜRE", [(j, 1.0)]
        liq_hit = reason == "LİKİDASYON"
        fund, prev = 0.0, f
        for end, r_ in rem:
            fund -= d * lev * r_ * fmark[prev:end + 1].sum()
            prev = end + 1
        # limit giriş = maker komisyonu (%0.02), çıkış taker
        fees = lev * (0.0002 + FEE)
        roe = -1.0 + fund - lev * 0.0002 if liq_hit else lev * pnl - fees + fund
        tr = {"i": int(i), "fill_i": int(f), "j": int(j), "dir": int(d), "entry": float(fill), "reason": reason, "bars": int(j - f + 1),
              "ret": float(pnl), "R": float(pnl / (risk_px / fill)) if not liq_hit else float(-liq_dist / (risk_px / fill)),
              "roe": float(max(roe, -1.0 - lev * FEE)), "liq": liq_hit, "t": int(t[i]), "t_exit": int(t[j]), "snap": snap}
        trades.append(tr)
        free_from = j + 1
    return trades
