"""Araştırma: V5 modelinin geçmiş futures verisinde kaldıraçlı long/short performansı,
gösterge bazında doğruluk analizi ve veriyle ağırlık/eşik optimizasyonu.

Veri: Binance resmi arşivi data.binance.vision (USDⓈ-M futures):
  - 15dk mumlar (30dk/1s/4s bunlardan üretilir)
  - metrics: 5 dakikalık Open Interest, global L/S, top trader L/S
  - fundingRate (aylık dosyalar)
Çıktı: state/research.json, state/research.md, state/model.json (+ Telegram özeti)

Yöntem:
  * Zaman bazlı ayrım: ilk %70 eğitim, son %30 TEST. Ağırlıklar yalnızca eğitimde öğrenilir,
    karar testte (modelin hiç görmediği dönem) verilir. Yeni model testte eskisini geçerse benimsenir.
  * Bileşen analizi: Bilgi katsayısı (IC = bileşen puanı ile sonraki getirinin Spearman korelasyonu),
    isabet oranı, işlemlerde "gösterge aynı yöndeyken" ve "ters yöndeyken" kazanma oranı.
"""
from __future__ import annotations

import io
import json
import os
import sys
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone

import numpy as np
import pandas as pd
import requests

sys.path.insert(0, os.path.dirname(__file__))
import binance  # noqa: E402
import sim  # noqa: E402
import telegram  # noqa: E402
import v5  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, "data", "cache")
STATE = os.path.join(ROOT, "state")
BASE = "https://data.binance.vision/data/futures/um"

N_COINS = int(os.environ.get("RES_COINS", 40))
EVAL_DAYS = int(os.environ.get("RES_DAYS", 90))
WARM_DAYS = 45                       # 4s EMA200 için ısınma
TFS = ["15m", "30m", "1h", "4h"]
LEVS = [5, 10]
HORIZON = {"15m": 16, "30m": 12, "1h": 12, "4h": 6}   # gösterge analizi için ileri getiri ufku (mum)
MAX_HOLD = {"15m": 96, "30m": 96, "1h": 72, "4h": 42}
COMPS = ["trend", "momentum", "oi", "volume", "deriv", "smc", "vwap"]
FEATS = {"f_ema_order": "EMA dizilimi", "f_htf": "Üst periyot trendi", "f_ema200": "Fiyat>EMA200", "f_rsi": "RSI",
         "f_macd": "MACD yönü", "f_z": "Z-Score", "f_squeeze": "Bollinger sıkışma", "f_oi_chg": "OI değişimi",
         "f_regime": "OI rejimi", "f_rvol": "RVOL", "f_taker": "Taker alım", "f_obv": "OBV yönü",
         "f_funding": "Funding", "f_gls": "Global L/S", "f_tls": "Top trader L/S", "f_sweep": "Likidite avı",
         "f_fvg": "FVG", "f_vwap": "VWAP üstü/altı"}
_s = requests.Session()


# ---------------------------------------------------------------- indirme
def fetch(url, path, recent):
    if os.path.exists(path):
        return path if os.path.getsize(path) > 0 else None
    for i in range(3):
        try:
            r = _s.get(url, timeout=30)
            if r.status_code == 200:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "wb") as f:
                    f.write(r.content)
                return path
            if r.status_code == 404:
                if not recent:  # eski dosya yoksa bir daha deneme
                    os.makedirs(os.path.dirname(path), exist_ok=True)
                    open(path, "wb").close()
                return None
        except requests.RequestException:
            time.sleep(1 + i)
    return None


def read_zip_csv(path, names):
    with zipfile.ZipFile(path) as z:
        raw = z.read(z.namelist()[0]).decode()
    first = raw.split("\n", 1)[0]
    has_header = not first.split(",")[0].strip().lstrip("-").isdigit()
    return pd.read_csv(io.StringIO(raw), header=0 if has_header else None, names=None if has_header else names)


KCOLS = ["open_time", "open", "high", "low", "close", "volume", "close_time", "quote_volume", "count",
         "taker_buy_volume", "taker_buy_quote_volume", "ignore"]


def jobs_for(sym, today):
    start = today - timedelta(days=EVAL_DAYS + WARM_DAYS)
    out = []
    m = datetime(start.year, start.month, 1, tzinfo=timezone.utc)
    cur_month = datetime(today.year, today.month, 1, tzinfo=timezone.utc)
    while m < cur_month:
        ym = m.strftime("%Y-%m")
        out.append(("k", f"{BASE}/monthly/klines/{sym}/15m/{sym}-15m-{ym}.zip", f"{CACHE}/k/{sym}/{ym}.zip", False))
        out.append(("f", f"{BASE}/monthly/fundingRate/{sym}/{sym}-fundingRate-{ym}.zip", f"{CACHE}/f/{sym}/{ym}.zip", False))
        m = (m + timedelta(days=32)).replace(day=1)
    d = cur_month
    while d < today:
        ds = d.strftime("%Y-%m-%d")
        out.append(("k", f"{BASE}/daily/klines/{sym}/15m/{sym}-15m-{ds}.zip", f"{CACHE}/kd/{sym}/{ds}.zip", (today - d).days <= 3))
        d += timedelta(days=1)
    d = today - timedelta(days=EVAL_DAYS)
    while d < today:
        ds = d.strftime("%Y-%m-%d")
        out.append(("m", f"{BASE}/daily/metrics/{sym}/{sym}-metrics-{ds}.zip", f"{CACHE}/m/{sym}/{ds}.zip", (today - d).days <= 3))
        d += timedelta(days=1)
    return out


def load_coin(sym, files):
    ks, ms, fs = [], [], []
    for kind, path in files:
        if not path:
            continue
        try:
            if kind == "k":
                ks.append(read_zip_csv(path, KCOLS))
            elif kind == "m":
                ms.append(read_zip_csv(path, None))
            else:
                fs.append(read_zip_csv(path, None))
        except Exception as e:
            print("okuma hatası", path, e)
    if not ks:
        return None
    k = pd.concat(ks)
    k = k.rename(columns={"open_time": "t", "open": "o", "high": "h", "low": "l", "close": "c", "volume": "v",
                          "quote_volume": "qv", "taker_buy_quote_volume": "tq"})
    k = k[["t", "o", "h", "l", "c", "v", "qv", "tq"]].apply(pd.to_numeric, errors="coerce").dropna()
    k["t"] = k["t"].astype(np.int64)
    k.loc[k["t"] > 1e14, "t"] //= 1000  # mikro saniye formatı
    k = k.drop_duplicates("t").sort_values("t").reset_index(drop=True)
    met = None
    if ms:
        met = pd.concat(ms)
        met["ts"] = pd.to_datetime(met["create_time"], utc=True).astype("int64") // 10 ** 6
        met = met.rename(columns={"sum_open_interest_value": "oi", "count_long_short_ratio": "gls",
                                  "sum_toptrader_long_short_ratio": "tls"})[["ts", "oi", "gls", "tls"]]
        met = met.apply(pd.to_numeric, errors="coerce").dropna(subset=["ts"]).sort_values("ts").drop_duplicates("ts")
    fund = None
    if fs:
        fund = pd.concat(fs)
        tcol = "calc_time" if "calc_time" in fund else fund.columns[0]
        rcol = "last_funding_rate" if "last_funding_rate" in fund else fund.columns[-1]
        fund = pd.DataFrame({"ts": pd.to_numeric(fund[tcol], errors="coerce"), "funding": pd.to_numeric(fund[rcol], errors="coerce")}).dropna()
        fund["ts"] = fund["ts"].astype(np.int64)
        fund = fund.sort_values("ts").drop_duplicates("ts")
    return k, met, fund


def with_extras(df, tf, met, fund):
    tf_ms = v5.TF_MS[tf]
    end = pd.DataFrame({"te": df["t"] + tf_ms})
    if met is not None and len(met):
        m = pd.merge_asof(end, met.rename(columns={"ts": "te"}), on="te", direction="backward", tolerance=30 * 60_000)
        for col in ("oi", "gls", "tls"):
            df[col] = m[col].values
    if fund is not None and len(fund):
        f = pd.merge_asof(end, fund.rename(columns={"ts": "te"}), on="te", direction="backward", tolerance=9 * 3600_000)
        df["funding"] = f["funding"].values
    return df


def tf_frame(k15, tf):
    if tf == "15m":
        return k15.copy()
    mult = v5.TF_MS[tf] // v5.TF_MS["15m"]
    r = v5.resample(k15, v5.TF_MS[tf])
    return r[r["n"] == mult].drop(columns="n").reset_index(drop=True)


# ---------------------------------------------------------------- skor (işaretli ağırlıklarla)
def score_with(R, w):
    keys = [k for k in COMPS if w.get(k, 0)]
    comp = R[keys].astype(float).values
    ww = np.array([w[k] for k in keys], float)
    mask = ~np.isnan(comp)
    num = np.nansum(comp * ww, axis=1)
    den = (mask * np.abs(ww)).sum(axis=1)
    s = 50 + 50 * num / np.where(den == 0, np.nan, den)
    s[R["score"].isna().values] = np.nan
    return s


def directions(score, lt, st):
    s = np.nan_to_num(score, nan=50)
    return np.where(s >= lt, 1, np.where(s <= st, -1, 0))


def run_trades(coins, tf, w, lt, st, lev, part, split_t):
    out = []
    for sym, (df, R, fm) in coins.items():
        sc = score_with(R, w)
        dr = directions(sc, lt, st)
        tt = df["t"].values
        if part == "train":
            dr = np.where(tt < split_t, dr, 0)
        elif part == "test":
            dr = np.where(tt >= split_t, dr, 0)
        snap = {k: R[k].values for k in COMPS}
        snap["score"] = sc
        tr = sim.simulate(tt, df["h"].values, df["l"].values, df["c"].values, R["atr"].values, dr, lev, v5.TF_MS[tf],
                          fmark=fm, max_hold=MAX_HOLD[tf], start=0, snap=snap)
        for x in tr:
            x["sym"] = sym
        out += tr
    return out


LIVE_W = {"trend": 20, "momentum": 18, "volume": 10, "smc": 10, "vwap": 5}  # canlıda da hesaplanabilen bileşenler
EXITS = [(1.5, 1.5, 3.0), (1.0, 1.5, 2.5), (2.0, 1.0, 2.0)]


def strategy_grid():
    g = []
    for sl, t1, t2 in EXITS:
        ex = {"sl": sl, "tp1": t1, "tp2": t2, "max_new": 3}
        for lt in (58, 66, 74):
            for me in (None, 1.0, 2.0):
                for h in (None, "with"):
                    g.append({"type": "trend", "lt": lt, "st": 100 - lt, "max_ext": me, "htf": h, **ex})
        for z in (2.0, 2.5, 3.0):
            for hi, lo in ((70, 30), (75, 25)):
                for sw in (False, True):
                    g.append({"type": "meanrev", "z": z, "rsi_hi": hi, "rsi_lo": lo, "need_sweep": sw, "htf": None, **ex})
        for h in (None, "with", "against"):
            g.append({"type": "sweep", "htf": h, **ex})
    # Geri çekilmede limit giriş: tepeden alma, yapısal stop, R katı hedefler
    for lt in (58, 66):
        for mp in (0.5, 0.7):
            for entry in ({"entry": "fib", "fib": 0.382}, {"entry": "fib", "fib": 0.5}, {"entry": "atr", "k": 0.5}, {"entry": "atr", "k": 1.0}):
                for tp1, tp2 in ((1.0, 2.0), (1.5, 3.0)):
                    for h in (None, "with"):
                        g.append({"type": "pullback", "lt": lt, "st": 100 - lt, "max_pos": mp, **entry, "expire": 6, "stop_lb": 12,
                                  "buf": 0.3, "max_risk": 3.0, "tp1": tp1, "tp2": tp2, "htf": h, "max_new": 3})
    return g


def run_strategy(coins, tf, strat, lev, part, split_t, scores):
    sig = {}
    rows = []
    for sym, (df, R, fm) in coins.items():
        d, strength = v5.signals(R, scores[sym], strat)
        tt = df["t"].values
        if part == "train":
            d = np.where(tt < split_t, d, 0)
        elif part == "test":
            d = np.where(tt >= split_t, d, 0)
        sig[sym] = d
        nz = np.flatnonzero(d)
        if len(nz):
            rows.append(pd.DataFrame({"t": tt[nz], "sym": sym, "i": nz, "s": strength[nz]}))
    mx = strat.get("max_new", 99)
    if rows and mx < 99:  # aynı mumda en fazla `max_new` yeni işlem (korelasyon/küme riski)
        allr = pd.concat(rows).sort_values(["t", "s"], ascending=[True, False])
        drop = allr[allr.groupby("t").cumcount() >= mx]
        for sym, grp in drop.groupby("sym"):
            sig[sym][grp["i"].values] = 0
    out = []
    for sym, (df, R, fm) in coins.items():
        if strat["type"] == "pullback":
            d = sig[sym]
            e, sl, t1, t2, ok = v5.pullback_levels(R, d, strat)
            idx = np.flatnonzero(ok)
            orders = [(int(i), int(d[i]), float(e[i]), float(sl[i]), float(t1[i]), float(t2[i]), strat.get("expire", 6), None) for i in idx]
            tr = sim.simulate_levels(df["t"].values, df["o"].values.astype(float), df["h"].values.astype(float), df["l"].values.astype(float),
                                     df["c"].values.astype(float), orders, lev, v5.TF_MS[tf], fmark=fm, max_hold=MAX_HOLD[tf])
            for x in tr:
                x["sym"] = sym
            out += tr
            continue
        tr = sim.simulate(df["t"].values, df["h"].values, df["l"].values, df["c"].values, R["atr"].values, sig[sym], lev,
                          v5.TF_MS[tf], fmark=fm, max_hold=MAX_HOLD[tf], sl_m=strat["sl"], tp1_m=strat["tp1"], tp2_m=strat["tp2"])
        for x in tr:
            x["sym"] = sym
        out += tr
    return out


def apply_contest(m, c, base_live):
    """Model kararı: TEST'te doğrulanan strateji benimsenir (demo/gerçek emir de bunu izler).
    Doğrulanan yoksa, eğitimin en iyisi TEST'te mevcut kuraldan iyiyse kâğıt hesaplarda 'ileri test' olarak denenir
    (para/demo emri yok; canlı veriyle ek kanıt toplamak için)."""
    top = c["top"][0] if c["top"] else None
    bl = c["live_baseline_test"]
    if c["adopted"]:
        m.update(strategy=top["strategy"], strategy_name=top["name"], strategy_adopted=True, strategy_mode="doğrulandı", strategy_test=top["test"])
    elif top and top["test"]["5"].get("n", 0) >= 40 and (top["test"]["5"].get("avg_R") or -9) > (bl.get("avg_R") or -9) \
            and (top["test"]["5"].get("pf") or 0) > (bl.get("pf") or 0):
        m.update(strategy=top["strategy"], strategy_name=top["name"], strategy_adopted=False, strategy_mode="ileri test", strategy_test=top["test"])
    else:
        m.update(strategy=base_live, strategy_name=v5.strategy_name(base_live), strategy_adopted=False, strategy_mode="varsayılan", strategy_test={"5": bl})


def spearman(a, b):
    m = np.isfinite(a) & np.isfinite(b)
    if m.sum() < 50:
        return None
    ra = pd.Series(a[m]).rank().values
    rb = pd.Series(b[m]).rank().values
    return float(np.corrcoef(ra, rb)[0, 1])


def comp_analysis(bars, trades):
    """bars: tüm değerlendirme mumları (bileşenler + ileri getiri)."""
    res = {}
    for k in COMPS + list(FEATS):
        if k not in bars or bars[k].notna().sum() < 50:
            continue
        x, y = bars[k].values.astype(float), bars["fwd"].values.astype(float)
        e = {"ic": spearman(x, y)}
        if k in COMPS:
            m = np.isfinite(x) & np.isfinite(y)
            up, dn = m & (x > 0.3), m & (x < -0.3)
            e["hit_up"] = round(float((y[up] > 0).mean() * 100), 1) if up.sum() > 30 else None
            e["hit_dn"] = round(float((y[dn] < 0).mean() * 100), 1) if dn.sum() > 30 else None
            n = up.sum() + dn.sum()
            e["accuracy"] = round(float(((y[up] > 0).sum() + (y[dn] < 0).sum()) / n * 100), 1) if n > 60 else None
            ag = [t for t in trades if t["snap"].get(k) is not None and t["snap"][k] * t["dir"] > 0.2]
            ds = [t for t in trades if t["snap"].get(k) is not None and t["snap"][k] * t["dir"] < -0.2]
            e["trade_agree"] = {"n": len(ag), "win": round(float(np.mean([t["roe"] > 0 for t in ag]) * 100), 1) if len(ag) > 10 else None,
                                "avg_R": round(float(np.mean([t["R"] for t in ag])), 3) if len(ag) > 10 else None}
            e["trade_disagree"] = {"n": len(ds), "win": round(float(np.mean([t["roe"] > 0 for t in ds]) * 100), 1) if len(ds) > 10 else None,
                                   "avg_R": round(float(np.mean([t["R"] for t in ds])), 3) if len(ds) > 10 else None}
        res[k] = e
    return res


def objective(st):
    if st.get("n", 0) < 40:
        return -1e9
    return st["avg_R"] * np.sqrt(st["n"])


# ---------------------------------------------------------------- ana
def main():
    t0 = time.time()
    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    try:
        syms = [x["symbol"] for x in binance.top_usdt(N_COINS + 15)]
    except Exception as e:
        print("coin listesi alınamadı, yedek liste:", e)
        syms = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT", "DOGEUSDT", "ADAUSDT", "AVAXUSDT", "LINKUSDT", "SUIUSDT"]
    jobs = []
    for s in syms:
        jobs += [(s, *j) for j in jobs_for(s, today)]
    print(f"{len(syms)} coin, {len(jobs)} dosya indirilecek/önbellekten okunacak")
    with ThreadPoolExecutor(32) as ex:
        paths = list(ex.map(lambda j: fetch(j[2], j[3], j[4]), jobs))
    per = {}
    for j, p in zip(jobs, paths):
        per.setdefault(j[0], []).append((j[1], p))
    print(f"indirme bitti ({time.time()-t0:.0f} sn)")

    raw = {}
    for s in syms:
        r = load_coin(s, per[s])
        if r is None or r[1] is None or len(r[0]) < 2000:
            continue
        raw[s] = r
        if len(raw) >= N_COINS:
            break
    print(f"verisi tam {len(raw)} coin")
    run(raw, today, t0)


def run(raw, today, t0=None):
    t0 = t0 or time.time()
    eval_start = int((today - timedelta(days=EVAL_DAYS)).timestamp() * 1000)
    split_t = int((today - timedelta(days=EVAL_DAYS * 0.3)).timestamp() * 1000)

    report = {"time": int(time.time() * 1000), "coins": list(raw), "eval_days": EVAL_DAYS,
              "eval_start": eval_start, "split": split_t, "tfs": {}}
    model = {"time": report["time"], "tfs": {}}
    base_w = {k: v5.WEIGHTS[k] for k in COMPS}

    for tf in TFS:
        tt0 = time.time()
        coins, bars = {}, []
        for s, (k15, met, fund) in raw.items():
            df = with_extras(tf_frame(k15, tf), tf, met, fund)
            if len(df) < 300:
                continue
            R = v5.compute(df, tf)
            ev = df["t"].values >= eval_start
            R.loc[~ev, "score"] = np.nan  # değerlendirme dışı: sinyal yok
            fm = sim.funding_marks(df["t"].values, v5.TF_MS[tf], df.get("funding"))
            coins[s] = (df, R, fm)
            b = R.loc[ev, ["t"] + [c for c in COMPS + list(FEATS) if c in R]].copy()
            b["fwd"] = (df["c"].shift(-HORIZON[tf]) / df["c"] - 1).loc[ev].values
            b["sym"] = s
            bars.append(b)
        bars = pd.concat(bars)
        tr_bars, te_bars = bars[bars["t"] < split_t], bars[bars["t"] >= split_t]
        out = {"bars": int(len(bars)), "baseline": {}, "baseline_test": {}}

        # 1) Mevcut model, tüm dönem, 5x ve 10x
        base_tr = {}
        for lev in LEVS:
            trs = run_trades(coins, tf, base_w, 58, 42.99, lev, "all", split_t)
            base_tr[lev] = trs
            out["baseline"][str(lev)] = sim.stats(trs)
            out["baseline_test"][str(lev)] = sim.stats([x for x in trs if x["t"] >= split_t])
        # 2) Gösterge analizi
        tr5 = base_tr[5]
        out["indicators_train"] = comp_analysis(tr_bars, [x for x in tr5 if x["t"] < split_t])
        out["indicators_test"] = comp_analysis(te_bars, [x for x in tr5 if x["t"] >= split_t])
        # 3) Optimizasyon (yalnız eğitim)
        ics = {k: (out["indicators_train"].get(k) or {}).get("ic") for k in COMPS}
        cands = {"mevcut": base_w}
        pos = {k: max(v or 0, 0) for k, v in ics.items()}
        if sum(pos.values()) > 0:
            cands["IC+"] = {k: round(v / sum(pos.values()) * 100, 1) for k, v in pos.items() if v > 0}
        sg = {k: (v or 0) for k, v in ics.items()}
        if sum(abs(x) for x in sg.values()) > 0:
            cands["IC±"] = {k: round(v / sum(abs(x) for x in sg.values()) * 100, 1) for k, v in sg.items() if abs(v) > 0.005}
        best = None
        grid = []
        for name, w in cands.items():
            for lt in (55, 58, 62, 66, 70, 74):
                trs = run_trades(coins, tf, w, lt, 100 - lt, 5, "train", split_t)
                stt = sim.stats(trs)
                grid.append({"w": name, "lt": lt, "n": stt.get("n"), "win": stt.get("win"), "avg_R": stt.get("avg_R"), "obj": round(objective(stt), 3)})
                if best is None or objective(stt) > best[0]:
                    best = (objective(stt), name, w, lt)
        out["grid_train"] = grid
        _, bname, bw, blt = best
        opt_test = {str(lev): sim.stats(run_trades(coins, tf, bw, blt, 100 - blt, lev, "test", split_t)) for lev in LEVS}
        bt, ot = out["baseline_test"]["5"], opt_test["5"]
        adopt = bool(ot.get("n", 0) >= 30 and ot.get("avg_R", -9) > 0 and ot.get("avg_R", -9) > (bt.get("avg_R") or -9))
        out["optimized"] = {"name": bname, "weights": bw, "long_th": blt, "short_th": 100 - blt, "test": opt_test, "adopted": adopt}
        model["tfs"][tf] = {"weights": bw if adopt else base_w, "long_th": blt if adopt else 58, "short_th": (100 - blt) if adopt else 42.99,
                            "learned": adopt, "test_avg_R": ot.get("avg_R"), "test_win": ot.get("win"), "baseline_test_avg_R": bt.get("avg_R")}
        # 4) STRATEJİ YARIŞMASI (yalnız canlıda da hesaplanabilen veriler)
        live_scores = {sym: score_with(R, LIVE_W) for sym, (df, R, fm) in coins.items()}
        res = []
        for stg in strategy_grid():
            stt = sim.stats(run_strategy(coins, tf, stg, 5, "train", split_t, live_scores))
            if stt.get("n", 0) >= 60:
                res.append((stt["avg_R"] * np.sqrt(stt["n"]), stg, stt))
        res.sort(key=lambda x: -x[0])
        top = []
        for obj, stg, stt in res[:5]:
            te = {str(lev): sim.stats(run_strategy(coins, tf, stg, lev, "test", split_t, live_scores)) for lev in LEVS}
            top.append({"strategy": stg, "name": v5.strategy_name(stg), "train": stt, "test": te})
        base_live = {"type": "trend", "lt": 58, "st": 42.99, "max_ext": None, "htf": None, "sl": 1.5, "tp1": 1.5, "tp2": 3.0, "max_new": 3}
        bl_test = sim.stats(run_strategy(coins, tf, base_live, 5, "test", split_t, live_scores))
        win = top[0] if top else None
        ok = bool(win and win["test"]["5"].get("n", 0) >= 40 and (win["test"]["5"].get("avg_R") or -9) > 0
                  and (win["test"]["5"].get("pf") or 0) > 1.05 and (win["test"]["5"].get("avg_R") or -9) > (bl_test.get("avg_R") or -9)
                  and win["train"]["avg_R"] > 0)
        out["contest"] = {"tested": len(res), "top": top, "live_baseline_test": bl_test, "adopted": ok}
        model["tfs"][tf]["live_weights"] = LIVE_W
        apply_contest(model["tfs"][tf], out["contest"], base_live)
        print(f"{tf} yarışma: {len(res)} strateji, kazanan {win['name'] if win else '-'} test {win['test']['5'] if win else '-'} -> {'BENİMSENDİ' if ok else 'reddedildi'}")
        report["tfs"][tf] = out
        print(f"{tf}: {len(bars)} mum, baz test {bt}, yeni {bname}/{blt} test {ot} -> {'BENİMSENDİ' if adopt else 'mevcut kalır'} ({time.time()-tt0:.0f} sn)")

    os.makedirs(STATE, exist_ok=True)
    with open(os.path.join(STATE, "research.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=1, default=float)
    with open(os.path.join(STATE, "model.json"), "w", encoding="utf-8") as f:
        json.dump(model, f, ensure_ascii=False, indent=1)
    md = to_markdown(report)
    with open(os.path.join(STATE, "research.md"), "w", encoding="utf-8") as f:
        f.write(md)
    print(md)
    notify(report)
    print(f"toplam {time.time()-t0:.0f} sn")


# ---------------------------------------------------------------- rapor
def _f(x, s=""):
    return "-" if x is None else f"{x}{s}"


def to_markdown(rep):
    d0 = datetime.fromtimestamp(rep["eval_start"] / 1000, timezone.utc).strftime("%d.%m.%Y")
    ds = datetime.fromtimestamp(rep["split"] / 1000, timezone.utc).strftime("%d.%m.%Y")
    L = [f"# V5 Araştırma Raporu — {datetime.fromtimestamp(rep['time']/1000, timezone.utc).strftime('%d.%m.%Y %H:%M')} UTC", "",
         f"{len(rep['coins'])} coin · değerlendirme {d0}'dan bugüne ({rep['eval_days']} gün) · eğitim/TEST ayrımı {ds}", "",
         "## 1. Mevcut model: kaldıraçlı işlem sonuçları (tüm dönem)", "",
         "| Periyot | Kaldıraç | İşlem | Kazanma | Ort. ROE | PF | Ort. R | Likidasyon | 100$ marjla net | Maks. DD |", "|---|---|---|---|---|---|---|---|---|---|"]
    for tf, o in rep["tfs"].items():
        for lev, s in o["baseline"].items():
            L.append(f"| {tf} | {lev}x | {s.get('n')} | %{_f(s.get('win'))} | %{_f(s.get('avg_roe'))} | {_f(s.get('pf'))} | {_f(s.get('avg_R'))} | {_f(s.get('liq'))} | {_f(s.get('net_100'), '$')} | {_f(s.get('max_dd_100'), '$')} |")
    L += ["", "PF = kâr faktörü (toplam kazanç / toplam kayıp, 1 üstü kârlı). R = risk birimi (stop mesafesi).", ""]
    L += ["## 2. Göstergelerin doğruluğu (TEST dönemi)", ""]
    for tf, o in rep["tfs"].items():
        L += [f"### {tf}", "", "| Bileşen | IC | İsabet | ↑ dediğinde yükseldi | ↓ dediğinde düştü | İşlemde aynı yöndeyken kazanma | Ters yöndeyken kazanma |", "|---|---|---|---|---|---|---|"]
        for k in COMPS:
            e = o["indicators_test"].get(k)
            if not e:
                continue
            L.append(f"| {v5.NAMES[k]} | {_f(round(e['ic'], 3) if e['ic'] is not None else None)} | %{_f(e['accuracy'])} | %{_f(e['hit_up'])} | %{_f(e['hit_dn'])} | %{_f(e['trade_agree']['win'])} ({e['trade_agree']['n']}) | %{_f(e['trade_disagree']['win'])} ({e['trade_disagree']['n']}) |")
        fe = sorted([(FEATS[k], o["indicators_test"][k]["ic"]) for k in FEATS if k in o["indicators_test"] and o["indicators_test"][k]["ic"] is not None], key=lambda x: -abs(x[1]))
        L += ["", "Ham göstergeler (IC, büyükten küçüğe): " + ", ".join(f"{n} {ic:+.3f}" for n, ic in fe[:10]), ""]
    L += ["## 3. Öğrenme: yeni ağırlıklar (eğitimde bulundu, TEST'te sınandı)", "",
          "| Periyot | Yöntem | Eşik | Mevcut model TEST ort. R / kazanma | Yeni model TEST ort. R / kazanma | Karar |", "|---|---|---|---|---|---|"]
    for tf, o in rep["tfs"].items():
        op, bt = o["optimized"], o["baseline_test"]["5"]
        ot = op["test"]["5"]
        L.append(f"| {tf} | {op['name']} | {op['long_th']}/{op['short_th']} | {_f(bt.get('avg_R'))} / %{_f(bt.get('win'))} ({bt.get('n')}) | {_f(ot.get('avg_R'))} / %{_f(ot.get('win'))} ({ot.get('n')}) | {'✅ benimsendi' if op['adopted'] else '❌ mevcut kalır'} |")
    L += ["", "Ağırlıklar:"]
    for tf, o in rep["tfs"].items():
        L.append(f"- {tf}: " + ", ".join(f"{v5.NAMES[k]} {v}" for k, v in o["optimized"]["weights"].items()))
    L += ["", "## 4. Strateji yarışması (yalnız canlı botun da görebildiği veriler; eğitimde seçildi, TEST'te sınandı)", ""]
    for tf, o in rep["tfs"].items():
        c = o.get("contest")
        if not c:
            continue
        bl = c["live_baseline_test"]
        L += [f"### {tf} — {c['tested']} strateji denendi · {'✅ kazanan benimsendi' if c['adopted'] else '❌ hiçbiri yeterince iyi değil, mevcut kalır'}", "",
              f"Mevcut (trend, filtresiz) TEST: {bl.get('n')} işlem, kazanma %{_f(bl.get('win'))}, ort R {_f(bl.get('avg_R'))}, PF {_f(bl.get('pf'))}", "",
              "| # | Strateji | Eğitim ort R (n) | TEST ort R | TEST kazanma | TEST PF | 5x ort ROE | 10x ort ROE | 10x likidasyon |", "|---|---|---|---|---|---|---|---|---|"]
        for i, x in enumerate(c["top"], 1):
            t5, t10 = x["test"]["5"], x["test"]["10"]
            L.append(f"| {i} | {x['name']} | {x['train']['avg_R']} ({x['train']['n']}) | {_f(t5.get('avg_R'))} | %{_f(t5.get('win'))} ({t5.get('n')}) | {_f(t5.get('pf'))} | %{_f(t5.get('avg_roe'))} | %{_f(t10.get('avg_roe'))} | {_f(t10.get('liq'))} |")
        L.append("")
    L += ["", "IC (bilgi katsayısı): gösterge puanı ile sonraki getiri arasındaki sıralama korelasyonu. Piyasada 0.02–0.05 bile anlamlıdır; negatif ise gösterge ters çalışıyor demektir.",
          "Geçmiş performans geleceği garanti etmez."]
    return "\n".join(L)


def notify(rep):
    chat = os.environ.get("TELEGRAM_CHAT_ID")
    p = os.path.join(STATE, "portfolio.json")
    if not chat and os.path.exists(p):
        chat = json.load(open(p, encoding="utf-8")).get("chat_id")
    fp = os.path.join(STATE, "futures.json")
    if not chat and os.path.exists(fp):
        chat = json.load(open(fp, encoding="utf-8")).get("chat_id")
    lines = [f"🧪 <b>V5 araştırma</b> ({len(rep['coins'])} coin, {rep['eval_days']} gün)"]
    for tf, o in rep["tfs"].items():
        b5, b10 = o["baseline"]["5"], o["baseline"]["10"]
        best = sorted([(v5.NAMES[k], e["ic"]) for k, e in o["indicators_test"].items() if k in COMPS and e.get("ic") is not None], key=lambda x: -x[1])
        op = o["optimized"]
        lines.append(f"\n<b>{tf}</b>: {b5.get('n')} işlem, kazanma %{_f(b5.get('win'))}, ort R {_f(b5.get('avg_R'))}\n"
                     f"5x ort ROE %{_f(b5.get('avg_roe'))} · 10x %{_f(b10.get('avg_roe'))} (likidasyon {_f(b10.get('liq'))})\n"
                     f"En faydalı: {', '.join(f'{n} {ic:+.3f}' for n, ic in best[:3])}\n"
                     f"En zayıf: {', '.join(f'{n} {ic:+.3f}' for n, ic in best[-2:])}\n"
                     f"Yeni ağırlıklar: {'✅' if op['adopted'] else '❌'} (test ort R {_f(op['test']['5'].get('avg_R'))})")
        c = o.get("contest")
        if c and c["top"]:
            w = c["top"][0]
            lines.append(f"Strateji yarışması kazananı: {w['name']} → TEST ort R {_f(w['test']['5'].get('avg_R'))}, kazanma %{_f(w['test']['5'].get('win'))}, PF {_f(w['test']['5'].get('pf'))} {'✅ bota uygulandı' if c['adopted'] else '❌ yetersiz'}")
    telegram.send(chat, "\n".join(lines))


if __name__ == "__main__":
    main()
