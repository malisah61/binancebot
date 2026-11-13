"""Binance kâğıt üzerinde (simülasyon) al-sat botu.

Gerçek para KULLANMAZ, Binance hesabına bağlanmaz. Her çalıştırmada:
  1) Hacimce ilk 100 USDT çiftini tarar (1 saatlik mumlar, 4s trend filtresi)
  2) Güçlü adaylara emir defteri + büyük işlem analizi ekler
  3) Sanal portföyde alım/satım yapar (komisyon dahil)
  4) Telegram'a bildirim yollar, Telegram komutlarını yanıtlar
Durum state/ klasöründe JSON olarak saklanır ve depoya geri yazılır.
"""
from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime, timezone, timedelta
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(__file__))
import binance  # noqa: E402
import telegram  # noqa: E402
from analysis import analyze  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(ROOT, "state")
TR = timezone(timedelta(hours=3))

CFG = {
    "start_cash": 1000.0,     # sanal başlangıç bakiyesi (USDT)
    "max_positions": 5,
    "position_frac": 0.19,    # her işlem toplam varlığın %19'u
    "fee": 0.001,             # Binance spot %0.1
    "buy_score": 68,          # bu skorun üstü AL adayı
    "min_agreement": 0.6,     # göstergelerin en az %60'ı aynı yönde
    "sell_score": 42,         # pozisyondaki coin bu skorun altına inerse SAT
    "min_quote_volume": 20e6, # 24s hacmi 20M$ altı coinlere girme
    "cooldown_h": 6,          # aynı coine satıştan sonra bekleme
    "signal_alert_h": 6,      # aynı coin için sinyal bildirimi aralığı
}


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
    return f"{x:.8g}"


def now_ms():
    return int(time.time() * 1000)


# ---------------------------------------------------------------- tarama
def scan():
    tick = binance.top_usdt(100)
    vol = {t["symbol"]: float(t["quoteVolume"]) for t in tick}

    def one(sym):
        try:
            k = binance.klines(sym, "1h", 1000)
            if len(k) < 250:
                return None
            a = analyze(k)
            a["symbol"] = sym
            a["qv24"] = vol[sym]
            a["_k"] = k
            return a
        except Exception as e:
            print("hata", sym, e)
            return None

    with ThreadPoolExecutor(8) as ex:
        res = [r for r in ex.map(one, list(vol)) if r]
    return res


def deep(a):
    """Emir defteri ve büyük işlemleri ekleyerek yeniden analiz."""
    try:
        book = binance.depth(a["symbol"])
        trades = binance.agg_trades(a["symbol"])
        b = analyze(a["_k"], book, trades)
        b.update(symbol=a["symbol"], qv24=a["qv24"], _k=a["_k"])
        return b
    except Exception as e:
        print("derin analiz hata", a["symbol"], e)
        return a


def comp(a, name):
    for c in a["components"]:
        if c["name"] == name:
            return c["score"]
    return 0.0


# ---------------------------------------------------------------- portföy
def equity(pf, px):
    return pf["cash"] + sum(p["qty"] * px.get(s, p["entry"]) for s, p in pf["positions"].items())


def sell(pf, sym, qty, price, reason, msgs):
    p = pf["positions"][sym]
    gross = qty * price
    fee = gross * CFG["fee"]
    pf["cash"] += gross - fee
    cost = qty * p["entry"] * (1 + CFG["fee"])
    pnl = gross - fee - cost
    p["qty"] -= qty
    p["realized"] = p.get("realized", 0) + pnl
    closed = p["qty"] <= p["qty0"] * 1e-6
    pf["trades"].append({"time": now_ms(), "symbol": sym, "side": "SAT", "price": price, "qty": qty,
                         "pnl": round(pnl, 4), "reason": reason})
    pct = (price / p["entry"] - 1) * 100
    e = "🟢" if pnl >= 0 else "🔴"
    msgs.append(f"{e} <b>SAT {sym}</b> @ {fmt(price)}\nSebep: {reason}\nSonuç: {pct:+.2f}% ({pnl:+.2f}$)")
    if closed:
        total = p["realized"]
        pf["closed"].append({"symbol": sym, "entry": p["entry"], "exit": price, "opened": p["time"],
                             "closed": now_ms(), "pnl": round(total, 4),
                             "pct": round(total / (p["qty0"] * p["entry"]) * 100, 2)})
        pf["cooldown"][sym] = now_ms()
        del pf["positions"][sym]


def manage(pf, scans, px, msgs):
    by = {a["symbol"]: a for a in scans}
    for sym in list(pf["positions"]):
        p = pf["positions"][sym]
        a = by.get(sym)
        try:
            k = a["_k"] if a else binance.klines(sym, "1h", 50)
        except Exception as e:
            print("pozisyon verisi yok", sym, e)
            continue
        # giriş mumundan sonraki mumlar (giriş öncesi fitiller yanlış stop tetiklemesin)
        since = [c for c in k if c["t"] >= p["time"] and c["t"] + 3600_000 > p["checked"]]
        cur = px.get(sym)
        if cur:
            since.append({"h": cur, "l": cur})
        A = p["atr"]
        for c in since:
            # önce zarar-durdur (kötümser varsayım)
            if c["l"] <= p["stop"]:
                sell(pf, sym, p["qty"], p["stop"], "Zarar durdur / iz süren stop", msgs)
                break
            if not p["tp1_done"] and c["h"] >= p["tp1"]:
                sell(pf, sym, p["qty"] * 0.5, p["tp1"], "1. hedef (yarısı satıldı)", msgs)
                p["tp1_done"] = True
                p["stop"] = max(p["stop"], p["entry"] * (1 + 2 * CFG["fee"]))
            if c["h"] >= p["tp2"]:
                sell(pf, sym, p["qty"], p["tp2"], "2. hedef", msgs)
                break
            p["high"] = max(p["high"], c["h"])
            if p["high"] - p["entry"] >= 1.5 * A:
                p["stop"] = max(p["stop"], p["entry"] * (1 + 2 * CFG["fee"]))
            p["stop"] = max(p["stop"], p["high"] - 2.2 * A)
        if sym in pf["positions"]:
            p["checked"] = now_ms()
            if a and a["score"] <= CFG["sell_score"]:
                sell(pf, sym, p["qty"], a["price"], f"Skor düştü ({a['score']})", msgs)


def buy(pf, a, eq, msgs):
    sym, price = a["symbol"], a["price"]
    budget = min(eq * CFG["position_frac"], pf["cash"])
    if budget < 10:
        return
    qty = budget / (price * (1 + CFG["fee"]))
    pf["cash"] -= qty * price * (1 + CFG["fee"])
    pl = a["plan"]
    pf["positions"][sym] = {"entry": price, "qty": qty, "qty0": qty, "time": now_ms(), "checked": now_ms(),
                            "stop": pl["stop"], "tp1": pl["tp1"], "tp2": pl["tp2"], "atr": a["atr"],
                            "high": price, "tp1_done": False, "score": a["score"], "realized": 0.0}
    pf["trades"].append({"time": now_ms(), "symbol": sym, "side": "AL", "price": price, "qty": qty,
                         "score": a["score"]})
    best = sorted(a["components"], key=lambda c: c["score"] * c["weight"], reverse=True)[:4]
    why = "\n".join(f"• {c['name']}: {c['text']}" for c in best)
    msgs.append(f"🛒 <b>AL {sym}</b> @ {fmt(price)}  (skor {a['score']}, uyum %{a['agreement']*100:.0f})\n"
                f"Tutar: {budget:.2f}$\nStop: {fmt(pl['stop'])}  Hedef1: {fmt(pl['tp1'])}  Hedef2: {fmt(pl['tp2'])}\n{why}")


# ---------------------------------------------------------------- mesajlar
def status_text(pf, px, scans=None):
    eq = equity(pf, px)
    st = pf["start"]
    lines = [f"💼 <b>Simülasyon portföyü</b>", f"Toplam: {eq:.2f}$ ({(eq/st-1)*100:+.2f}%)  Nakit: {pf['cash']:.2f}$"]
    for s, p in pf["positions"].items():
        cur = px.get(s, p["entry"])
        lines.append(f"• {s}: {fmt(p['entry'])} → {fmt(cur)} ({(cur/p['entry']-1)*100:+.2f}%) stop {fmt(p['stop'])}")
    cl = pf["closed"]
    if cl:
        w = sum(1 for x in cl if x["pnl"] > 0)
        lines.append(f"Kapanan işlem: {len(cl)}, kazanma oranı %{w/len(cl)*100:.0f}, "
                     f"toplam {sum(x['pnl'] for x in cl):+.2f}$")
    if scans:
        up = sorted(scans, key=lambda a: -a["score"])[:5]
        dn = sorted(scans, key=lambda a: a["score"])[:5]
        lines.append("\n📈 <b>Yükseliş skoru en yüksek</b>")
        lines += [f"{a['symbol']} {a['score']} ({a['change24']*100:+.1f}% 24s)" for a in up]
        lines.append("📉 <b>Düşüş riski en yüksek</b>")
        lines += [f"{a['symbol']} {a['score']} ({a['change24']*100:+.1f}% 24s)" for a in dn]
    return "\n".join(lines)


def handle_commands(pf, px, scans):
    ups = telegram.updates(pf.get("tg_offset"))
    for u in ups:
        pf["tg_offset"] = u["update_id"] + 1
        m = u.get("message") or {}
        chat = (m.get("chat") or {}).get("id")
        txt = (m.get("text") or "").strip().lower()
        if not chat:
            continue
        if not pf.get("chat_id"):
            pf["chat_id"] = chat
            telegram.send(chat, "✅ Bağlandı! Bildirimler bu sohbete gelecek.\nKomutlar: /durum /sinyal /coin BTC")
            continue
        if chat != pf["chat_id"]:
            continue
        if txt.startswith("/durum") or txt.startswith("/start"):
            telegram.send(chat, status_text(pf, px))
        elif txt.startswith("/sinyal"):
            telegram.send(chat, status_text(pf, px, scans))
        elif txt.startswith("/coin"):
            sym = txt.split()[-1].upper() if len(txt.split()) > 1 else "BTC"
            sym = sym if sym.endswith("USDT") else sym + "USDT"
            a = next((x for x in scans if x["symbol"] == sym), None)
            if not a:
                telegram.send(chat, f"{sym} ilk 100'de değil.")
            else:
                a = deep(a)
                c = "\n".join(f"{'🟢' if x['score']>0.1 else '🔴' if x['score']<-0.1 else '⚪'} {x['name']}: {x['text']}"
                              for x in a["components"])
                sup = ", ".join(fmt(x["price"]) for x in a["supports"][:3])
                res = ", ".join(fmt(x["price"]) for x in a["resistances"][:3])
                telegram.send(chat, f"<b>{sym}</b> {fmt(a['price'])} — skor {a['score']} ({a['label']})\n"
                                    f"Destek: {sup}\nDirenç: {res}\n{c}")


# ---------------------------------------------------------------- ana
def main():
    pf = load("portfolio.json", None) or {
        "start": CFG["start_cash"], "cash": CFG["start_cash"], "positions": {}, "trades": [],
        "closed": [], "cooldown": {}, "equity": [], "alerts": {}, "created": now_ms()}
    if os.environ.get("TELEGRAM_CHAT_ID"):
        pf["chat_id"] = int(os.environ["TELEGRAM_CHAT_ID"])
    msgs = []

    t0 = time.time()
    scans = scan()
    print(f"{len(scans)} coin tarandı ({time.time()-t0:.0f} sn)")
    px = {a["symbol"]: a["price"] for a in scans}
    if pf["positions"]:
        try:
            allp = binance.prices()
            px.update({s: allp[s] for s in pf["positions"] if s in allp})
        except Exception:
            pass

    manage(pf, scans, px, msgs)

    # alım adayları
    cands = [a for a in scans if a["score"] >= CFG["buy_score"] - 3 and a["qv24"] >= CFG["min_quote_volume"]]
    cands = sorted(cands, key=lambda a: -a["score"])[:12]
    deep_res = [deep(a) for a in cands]
    eq = equity(pf, px)
    for a in sorted(deep_res, key=lambda a: -a["score"]):
        sym = a["symbol"]
        if len(pf["positions"]) >= CFG["max_positions"] or sym in pf["positions"]:
            continue
        if now_ms() - pf["cooldown"].get(sym, 0) < CFG["cooldown_h"] * 3600_000:
            continue
        if a["score"] >= CFG["buy_score"] and a["agreement"] >= CFG["min_agreement"] and comp(a, "4s trend") > 0 \
                and a["rsi"] < 78:
            buy(pf, a, eq, msgs)

    # güçlü sinyal bildirimleri (pozisyon açılmasa da)
    strong = [a for a in deep_res if a["score"] >= 72 and a["symbol"] not in pf["positions"]]
    for a in strong:
        if now_ms() - pf["alerts"].get(a["symbol"], 0) > CFG["signal_alert_h"] * 3600_000:
            pf["alerts"][a["symbol"]] = now_ms()
            msgs.append(f"⚡ Güçlü yükseliş sinyali: <b>{a['symbol']}</b> skor {a['score']} @ {fmt(a['price'])}")
    weak = [a for a in scans if a["score"] <= 25 and a["qv24"] >= CFG["min_quote_volume"]]
    for a in sorted(weak, key=lambda a: a["score"])[:3]:
        key = "D_" + a["symbol"]
        if now_ms() - pf["alerts"].get(key, 0) > CFG["signal_alert_h"] * 3600_000:
            pf["alerts"][key] = now_ms()
            msgs.append(f"⚠️ Güçlü düşüş sinyali: <b>{a['symbol']}</b> skor {a['score']} @ {fmt(a['price'])}")

    handle_commands(pf, px, scans)

    # günlük özet (TR 21:00 sonrası, günde bir)
    today = datetime.now(TR).strftime("%Y-%m-%d")
    if datetime.now(TR).hour >= 21 and pf.get("last_summary") != today:
        pf["last_summary"] = today
        msgs.append("🗓 <b>Günlük özet</b>\n" + status_text(pf, px, scans))

    eq = equity(pf, px)
    pf["equity"].append([now_ms(), round(eq, 2)])
    pf["equity"] = pf["equity"][-3000:]
    pf["trades"] = pf["trades"][-500:]
    pf["updated"] = now_ms()

    if msgs:
        telegram.send(pf.get("chat_id"), "\n\n".join(msgs))

    save("portfolio.json", pf)
    slim = sorted(({k: v for k, v in a.items() if k not in ("_k", "fib", "components", "supports", "resistances")}
                   | {"components": a["components"]} for a in scans), key=lambda a: -a["score"])
    save("scan.json", {"time": now_ms(), "coins": slim})
    print(status_text(pf, px))


if __name__ == "__main__":
    main()
