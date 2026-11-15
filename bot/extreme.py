"""Uç hareketler: SERT DÜŞENLER ve TREND TERSİ SERT YÜKSELENLER — işlem denemesi (küçük coinler dahil).

Evren: Binance'te hacme göre ilk EX_COINS (varsayılan 300) USDT çifti. Hacim sırasına göre katman:
  büyük (1-50), orta (51-150), küçük (151+). Futures verisi olan coinlerde futures mumları, olmayanlarda spot.

Olaylar (1 saatlik mumlar, aynı coinde aynı tür olay en az 48 saat arayla):
  ÇÖKÜŞ   : kapanış son 24 saatin tepesinden en az D% aşağıda (D = 10/15/20/30).
  TT-POMPA: 1 gün önce fiyat EMA200'ün altında ve 30 günde %10+ düşmüşken (düşüş trendi),
            kapanış son 24 saatin dibinden en az P% yukarıda (P = 10/15/25/40).

Her olayda iki yön ve üç giriş biçimi denenir:
  piyasa  : olay mumunun kapanışında gir.
  limit   : daha iyi fiyata limit emir (12 saat içinde dolmazsa işlem yok).
  onay    : 12 saat içinde dönüş mumu bekle (long: önceki mumun tepesi üstünde kapanış; short: dibi altında).
Stoplar yapısal (olayın dibi/tepesi ± ATR), hedefler 1.5R (yarısı, stop girişe) ve 3R, en çok 72 saat.
Maliyet: komisyon %0.1 gidiş-dönüş + katmana göre kayma + funding (long pozitif funding öder).
Kaldıraç: 3x/5x/10x marjin getirisi; fiyat stoptan önce tasfiye mesafesine (1/kaldıraç - %0.5) giderse marjin biter.

Benimseme kuralı her yerdeki gibi: varyant + eşik EĞİTİM döneminde (ilk %70) seçilir; modelin görmediği TEST
döneminde n≥40, ort R>0, PF>1.05 ve eğitimde ort R>0 ise "doğrulandı". Değilse yalnızca kâğıt ileri test.
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

sys.path.insert(0, os.path.dirname(__file__))
import binance  # noqa: E402
import research  # noqa: E402
import telegram  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, "data", "cache", "ext")
FUT = "https://data.binance.vision/data/futures/um"
SPOT = "https://data.binance.vision/data/spot"
N_COINS = int(os.environ.get("EX_COINS", 300))
DAYS = int(os.environ.get("EX_DAYS", 365))
MET_DAYS = int(os.environ.get("EX_MET_DAYS", 60))
HOLD, WAIT, COOL = 72, 12, 48
FEE = 0.0010
SLIP = {"büyük": 0.0002, "orta": 0.0006, "küçük": 0.0015}   # her yön
DROPS = (0.10, 0.15, 0.20, 0.30)
PUMPS = (0.10, 0.15, 0.25, 0.40)
LEVS = (3, 5, 10)

# (olay, ad) -> (yön, giriş biçimi, açıklama)
VARIANTS = {
    "crash": {
        "L_mkt": (1, "mkt", "Sert düşüşte hemen LONG (tepki alımı)"),
        "L_lim": (1, "lim", "Sert düşüşte 1 ATR aşağıya limit LONG"),
        "L_conf": (1, "conf", "Sert düşüşten sonra dönüş mumu gelince LONG"),
        "S_mkt": (-1, "mkt", "Sert düşüşte hemen SHORT (devam)"),
        "S_lim": (-1, "lim", "Sert düşüşte 1.5 ATR tepki yukarısına limit SHORT"),
        "S_conf": (-1, "conf", "Sert düşüşte tepki bitip kırılım gelince SHORT"),
        "S_f38": (-1, "fib", "Düşüşün %38.2 tepkisinde limit SHORT (aynı yön)"),
        "S_f50": (-1, "fib", "Düşüşün %50 tepkisinde limit SHORT (aynı yön)"),
        "S_f62": (-1, "fib", "Düşüşün %61.8 tepkisinde limit SHORT (aynı yön)"),
    },
    "ctpump": {
        "S_mkt": (-1, "mkt", "Trend tersi pompada hemen SHORT (geri sönme)"),
        "S_lim": (-1, "lim", "Trend tersi pompada 1 ATR yukarıya limit SHORT"),
        "S_conf": (-1, "conf", "Trend tersi pompadan sonra kırılım mumu gelince SHORT"),
        "L_mkt": (1, "mkt", "Trend tersi pompada hemen LONG (devam)"),
        "L_lim": (1, "lim", "Trend tersi pompada 1.5 ATR geri çekilmeye limit LONG"),
        "L_conf": (1, "conf", "Trend tersi pompada geri çekilme sonrası yeni tepe kırılımında LONG"),
        "L_f38": (1, "fib", "Pompanın %38.2 geri çekilmesinde limit LONG (aynı yön)"),
        "L_f50": (1, "fib", "Pompanın %50 geri çekilmesinde limit LONG (aynı yön)"),
        "L_f62": (1, "fib", "Pompanın %61.8 geri çekilmesinde limit LONG (aynı yön)"),
    },
    "pump": {
        "L_mkt": (1, "mkt", "Sert yükselişte hemen LONG"),
        "L_f38": (1, "fib", "Yükselişin %38.2 geri çekilmesinde limit LONG (aynı yön)"),
        "L_f50": (1, "fib", "Yükselişin %50 geri çekilmesinde limit LONG (aynı yön)"),
        "L_f62": (1, "fib", "Yükselişin %61.8 geri çekilmesinde limit LONG (aynı yön)"),
        "S_mkt": (-1, "mkt", "Sert yükselişte hemen SHORT"),
        "S_conf": (-1, "conf", "Sert yükselişten sonra kırılım mumu gelince SHORT"),
    },
}
EVENT_NAME = {"crash": "Sert düşüş", "ctpump": "Trend tersi sert yükseliş", "pump": "Sert yükseliş (her trendde)"}
FIB_WAIT = 24   # geri çekilme limit emri 24 saat bekler
FEATS = {"size": "Hareket büyüklüğü %", "ext_atr": "Hareket / ATR", "rvol24": "Son 24s hacim / önceki 7g ort.",
         "taker24": "Son 24s agresif alım oranı", "ret30": "30 günlük getiri %", "btc24": "BTC son 24s %",
         "wick": "Olay mumunun ters fitil oranı", "btc30": "BTC son 30g %", "rank": "Hacim sırası (büyük = küçük coin)", "oi24": "OI değişimi 24s %",
         "fund": "Funding", "tls": "Top trader L/S"}


# ---------------------------------------------------------------- veri
def _months(today):
    start = today - timedelta(days=DAYS + 35)
    m = datetime(start.year, start.month, 1, tzinfo=timezone.utc)
    cur = datetime(today.year, today.month, 1, tzinfo=timezone.utc)
    out = []
    while m < cur:
        out.append(m.strftime("%Y-%m"))
        m = (m + timedelta(days=32)).replace(day=1)
    days, d = [], cur
    while d < today:
        days.append(d)
        d += timedelta(days=1)
    return out, days


def jobs(sym, today, market):
    months, days = _months(today)
    base = FUT if market == "fut" else SPOT
    out = [("k", f"{base}/monthly/klines/{sym}/1h/{sym}-1h-{ym}.zip", f"{CACHE}/{market}/{sym}/{ym}.zip", False) for ym in months]
    out += [("k", f"{base}/daily/klines/{sym}/1h/{sym}-1h-{d:%Y-%m-%d}.zip", f"{CACHE}/{market}d/{sym}/{d:%Y-%m-%d}.zip",
             (today - d).days <= 3) for d in days]
    if market == "fut":
        out += [("f", f"{FUT}/monthly/fundingRate/{sym}/{sym}-fundingRate-{ym}.zip", f"{research.CACHE}/f/{sym}/{ym}.zip", False)
                for ym in months]
        d = today - timedelta(days=MET_DAYS)
        while d < today:
            out.append(("m", f"{FUT}/daily/metrics/{sym}/{sym}-metrics-{d:%Y-%m-%d}.zip", f"{research.CACHE}/m/{sym}/{d:%Y-%m-%d}.zip",
                        (today - d).days <= 3))
            d += timedelta(days=1)
    return out


def _download(J):
    with ThreadPoolExecutor(32) as ex:
        paths = list(ex.map(lambda j: research.fetch(j[2], j[3], j[4]), J))
    per = {}
    for j, p in zip(J, paths):
        per.setdefault(j[0], []).append((j[1], p))
    return per


def tier_of(rank):
    return "büyük" if rank <= 50 else ("orta" if rank <= 150 else "küçük")


def load_all(today):
    rows = binance.top_usdt(N_COINS)
    syms = [x["symbol"] for x in rows]
    rank = {s: i + 1 for i, s in enumerate(syms)}
    if "BTCUSDT" not in syms:
        syms.insert(0, "BTCUSDT")
        rank["BTCUSDT"] = 1
    per = _download([(s, *j) for s in syms for j in jobs(s, today, "fut")])
    data, spot_need = {}, []
    for s in syms:
        r = research.load_coin(s, per.get(s, []))
        if r is None or len(r[0]) < 800:
            spot_need.append(s)
            continue
        k, met, fund = r
        data[s] = (research.with_extras(k, "1h", met, fund), "fut")
    if spot_need:
        per = _download([(s, *j) for s in spot_need for j in jobs(s, today, "spot")])
        for s in spot_need:
            r = research.load_coin(s, per.get(s, []))
            if r is not None and len(r[0]) >= 800:
                data[s] = (r[0], "spot")
    vol = {s: float(k[0]["qv"].tail(24 * 90).sum()) for s, k in data.items()}     # katman: son 90 günün hacmi (anlık patlamadan etkilenmez)
    rank = {s: i + 1 for i, s in enumerate(sorted(vol, key=vol.get, reverse=True))}
    print(f"{len(syms)} coin istendi, {len(data)} yüklendi ({sum(1 for v in data.values() if v[1] == 'spot')} yalnız spot)")
    return data, rank


# ---------------------------------------------------------------- göstergeler
def ema(x, n):
    return pd.Series(x).ewm(span=n, adjust=False).mean().values


def atr(h, l, c, n=14):
    pc = np.r_[c[0], c[:-1]]
    tr = np.maximum(h - l, np.maximum(np.abs(h - pc), np.abs(l - pc)))
    return pd.Series(tr).ewm(alpha=1 / n, adjust=False).mean().values


def roll_max(x, n):
    return pd.Series(x).rolling(n, min_periods=1).max().values


def roll_min(x, n):
    return pd.Series(x).rolling(n, min_periods=1).min().values


def btc_ret24(k):
    c = k["c"].values.astype(float)
    t = k["t"].values
    m = dict(zip(t, np.r_[np.full(24, np.nan), (c[24:] / c[:-24] - 1) * 100]))
    m.update({("30", x): v for x, v in zip(t, np.r_[np.full(720, np.nan), (c[720:] / c[:-720] - 1) * 100])})
    return m


# ---------------------------------------------------------------- işlem simülasyonu
def sim(o, h, l, c, i, d, entry, stop, mode, cost, fund=0.0, hold=HOLD, wait=WAIT):
    """i: olay mumu. d: +1 long / -1 short. mode mkt|lim (conf çağıran tarafta mkt'ye çevrilir).
    Döner: dict(R, risk, mae, bars, filled). Aynı mumda stop ve hedef → önce stop (temkinli)."""
    n = len(c)
    if mode in ("lim", "fib"):
        if mode == "fib":
            wait = FIB_WAIT
        j0 = None
        for j in range(i + 1, min(n, i + 1 + wait)):
            if (d == 1 and l[j] <= entry) or (d == -1 and h[j] >= entry):
                j0 = j
                if (d == 1 and o[j] < entry) or (d == -1 and o[j] > entry):
                    entry = o[j]           # boşlukla açıldıysa açılıştan dolar
                break
        if j0 is None:
            return {"filled": False}
        start, first_bar_fill = j0, True
    else:
        start, first_bar_fill = i + 1, False
    risk = abs(entry - stop)
    if risk <= 0 or (d == 1 and stop >= entry) or (d == -1 and stop <= entry):
        return {"filled": False}
    rf = risk / entry
    t1, t2 = entry + d * 1.5 * risk, entry + d * 3 * risk
    st, R, left, mae, tp1 = stop, 0.0, 1.0, 0.0, False
    end = min(n - 1, start + hold)
    k = start
    while k <= end:
        adv = l[k] if d == 1 else h[k]
        fav = h[k] if d == 1 else l[k]
        mae = max(mae, d * (entry - adv) / entry)
        if (d == 1 and adv <= st) or (d == -1 and adv >= st):
            gap = (d == 1 and o[k] < st) or (d == -1 and o[k] > st)
            px = o[k] if gap and not (first_bar_fill and k == start) else st
            R += left * d * (px - entry) / risk
            left = 0
            break
        if not tp1 and ((d == 1 and fav >= t1) or (d == -1 and fav <= t1)):
            R += 0.5 * 1.5
            left, tp1, st = 0.5, True, entry
        if tp1 and ((d == 1 and fav >= t2) or (d == -1 and fav <= t2)):
            R += left * 3
            left = 0
            break
        k += 1
    if left > 0:
        k = end
        R += left * d * (c[end] - entry) / risk
    bars = k - start + 1
    R -= cost / rf
    R -= d * fund * (bars / 8) / rf
    return {"filled": True, "R": float(R), "risk": float(rf), "mae": float(mae), "bars": int(bars), "start": int(start)}


def confirm(o, h, l, c, i, d, ref):
    """12 saat içinde dönüş mumu: long → önceki mumun tepesi üstünde ve olay kapanışının üstünde kapanış."""
    for j in range(i + 1, min(len(c) - 1, i + 1 + WAIT)):
        if d == 1 and c[j] > h[j - 1] and c[j] > ref:
            return j
        if d == -1 and c[j] < l[j - 1] and c[j] < ref:
            return j
    return None


def plan(ev, name, o, h, l, c, i, a, lo24, hi24):
    """Varyant için (giriş, stop, biçim, giriş mumu) üret."""
    d, mode, _ = VARIANTS[ev][name]
    e = c[i]
    if mode == "fib":
        f = {"38": 0.382, "50": 0.5, "62": 0.618}[name[-2:]]
        mv = hi24 - lo24
        if d == -1:     # düşüşten sonra tepkiye short: seviye dipten f kadar yukarıda, stop f+0.25 üstünde
            lv = lo24 + f * mv
            return (lv, lo24 + (f + 0.25) * mv + 0.3 * a, "fib", i) if lv > e else None
        lv = hi24 - f * mv   # yükselişten sonra geri çekilmeye long
        return (lv, hi24 - (f + 0.25) * mv - 0.3 * a, "fib", i) if lv < e else None
    if ev == "crash":
        if name == "L_mkt":
            return e, min(lo24 - 0.5 * a, e - a), "mkt", i
        if name == "L_lim":
            lv = e - a
            return lv, min(lo24, lv) - a, "lim", i
        if name == "S_mkt":
            return e, max(h[max(0, i - 2):i + 1].max() + 0.5 * a, e + a), "mkt", i
        if name == "S_lim":
            lv = e + 1.5 * a
            return lv, lv + 1.5 * a, "lim", i
    else:
        if name == "S_mkt":
            return e, max(hi24 + 0.5 * a, e + a), "mkt", i
        if name == "S_lim":
            lv = e + a
            return lv, max(hi24, lv) + a, "lim", i
        if name == "L_mkt":
            return e, e - 2 * a, "mkt", i
        if name == "L_lim":
            lv = e - 1.5 * a
            return lv, lv - 1.5 * a, "lim", i
    j = confirm(o, h, l, c, i, d, e)          # onaylı girişler
    if j is None:
        return None
    if d == 1:
        return c[j], min(l[i:j + 1].min(), lo24) - 0.5 * a, "mkt", j
    return c[j], max(h[i:j + 1].max(), hi24) + 0.5 * a, "mkt", j


# ---------------------------------------------------------------- olaylar
def events(sym, k, market, rank, btc=None, label=True):
    o, h, l, c = (k[q].values.astype(float) for q in "ohlc")
    qv = k["qv"].values.astype(float)
    tq = k["tq"].values.astype(float) if "tq" in k else np.full(len(c), np.nan)
    t = k["t"].values
    n = len(c)
    if n < 800:
        return []
    a = atr(h, l, c)
    e200 = ema(c, 200)
    hi24, lo24 = roll_max(h, 24), roll_min(l, 24)
    v24 = pd.Series(qv).rolling(24).sum().values
    v7 = pd.Series(qv).rolling(168).sum().shift(24).values / 7
    tk24 = pd.Series(tq).rolling(24).sum().values / np.maximum(v24, 1e-9)
    oi = k["oi"].values.astype(float) if "oi" in k else np.full(n, np.nan)
    fu = k["funding"].values.astype(float) if "funding" in k else np.full(n, np.nan)
    tls = k["tls"].values.astype(float) if "tls" in k else np.full(n, np.nan)
    tier = tier_of(rank)
    cost = FEE + 2 * SLIP[tier]
    drop = c / hi24 - 1
    pump = c / lo24 - 1
    out = []
    last = {}
    for i in range(744, n):
        evs = [("crash", th) for th in DROPS if drop[i] <= -th and drop[i - 1] > -th]
        up = [th for th in PUMPS if pump[i] >= th and pump[i - 1] < th]
        evs += [("pump", th) for th in up]
        if c[i - 24] < e200[i - 24] and c[i - 24] / c[i - 744] - 1 < -0.10:
            evs += [("ctpump", th) for th in up]
        for ev, th in evs:
            size = -drop[i] if ev == "crash" else pump[i]
            
            if i - last.get((ev, th), -10 ** 9) < COOL:
                continue
            last[(ev, th)] = i
            wick = ((min(o[i], c[i]) - l[i]) if ev == "crash" else (h[i] - max(o[i], c[i]))) / (h[i] - l[i] + 1e-12)
            f = {"sym": sym, "t": int(t[i]), "ev": ev, "th": th, "tier": tier, "market": market, "rank": rank, "price": float(c[i]),
                 "size": float(size * 100), "ext_atr": float(size * c[i] / max(a[i], 1e-12)),
                 "rvol24": float(v24[i] / max(v7[i], 1e-9)) if v7[i] == v7[i] else np.nan, "taker24": float(tk24[i]),
                 "ret30": float((c[i] / c[i - 720] - 1) * 100), "wick": float(wick),
                 "btc24": float(btc.get(t[i], np.nan)) if btc else np.nan,
                 "btc30": float(btc.get(("30", t[i]), np.nan)) if btc else np.nan,
                 "oi24": float((oi[i] / oi[i - 24] - 1) * 100) if oi[i] == oi[i] and oi[i - 24] == oi[i - 24] and oi[i - 24] > 0 else np.nan,
                 "fund": float(fu[i]) if fu[i] == fu[i] else np.nan, "tls": float(tls[i]) if tls[i] == tls[i] else np.nan,
                 "atr": float(a[i]), "lo24": float(lo24[i]), "hi24": float(hi24[i])}
            if label:
                fr = f["fund"] if f["fund"] == f["fund"] else 0.0
                for name, (d, _, _) in VARIANTS[ev].items():
                    if d == -1 and market != "fut":
                        continue                         # yalnız spot coinde short açılamaz
                    p = plan(ev, name, o, h, l, c, i, a[i], lo24[i], hi24[i])
                    if p is None:
                        f[name] = None
                        continue
                    en, sp, mode, j = p
                    r = sim(o, h, l, c, j, d, en, sp, mode, cost, fr)
                    f[name] = r if r.get("filled") else None
            out.append(f)
    return out


# ---------------------------------------------------------------- istatistik
def stats(trades):
    R = np.array([x["R"] for x in trades], float)
    if not len(R):
        return {"n": 0}
    g, ls = R[R > 0].sum(), -R[R < 0].sum()
    res = {"n": int(len(R)), "win": round(float((R > 0).mean() * 100), 1), "avg_R": round(float(R.mean()), 3),
           "pf": round(float(g / ls), 2) if ls > 0 else None, "risk": round(float(np.mean([x["risk"] for x in trades]) * 100), 1)}
    for lev in LEVS:
        liq = 1 / lev - 0.005
        ret = np.array([-1.0 if x["mae"] >= liq else lev * x["R"] * x["risk"] for x in trades])
        res[f"x{lev}"] = {"avg": round(float(ret.mean() * 100), 1), "liq": int(sum(x["mae"] >= liq for x in trades))}
    return res


REGIMES = {"tümü": None, "BTC düşüşte": lambda D: D["btc30"] < 0, "BTC yükselişte": lambda D: D["btc30"] >= 0}


def collect(E, ev, name, lo, mask=None, regime="tümü"):
    D = E[(E["ev"] == ev) & (E["th"] == lo)]
    if REGIMES.get(regime) is not None and "btc30" in D:
        D = D[REGIMES[regime](D)]
    if mask is not None:
        D = D[mask(D)]
    if name not in D:
        return []
    return [x for x in D[name].values if isinstance(x, dict)]


def grid(E, split):
    tr, te = E[E["t"] < split], E[E["t"] >= split]
    res = []
    for ev, V in VARIANTS.items():
        ths = DROPS if ev == "crash" else PUMPS
        nev = {}
        for name, (d, mode, desc) in V.items():
            for th in ths:
                for tiers in (None, ("küçük",), ("orta", "küçük"), ("büyük",)):
                    mk = (lambda D, tiers=tiers: D["tier"].isin(tiers)) if tiers else None
                    for rg in REGIMES:
                        ta, tb = collect(tr, ev, name, th, mk, rg), collect(te, ev, name, th, mk, rg)
                        a, b = stats(ta), stats(tb)
                        key = (th, tiers, rg)
                        if key not in nev:
                            D = E[(E["ev"] == ev) & (E["th"] == th)]
                            if mk is not None:
                                D = D[mk(D)]
                            if REGIMES[rg] is not None:
                                D = D[REGIMES[rg](D)]
                            nev[key] = max(len(D), 1)
                        res.append({"fill": round(100 * (len(ta) + len(tb)) / nev[key], 1), "ev": ev, "name": name, "desc": desc, "th": th, "tiers": list(tiers) if tiers else ["tümü"],
                                    "regime": rg, "train": a, "test": b})
    return res


def adopt(row):
    a, b = row["train"], row["test"]
    return bool(b.get("n", 0) >= 40 and (b.get("avg_R") or -9) > 0 and (b.get("pf") or 0) > 1.05 and (a.get("avg_R") or -9) > 0)


def choose(G, ev):
    """Eğitimde en iyi (n≥40) — test sonucuna bakılmadan seçilir."""
    cand = [g for g in G if g["ev"] == ev and g["train"].get("n", 0) >= 100]   # küçük alt kümeler şansla öne çıkmasın
    cand.sort(key=lambda g: g["train"]["avg_R"], reverse=True)
    return cand[0] if cand else None


def compare(E, split, ev, name, th, regime="tümü"):
    """Seçilen varyantta kazanan vs kaybeden işlemlerin özellik farkı (Cohen d, eğitim ve test ayrı)."""
    D = E[(E["ev"] == ev) & (E["th"] == th)].copy()
    if REGIMES.get(regime) is not None:
        D = D[REGIMES[regime](D)]
    D = D[D[name].apply(lambda x: isinstance(x, dict))]
    if len(D) < 30:
        return []
    D["win"] = D[name].apply(lambda x: x["R"] > 0)
    out = []
    for f, nm in FEATS.items():
        row = {"f": f, "name": nm}
        ok = True
        for part, P in (("train", D[D["t"] < split]), ("test", D[D["t"] >= split])):
            w, ls = P.loc[P["win"], f].dropna(), P.loc[~P["win"], f].dropna()
            if len(w) < 8 or len(ls) < 8:
                ok = False
                break
            sd = np.sqrt((w.var() + ls.var()) / 2) or 1e-9
            row[part] = {"win": round(float(w.median()), 4), "loss": round(float(ls.median()), 4), "d": round(float((w.mean() - ls.mean()) / sd), 2)}
        if ok:
            row["stable"] = bool(np.sign(row["train"]["d"]) == np.sign(row["test"]["d"]) and min(abs(row["train"]["d"]), abs(row["test"]["d"])) >= 0.2)
            out.append(row)
    out.sort(key=lambda r: -abs(r["train"]["d"]))
    return out


# ---------------------------------------------------------------- canlı tarama + kâğıt ileri test
def live_scan(picks, rank_hist=None):
    rows = binance.top_usdt(N_COINS)
    rank = {x["symbol"]: i + 1 for i, x in enumerate(rows)}
    if rank_hist:
        rank = {s: rank_hist.get(s, r) for s, r in rank.items()}
    try:
        bk = pd.DataFrame(binance.klines("BTCUSDT", "1h", 1000))
        btc30 = float(bk["c"].iloc[-1] / bk["c"].iloc[-721] - 1) * 100
    except Exception:
        btc30 = float("nan")
    reg_now = "BTC düşüşte" if btc30 < 0 else "BTC yükselişte"

    def one(s):
        try:
            return s, pd.DataFrame(binance.klines(s, "1h", 1000))
        except Exception:
            return s, None
    with ThreadPoolExecutor(8) as ex:
        K = dict(ex.map(one, list(rank)))
    now = time.time() * 1000
    found = []
    for s, k in K.items():
        if k is None or len(k) < 800:
            continue
        k = k.iloc[:-1].reset_index(drop=True)                # yalnız kapanmış mumlar
        for e in events(s, k, "fut", rank[s], label=False):
            if now - e["t"] > 26 * 3600_000:
                continue
            p = picks.get(e["ev"])
            e["hours_ago"] = int((now - e["t"]) / 3600_000)
            e["pick"] = None
            if p and e["th"] == p["th"] and ("tümü" in p["tiers"] or e["tier"] in p["tiers"]) and p["regime"] in ("tümü", reg_now):
                d, mode, desc = VARIANTS[e["ev"]][p["name"]]
                e["pick"] = {"name": p["name"], "desc": desc, "dir": "LONG" if d == 1 else "SHORT"}
            found.append({q: (None if isinstance(v, float) and v != v else v) for q, v in e.items()})
    best = {}
    for x in found:                                            # coin+olay başına tek satır: önce kâğıt seçimi, sonra en büyük eşik
        key = (x["sym"], x["ev"])
        cur = best.get(key)
        if cur is None or (bool(x["pick"]), x["th"]) > (bool(cur["pick"]), cur["th"]):
            best[key] = x
    found = sorted(best.values(), key=lambda x: -x["size"])
    return found, {"btc30": round(btc30, 1), "regime": reg_now}


def ledger_update(scan, picks):
    """Seçilen varyantla kâğıt işlem: olay kaydedilir, 72+12 saat sonra gerçek mumlarla sonuçlandırılır."""
    path = os.path.join(ROOT, "state", "extreme_ledger.json")
    L = json.load(open(path)) if os.path.exists(path) else []
    have = {(x["sym"], x["t"], x["ev"]) for x in L}
    for x in scan:
        if x.get("pick") and (x["sym"], x["t"], x["ev"]) not in have:
            L.append({k: x[k] for k in ("sym", "t", "ev", "tier", "size", "price", "atr", "lo24", "hi24", "fund")} | {"name": x["pick"]["name"], "done": False})
    now = time.time() * 1000
    for x in L:
        if x["done"] or now - x["t"] < (HOLD + WAIT + 2) * 3600_000:
            continue
        try:
            k = pd.DataFrame(binance.klines(x["sym"], "1h", 1000))
        except Exception:
            continue
        k = k[k["t"] >= x["t"]].reset_index(drop=True)
        if len(k) < 3:
            continue
        o, h, l, c = (k[q].values.astype(float) for q in "ohlc")
        c[0] = x["price"]
        d = VARIANTS[x["ev"]][x["name"]][0]
        p = plan(x["ev"], x["name"], o, h, l, c, 0, x["atr"], x["lo24"], x["hi24"])
        r = None if p is None else sim(o, h, l, c, p[3], d, p[0], p[1], p[2], FEE + 2 * SLIP[x["tier"]], x.get("fund") or 0.0)
        x["result"] = r if r and r.get("filled") else None
        x["done"] = True
    json.dump(L[-3000:], open(path, "w"), ensure_ascii=False, default=float)
    out = {"open": sum(1 for x in L if not x["done"])}
    for ev in VARIANTS:
        out[ev] = stats([x["result"] for x in L if x["done"] and x["ev"] == ev and x.get("result")])
    return out


# ---------------------------------------------------------------- rapor
def fmt_st(s):
    if not s.get("n"):
        return "işlem yok"
    return (f"{s['n']} işlem, %{s['win']} kazanç, ort {s['avg_R']}R, PF {s['pf']}, ort stop %{s['risk']} · "
            f"marjin/işlem 3x %{s['x3']['avg']} ({s['x3']['liq']} tasfiye), 5x %{s['x5']['avg']} ({s['x5']['liq']}), 10x %{s['x10']['avg']} ({s['x10']['liq']})")


def to_md(r):
    d = datetime.fromtimestamp(r["time"] / 1000, timezone.utc) + timedelta(hours=3)
    L = [f"# Uç hareketler: sert düşenler ve trend tersi yükselenler — {d:%d.%m.%Y %H:%M}", "",
         f"{r['coins']} coin (ilk {N_COINS} hacim; büyük 1-50, orta 51-150, küçük 151+), son {DAYS} gün, 1s mum. "
         f"Olaylar: {r['n_events']['crash']} sert düşüş, {r['n_events']['ctpump']} trend tersi pompa, {r['n_events'].get('pump', 0)} sert yükseliş (tümü). "
         "Eğitim ilk %70, TEST son %30 (model görmeden).", ""]
    for ev in VARIANTS:
        L += [f"## {EVENT_NAME[ev]} — varyantlar (tüm coinler, en düşük eşik)", "", "| Varyant | Eğitim | TEST |", "|---|---|---|"]
        for g in r["grid"]:
            if g["ev"] == ev and g["th"] == (DROPS if ev == "crash" else PUMPS)[0] and g["tiers"] == ["tümü"] and g["regime"] == "tümü":
                L.append(f"| {g['desc']} (dolma %{g.get('fill')}) | {fmt_st(g['train'])} | {fmt_st(g['test'])} |")
        L += ["", f"### {EVENT_NAME[ev]} — coin büyüklüğüne göre (TEST, en düşük eşik)", "", "| Varyant | büyük | orta+küçük | küçük |", "|---|---|---|---|"]
        for name in VARIANTS[ev]:
            cells = []
            for tiers in (["büyük"], ["orta", "küçük"], ["küçük"]):
                g = next((g for g in r["grid"] if g["ev"] == ev and g["name"] == name and g["th"] == (DROPS if ev == "crash" else PUMPS)[0] and g["tiers"] == tiers and g["regime"] == "tümü"), None)
                s = g["test"] if g else {}
                cells.append(f"{s['n']} işl, ort {s['avg_R']}R, PF {s['pf']}" if s.get("n") else "-")
            L.append(f"| {VARIANTS[ev][name][2]} | " + " | ".join(cells) + " |")
        sh = lambda s: f"{s['n']} işl, ort {s['avg_R']}R, PF {s['pf']}" if s.get("n") else "-"
        L += ["", f"### {EVENT_NAME[ev]} — piyasa rejimine göre (BTC 30 günlük yönü, tüm coinler, en düşük eşik)", "",
              "| Varyant | BTC düşüşte: eğitim | BTC düşüşte: TEST | BTC yükselişte: eğitim | BTC yükselişte: TEST |", "|---|---|---|---|---|"]
        for name in VARIANTS[ev]:
            cells = []
            for rg in ("BTC düşüşte", "BTC yükselişte"):
                g = next((g for g in r["grid"] if g["ev"] == ev and g["name"] == name and g["th"] == (DROPS if ev == "crash" else PUMPS)[0] and g["tiers"] == ["tümü"] and g["regime"] == rg), None)
                cells += [sh(g["train"]) if g else "-", sh(g["test"]) if g else "-"]
            L.append(f"| {VARIANTS[ev][name][2]} | " + " | ".join(cells) + " |")
        p = r["picks"].get(ev)
        if p:
            st = "✅ DOĞRULANDI" if p["adopted"] else "❌ testte tutmadı → yalnız kâğıt ileri test"
            L += ["", f"**Eğitimde seçilen:** {p['desc']}, hareket ≥ %{int(p['th']*100)}, coinler: {', '.join(p['tiers'])}, piyasa: {p['regime']} → {st}",
                  f"- Eğitim: {fmt_st(p['train'])}", f"- TEST: {fmt_st(p['test'])}"]
            cmp_ = r["compare"].get(ev) or []
            if cmp_:
                L += ["", "Bu varyantta kazanan vs kaybeden işlemler (medyan; d = etki büyüklüğü, ✓ iki dönemde de aynı yönde ≥0.2):", "",
                      "| Özellik | Kazanan | Kaybeden | d eğitim / test | |", "|---|---|---|---|---|"]
                for c in cmp_[:8]:
                    L.append(f"| {c['name']} | {c['test']['win']} | {c['test']['loss']} | {c['train']['d']} / {c['test']['d']} | {'✓' if c['stable'] else ''} |")
        L.append("")
    good = [g for g in r["grid"] if g["adopt"]]
    for ev in VARIANTS:                                     # aynı yönlü geri çekilme özeti
        rows = [g for g in r["grid"] if g["ev"] == ev and g["tiers"] == ["tümü"] and VARIANTS[ev][g["name"]][1] == "fib"]
        if rows:
            L += [f"### Aynı yönlü geri çekilme girişi — {EVENT_NAME[ev]} (tüm coinler)", "",
                  "| Seviye | Hareket ≥ | Piyasa | dolma % | Eğitim | TEST |", "|---|---|---|---|---|---|"]
            for g in rows:
                if g["regime"] != "tümü" and g["th"] != (DROPS if ev == "crash" else PUMPS)[1]:
                    continue
                sh = lambda s: f"{s['n']} işl, %{s['win']}, ort {s['avg_R']}R, PF {s['pf']}" if s.get("n") else "-"
                L.append(f"| %{g['name'][-2:].replace('38','38.2').replace('62','61.8')} | %{int(g['th']*100)} | {g['regime']} | {g['fill']} | {sh(g['train'])} | {sh(g['test'])} |")
            L.append("")
    L += ["## Testi geçen tüm kombinasyonlar (bilgi amaçlı — eğitimde seçilmedikçe benimsenmez)", ""]
    good.sort(key=lambda g: -(g["test"].get("avg_R") or 0) * min(g["test"]["n"], 200))
    L += [f"- {EVENT_NAME[g['ev']]} · {g['desc']} · ≥%{int(g['th']*100)} · {', '.join(g['tiers'])} · {g['regime']} · eğitim ort {g['train']['avg_R']}R (n {g['train']['n']}) · TEST {fmt_st(g['test'])}" for g in good[:15]] or ["- Yok."]
    rn = r.get("regime_now") or {}
    L += ["", f"## Şu an (son 26 saat) — piyasa: {rn.get('regime', '?')} (BTC 30g %{rn.get('btc30', '?')})", ""]
    for x in r["scan"][:20]:
        pk = f" → kâğıt: {x['pick']['dir']} ({x['pick']['desc']})" if x.get("pick") else ""
        L.append(f"- {x['sym'].replace('USDT','')} [{x['tier']}] {EVENT_NAME[x['ev']]} %{x['size']:.1f}, {x['hours_ago']} saat önce, RVOL {x['rvol24'] if x['rvol24'] is None else round(x['rvol24'],2)}{pk}")
    if not r["scan"]:
        L.append("- Uç hareket yok.")
    g = r.get("ledger")
    if g:
        L += ["", f"## Kâğıt ileri test (açık: {g['open']})", ""] + [f"- {EVENT_NAME[ev]}: {fmt_st(g[ev])}" for ev in VARIANTS]
    L += ["", "_Simülasyondur, yatırım tavsiyesi değildir. Küçük coinlerde kayma ve likidite riski yüksektir._"]
    return "\n".join(L)


# ---------------------------------------------------------------- ana
def analyze(data, rank, btc=None):
    rows = []
    for s, (k, market) in data.items():
        rows += events(s, k, market, rank.get(s, 999), btc)
    E = pd.DataFrame(rows)
    split = float(np.quantile(E["t"], 0.7))
    G = grid(E, split)
    for g in G:
        g["adopt"] = adopt(g)
    picks, cmps = {}, {}
    for ev in VARIANTS:
        p = choose(G, ev)
        if p:
            picks[ev] = {**p, "adopted": adopt(p)}
            cmps[ev] = compare(E, split, ev, p["name"], p["th"], p["regime"])
    return E, split, G, picks, cmps


def main():
    t0 = time.time()
    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    data, rank = load_all(today)
    btc = btc_ret24(data["BTCUSDT"][0]) if "BTCUSDT" in data else None
    E, split, G, picks, cmps = analyze(data, rank, btc)
    E = E[E["t"] >= (today - timedelta(days=DAYS)).timestamp() * 1000]
    print(f"{len(E)} olay ({time.time()-t0:.0f} sn)")
    scan, regime_now = live_scan(picks, rank)
    try:
        ledger = ledger_update(scan, picks)
    except Exception as e:
        print("defter hatası:", e)
        ledger = None
    rep = {"time": int(time.time() * 1000), "coins": len(data), "split": int(split),
           "n_events": {ev: int(((E["ev"] == ev) & (E["th"] == (DROPS if ev == "crash" else PUMPS)[0])).sum()) for ev in VARIANTS}, "grid": G, "picks": picks, "compare": cmps,
           "scan": scan, "regime_now": regime_now, "ledger": ledger, "rank_hist": rank}
    json.dump(rep, open(os.path.join(ROOT, "state", "extreme.json"), "w"), ensure_ascii=False, default=float)
    md = to_md(rep)
    path = f"docs/gunluk/uc-hareket-{(today + timedelta(hours=3)):%Y-%m-%d}.md"
    open(os.path.join(ROOT, path), "w", encoding="utf-8").write(md)
    print(md)
    import notify
    chat = os.environ.get("TELEGRAM_CHAT_ID") or json.load(open(os.path.join(ROOT, "state", "futures.json"))).get("chat_id")
    telegram.send(chat, notify.md_to_tg(md))
    print(f"toplam {time.time()-t0:.0f} sn")


if __name__ == "__main__":
    main()
