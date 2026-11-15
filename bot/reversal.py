"""Dipten dönüş yükselişleri: öncesinde ne oluyor? + strateji simülasyonu.

Tanım (1 saatlik mumlar):
  TETİK: coin son 30 günün en düşük fiyatını son 24 saat içinde gördü (yeni 30g dip = L) ve fiyat bu dipten
         ilk kez %3 yukarıda kapattı. Her dip için tek tetik. (O anda bilinmeyen hiçbir şey kullanılmaz.)
  SONUÇ: sonraki 7 gün içinde fiyat dibin %20 üstüne çıktı mı (BAŞARILI DÖNÜŞ / "pump"),
         yoksa önce dibin altına mı indi (BAŞARISIZ DİP)?
Öncü işaretler (tetik anında): son 30 günde düşüş derinliği, hacim artışı (RVOL), agresif alım oranı ve
  değişimi, oynaklık sıkışması, RSI ve pozitif uyumsuzluk, dip mumunun alt fitili, likidite avı, BTC'nin
  durumu, dipten bu yana geçen süre + (futures arşivinden) Open Interest değişimi, funding, long/short oranları.
Analiz: başarılı ve başarısız diplerin bu özelliklerdeki farkı (eğitim ve test ayrı), sonra eğitimde kural
  arama ve modelin görmediği dönemde test. Strateji: tetikte gir, stop dibin %0.5 altı, hedef 3R (yarısı 1.5R'de),
  en çok 7 gün; 3x ve 5x kaldıraçla simülasyon.
"""
from __future__ import annotations

import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone

import numpy as np
import pandas as pd
import requests

sys.path.insert(0, os.path.dirname(__file__))
import binance  # noqa: E402
import research  # noqa: E402
import telegram  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, "data", "cache", "rev")
BASE = "https://data.binance.vision/data/futures/um"
N_COINS = int(os.environ.get("REV_COINS", 120))
DAYS = int(os.environ.get("REV_DAYS", 120))
MET_DAYS = 90
H30, H24, H7D = 720, 24, 168
PUMP = 0.20
FEE = 0.0010   # gidiş-dönüş taker

FEATS = {"dd30": "30 günlük tepeden düşüş %", "rvol24": "Son 24s hacim / önceki 7g ort.", "taker24": "Son 24s agresif alım oranı",
         "taker_chg": "Agresif alım değişimi (24s - önceki 72s)", "squeeze": "Oynaklık sıkışması (24s ATR / 7g ATR)",
         "rsi": "RSI(14s) tetikte", "div": "RSI pozitif uyumsuzluk (dip daha alçak, RSI daha yüksek)", "wick": "Dip mumunun alt fitil oranı",
         "sweep": "Likidite avı (7g dibin altına fitil, üstünde kapanış)", "btc24": "BTC son 24s %", "btc7": "BTC son 7g %",
         "hrs": "Dipten bu yana saat", "drop24": "Dibe son 24s'te düşüş %", "vol_trend": "Hacim eğilimi (son 3g / önceki 7g)",
         "oi72": "OI değişimi dipten önceki 72s %", "oi24": "OI değişimi son 24s %", "fund": "Funding (son)",
         "gls": "Global L/S", "gls_chg": "Global L/S 24s değişim", "tls": "Top trader L/S", "risk": "Stop mesafesi %"}
LIVE_FEATS = ["dd30", "rvol24", "taker24", "taker_chg", "squeeze", "rsi", "div", "wick", "sweep", "btc24", "btc7", "hrs", "drop24", "vol_trend", "risk"]


# ---------------------------------------------------------------- veri
def jobs(sym, today):
    out = []
    start = today - timedelta(days=DAYS + 35)
    m = datetime(start.year, start.month, 1, tzinfo=timezone.utc)
    cur = datetime(today.year, today.month, 1, tzinfo=timezone.utc)
    while m < cur:
        ym = m.strftime("%Y-%m")
        out.append(("k", f"{BASE}/monthly/klines/{sym}/1h/{sym}-1h-{ym}.zip", f"{CACHE}/k/{sym}/{ym}.zip", False))
        out.append(("f", f"{BASE}/monthly/fundingRate/{sym}/{sym}-fundingRate-{ym}.zip", f"{research.CACHE}/f/{sym}/{ym}.zip", False))
        m = (m + timedelta(days=32)).replace(day=1)
    d = cur
    while d < today:
        ds = d.strftime("%Y-%m-%d")
        out.append(("k", f"{BASE}/daily/klines/{sym}/1h/{sym}-1h-{ds}.zip", f"{CACHE}/kd/{sym}/{ds}.zip", (today - d).days <= 3))
        d += timedelta(days=1)
    d = today - timedelta(days=MET_DAYS)
    while d < today:
        ds = d.strftime("%Y-%m-%d")
        out.append(("m", f"{BASE}/daily/metrics/{sym}/{sym}-metrics-{ds}.zip", f"{research.CACHE}/m/{sym}/{ds}.zip", (today - d).days <= 3))
        d += timedelta(days=1)
    return out


def load_all(today):
    syms = [x["symbol"] for x in binance.top_usdt(N_COINS + 20)]
    if "BTCUSDT" not in syms:
        syms = ["BTCUSDT"] + syms
    J = [(s, *j) for s in syms for j in jobs(s, today)]
    print(f"{len(syms)} coin, {len(J)} dosya")
    with ThreadPoolExecutor(32) as ex:
        paths = list(ex.map(lambda j: research.fetch(j[2], j[3], j[4]), J))
    per = {}
    for j, p in zip(J, paths):
        per.setdefault(j[0], []).append((j[1], p))
    data = {}
    for s in syms:
        r = research.load_coin(s, per[s])
        if r is None or len(r[0]) < H30 + 200:
            continue
        k, met, fund = r
        k = research.with_extras(k, "1h", met, fund)
        data[s] = k
        if len(data) >= N_COINS:
            break
    return data


# ---------------------------------------------------------------- özellikler + tetikler
def rsi(c, n=14):
    d = np.diff(c, prepend=c[0])
    up = pd.Series(np.clip(d, 0, None)).ewm(alpha=1 / n, adjust=False).mean().values
    dn = pd.Series(np.clip(-d, 0, None)).ewm(alpha=1 / n, adjust=False).mean().values
    return 100 - 100 / (1 + up / np.maximum(dn, 1e-12))


def triggers(k, btc=None, label=True):
    """Bir coinde tüm tetikler + özellikler (+ sonuç etiketi)."""
    o, h, l, c, v = (k[x].values.astype(float) for x in "ohlcv")
    qv, tq = k["qv"].values.astype(float), k["tq"].values.astype(float)
    t = k["t"].values
    n = len(c)
    if n < H30 + 30:
        return []
    low30 = pd.Series(l).rolling(H30, min_periods=H30).min().values
    hi30 = pd.Series(h).rolling(H30, min_periods=H30).max().values
    low24 = pd.Series(l).rolling(H24).min().values
    tr = np.maximum(h - l, np.maximum(abs(h - np.r_[c[0], c[:-1]]), abs(l - np.r_[c[0], c[:-1]])))
    atr24 = pd.Series(tr).rolling(24).mean().values
    atr7 = pd.Series(tr).rolling(H7D).mean().values
    R = rsi(c)
    cv = pd.Series(v)
    vol24 = cv.rolling(24).sum().values
    vol7 = cv.rolling(H7D).sum().values
    vol3d = cv.rolling(72).sum().values
    tqs, qvs = pd.Series(tq), pd.Series(qv)
    tk24 = (tqs.rolling(24).sum() / qvs.rolling(24).sum()).values
    tk72p = (tqs.shift(24).rolling(72).sum() / qvs.shift(24).rolling(72).sum()).values
    oi = k["oi"].values.astype(float) if "oi" in k else np.full(n, np.nan)
    gls = k["gls"].values.astype(float) if "gls" in k else np.full(n, np.nan)
    tls = k["tls"].values.astype(float) if "tls" in k else np.full(n, np.nan)
    fund = k["funding"].values.astype(float) if "funding" in k else np.full(n, np.nan)
    out = []
    last_bottom = -10 ** 9
    i = H30
    while i < n - 1:
        # son 24 saatte yeni 30g dip görülmüş ve fiyat dipten ilk kez %3 yukarıda kapatmış
        if low24[i] <= low30[i] + 1e-12 and c[i] >= low24[i] * 1.03 and c[i - 1] < low24[i] * 1.03:
            b = i - 23 + int(np.argmin(l[i - 23:i + 1]))  # dip mumu
            if b - last_bottom < 48 or i - b < 1:
                i += 1
                continue
            L = l[b]
            last_bottom = b
            prev = np.where(l[max(0, b - H30):b - 24] <= np.min(l[max(0, b - H30):b - 24]) + 1e-12)[0]
            pb = max(0, b - H30) + int(prev[-1]) if len(prev) else None
            f = {"dd30": (L / hi30[i] - 1) * 100,
                 "rvol24": vol24[i] / max(vol7[i] / 7, 1e-12),
                 "taker24": tk24[i], "taker_chg": tk24[i] - tk72p[i],
                 "squeeze": atr24[i] / max(atr7[i], 1e-12), "rsi": R[i],
                 "div": float(pb is not None and l[b] < l[pb] and R[b] > R[pb]),
                 "wick": (min(o[b], c[b]) - l[b]) / max(h[b] - l[b], 1e-12),
                 "sweep": float(l[b] < np.min(l[b - H7D:b - 1]) and c[b] > np.min(l[b - H7D:b - 1])),
                 "hrs": float(i - b), "drop24": (L / h[max(0, b - 24):b + 1].max() - 1) * 100,
                 "vol_trend": (vol3d[i] / 3) / max(vol7[i - 72] / 7, 1e-12) if i >= 72 + H7D else np.nan,
                 "oi72": (oi[b] / oi[b - 72] - 1) * 100 if b >= 72 and oi[b - 72] > 0 else np.nan,
                 "oi24": (oi[i] / oi[i - 24] - 1) * 100 if oi[i - 24] > 0 else np.nan,
                 "fund": fund[i] * 100, "gls": gls[i], "gls_chg": gls[i] - gls[i - 24], "tls": tls[i],
                 "risk": (c[i] / (L * 0.995) - 1) * 100}
            if btc is not None:
                f["btc24"] = float(btc.get(t[i], np.nan))
                f["btc7"] = float(btc.get(("7", t[i]), np.nan))
            ev = {"i": i, "b": b, "t": int(t[i]), "tb": int(t[b]), "price": float(c[i]), "low": float(L), **f}
            if label:
                ev.update(outcome(h, l, c, i, L))
            out.append(ev)
        i += 1
    return out


def outcome(h, l, c, i, L):
    """Sonraki 7 gün: dibin %20 üstü mü önce, yoksa dibin altı mı? + strateji işlemi (R)."""
    e = c[i]
    stop = L * 0.995
    risk = (e - stop) / e
    H, Lw = h[i + 1:i + 1 + H7D], l[i + 1:i + 1 + H7D]
    if not len(H):
        return {"pump": np.nan, "R": np.nan}
    js = int(np.argmax(Lw <= stop)) if (Lw <= stop).any() else 10 ** 9
    jp = int(np.argmax(H >= L * (1 + PUMP))) if (H >= L * (1 + PUMP)).any() else 10 ** 9
    pump = 1.0 if jp < js else 0.0
    t1, t2 = e * (1 + 1.5 * risk), e * (1 + 3 * risk)
    j1 = int(np.argmax(H >= t1)) if (H >= t1).any() else 10 ** 9
    j2 = int(np.argmax(H >= t2)) if (H >= t2).any() else 10 ** 9
    if js <= j1 and js < 10 ** 9:
        r = -1.0
    elif j1 < 10 ** 9:
        after = Lw[j1 + 1:]
        jb = int(np.argmax(after <= e)) if (after <= e).any() else 10 ** 9
        if j2 <= j1:
            r = 2.25
        elif j2 < 10 ** 9 and (jb >= j2 - j1 - 1):
            r = 2.25
        elif jb < 10 ** 9:
            r = 0.75
        else:
            r = 0.75 + 0.5 * (c[min(len(c) - 1, i + H7D)] / e - 1) / risk
    else:
        r = (c[min(len(c) - 1, i + H7D)] / e - 1) / risk
    r -= FEE / max(risk, 1e-9)
    mx = float(H.max() / L - 1) * 100
    return {"pump": pump, "R": float(r), "max_up": mx, "risk_pct": risk * 100}


def btc_map(k):
    c = k["c"].values.astype(float)
    t = k["t"].values
    m = {}
    for i in range(H7D, len(c)):
        m[t[i]] = (c[i] / c[i - 24] - 1) * 100
        m[("7", t[i])] = (c[i] / c[i - H7D] - 1) * 100
    return m


# ---------------------------------------------------------------- analiz
def compare(E, split):
    res = []
    for f, name in FEATS.items():
        if f not in E or E[f].notna().sum() < 30:
            continue
        row = {"feat": f, "name": name}
        for tag, D in (("train", E[E["t"] < split]), ("test", E[E["t"] >= split])):
            a, b = D.loc[D["pump"] == 1, f].dropna(), D.loc[D["pump"] == 0, f].dropna()
            sd = float(D[f].std()) or 1e-9
            row[tag] = {"pump": round(float(a.median()), 3) if len(a) else None, "fail": round(float(b.median()), 3) if len(b) else None,
                        "d": round(float((a.mean() - b.mean()) / sd), 3) if len(a) and len(b) else None, "n": [int(len(a)), int(len(b))]}
        row["stable"] = bool(row["train"]["d"] is not None and row["test"]["d"] is not None and np.sign(row["train"]["d"]) == np.sign(row["test"]["d"])
                             and abs(row["test"]["d"]) >= 0.1 and abs(row["train"]["d"]) >= 0.1)
        res.append(row)
    res.sort(key=lambda r: -abs(r["train"]["d"] or 0))
    return res


def mine(E, split, feats, beam=6, max_rules=5):
    tr = E[(E["t"] < split) & E["R"].notna()]
    y = tr["R"].values
    mid = tr["t"].median()
    h1 = tr["t"].values < mid
    nmin = max(25, int(len(tr) * 0.08))
    cands = []
    for f in feats:
        x = tr[f].values.astype(float)
        if np.isnan(x).mean() > 0.3:
            continue
        for q in np.unique(np.nanquantile(x, [0.2, 0.33, 0.5, 0.67, 0.8])):
            cands += [(f, ">=", float(q)), (f, "<=", float(q))]
    M = {cd: np.nan_to_num((tr[cd[0]].values >= cd[2]) if cd[1] == ">=" else (tr[cd[0]].values <= cd[2]), nan=0).astype(bool) for cd in cands}
    frontier, found = [((), np.ones(len(y), bool))], []
    for _ in range(3):
        nxt = []
        for conds, m in frontier:
            used = {c[0] for c in conds}
            for cd in cands:
                if cd[0] in used:
                    continue
                mm = m & M[cd]
                if mm.sum() < nmin or (mm & h1).sum() < nmin // 3 or (mm & ~h1).sum() < nmin // 3:
                    continue
                nxt.append((float(y[mm].mean()), conds + (cd,), mm))
        nxt.sort(key=lambda x: -x[0])
        frontier, seen = [], set()
        for mu, conds, mm in nxt:
            key = frozenset(conds)
            if key in seen:
                continue
            seen.add(key)
            frontier.append((conds, mm))
            a, b = y[mm & h1].mean(), y[mm & ~h1].mean()
            if a > 0 and b > 0:
                found.append({"conds": [list(c) for c in conds], "train": {"avg_R": round(mu, 3), "n": int(mm.sum()),
                              "pump": round(float(tr["pump"].values[mm].mean() * 100), 1)}, "halves": [round(float(a), 3), round(float(b), 3)]})
            if len(frontier) >= beam:
                break
    found.sort(key=lambda r: -r["train"]["avg_R"] * np.sqrt(r["train"]["n"]))
    out, seen = [], set()
    for r in found:
        k = frozenset((c[0], c[1]) for c in r["conds"])
        if k not in seen:
            seen.add(k); out.append(r)
        if len(out) >= max_rules:
            break
    return out


def apply_rule(D, conds):
    m = np.ones(len(D), bool)
    for f, op, th in conds:
        x = D[f].values.astype(float)
        m &= np.nan_to_num((x >= th) if op == ">=" else (x <= th), nan=0).astype(bool)
    return m


def trade_stats(D, lev):
    r = D["R"].dropna().values
    if not len(r):
        return {"n": 0}
    risk = D.loc[D["R"].notna(), "risk_pct"].values / 100
    roe = np.maximum(lev * r * risk, -1.0)  # R × risk% × kaldıraç (likidasyon tavanı)
    pos, neg = roe[roe > 0].sum(), -roe[roe < 0].sum()
    return {"n": int(len(r)), "win": round(float((r > 0).mean() * 100), 1), "avg_R": round(float(r.mean()), 3),
            "avg_roe": round(float(roe.mean() * 100), 2), "pf": round(float(pos / neg), 2) if neg > 0 else None,
            "pump": round(float(D["pump"].mean() * 100), 1), "liq": int((lev * risk >= 1 - 0.005 * lev).sum())}


def rule_text(conds):
    return " VE ".join(f"{FEATS.get(f, f)} {'≥' if op == '>=' else '≤'} {th:.3g}" for f, op, th in conds)


# ---------------------------------------------------------------- canlı tarama (şu an dipten dönen coinler)
def coingecko_trending():
    try:
        r = requests.get("https://api.coingecko.com/api/v3/search/trending", timeout=15)
        return [x["item"]["symbol"].upper() for x in r.json().get("coins", [])]
    except Exception as e:
        print("coingecko:", e)
        return []


def live_scan(rules):
    out = []
    trend = coingecko_trending()
    tick = binance.top_usdt(N_COINS)
    btc = pd.DataFrame(binance.klines("BTCUSDT", "1h", 1000))
    bm = btc_map(btc)
    for x in tick:
        s = x["symbol"]
        try:
            k = pd.DataFrame(binance.klines(s, "1h", 1000))
        except Exception:
            continue
        k = k[k["t"] + 3_600_000 <= time.time() * 1000].reset_index(drop=True)
        ev = triggers(k, bm, label=False)
        ev = [e for e in ev if e["i"] >= len(k) - 48]  # son 48 saatte tetik
        for e in ev:
            D = pd.DataFrame([e])
            match = [r["text"] for r in rules if apply_rule(D, r["conds"])[0]]
            out.append({"symbol": s, "hours_ago": int(len(k) - 1 - e["i"]), "price": e["price"], "low": e["low"],
                        "now": float(k["c"].iloc[-1]), "dd30": round(e["dd30"], 1), "rvol24": round(e["rvol24"], 2),
                        "taker24": round(e["taker24"], 3), "rules": match, "trending": s[:-4] in trend,
                        "feats": {f: (round(float(e[f]), 4) if f in e and e[f] == e[f] else None) for f in LIVE_FEATS}})
    return out, trend


# ---------------------------------------------------------------- ileri test defteri (canlı kayıt)
def ledger_update(scan):
    """Her yeni dip tetiğini (özellikleri, kurala uyup uymadığı, CoinGecko trendi) kaydet; 7 gün dolunca
    gerçek sonucu (dibin %20 üstü mü, stop mu, R) hesapla. Böylece internet trendi gibi geçmişi olmayan
    işaretlerin de etkisi zamanla ölçülür."""
    path = os.path.join(ROOT, "state", "reversal_ledger.json")
    L = json.load(open(path)) if os.path.exists(path) else []
    have = {(x["symbol"], x["low"]) for x in L}
    for x in scan:
        if (x["symbol"], x["low"]) not in have:
            L.append({**x, "t_add": int(time.time() * 1000), "done": False})
    now = time.time() * 1000
    for x in L:
        if x["done"] or now - x["t_add"] < 3600_000:
            continue
        try:
            k = pd.DataFrame(binance.klines(x["symbol"], "1h", 1000))
        except Exception:
            continue
        t0 = x["t_add"] - x["hours_ago"] * 3600_000
        k = k[k["t"] >= t0 - 3600_000].reset_index(drop=True)
        if len(k) < 2:
            continue
        h, l, c = (k[q].values.astype(float) for q in "hlc")
        h = np.r_[np.nan, h[1:]]; l = np.r_[np.nan, l[1:]]
        c[0] = x["price"]
        o = outcome(np.nan_to_num(h, nan=x["price"]), np.nan_to_num(l, nan=x["price"]), c, 0, x["low"])
        x.update({k2: (None if isinstance(v, float) and np.isnan(v) else v) for k2, v in o.items()})
        x["done"] = bool(now - t0 > H7D * 3600_000 or (x.get("pump") == 1.0) or (x.get("R") is not None and x["R"] <= -0.99))
    json.dump(L[-3000:], open(path, "w"), ensure_ascii=False, default=float)
    D = [x for x in L if x["done"] and x.get("R") is not None]

    def st(g):
        return {"n": len(g), "pump": round(100 * np.mean([y.get("pump", 0) for y in g]), 1) if g else None,
                "avg_R": round(float(np.mean([y["R"] for y in g])), 3) if g else None}
    return {"all": st(D), "rule": st([y for y in D if y.get("rules")]), "trending": st([y for y in D if y.get("trending")]),
            "not_trending": st([y for y in D if not y.get("trending")]), "open": sum(1 for x in L if not x["done"])}


# ---------------------------------------------------------------- ana
def main():
    t0 = time.time()
    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    data = load_all(today)
    print(f"{len(data)} coin yüklendi ({time.time()-t0:.0f} sn)")
    bm = btc_map(data["BTCUSDT"]) if "BTCUSDT" in data else None
    rows = []
    for s, k in data.items():
        for e in triggers(k, bm):
            e["sym"] = s
            rows.append(e)
    E = pd.DataFrame(rows)
    E = E[E["t"] >= (today - timedelta(days=DAYS)).timestamp() * 1000].reset_index(drop=True)
    split = float(np.quantile(E["t"], 0.7))
    print(f"{len(E)} tetik, başarılı dönüş oranı %{E['pump'].mean()*100:.1f}")
    cmp_ = compare(E, split)
    rules_all = mine(E, split, [f for f in FEATS if f in E])
    rules_live = mine(E, split, [f for f in LIVE_FEATS if f in E])
    te = E[E["t"] >= split]
    for r in rules_all + rules_live:
        m = apply_rule(te, r["conds"])
        r["test"] = {"3": trade_stats(te[m], 3), "5": trade_stats(te[m], 5)}
        r["text"] = rule_text(r["conds"])
    base = {"train": {"3": trade_stats(E[E["t"] < split], 3)}, "test": {"3": trade_stats(te, 3), "5": trade_stats(te, 5)}}
    best = rules_live[0] if rules_live else None
    adopted = bool(best and best["test"]["3"].get("n", 0) >= 20 and (best["test"]["3"].get("avg_R") or -9) > 0.1
                   and (best["test"]["3"].get("pf") or 0) > 1.1 and best["train"]["avg_R"] > 0.1)
    top = E.sort_values("max_up", ascending=False).head(25)
    biggest = [{"sym": r.sym, "date": datetime.fromtimestamp(r.tb / 1000, timezone.utc).strftime("%d.%m.%Y %H:00"), "low": r.low,
                "max_up": round(r.max_up, 1), "dd30": round(r.dd30, 1), "rvol24": round(r.rvol24, 2), "oi72": None if np.isnan(r.oi72) else round(r.oi72, 1),
                "fund": None if np.isnan(r.fund) else round(r.fund, 4)} for r in top.itertuples()]
    scan, trend = live_scan(rules_live)
    try:
        ledger = ledger_update(scan)
    except Exception as e:
        print("defter hatası:", e)
        ledger = None
    rep = {"time": int(time.time() * 1000), "coins": len(data), "triggers": int(len(E)), "pump_rate": round(float(E["pump"].mean() * 100), 1),
           "split": int(split), "compare": cmp_, "rules_all": rules_all, "rules_live": rules_live, "baseline": base,
           "adopted": adopted, "strategy": ({"conds": best["conds"], "text": best["text"]} if best else None),
           "biggest": biggest, "scan": scan, "trending": trend, "ledger": ledger}
    json.dump(rep, open(os.path.join(ROOT, "state", "reversal.json"), "w"), ensure_ascii=False, default=float)
    md = to_md(rep)
    path = f"docs/gunluk/dipten-donus-{(today + timedelta(hours=3)).strftime('%Y-%m-%d')}.md"
    open(os.path.join(ROOT, path), "w", encoding="utf-8").write(md)
    print(md)
    import notify
    chat = os.environ.get("TELEGRAM_CHAT_ID") or json.load(open(os.path.join(ROOT, "state", "futures.json"))).get("chat_id")
    telegram.send(chat, notify.md_to_tg(md))
    print(f"toplam {time.time()-t0:.0f} sn")


def to_md(r):
    d = datetime.fromtimestamp(r["split"] / 1000, timezone.utc).strftime("%d.%m.%Y")
    L = [f"# 🚀 Dipten Dönüş Raporu — {datetime.fromtimestamp(r['time']/1000, timezone.utc).strftime('%d.%m.%Y')}", "",
         f"{r['coins']} coin, son {DAYS} gün, 1 saatlik mumlar. {r['triggers']} dip tetiği (yeni 30g dip + dipten %3 dönüş); "
         f"bunların %{r['pump_rate']}'i 7 gün içinde dibin %20 üstüne çıktı (başarılı dönüş). Eğitim/TEST ayrımı {d}.", "",
         "## Başarılı dönüşlerden önce ne oluyor? (başarısız diplerle kıyas, medyan)", "",
         "| Öncü işaret | Başarılı | Başarısız | Etki (eğitim) | Etki (test) | Kalıcı |", "|---|---|---|---|---|---|"]
    for c in r["compare"][:14]:
        L.append(f"| {c['name']} | {c['train']['pump']} | {c['train']['fail']} | {c['train']['d']:+.2f} | {c['test']['d'] if c['test']['d'] is None else format(c['test']['d'], '+.2f')} | {'✓' if c['stable'] else '✗'} |")
    b = r["baseline"]
    L += ["", "Etki: standart fark (+ = başarılı dönüşlerde daha yüksek). Kalıcı ✓: eğitim ve test döneminde aynı yönde ve belirgin.", "",
          "## Strateji simülasyonu (tetikte gir, stop dibin altı, hedef 1,5R + 3R, en çok 7 gün)", "",
          f"Her dipte körlemesine giriş — TEST: {b['test']['3'].get('n')} işlem, kazanma %{b['test']['3'].get('win')}, ort {b['test']['3'].get('avg_R')}R, "
          f"3x ort ROE %{b['test']['3'].get('avg_roe')}, PF {b['test']['3'].get('pf')}", "",
          "| Kural (yalnız canlı verilebilen işaretler) | Eğitim ort R (n, başarılı %) | TEST n / kazanma / ort R / PF | 3x ort ROE | 5x ort ROE |", "|---|---|---|---|---|"]
    for x in r["rules_live"]:
        t3, t5 = x["test"]["3"], x["test"]["5"]
        L.append(f"| {x['text']} | {x['train']['avg_R']} ({x['train']['n']}, %{x['train']['pump']}) | {t3.get('n')} / %{t3.get('win')} / {t3.get('avg_R')} / {t3.get('pf')} | %{t3.get('avg_roe')} | %{t5.get('avg_roe')} |")
    if r["rules_all"]:
        L += ["", "Futures verisi (OI, funding, L/S) de dahil edilince:", "", "| Kural | Eğitim ort R (n) | TEST n / ort R / PF |", "|---|---|---|"]
        for x in r["rules_all"][:3]:
            t3 = x["test"]["3"]
            L.append(f"| {x['text']} | {x['train']['avg_R']} ({x['train']['n']}) | {t3.get('n')} / {t3.get('avg_R')} / {t3.get('pf')} |")
    L += ["", f"Karar: {'✅ kural TEST dönemini geçti, kâğıt hesapta uygulanıyor' if r['adopted'] else '❌ hiçbir kural TEST dönemini yeterince geçemedi; kâğıt hesapta ileri test olarak izleniyor'}", "",
          "## Son 120 günün en büyük dipten dönüşleri", ""]
    for x in r["biggest"][:12]:
        L.append(f"- {x['sym'].replace('USDT', '')} {x['date']}: dipten +%{x['max_up']} (öncesinde 30g tepeden %{x['dd30']}, RVOL {x['rvol24']}, OI 72s %{x['oi72']}, funding {x['fund']})")
    if r["scan"]:
        L += ["", "## Şu an dipten dönen coinler (son 48 saat)", ""]
        for x in sorted(r["scan"], key=lambda x: x["hours_ago"]):
            L.append(f"- {x['symbol'].replace('USDT', '')}: dip {x['low']:.6g}, şimdi {x['now']:.6g} ({x['hours_ago']} saat önce tetik), 30g düşüş %{x['dd30']}, RVOL {x['rvol24']}"
                     + (" · ✅ kurala uyuyor" if x["rules"] else "") + (" · 🔥 CoinGecko trend" if x["trending"] else ""))
    if r["trending"]:
        L += ["", "CoinGecko'da şu an trend olanlar: " + ", ".join(r["trending"][:15])]
    g = r.get("ledger")
    if g:
        L += ["", f"## İleri test defteri (canlı kaydedilen dipler, 7 gün sonra sonuçlanır; açık: {g['open']})", "",
              f"- Tümü: {g['all']['n']} dip, %{g['all']['pump']} başarılı dönüş, ort {g['all']['avg_R']}R",
              f"- Kurala uyanlar: {g['rule']['n']} dip, %{g['rule']['pump']} başarılı, ort {g['rule']['avg_R']}R",
              f"- İnternette trend olan (CoinGecko): {g['trending']['n']} dip, %{g['trending']['pump']} başarılı, ort {g['trending']['avg_R']}R · trend olmayan: {g['not_trending']['n']} dip, %{g['not_trending']['pump']}, ort {g['not_trending']['avg_R']}R"]
    L += ["", "Simülasyon/araştırmadır, yatırım tavsiyesi değildir."]
    return "\n".join(L)


if __name__ == "__main__":
    main()
