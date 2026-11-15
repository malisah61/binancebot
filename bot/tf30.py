"""30 dakikalık botun 1 yıllık testi: BTC trend filtresi + gerçek hesap risk kuralları.

Botun 30dk kâğıt hesabındaki kuralın aynısı (canlı ağırlıklar + 30dk stratejisi, aynı mumda en çok 3 yeni işlem)
ilk EX30_COINS futures coininde son 365 günde çalıştırılır; işlemler 3x kaldıraçla simüle edilir (komisyon + funding dahil).
Filtre varyantları (sinyal anında bilinen BTC durumuyla):
  yok · long yalnız BTC 30g yükselişte (short serbest) · BTC 30g yönünde · BTC 4s trend yönünde · yalnız short
Seçim eğitimde (ilk %70), karar modelin görmediği TEST'te (son %30): n≥40, ort R>0, PF>1.05, eğitimde ort R>0.
Her varyant ayrıca gerçek hesap kurallarıyla tek hesapta yeniden oynatılır: bakiyenin %15'i marjin, 3x, en çok 3 açık
işlem, günlük %5 zarar limiti (1000$ ile başlar).
"""
from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime, timedelta, timezone

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
import binance  # noqa: E402
import research  # noqa: E402
import sim  # noqa: E402
import telegram  # noqa: E402
import v5  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TF = os.environ.get("EX_TF", "30m")
BPD = 86_400_000 // v5.TF_MS[TF]                       # günde mum
TFH = v5.TF_MS[TF] / 3_600_000                          # mum saat
TAG = {"30m": "30dk", "2h": "2s", "1h": "1s", "4h": "4s"}.get(TF, TF)
EV_TH = (0.05, 0.08, 0.12) if TFH <= 0.5 else (0.08, 0.12, 0.20)
research.MAX_HOLD.setdefault(TF, int(72 / TFH) if TFH >= 1 else 96)
N = int(os.environ.get("EX30_COINS", 50))
DAYS = int(os.environ.get("EX30_DAYS", 365))
WARM = 45
LEV = 3
RULES = {"frac": 0.15, "lev": 3, "max_pos": 3, "daily": 0.05}
VARIANTS = {
    "yok": "Filtre yok (botun şu anki hali)",
    "long_btc_up": "Long yalnız BTC 30g yükselişteyken (short serbest)",
    "btc30_dir": "Yalnız BTC 30 günlük yönünde",
    "btc4h_dir": "Yalnız BTC 4s trend yönünde",
    "short_only": "Yalnız short",
}


def jobs(sym, today):
    start = today - timedelta(days=DAYS + WARM)
    m = datetime(start.year, start.month, 1, tzinfo=timezone.utc)
    cur = datetime(today.year, today.month, 1, tzinfo=timezone.utc)
    B, C = research.BASE, research.CACHE
    out = []
    while m < cur:
        ym = m.strftime("%Y-%m")
        out.append(("k", f"{B}/monthly/klines/{sym}/{TF}/{sym}-{TF}-{ym}.zip", f"{C}/k{TF}/{sym}/{ym}.zip", False))
        out.append(("f", f"{B}/monthly/fundingRate/{sym}/{sym}-fundingRate-{ym}.zip", f"{C}/f/{sym}/{ym}.zip", False))
        m = (m + timedelta(days=32)).replace(day=1)
    d = cur
    while d < today:
        out.append(("k", f"{B}/daily/klines/{sym}/{TF}/{sym}-{TF}-{d:%Y-%m-%d}.zip", f"{C}/k{TF}d/{sym}/{d:%Y-%m-%d}.zip", (today - d).days <= 3))
        d += timedelta(days=1)
    return out


def load(today):
    from concurrent.futures import ThreadPoolExecutor
    syms = [x["symbol"] for x in binance.top_usdt(N + 15)]
    if "BTCUSDT" not in syms:
        syms.insert(0, "BTCUSDT")
    J = [(s, *j) for s in syms for j in jobs(s, today)]
    with ThreadPoolExecutor(32) as ex:
        paths = list(ex.map(lambda j: research.fetch(j[2], j[3], j[4]), J))
    per = {}
    for j, p in zip(J, paths):
        per.setdefault(j[0], []).append((j[1], p))
    raw = {}
    for s in syms:
        r = research.load_coin(s, per[s])
        if r is None or len(r[0]) < BPD * 120:
            continue
        raw[s] = r
        if len(raw) >= N + 1:
            break
    return raw


def btc_maps(btc_df, btc_R):
    c = btc_df["c"].values.astype(float)
    r30 = np.r_[np.full(30 * BPD, np.nan), c[30 * BPD:] / c[:-30 * BPD] - 1]
    return dict(zip(btc_df["t"].values, r30)), dict(zip(btc_df["t"].values, np.sign(np.nan_to_num(btc_R["f_htf"].values.astype(float)))))


def filtered_scores(name, t, score, b30, b4):
    s = score.copy()
    r30 = np.array([b30.get(x, np.nan) for x in t])
    h4 = np.array([b4.get(x, 0.0) for x in t])
    up30, dn30 = r30 > 0, r30 < 0
    no_long = no_short = np.zeros(len(s), bool)
    if name == "long_btc_up":
        no_long = ~up30
    elif name == "btc30_dir":
        no_long, no_short = ~up30, ~dn30
    elif name == "btc4h_dir":
        no_long, no_short = h4 <= 0, h4 >= 0
    elif name == "short_only":
        no_long = np.ones(len(s), bool)
    s[no_long] = np.minimum(s[no_long], 50.0)
    s[no_short] = np.maximum(s[no_short], 50.0)
    return s


def tstats(T):
    if not T:
        return {"n": 0}
    R = np.array([x["R"] for x in T])
    roe = np.array([x["roe"] for x in T])
    g, ls = roe[roe > 0].sum(), -roe[roe < 0].sum()
    lo = [x for x in T if x["dir"] > 0]
    return {"n": len(T), "win": round(float((roe > 0).mean() * 100), 1), "avg_R": round(float(R.mean()), 3),
            "pf": round(float(g / ls), 2) if ls > 0 else None, "avg_roe": round(float(roe.mean() * 100), 2),
            "long": len(lo), "short": len(T) - len(lo), "liq": int(sum(x["liq"] for x in T))}


def replay(T, start=1000.0, frac=None, max_pos=None):
    """Gerçek hesap kurallarıyla tek hesap: marjin = bakiye×%15, en çok 3 açık, günlük %5 zarar limiti."""
    eq, peak, mdd, opened, skipped, n, day0 = start, start, 0.0, {}, 0, 0, {}
    ev = sorted([(x["t"], 1, i) for i, x in enumerate(T)] + [(x["t_exit"] + 1, 0, i) for i, x in enumerate(T)])
    for t, kind, i in ev:
        day = (t // 1000 + 3 * 3600) // 86400
        day0.setdefault(day, eq)
        if kind == 0:
            if i in opened:
                eq += opened.pop(i) * T[i]["roe"]
                peak, mdd = max(peak, eq), max(mdd, 1 - eq / peak)
                n += 1
        elif len(opened) >= (max_pos or RULES["max_pos"]) or eq < day0[day] * (1 - RULES["daily"]) or any(T[j]["sym"] == T[i]["sym"] for j in opened):
            skipped += 1
        else:
            opened[i] = eq * (frac or RULES["frac"])
    return {"final": round(eq, 1), "ret": round((eq / start - 1) * 100, 1), "mdd": round(mdd * 100, 1), "n": n, "skip": skipped}


# ---------------------------------------------------------------- seçici kurallar
SEL_DAILY = 4          # günde en çok yeni işlem


def score_rules(strat):
    tr = dict(strat, type="trend", lt=74, st=26, max_new=1)
    out = {"A_trend74": ("Skor ≥74/≤26 uç sinyal, BTC 30g yönünde, mumda 1 işlem", tr)}
    for fib in (0.382, 0.5):
        for h in (None, "with"):
            out[f"A_pb{int(fib*1000)}_{h or 'x'}"] = (
                f"Skor ≥66 + %{fib*100:.1f} geri çekilmede limit{' + 4s trend yönünde' if h else ''}, BTC 30g yönünde",
                {"type": "pullback", "lt": 66, "st": 34, "max_pos": 0.5, "entry": "fib", "fib": fib, "expire": 6, "stop_lb": 12,
                 "buf": 0.3, "max_risk": 3.0, "tp1": 1.5, "tp2": 3.0, "htf": h, "max_new": 1})
    return out


def event_trades(coins, b30):
    """30dk sert hareketler (6 saatte ≥ eşik): aynı yönde Fib geri çekilmesine limit veya ters yöne piyasa girişi."""
    import extreme as X
    X.FIB_WAIT = max(6, int(12 / TFH))    # 12 saat bekler
    win_h = int(12 * TFH)                   # pencere: 12 mum
    cost = X.FEE + 2 * X.SLIP["büyük"]
    res = {}
    for s, (df, R, fm) in coins.items():
        o, h, l, c = (df[q].values.astype(float) for q in "ohlc")
        t = df["t"].values
        a = X.atr(h, l, c)
        hi, lo = X.roll_max(h, 12), X.roll_min(l, 12)
        dn, up = c / hi - 1, c / lo - 1
        fu = df["funding"].values.astype(float) if "funding" in df else np.zeros(len(c))
        for th in EV_TH:
            last = -10 ** 9
            for i in np.flatnonzero(((dn <= -th) & (np.r_[0, dn[:-1]] > -th)) | ((up >= th) & (np.r_[0, up[:-1]] < th))):
                if i < 31 * BPD or i - last < 12 or i >= len(c) - 2:
                    continue
                last = i
                ev = "crash" if dn[i] <= -th else "pump"
                r30 = b30.get(t[i], np.nan)
                for name in ("S_f38", "S_f50", "S_f62", "L_mkt") if ev == "crash" else ("L_f38", "L_f50", "L_f62", "S_mkt"):
                    d = X.VARIANTS[ev][name][0]
                    if ev == "crash" and name == "L_mkt":
                        e, sp, mode = c[i], min(lo[i] - 0.5 * a[i], c[i] - a[i]), "mkt"
                    elif ev == "pump" and name == "S_mkt":
                        e, sp, mode = c[i], max(hi[i] + 0.5 * a[i], c[i] + a[i]), "mkt"
                    else:
                        p = X.plan(ev, name, o, h, l, c, i, a[i], lo[i], hi[i])
                        if p is None:
                            continue
                        e, sp, mode, _ = p
                    r = X.sim(o, h, l, c, i, d, e, sp, mode, cost, float(np.nan_to_num(fu[i])) * TFH, hold=int(36 / TFH))
                    if not r.get("filled"):
                        continue
                    tr = {"sym": s, "t": int(t[min(r["start"], len(t) - 1)]), "t_exit": int(t[min(r["start"] + r["bars"] - 1, len(t) - 1)]),
                          "dir": d, "R": r["R"], "roe": LEV * r["R"] * r["risk"], "liq": False}
                    for rg in ("tümü", "btc"):
                        if rg == "btc" and not ((d > 0 and r30 > 0) or (d < 0 and r30 < 0)):
                            continue
                        key = f"B_{ev}_{name}_{int(th*100)}_{rg}"
                        desc = (f"{win_h} saatte %{int(th*100)}+ {'düşüş' if ev == 'crash' else 'yükseliş'} → {X.VARIANTS[ev][name][2] if 'f' in name else ('ters yöne hemen giriş')}"
                                f"{', BTC 30g yönünde' if rg == 'btc' else ''}")
                        res.setdefault(key, [desc, []])[1].append(tr)
    return res


def daily_cap(T, cap=SEL_DAILY):
    T = sorted(T, key=lambda x: x["t"])
    cnt, out = {}, []
    for x in T:
        d = x["t"] // 86400000
        if cnt.get(d, 0) < cap:
            cnt[d] = cnt.get(d, 0) + 1
            out.append(x)
    return out


def selective(coins, scores, b30, b4, strat, split):
    pool = {}
    for key, (desc, st) in score_rules(strat).items():
        sv = {s: filtered_scores("btc30_dir", coins[s][0]["t"].values, scores[s], b30, b4) for s in coins}
        pool[key] = (desc, research.run_strategy(coins, TF, st, LEV, "all", split, sv))
    for key, (desc, T) in event_trades(coins, b30).items():
        pool[key] = (desc, T)
    rows = {}
    for key, (desc, T) in pool.items():
        T = daily_cap(T)
        tr, te = [x for x in T if x["t"] < split], [x for x in T if x["t"] >= split]
        rows[key] = {"desc": desc, "train": tstats(tr), "test": tstats(te), "replay_train": replay(tr), "replay_test": replay(te),
                     "replay_all": replay(T), "per_day": round(len(T) / DAYS, 2)}
    cand = [k for k, v in rows.items() if v["train"].get("n", 0) >= 100]
    pick = max(cand, key=lambda k: rows[k]["train"]["avg_roe"]) if cand else None
    te = rows[pick]["test"] if pick else {}
    adopted = bool(pick and te.get("n", 0) >= 40 and te["avg_roe"] > 0 and (te.get("pf") or 0) > 1.05 and rows[pick]["train"]["avg_roe"] > 0)
    return {"rows": rows, "pick": pick, "adopted": adopted}


def monthly(T):
    m = {}
    for x in T:
        k = datetime.fromtimestamp(x["t"] / 1000, timezone.utc).strftime("%Y-%m")
        m.setdefault(k, []).append(x["R"])
    return {k: round(float(np.mean(v)), 3) for k, v in sorted(m.items())}


def analyze(raw, today):
    eval_start = int((today - timedelta(days=DAYS)).timestamp() * 1000)
    split = int((today - timedelta(days=DAYS * 0.3)).timestamp() * 1000)
    import fbot
    w, strat, sname, _ = fbot.model_for(TF)
    if strat.get("max_new", 99) >= 99:
        strat = dict(strat, max_new=3)
    coins, scores = {}, {}
    for s, (k, met, fund) in raw.items():
        df = research.with_extras(k.copy(), TF, None, fund)
        R = v5.compute(df, TF)
        sc = fbot.score_with(R, w)
        sc[df["t"].values < eval_start] = np.nan
        coins[s] = (df, R, sim.funding_marks(df["t"].values, v5.TF_MS[TF], df.get("funding")))
        scores[s] = sc
    b30, b4 = btc_maps(coins["BTCUSDT"][0], coins["BTCUSDT"][1])
    res = {}
    for name in VARIANTS:
        sv = {s: filtered_scores(name, coins[s][0]["t"].values, scores[s], b30, b4) for s in coins}
        T = research.run_strategy(coins, TF, strat, LEV, "all", split, sv)
        tr, te = [x for x in T if x["t"] < split], [x for x in T if x["t"] >= split]
        res[name] = {"desc": VARIANTS[name], "train": tstats(tr), "test": tstats(te), "replay_train": replay(tr), "replay_test": replay(te),
                     "replay_all": replay(T), "monthly": monthly(T)}
    sel = selective(coins, scores, b30, b4, strat, split)
    cand = [k for k, v in res.items() if v["train"].get("n", 0) >= 100]
    pick = max(cand, key=lambda k: res[k]["train"]["avg_R"]) if cand else None
    te = res[pick]["test"] if pick else {}
    adopted = bool(pick and te.get("n", 0) >= 40 and te["avg_R"] > 0 and (te.get("pf") or 0) > 1.05 and res[pick]["train"]["avg_R"] > 0)
    return {"time": int(time.time() * 1000), "coins": len(coins), "days": DAYS, "split": split, "strategy": sname,
            "variants": res, "pick": pick, "adopted": adopted, "selective": sel}


def fs(s):
    return f"{s['n']} işl · %{s['win']} · ort {s['avg_R']}R · PF {s['pf']} (L{s['long']}/S{s['short']})" if s.get("n") else "-"


def fs2(s):
    return f"{s['n']} işl · %{s['win']} · ort %{s['avg_roe']} · PF {s['pf']}" if s.get("n") else "-"


def to_md(r):
    d = datetime.fromtimestamp(r["time"] / 1000, timezone.utc) + timedelta(hours=3)
    sp = datetime.fromtimestamp(r["split"] / 1000, timezone.utc)
    L = [f"# {TAG} grafik — 1 yıllık test ({d:%d.%m.%Y})", "",
         f"{r['coins']} coin, son {r['days']} gün, {TAG} mum, 3x kaldıraç (komisyon + funding dahil). Strateji: {r['strategy']}. "
         f"Eğitim → {sp:%d.%m.%Y} → TEST.", "",
         "## İşlem bazında", "", "| Varyant | Eğitim | TEST |", "|---|---|---|"]
    for k, v in r["variants"].items():
        L.append(f"| {v['desc']} | {fs(v['train'])} | {fs(v['test'])} |")
    L += ["", "## Gerçek hesap kurallarıyla (1000$; %15 marjin, 3x, en çok 3 işlem, günlük %5 limit)", "",
          "| Varyant | Eğitim dönemi | TEST dönemi | Tüm yıl |", "|---|---|---|---|"]
    for k, v in r["variants"].items():
        a, b, c = v["replay_train"], v["replay_test"], v["replay_all"]
        L.append(f"| {v['desc']} | %{a['ret']:+} (en büyük düşüş %{a['mdd']}) | %{b['ret']:+} (düşüş %{b['mdd']}) | %{c['ret']:+} (düşüş %{c['mdd']}, {c['n']} işlem) |")
    L += ["", "## Aylara göre ortalama R", "", "| Ay | " + " | ".join(r["variants"]) + " |", "|---" * (len(r["variants"]) + 1) + "|"]
    months = sorted({m for v in r["variants"].values() for m in v["monthly"]})
    for m in months:
        L.append(f"| {m} | " + " | ".join(str(v["monthly"].get(m, "-")) for v in r["variants"].values()) + " |")
    p = r["pick"]
    if p:
        L += ["", f"**Eğitimde en iyi:** {r['variants'][p]['desc']} → " + ("✅ TEST'te DOĞRULANDI" if r["adopted"] else "❌ TEST'te tutmadı")]
    S = r.get("selective")
    if S:
        rows = sorted(S["rows"].items(), key=lambda kv: -(kv[1]["train"].get("avg_roe") or -99) if kv[1]["train"].get("n", 0) >= 100 else 99)
        L += ["", f"## Seçici kurallar (günde en çok {SEL_DAILY} yeni işlem) — eğitime göre en iyi 12", "",
              "| Kural | günde | Eğitim | TEST | Gerçek kurallarla TEST dönemi | Tüm yıl |", "|---|---|---|---|---|---|"]
        for k, v in rows[:12]:
            b, c = v["replay_test"], v["replay_all"]
            L.append(f"| {v['desc']} | {v['per_day']} | {fs2(v['train'])} | {fs2(v['test'])} | %{b['ret']:+} (düşüş %{b['mdd']}) | %{c['ret']:+} (düşüş %{c['mdd']}) |")
        good = [(k, v) for k, v in S["rows"].items() if v["test"].get("n", 0) >= 40 and v["test"]["avg_roe"] > 0 and (v["test"].get("pf") or 0) > 1.05 and (v["train"].get("avg_roe") or -1) > 0]
        L += ["", "Hem eğitimde hem TEST'te kârlı olanlar (bilgi amaçlı): " + ("; ".join(f"{v['desc']} (TEST {fs2(v['test'])})" for k, v in good[:6]) or "yok")]
        if S["pick"]:
            L += ["", f"**Seçici kurallarda eğitimde en iyi:** {S['rows'][S['pick']]['desc']} → " + ("✅ TEST'te DOĞRULANDI" if S["adopted"] else "❌ TEST'te tutmadı")]
    L += ["", "_Simülasyondur, yatırım tavsiyesi değildir._"]
    return "\n".join(L)


def main():
    t0 = time.time()
    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    raw = load(today)
    print(f"{len(raw)} coin yüklendi ({time.time()-t0:.0f} sn)")
    r = analyze(raw, today)
    json.dump(r, open(os.path.join(ROOT, "state", f"tf{TF}.json"), "w"), ensure_ascii=False, default=float)
    md = to_md(r)
    os.makedirs(os.path.join(ROOT, "docs", "arastirma"), exist_ok=True)
    open(os.path.join(ROOT, "docs", "arastirma", f"{TAG}-1yil-{(today + timedelta(hours=3)):%Y-%m-%d}.md"), "w", encoding="utf-8").write(md)
    print(md)
    import notify
    chat = os.environ.get("TELEGRAM_CHAT_ID") or json.load(open(os.path.join(ROOT, "state", "futures.json"))).get("chat_id")
    telegram.send(chat, notify.md_to_tg(md))
    print(f"toplam {time.time()-t0:.0f} sn")


if __name__ == "__main__":
    main()
