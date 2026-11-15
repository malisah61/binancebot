"""Kazanan işlemlerin ortak noktalarından kural çıkarma (15dk) — aşırı uyumu önleyen kurallarla.

1) Her coinde her mumda (skor yönüne göre) olası bir giriş "olay" sayılır ve bağımsız olarak
   sonucu etiketlenir: SL 1 ATR, TP1 1.5 ATR (yarısı + stop girişe), TP2 2.5 ATR, en çok 96 mum;
   komisyon R cinsinden düşülür. → net R
2) Her olay için o anki özellikler (yöne göre işaretlenmiş): bileşenler, Z-Score, RSI, üst trend,
   VWAP uzaklığı, RVOL, taker oranı, dip-tepe konumu, likidite avı, saat, ATR%, BTC'nin yönü.
3) Yalnızca EĞİTİM döneminde ışın araması (en çok 3 koşul): ortalama net R'yi en çok artıran
   koşul kombinasyonları. Kural; eğitimin İKİ YARISINDA da pozitif olmalı ve yeterli olay içermeli.
4) Bulunan kurallar strateji yarışmasına "rules" tipi olarak girer; benimseme kararı her zamanki gibi
   modelin görmediği TEST döneminde verilir.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

FEE_RT = 0.0007        # gidiş-dönüş komisyon (limit/taker karışık, temkinli)
SL_M, TP1_M, TP2_M, HOLD = 1.0, 1.5, 2.5, 96


def _first(m):
    return int(m.argmax()) if m.any() else 10 ** 9


def label(h, l, c, atr, idx, d, limit_k=None, expire=6, o=None):
    """Olay başına net R (bağımsız, çakışma serbest).
    limit_k verilirse: giriş = fiyatın k ATR gerisine limit emir; `expire` mum içinde dolmazsa NaN (işlem yok).
    Doluş mumunda stop da görüldüyse kötümser: stop."""
    out = np.full(len(idx), np.nan)
    n = len(c)
    for k, (i, dd) in enumerate(zip(idx, d)):
        if i >= n - 2 or not np.isfinite(atr[i]) or atr[i] <= 0:
            continue
        A = atr[i]
        if limit_k is None:
            e, start = c[i], i + 1
        else:
            e = c[i] - dd * limit_k * A
            w = (l[i + 1:i + 1 + expire] <= e) if dd > 0 else (h[i + 1:i + 1 + expire] >= e)
            if not w.any():
                continue
            f = i + 1 + int(w.argmax())
            if o is not None:
                e = min(e, o[f]) if dd > 0 else max(e, o[f])
            sl0 = e - dd * SL_M * A
            if (dd > 0 and l[f] <= sl0) or (dd < 0 and h[f] >= sl0):
                out[k] = -1.0 - FEE_RT / (SL_M * A / e)
                continue
            start = f + 1
        sl, t1, t2 = e - dd * SL_M * A, e + dd * TP1_M * A, e + dd * TP2_M * A
        H, L = h[start:start + HOLD], l[start:start + HOLD]
        i = start - 1
        if dd > 0:
            js, j1, j2 = _first(L <= sl), _first(H >= t1), _first(H >= t2)
        else:
            js, j1, j2 = _first(H >= sl), _first(L <= t1), _first(L <= t2)
        if js <= j1 and js < 10 ** 9:
            r = -1.0
        elif j1 < 10 ** 9:
            if j2 <= j1:
                r = (TP1_M + TP2_M) / 2 / SL_M
            else:
                H2, L2 = H[j1 + 1:], L[j1 + 1:]
                jb, jt = (_first(L2 <= e), _first(H2 >= t2)) if dd > 0 else (_first(H2 >= e), _first(L2 <= t2))
                if jb <= jt and jb < 10 ** 9:
                    r = 0.5 * TP1_M / SL_M
                elif jt < 10 ** 9:
                    r = (TP1_M + TP2_M) / 2 / SL_M
                else:
                    r = 0.5 * TP1_M / SL_M + 0.5 * dd * (c[min(n - 1, i + HOLD)] / e - 1) / (SL_M * A / e)
        else:
            r = dd * (c[min(n - 1, i + HOLD)] / e - 1) / (SL_M * A / e)
        out[k] = r - FEE_RT / (SL_M * A / e)
    return out


FEATS = ["trend", "momentum", "volume", "smc", "vwap", "z", "rsi", "htf", "ext", "rvol", "taker", "pos", "sweep", "hour", "atrp", "btc"]
NAMES = {"trend": "Trend (yön)", "momentum": "Momentum (yön)", "volume": "Hacim (yön)", "smc": "FVG+Likidite (yön)", "vwap": "VWAP bileşeni (yön)",
         "z": "Z-Score (yön)", "rsi": "RSI (yön, 50 merkez)", "htf": "Üst trend (yön)", "ext": "VWAP'tan uzaklık ATR (yön)", "rvol": "RVOL",
         "taker": "Agresif alım-satım (yön)", "pos": "Dip-tepe konumu (yön)", "sweep": "Likidite avı (yön)", "hour": "Saat (UTC)",
         "atrp": "ATR %", "btc": "BTC 1s yönü (yön)"}


def features(R, d, btc=None):
    """Yöne göre işaretli özellikler: pozitif = işlem yönünü destekliyor."""
    d = np.asarray(d, float)
    if btc is None and "btc4" in R:
        btc = R["btc4"].values.astype(float)
    F = {}
    for k in ("trend", "momentum", "volume", "smc", "vwap"):
        F[k] = R[k].values.astype(float) * d
    F["z"] = R["f_z"].values.astype(float) * d
    F["rsi"] = (R["f_rsi"].values.astype(float) - 50) * d
    F["htf"] = np.nan_to_num(R["f_htf"].values.astype(float)) * d
    F["ext"] = R["f_vwap_atr"].values.astype(float) * d
    F["rvol"] = R["f_rvol"].values.astype(float)
    F["taker"] = (R["f_taker"].values.astype(float) - 0.5) * d
    pos = R["f_pos"].values.astype(float)
    F["pos"] = np.where(d > 0, pos, 1 - pos)  # 0 = dipte long / tepede short (ucuz), 1 = tepede long (pahalı)
    F["sweep"] = (R["f_ssl3"].values - R["f_bsl3"].values) * d
    F["hour"] = ((R["t"].values // 3_600_000) % 24).astype(float)
    F["atrp"] = R["atr_pct"].values.astype(float)
    F["btc"] = (btc * d) if btc is not None else np.zeros(len(d))
    return F


def btc_trend(R_btc, t):
    """BTC'nin son 4 mumluk (1 saat) yönü, verilen zamanlara hizalanmış."""
    s = pd.Series(np.sign(R_btc["c"].values - np.roll(R_btc["c"].values, 4)), index=R_btc["t"].values)
    s.iloc[:4] = 0
    return s.reindex(t).fillna(0).values


def cond_mask(F, cond):
    f, op, th = cond
    x = F[f]
    return (x >= th) if op == ">=" else (x <= th)


def mine(coins, split_t, lt=55, st=45, max_rules=5, min_frac=0.03, beam=6, limit_k=None):
    """coins: {sym: (df, R, fm)} 15dk. Dönen: kural listesi [{'conds':[...], 'train':..., 'halves':...}]"""
    rows = []
    btcR = coins.get("BTCUSDT", (None, None, None))[1]
    w = {"trend": 20, "momentum": 18, "volume": 10, "smc": 10, "vwap": 5}
    for sym, (df, R, fm) in coins.items():
        comp = R[list(w)].astype(float).values
        ww = np.array(list(w.values()), float)
        mask = ~np.isnan(comp)
        sc = 50 + 50 * np.nansum(comp * ww, axis=1) / np.maximum((mask * ww).sum(axis=1), 1e-9)
        sc[R["score"].isna().values] = np.nan
        d = np.where(sc >= lt, 1, np.where(sc <= st, -1, 0))
        idx = np.flatnonzero(d)
        if not len(idx):
            continue
        if btcR is not None:
            R["btc4"] = btc_trend(btcR, R["t"].values)
        F = features(R, d)
        y = label(df["h"].values.astype(float), df["l"].values.astype(float), df["c"].values.astype(float), R["atr"].values.astype(float), idx, d[idx],
                  limit_k=limit_k, o=df["o"].values.astype(float))
        part = {k: v[idx] for k, v in F.items()}
        part["y"], part["t"] = y, R["t"].values[idx]
        rows.append(pd.DataFrame(part))
    E = pd.concat(rows).dropna(subset=["y"])
    E = E.replace([np.inf, -np.inf], np.nan).dropna()
    tr = E[E["t"] < split_t]
    te0 = E[E["t"] >= split_t]
    compare = win_loss_compare(tr, te0)
    mid = tr["t"].median()
    base = float(tr["y"].mean())
    nmin = max(400, int(len(tr) * min_frac))
    Ftr = {k: tr[k].values for k in FEATS}
    y = tr["y"].values
    h1 = tr["t"].values < mid
    cands = []
    for f in FEATS:
        qs = np.unique(np.nanquantile(Ftr[f], [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]))
        for q in qs:
            cands += [(f, ">=", float(q)), (f, "<=", float(q))]
    cache = {c: cond_mask(Ftr, c) for c in cands}

    def score(m):
        n = int(m.sum())
        if n < nmin:
            return None
        a, b = y[m & h1], y[m & ~h1]
        if len(a) < nmin // 3 or len(b) < nmin // 3:
            return None
        mu = float(y[m].mean())
        return mu, n, float(a.mean()), float(b.mean())

    frontier = [((), np.ones(len(y), bool))]
    found = []
    for depth in range(3):
        nxt = []
        for conds, m in frontier:
            used = {c[0] for c in conds}
            for c in cands:
                if c[0] in used:
                    continue
                mm = m & cache[c]
                s = score(mm)
                if s is None:
                    continue
                nxt.append((s[0], conds + (c,), mm, s))
        nxt.sort(key=lambda x: -x[0])
        # ışın: en iyi `beam` (farklı kombinasyonlar)
        seen, frontier = set(), []
        for mu, conds, mm, s in nxt:
            key = frozenset(conds)
            if key in seen:
                continue
            seen.add(key)
            frontier.append((conds, mm))
            if s[2] > 0 and s[3] > 0:  # eğitimin iki yarısında da pozitif
                found.append({"conds": [list(c) for c in conds], "train": {"avg_R": round(s[0], 3), "n": s[1]},
                              "halves": [round(s[2], 3), round(s[3], 3)]})
            if len(frontier) >= beam:
                break
    found.sort(key=lambda r: -r["train"]["avg_R"] * np.sqrt(r["train"]["n"]))
    uniq, out = set(), []
    for r in found:
        k = frozenset((c[0], c[1]) for c in r["conds"])
        if k not in uniq:
            uniq.add(k); out.append(r)
        if len(out) >= max_rules:
            break
    # test dönemi olay istatistiği (bilgi amaçlı; seçim eğitimde yapıldı)
    te = E[E["t"] >= split_t]
    Fte = {k: te[k].values for k in FEATS}
    for r in out:
        m = np.ones(len(te), bool)
        for c in r["conds"]:
            m &= cond_mask(Fte, tuple(c))
        r["test_events"] = {"avg_R": round(float(te["y"].values[m].mean()), 3) if m.any() else None, "n": int(m.sum())}
        r["text"] = rule_text(r["conds"])
    return {"base_train_avg_R": round(base, 3), "base_test_avg_R": round(float(te["y"].mean()), 3), "events_train": int(len(tr)),
            "events_test": int(len(te)), "rules": out, "compare": compare, "limit_k": limit_k,
            "win_rate_train": round(float((tr["y"] > 0).mean() * 100), 1), "win_rate_test": round(float((te["y"] > 0).mean() * 100), 1)}


def win_loss_compare(tr, te):
    """Kazanan ve kaybeden girişlerin o anki özelliklerini kıyasla (eğitim ve test ayrı; etki = std. fark)."""
    res = []
    for f in FEATS:
        row = {"feat": f, "name": NAMES[f]}
        for tag, D in (("train", tr), ("test", te)):
            w, l = D.loc[D["y"] > 0, f], D.loc[D["y"] <= 0, f]
            sd = float(D[f].std()) or 1e-9
            row[tag] = {"win": round(float(w.mean()), 3), "loss": round(float(l.mean()), 3), "d": round(float((w.mean() - l.mean()) / sd), 3)}
        row["stable"] = bool(np.sign(row["train"]["d"]) == np.sign(row["test"]["d"]) and abs(row["test"]["d"]) >= 0.03)
        res.append(row)
    res.sort(key=lambda r: -abs(r["train"]["d"]))
    return res


def rule_text(conds):
    parts = []
    for f, op, th in conds:
        parts.append(f"{NAMES.get(f, f)} {'≥' if op == '>=' else '≤'} {th:.2f}")
    return " VE ".join(parts)


def rule_signals(R, d, conds, btc=None):
    F = features(R, d, btc)
    m = np.ones(len(d), bool)
    for c in conds:
        m &= np.nan_to_num(cond_mask(F, tuple(c)), nan=0).astype(bool)
    return np.where(m, d, 0)
