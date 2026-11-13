"""Canlı kaldıraçlı simülasyon botu — 8 sanal hesap: {15m, 30m, 1h, 4h} × {5x, 10x}.

Her 15 dakikada (GitHub Actions) çalışır:
  1) Hacimce ilk 40 USDT coinin kapanmış mumlarını alır, V5 skorunu hesaplar.
     (Ağırlıklar state/model.json'daki öğrenilmiş model; yoksa varsayılan.)
     Not: GitHub sunucusu ABD'de olduğu için canlı futures verisi (OI, funding, L/S) alınamaz;
     canlıda Trend, Momentum, Hacim, FVG+Likidite avı ve VWAP kullanılır.
  2) Yeni kapanan mumda LONG/SHORT kararı çıkan coinlerde pozisyon açar (marj = varlığın %10'u).
  3) Açık pozisyonları 15dk mumlarla takip eder: SL 1.5×ATR, TP1 1.5×ATR (yarısı + stop girişe),
     TP2 3×ATR, likidasyon, süre sınırı. Komisyon %0.05/işlem.
  4) Telegram'a bildirim, komutlar: /durum /sinyal /coin XXX
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
import telegram  # noqa: E402
import v5  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(ROOT, "state")
TR = timezone(timedelta(hours=3))
TFS = ["15m", "30m", "1h", "4h"]
LEVS = [5, 10]
LIVE_COMPS = ["trend", "momentum", "volume", "smc", "vwap"]
CFG = {"start": 1000.0, "margin_frac": 0.10, "max_pos": 6, "fee": 0.0005, "mmr": 0.005, "coins": 40,
       "max_hold": {"15m": 96, "30m": 96, "1h": 72, "4h": 42}}


def now_ms():
    return int(time.time() * 1000)


def load(name, default):
    p = os.path.join(STATE, name)
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    return default


def save(name, data):
    os.makedirs(STATE, exist_ok=True)
    with open(os.path.join(STATE, name), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)


def fmt(x):
    if x >= 100: return f"{x:,.2f}"
    if x >= 1: return f"{x:.4f}"
    return f"{x:.6g}"


def model_for(tf):
    """Canlı ağırlıklar + strateji (araştırmanın TEST'te doğruladığı; yoksa varsayılan trend)."""
    m = load("model.json", {}).get("tfs", {}).get(tf) or {}
    w = {k: v for k, v in (m.get("live_weights") or {}).items() if k in LIVE_COMPS and v} or {k: v5.WEIGHTS[k] for k in LIVE_COMPS}
    st = dict(v5.DEFAULT_STRATEGY, **(m.get("strategy") or {}))
    return w, st, m.get("strategy_name") or v5.strategy_name(st), bool(m.get("strategy_adopted"))


def score_with(R, w):
    keys = list(w)
    comp = R[keys].astype(float).values
    ww = np.array([w[k] for k in keys], float)
    mask = ~np.isnan(comp)
    s = 50 + 50 * np.nansum(comp * ww, axis=1) / np.where((mask * np.abs(ww)).sum(axis=1) == 0, np.nan, (mask * np.abs(ww)).sum(axis=1))
    return s


def closed(df, tf):
    return df[df["t"] + v5.TF_MS[tf] <= now_ms()].reset_index(drop=True)


def fetch_coin(sym):
    k15 = pd.DataFrame(binance.klines(sym, "15m", 1000))
    k1h = pd.DataFrame(binance.klines(sym, "1h", 600))
    k4h = pd.DataFrame(binance.klines(sym, "4h", 600))
    r30 = v5.resample(k15, v5.TF_MS["30m"])
    k30 = r30[r30["n"] == 2].drop(columns="n").reset_index(drop=True)
    return {"15m": closed(k15, "15m"), "30m": closed(k30, "30m"), "1h": closed(k1h, "1h"), "4h": closed(k4h, "4h")}, closed(k15, "15m")


def new_account():
    return {"equity": CFG["start"], "start": CFG["start"], "positions": [], "closed": [], "curve": []}


# ---------------------------------------------------------------- pozisyon yönetimi
def step_position(p, c):
    """Tek bir 15dk mumu uygular. Kapanırsa (sebep, fiyat getirisi) döner."""
    d, e = p["dir"], p["entry"]
    hit_stop = c["l"] <= p["stop"] if d > 0 else c["h"] >= p["stop"]
    hit1 = c["h"] >= p["tp1"] if d > 0 else c["l"] <= p["tp1"]
    hit2 = c["h"] >= p["tp2"] if d > 0 else c["l"] <= p["tp2"]
    if not p["tp1_done"]:
        if hit_stop:
            return ("LİKİDASYON" if p["stop_is_liq"] else "SL"), d * (p["stop"] / e - 1)
        if hit2:
            return "TP2", d * ((p["tp1"] + p["tp2"]) / 2 / e - 1)
        if hit1:
            p["tp1_done"], p["stop"], p["stop_is_liq"] = True, e, False
            p["realized"] = 0.5 * d * (p["tp1"] / e - 1)
            return None
    else:
        if hit_stop:
            return "TP1→BE", p["realized"]
        if hit2:
            return "TP2", p["realized"] + 0.5 * d * (p["tp2"] / e - 1)
    if c["t"] + 900_000 >= p["until"]:
        rem = 0.5 if p["tp1_done"] else 1.0
        return "SÜRE", p.get("realized", 0) + rem * d * (c["c"] / e - 1)
    return None


def close_pos(acc, p, reason, ret, lev, tf, msgs):
    fees = lev * CFG["fee"] * 2
    roe = (-1.0 - lev * CFG["fee"]) if reason == "LİKİDASYON" else lev * ret - fees
    pnl = p["margin"] * roe
    acc["equity"] += pnl
    risk = abs(p["entry"] - p["sl"]) / p["entry"]
    acc["closed"].append({"sym": p["sym"], "dir": p["dir"], "entry": p["entry"], "opened": p["opened"], "closed": now_ms(),
                          "reason": reason, "roe": round(roe * 100, 2), "pnl": round(pnl, 2), "R": round(ret / risk, 2),
                          "score": p["score"], "snap": p.get("snap")})
    acc["closed"] = acc["closed"][-400:]
    e = "🟢" if pnl > 0 else "🔴"
    msgs.append(f"{e} {tf} {lev}x {'LONG' if p['dir'] > 0 else 'SHORT'} {p['sym'].replace('USDT', '')} kapandı: {reason} · ROE {roe*100:+.1f}% ({pnl:+.1f}$)")


def manage(state, k15s, msgs):
    for key, acc in state["accounts"].items():
        tf, lev = key.split("_")[0], int(key.split("_")[1][:-1])
        keep = []
        for p in acc["positions"]:
            k = k15s.get(p["sym"])
            if k is None:
                keep.append(p); continue
            done = None
            for c in k[k["t"] >= p["checked"]].to_dict("records"):
                if c["t"] + 900_000 <= p["opened"]:
                    continue
                done = step_position(p, c)
                p["checked"] = int(c["t"]) + 900_000
                if done:
                    break
            if done:
                close_pos(acc, p, done[0], done[1], lev, tf, msgs)
            else:
                keep.append(p)
        acc["positions"] = keep


def open_pos(acc, sym, d, row, tf, lev, score, snap, msgs, st=None):
    st = st or v5.DEFAULT_STRATEGY
    e, A = float(row["c"]), float(row["atr"])
    if not np.isfinite(A) or A <= 0:
        return
    margin = acc["equity"] * CFG["margin_frac"]
    if margin < 5:
        return
    liq = e * (1 - d * (1 / lev - CFG["mmr"]))
    sl = e - d * st["sl"] * A
    stop_is_liq = d * (liq - sl) > 0
    p = {"sym": sym, "dir": d, "entry": e, "atr": A, "sl": sl, "tp1": e + d * st["tp1"] * A, "tp2": e + d * st["tp2"] * A, "strategy": st.get("type"),
         "stop": liq if stop_is_liq else sl, "stop_is_liq": bool(stop_is_liq), "liq": liq, "tp1_done": False, "realized": 0.0,
         "margin": round(margin, 2), "opened": int(row["t"]) + v5.TF_MS[tf], "checked": int(row["t"]) + v5.TF_MS[tf],
         "until": int(row["t"]) + v5.TF_MS[tf] * (1 + CFG["max_hold"][tf]), "score": float(score), "snap": snap}
    acc["positions"].append(p)
    msgs.append(f"{'🟢 LONG' if d > 0 else '🔴 SHORT'} {tf} {lev}x <b>{sym.replace('USDT', '')}</b> @ {fmt(e)} (skor {score:.0f}) "
                f"SL {fmt(p['sl'])} TP1 {fmt(p['tp1'])} TP2 {fmt(p['tp2'])}{' ⚠️likidasyon stoptan yakın' if stop_is_liq else ''}")


# ---------------------------------------------------------------- mesajlar
def status_text(state, px=None):
    L = ["💼 <b>8 sanal hesap</b> (başlangıç 1000$)", "<code>Hesap     Varlık   Açık İşlem Kazan</code>"]
    for key, a in state["accounts"].items():
        cl = a["closed"]
        win = f"%{sum(1 for x in cl if x['pnl'] > 0) / len(cl) * 100:.0f}" if cl else "-"
        unreal = 0.0
        if px:
            for p in a["positions"]:
                cur = px.get(p["sym"])
                if cur:
                    lev = int(key.split("_")[1][:-1])
                    rem = 0.5 if p["tp1_done"] else 1.0
                    unreal += p["margin"] * lev * (p["realized"] + rem * p["dir"] * (cur / p["entry"] - 1))
        eq = a["equity"] + unreal
        L.append(f"<code>{key:<9} {eq:7.0f}$ {len(a['positions']):>4} {len(cl):>5} {win:>5}</code>")
    return "\n".join(L)


def handle_commands(state, px, latest):
    for u in telegram.updates(state.get("tg_offset")):
        state["tg_offset"] = u["update_id"] + 1
        m = u.get("message") or {}
        chat = (m.get("chat") or {}).get("id")
        txt = (m.get("text") or "").strip().lower()
        if not chat:
            continue
        if not state.get("chat_id"):
            state["chat_id"] = chat
            telegram.send(chat, "✅ Bağlandı! Komutlar: /durum /sinyal /coin BTC")
            continue
        if chat != state["chat_id"]:
            continue
        if txt.startswith(("/durum", "/start")):
            telegram.send(chat, status_text(state, px))
        elif txt.startswith("/sinyal"):
            L = []
            for tf in TFS:
                rows = sorted(latest.get(tf, []), key=lambda x: -x[1])
                if rows:
                    L.append(f"<b>{tf}</b> 📈 " + ", ".join(f"{s.replace('USDT', '')} {sc:.0f}" for s, sc in rows[:4])
                             + " · 📉 " + ", ".join(f"{s.replace('USDT', '')} {sc:.0f}" for s, sc in rows[-3:]))
            telegram.send(chat, "\n".join(L) or "Veri yok")
        elif txt.startswith("/coin"):
            sym = (txt.split()[-1] if len(txt.split()) > 1 else "btc").upper()
            sym = sym if sym.endswith("USDT") else sym + "USDT"
            L = [f"<b>{sym}</b>"]
            for tf in TFS:
                r = next((x for x in latest.get(tf, []) if x[0] == sym), None)
                if r:
                    L.append(f"{tf}: skor {r[1]:.1f} → {v5.decision([r[1]])[0]}")
            telegram.send(chat, "\n".join(L) if len(L) > 1 else f"{sym} ilk 40'ta değil.")


# ---------------------------------------------------------------- ana
def main():
    state = load("futures.json", None)
    if not state:
        old = load("portfolio.json", {})
        state = {"created": now_ms(), "accounts": {f"{tf}_{lev}x": new_account() for tf in TFS for lev in LEVS},
                 "last_bar": {}, "chat_id": old.get("chat_id"), "tg_offset": old.get("tg_offset")}
    if os.environ.get("TELEGRAM_CHAT_ID"):
        state["chat_id"] = int(os.environ["TELEGRAM_CHAT_ID"])
    msgs = []
    t0 = time.time()
    syms = [x["symbol"] for x in binance.top_usdt(CFG["coins"])]
    held = {p["sym"] for a in state["accounts"].values() for p in a["positions"]}
    syms += [s for s in held if s not in syms]

    def one(s):
        try:
            return s, fetch_coin(s)
        except Exception as e:
            print("veri hatası", s, e)
            return s, None
    with ThreadPoolExecutor(8) as ex:
        data = {s: r for s, r in ex.map(one, syms) if r}
    print(f"{len(data)} coin verisi ({time.time()-t0:.0f} sn)")
    k15s = {s: r[1] for s, r in data.items()}
    px = {s: float(r[1]["c"].iloc[-1]) for s, r in data.items() if len(r[1])}

    manage(state, k15s, msgs)

    latest = {}
    for tf in TFS:
        w, st, st_name, adopted = model_for(tf)
        rows = []
        for s, (frames, _) in data.items():
            df = frames[tf]
            if len(df) < 260:
                continue
            R = v5.compute(df, tf)
            sc = score_with(R, w)
            if not np.isfinite(sc[-1]):
                continue
            d, strength = v5.signals(R, sc, st)
            snap = {k: (round(float(R[k].iloc[-1]), 2) if np.isfinite(R[k].iloc[-1]) else None) for k in LIVE_COMPS}
            for f in ("f_z", "f_rsi", "f_htf", "f_vwap_atr", "f_rvol", "f_ssl3", "f_bsl3"):
                val = R[f].iloc[-1]
                snap[f] = round(float(val), 2) if np.isfinite(val) else None
            rows.append((s, float(sc[-1]), R.iloc[-1], int(df["t"].iloc[-1]), snap, int(d[-1]), float(strength[-1])))
        latest[tf] = [(r[0], r[1]) for r in rows]
        if not rows:
            continue
        bar_t = max(r[3] for r in rows)
        if state["last_bar"].get(tf) == bar_t:
            continue  # bu periyotta yeni mum kapanmadı
        state["last_bar"][tf] = bar_t
        cands = sorted([r for r in rows if r[3] == bar_t and r[5] != 0], key=lambda r: -r[6])
        cands = cands[:st.get("max_new", 99)]  # aynı anda çok sayıda aynı yönlü işlem = tek büyük bahis; sınırla
        for lev in LEVS:
            acc = state["accounts"][f"{tf}_{lev}x"]
            busy = {p["sym"] for p in acc["positions"]}
            for s, sc, row, _, snap, d, _ in cands:
                if len(acc["positions"]) >= CFG["max_pos"]:
                    break
                if s in busy:
                    continue
                open_pos(acc, s, d, row, tf, lev, sc, snap, msgs, st)
                busy.add(s)
        state.setdefault("strategy", {})[tf] = st_name

    handle_commands(state, px, latest)

    for key, a in state["accounts"].items():
        a["curve"].append([now_ms(), round(a["equity"], 2)])
        a["curve"] = a["curve"][-2000:]
    today = datetime.now(TR).strftime("%Y-%m-%d")
    if datetime.now(TR).hour >= 21 and state.get("last_summary") != today:
        state["last_summary"] = today
        msgs.append("🗓 <b>Günlük özet</b>\n" + status_text(state, px))
    state["updated"] = now_ms()
    if msgs:
        telegram.send(state.get("chat_id"), "\n".join(msgs))
    save("futures.json", state)
    print("\n".join(msgs))
    print(status_text(state, px))


if __name__ == "__main__":
    main()
