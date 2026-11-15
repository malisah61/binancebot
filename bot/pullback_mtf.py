"""Trend yönünde geri çekilmede giriş — 1 gün / 4 saat / 2 saat / 1 saat karşılaştırması + ortak göstergeler.

Trend (her zaman diliminde kendi mumlarıyla): YUKARI = kapanış > EMA200, EMA50 > EMA200 ve EMA50 son 5 mumda yükseliyor
(AŞAĞI tersi). Kurulum: trend yönünde son 3 mumda yeni 20 mumluk tepe (düşüşte dip) yapılmış ve fiyat hâlâ EMA20'nin
trend tarafında. Girişler (6 mum içinde dolmazsa iptal):
  ema20  : EMA20'ye limit · f38/f50 : son 20 mumluk salınımın %38.2 / %50 geri çekilmesine limit
  donus  : fiyat EMA20'nin altına sarktıktan sonra önceki mumun tepesi üstünde kapanınca piyasa
Stop: giriş − 1 ATR ve son 10 mumun dibinin 0.3 ATR altı (hangisi daha uzaksa); hedef 1.5R (yarısı, stop girişe) / 3R.
Varyant: BTC aynı zaman diliminde de aynı trendde mi. Gerçek hesap kurallarıyla yeniden oynatılır (3x, %15, 3 işlem, %5).
Ortak gösterge analizi: temel kurulumda (f38) kazanan vs kaybeden; dört zaman diliminde ve iki dönemde aynı yönde olanlar.
"""
from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime, timedelta, timezone

os.environ.setdefault("EX_COINS", os.environ.get("PB_COINS", "60"))
os.environ.setdefault("EX_DAYS", "365")
os.environ.setdefault("EX_MET_DAYS", "2")

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
import extreme as X  # noqa: E402
import research  # noqa: E402
import telegram  # noqa: E402
import tf30  # noqa: E402
import v5  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TFS = ["1d", "4h", "2h", "1h"]
HOLD = {"1d": 20, "4h": 42, "2h": 48, "1h": 72}
D_DAYS = 3 * 365          # günlük grafik için 3 yıl (EMA200 ısınması)
ENTRIES = {"ema20": "EMA20'ye limit", "f38": "%38.2 geri çekilmeye limit", "f50": "%50 geri çekilmeye limit", "donus": "EMA20 altına sarkıp dönünce piyasa"}
FEATS = {"f_rsi": "RSI", "f_z": "Z-puanı (fiyat sapması)", "f_htf": "Üst periyot trendi", "f_rvol": "Hacim patlaması (RVOL)",
         "f_taker": "Agresif alım oranı", "f_obv": "OBV eğimi", "f_vwap_atr": "VWAP'a uzaklık (ATR)", "f_squeeze": "Bollinger sıkışması",
         "f_macd": "MACD", "dist200": "EMA200'e uzaklık (ATR)", "swing": "Salınım boyu (ATR)", "atr_pct": "Oynaklık (ATR %)", "btc_ok": "BTC aynı trendde"}


def daily_jobs(sym, today):
    start = today - timedelta(days=D_DAYS + 40)
    m = datetime(start.year, start.month, 1, tzinfo=timezone.utc)
    cur = datetime(today.year, today.month, 1, tzinfo=timezone.utc)
    out = []
    while m < cur:
        ym = m.strftime("%Y-%m")
        out.append(("k", f"{research.BASE}/monthly/klines/{sym}/1d/{sym}-1d-{ym}.zip", f"{research.CACHE}/k1d/{sym}/{ym}.zip", False))
        m = (m + timedelta(days=32)).replace(day=1)
    d = cur
    while d < today:
        out.append(("k", f"{research.BASE}/daily/klines/{sym}/1d/{sym}-1d-{d:%Y-%m-%d}.zip", f"{research.CACHE}/k1dd/{sym}/{d:%Y-%m-%d}.zip", (today - d).days <= 3))
        d += timedelta(days=1)
    return out


def load_daily(syms, today):
    from concurrent.futures import ThreadPoolExecutor
    J = [(s, *j) for s in syms for j in daily_jobs(s, today)]
    with ThreadPoolExecutor(32) as ex:
        paths = list(ex.map(lambda j: research.fetch(j[2], j[3], j[4]), J))
    per = {}
    for j, p in zip(J, paths):
        per.setdefault(j[0], []).append((j[1], p))
    out = {}
    for s in syms:
        r = research.load_coin(s, per.get(s, []))
        if r is not None and len(r[0]) >= 300:
            out[s] = r[0]
    return out


def frames(k1h, tf):
    if tf == "1h":
        return k1h[["t", "o", "h", "l", "c", "v", "qv", "tq"]].reset_index(drop=True)
    ms = v5.TF_MS[tf]
    r = v5.resample(k1h, ms)
    return r[r["n"] == ms // 3_600_000].drop(columns="n").reset_index(drop=True)


def trend(c):
    e20, e50, e200 = (pd.Series(c).ewm(span=n, adjust=False).mean().values for n in (20, 50, 200))
    s50 = e50 > np.r_[np.full(5, np.nan), e50[:-5]]
    up = (c > e200) & (e50 > e200) & s50
    dn = (c < e200) & (e50 < e200) & (e50 < np.r_[np.full(5, np.nan), e50[:-5]])
    up[:200] = dn[:200] = False
    return e20, e50, e200, up, dn


def coin_trades(s, df, tf, btc_tr, tier, split):
    o, h, l, c = (df[q].values.astype(float) for q in "ohlc")
    t = df["t"].values
    n = len(c)
    if n < 300:
        return {}, []
    a = X.atr(h, l, c)
    e20, e50, e200, up, dn = trend(c)
    R = v5.compute(df, tf)
    hh, ll = X.roll_max(h, 20), X.roll_min(l, 20)
    ll10, hh10 = X.roll_min(l, 10), X.roll_max(h, 10)
    hh3, ll3 = X.roll_max(h, 3), X.roll_min(l, 3)
    cost = X.FEE + 2 * X.SLIP[tier]
    tfh = v5.TF_MS[tf] / 3_600_000
    bt = np.array([btc_tr.get(x, 0) for x in t])
    out, samples = {}, []
    for d, tr_ok in ((1, up), (-1, dn)):
        fresh = (hh3 >= hh) if d == 1 else (ll3 <= ll)
        side = (c > e20) if d == 1 else (c < e20)
        setup = tr_ok & fresh & side
        for ent in ENTRIES:
            last = -10 ** 9
            for i in np.flatnonzero(setup):
                if i - last < 6 or i >= n - 2:
                    continue
                last = i
                mode, j = "lim", i
                if ent == "ema20":
                    lv = e20[i]
                elif ent in ("f38", "f50"):
                    f = 0.382 if ent == "f38" else 0.5
                    lv = hh[i] - f * (hh[i] - ll[i]) if d == 1 else ll[i] + f * (hh[i] - ll[i])
                else:
                    mode, j, dipped = "mkt", None, False
                    for q in range(i + 1, min(n - 1, i + 7)):
                        dipped = dipped or ((l[q] < e20[q]) if d == 1 else (h[q] > e20[q]))
                        if dipped and ((c[q] > h[q - 1]) if d == 1 else (c[q] < l[q - 1])):
                            j = q
                            break
                    if j is None:
                        continue
                    lv = c[j]
                if (d == 1 and lv >= c[i] and mode == "lim") or (d == -1 and lv <= c[i] and mode == "lim"):
                    continue
                stop = min(lv - a[i], ll10[j] - 0.3 * a[i]) if d == 1 else max(lv + a[i], hh10[j] + 0.3 * a[i])
                fund = 0.0
                r = X.sim(o, h, l, c, j, d, lv, stop, mode, cost, fund, hold=HOLD[tf], wait=6)
                if not r.get("filled"):
                    continue
                tr = {"sym": s, "t": int(t[min(r["start"], n - 1)]), "t_exit": int(t[min(r["start"] + r["bars"] - 1, n - 1)]),
                      "dir": d, "R": r["R"], "roe": 3 * r["R"] * r["risk"], "liq": False, "btc_ok": bool(bt[i] == d)}
                out.setdefault(ent, []).append(tr)
                if ent == "f38":
                    row = {q: float(R[q].iloc[i]) if q in R and R[q].iloc[i] == R[q].iloc[i] else np.nan for q in FEATS if q.startswith("f_")}
                    if "f_htf" in row and row["f_htf"] == row["f_htf"]:
                        row["f_htf"] *= d                                  # trend yönüne göre işaretle
                    for q in ("f_z", "f_vwap_atr", "f_obv", "f_macd"):
                        if q in row and row[q] == row[q]:
                            row[q] *= d
                    if "f_rsi" in row and row["f_rsi"] == row["f_rsi"] and d == -1:
                        row["f_rsi"] = 100 - row["f_rsi"]
                    if "f_taker" in row and row["f_taker"] == row["f_taker"] and d == -1:
                        row["f_taker"] = 1 - row["f_taker"]
                    row.update(dist200=d * (c[i] - e200[i]) / max(a[i], 1e-12), swing=(hh[i] - ll[i]) / max(a[i], 1e-12),
                               atr_pct=a[i] / c[i] * 100, btc_ok=float(bt[i] == d), t=int(t[i]), win=r["R"] > 0, train=bool(t[i] < split))
                    samples.append(row)
    return out, samples


def btc_trend_map(df):
    c = df["c"].values.astype(float)
    _, _, _, up, dn = trend(c)
    return dict(zip(df["t"].values, np.where(up, 1, np.where(dn, -1, 0))))


def cohen(S):
    res = {}
    for q in FEATS:
        if q not in S:
            continue
        r = {}
        for part, P in (("train", S[S["train"]]), ("test", S[~S["train"]])):
            w, lo = P.loc[P["win"], q].dropna(), P.loc[~P["win"], q].dropna()
            if len(w) < 15 or len(lo) < 15:
                break
            sd = np.sqrt((w.var() + lo.var()) / 2) or 1e-9
            r[part] = {"d": round(float((w.mean() - lo.mean()) / sd), 2), "win": round(float(w.median()), 3), "loss": round(float(lo.median()), 3)}
        if len(r) == 2:
            res[q] = r
    return res


def analyze(data1h, daily, rank, today):
    start = int((today - timedelta(days=int(os.environ["EX_DAYS"]))).timestamp() * 1000)
    split = int(start + 0.7 * (today.timestamp() * 1000 - start))
    dstart = int((today - timedelta(days=D_DAYS)).timestamp() * 1000)
    dsplit = int(dstart + 0.7 * (today.timestamp() * 1000 - dstart))
    rep = {"tfs": {}, "split": split, "dsplit": dsplit}
    for tf in TFS:
        sp = dsplit if tf == "1d" else split
        src = daily if tf == "1d" else {s: frames(k, tf) for s, (k, m) in data1h.items()}
        if "BTCUSDT" not in src:
            continue
        btc = btc_trend_map(src["BTCUSDT"])
        allt, samples = {}, []
        for s, df in src.items():
            o, smp = coin_trades(s, df, tf, btc, X.tier_of(rank.get(s, 999)), sp)
            for k, v in o.items():
                allt.setdefault(k, []).extend(v)
            samples += smp
        res = {}
        for ent, T in allt.items():
            for flt in ("tümü", "btc"):
                TT = [x for x in T if flt == "tümü" or x["btc_ok"]]
                tr, te = [x for x in TT if x["t"] < sp], [x for x in TT if x["t"] >= sp]
                res[f"{ent}|{flt}"] = {"desc": ENTRIES[ent] + (", BTC aynı trendde" if flt == "btc" else ""), "train": tf30.tstats(tr), "test": tf30.tstats(te),
                                       "replay_train": tf30.replay(tr), "replay_test": tf30.replay(te)}
        cand = [k for k, v in res.items() if v["train"].get("n", 0) >= 60]
        pick = max(cand, key=lambda k: res[k]["train"]["avg_roe"]) if cand else None
        te = res[pick]["test"] if pick else {}
        adopted = bool(pick and te.get("n", 0) >= 40 and te["avg_roe"] > 0 and (te.get("pf") or 0) > 1.05 and res[pick]["train"]["avg_roe"] > 0)
        rep["tfs"][tf] = {"rules": res, "pick": pick, "adopted": adopted, "feat": cohen(pd.DataFrame(samples)) if samples else {}, "split": sp}
    common = []
    for q, nm in FEATS.items():
        ds = [(tf, v["feat"][q]) for tf, v in rep["tfs"].items() if q in v["feat"]]
        if len(ds) < 3:
            continue
        signs = [np.sign(x["train"]["d"]) for _, x in ds] + [np.sign(x["test"]["d"]) for _, x in ds]
        mags = [min(abs(x["train"]["d"]), abs(x["test"]["d"])) for _, x in ds]
        common.append({"f": q, "name": nm, "n_tf": len(ds), "same_sign": bool(len(set(signs)) == 1), "min_d": round(float(min(mags)), 2),
                       "by_tf": {tf: f"{x['train']['d']}/{x['test']['d']}" for tf, x in ds}, "sign": int(signs[0])})
    common.sort(key=lambda r: (-r["same_sign"], -r["min_d"]))
    rep["common"] = common
    return rep


def to_md(r):
    d = datetime.fromtimestamp(r["time"] / 1000, timezone.utc) + timedelta(hours=3)
    fs = tf30.fs2
    L = [f"# Trend yönünde geri çekilmede giriş — 1g / 4s / 2s / 1s ({d:%d.%m.%Y})", "",
         f"{r['coins']} futures coini; 1 saat-4 saat: son 1 yıl, 1 gün: son 3 yıl. Eğitim %70 → TEST %30. 3x, komisyon + kayma dahil.", "",
         "## Karşılaştırma (TEST dönemi, gerçek hesap kurallarıyla 1000$)", "", "| Giriş | " + " | ".join(r["tfs"]) + " |", "|---" * (len(r["tfs"]) + 1) + "|"]
    for ent in ENTRIES:
        for flt in ("tümü", "btc"):
            cells = []
            for tf, v in r["tfs"].items():
                x = v["rules"].get(f"{ent}|{flt}")
                cells.append(f"{x['test']['n']} işl · PF {x['test']['pf']} · %{x['replay_test']['ret']:+}" if x and x["test"].get("n") else "-")
            L.append(f"| {ENTRIES[ent]}{' + BTC' if flt == 'btc' else ''} | " + " | ".join(cells) + " |")
    for tf, v in r["tfs"].items():
        sp = datetime.fromtimestamp(v["split"] / 1000, timezone.utc)
        L += ["", f"## {tf} (eğitim → {sp:%d.%m.%Y} → TEST)", "", "| Giriş | Eğitim | TEST | Gerçek kurallarla eğitim / TEST |", "|---|---|---|---|"]
        for k, x in v["rules"].items():
            L.append(f"| {x['desc']} | {fs(x['train'])} | {fs(x['test'])} | %{x['replay_train']['ret']:+} / %{x['replay_test']['ret']:+} (düşüş %{x['replay_test']['mdd']}) |")
        if v["pick"]:
            L.append(f"\n**Eğitimde en iyi:** {v['rules'][v['pick']]['desc']} → " + ("✅ TEST'te DOĞRULANDI" if v["adopted"] else "❌ TEST'te tutmadı"))
    L += ["", "## Ortak göstergeler (kazanan vs kaybeden, d = etki büyüklüğü; eğitim/TEST, her zaman diliminde)", "",
          "Pozitif d: kazananlarda daha yüksek. Değerler trend yönüne göre işaretli (short'ta RSI = 100−RSI vb.).", "",
          "| Gösterge | Tüm dilimlerde aynı yön | en küçük |d| | " + " | ".join(r["tfs"]) + " |", "|---|---|---|" + "---|" * len(r["tfs"])]
    for c in r["common"]:
        L.append(f"| {c['name']} | {'✓ ' + ('yüksek iyi' if c['sign'] > 0 else 'düşük iyi') if c['same_sign'] else ''} | {c['min_d']} | "
                 + " | ".join(c["by_tf"].get(tf, "-") for tf in r["tfs"]) + " |")
    L += ["", "_Simülasyondur, yatırım tavsiyesi değildir._"]
    return "\n".join(L)


def main():
    t0 = time.time()
    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    data, rank = X.load_all(today)
    data = {s: v for s, v in data.items() if v[1] == "fut"}
    daily = load_daily(list(data), today)
    print(f"{len(data)} coin 1s, {len(daily)} coin günlük ({time.time()-t0:.0f} sn)")
    r = analyze(data, daily, rank, today)
    r.update(time=int(time.time() * 1000), coins=len(data))
    json.dump(r, open(os.path.join(ROOT, "state", "pullback_mtf.json"), "w"), ensure_ascii=False, default=float)
    md = to_md(r)
    os.makedirs(os.path.join(ROOT, "docs", "arastirma"), exist_ok=True)
    open(os.path.join(ROOT, "docs", "arastirma", f"geri-cekilme-mtf-{(today + timedelta(hours=3)):%Y-%m-%d}.md"), "w", encoding="utf-8").write(md)
    print(md)
    import notify
    chat = os.environ.get("TELEGRAM_CHAT_ID") or json.load(open(os.path.join(ROOT, "state", "futures.json"))).get("chat_id")
    telegram.send(chat, notify.md_to_tg(md))
    print(f"toplam {time.time()-t0:.0f} sn")


if __name__ == "__main__":
    main()
