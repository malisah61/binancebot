"""Binance Futures DEMO (testnet) emir modülü — sahte parayla GERÇEK emir akışı.

Bot bir pozisyon açtığında (seçilen hesap: varsayılan 4s × 5x, araştırmada doğrulanan strateji)
demo hesapta aynı işlemi gerçek emirlerle açar:
  piyasa emri + borsa tarafında STOP (SL) + TP1 (yarısı) + TP2 (kalanı)
Her çalıştırmada senkronize eder: TP1 dolduysa stop girişe çekilir, pozisyon kapandıysa kalan
emirler iptal edilir ve gerçekleşen kâr/zarar (komisyon dahil) kaydedilir.

Güvenlik: yalnızca DEMO adreslerine bağlanır (gerçek hesaba emir gönderemez).
Telegram: /dur (yeni işlem açma), /devam, /kapat (tüm demo pozisyonları kapat).
Günlük zarar limiti: demo bakiyesi gün başına göre %5 düşerse o gün yeni işlem açılmaz.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import math
import os
import time
from urllib.parse import urlencode

import requests

DEMO_HOSTS = [h for h in [os.environ.get("BINANCE_DEMO_BASE"), "https://demo-fapi.binance.com", "https://testnet.binancefuture.com"] if h]
ALLOWED = ("demo-fapi.binance.com", "testnet.binancefuture.com")  # gerçek hesaba emir gitmesin
KEY = os.environ.get("BINANCE_DEMO_KEY", "").strip()
SECRET = os.environ.get("BINANCE_DEMO_SECRET", "").strip()
CFG = {"tf": os.environ.get("DEMO_TF", "4h"), "lev": int(os.environ.get("DEMO_LEV", 5)), "margin_frac": 0.10,
       "max_pos": 5, "daily_loss": 0.05}


def enabled():
    return bool(KEY and SECRET)


class Demo:
    def __init__(self):
        self.s = requests.Session()
        self.s.headers["X-MBX-APIKEY"] = KEY
        self.base = None
        self.offset = 0
        self.info = {}
        self.algo = None  # koşullu emirler eski uç mu yeni "algo" uç mu
        self.log = []

    # ------------------------------------------------ düşük seviye
    def _find_base(self):
        for h in DEMO_HOSTS:
            if not any(a in h for a in ALLOWED):
                continue
            try:
                r = self.s.get(h + "/fapi/v1/time", timeout=10)
                if r.status_code == 200:
                    self.base = h
                    self.offset = r.json()["serverTime"] - int(time.time() * 1000)
                    return
                self.log.append(f"{h} → HTTP {r.status_code} {r.text[:120]}")
            except requests.RequestException as e:
                self.log.append(f"{h} → {e}")
        raise RuntimeError("Demo sunucusuna ulaşılamadı: " + " | ".join(self.log[-3:]))

    def req(self, method, path, params=None, signed=True):
        if not self.base:
            self._find_base()
        p = dict(params or {})
        if signed:
            p["timestamp"] = int(time.time() * 1000) + self.offset
            p["recvWindow"] = 10000
            q = urlencode(p, doseq=True)
            q += "&signature=" + hmac.new(SECRET.encode(), q.encode(), hashlib.sha256).hexdigest()
        else:
            q = urlencode(p)
        url = f"{self.base}{path}?{q}"
        for i in range(3):
            try:
                r = self.s.request(method, url, timeout=15)
                if r.status_code in (429, 418) or r.status_code >= 500:
                    time.sleep(2 + 3 * i); continue
                data = r.json() if r.text else {}
                if r.status_code != 200:
                    raise BinanceError(data.get("code"), data.get("msg", r.text[:200]))
                return data
            except requests.RequestException:
                time.sleep(2 + 3 * i)
        raise BinanceError(-1, f"{method} {path} cevap yok")

    # ------------------------------------------------ yardımcılar
    def load_info(self):
        if self.info:
            return
        ex = self.req("GET", "/fapi/v1/exchangeInfo", signed=False)
        for s in ex["symbols"]:
            if s.get("contractType") != "PERPETUAL" or s.get("status") != "TRADING":
                continue
            f = {x["filterType"]: x for x in s["filters"]}
            self.info[s["symbol"]] = {"step": float(f["MARKET_LOT_SIZE"]["stepSize"] if "MARKET_LOT_SIZE" in f else f["LOT_SIZE"]["stepSize"]),
                                      "minq": float(f["LOT_SIZE"]["minQty"]), "tick": float(f["PRICE_FILTER"]["tickSize"]),
                                      "notional": float(f.get("MIN_NOTIONAL", {}).get("notional", 5))}

    def rq(self, sym, q):
        st = self.info[sym]["step"]
        return float(f"{math.floor(q / st + 1e-9) * st:.10f}")

    def rp(self, sym, p):
        t = self.info[sym]["tick"]
        return float(f"{round(p / t) * t:.10f}")

    def balance(self):
        for b in self.req("GET", "/fapi/v2/balance"):
            if b["asset"] == "USDT":
                return float(b["balance"]) + float(b.get("crossUnPnl", 0)), float(b["availableBalance"])
        return 0.0, 0.0

    def position(self, sym):
        for p in self.req("GET", "/fapi/v2/positionRisk", {"symbol": sym}):
            if float(p["positionAmt"]) != 0:
                return float(p["positionAmt"]), float(p["entryPrice"])
        return 0.0, 0.0

    def cond(self, sym, side, typ, trigger, qty=None, close=False):
        """Borsa tarafında koşullu emir (STOP_MARKET / TAKE_PROFIT_MARKET). Önce klasik uç, gerekirse algo ucu."""
        trigger = self.rp(sym, trigger)
        if self.algo is not True:
            p = {"symbol": sym, "side": side, "type": typ, "stopPrice": trigger, "workingType": "MARK_PRICE"}
            p.update({"closePosition": "true"} if close else {"quantity": qty, "reduceOnly": "true"})
            try:
                o = self.req("POST", "/fapi/v1/order", p)
                self.algo = False
                return {"kind": "order", "id": o["orderId"]}
            except BinanceError as e:
                if self.algo is False or not (e.code in (-4120,) or "algo" in str(e.msg).lower()):
                    raise
                self.algo = True
        p = {"symbol": sym, "side": side, "algoType": "CONDITIONAL", "type": typ, "triggerPrice": trigger, "workingType": "MARK_PRICE"}
        p.update({"closePosition": "true"} if close else {"quantity": qty, "reduceOnly": "true"})
        o = self.req("POST", "/fapi/v1/algoOrder", p)
        return {"kind": "algo", "id": o.get("algoId")}

    def cancel(self, sym, ref):
        try:
            if ref["kind"] == "algo":
                self.req("DELETE", "/fapi/v1/algoOrder", {"algoId": ref["id"]})
            else:
                self.req("DELETE", "/fapi/v1/order", {"symbol": sym, "orderId": ref["id"]})
        except BinanceError:
            pass

    def cancel_all(self, sym):
        try:
            self.req("DELETE", "/fapi/v1/allOpenOrders", {"symbol": sym})
        except BinanceError:
            pass
        try:
            for o in self.req("GET", "/fapi/v1/openAlgoOrders", {"symbol": sym}) or []:
                self.cancel(sym, {"kind": "algo", "id": o.get("algoId")})
        except BinanceError:
            pass

    def realized(self, sym, since):
        pnl = 0.0
        for kind in ("REALIZED_PNL", "COMMISSION", "FUNDING_FEE"):
            try:
                for x in self.req("GET", "/fapi/v1/income", {"symbol": sym, "incomeType": kind, "startTime": since, "limit": 1000}):
                    pnl += float(x["income"])
            except BinanceError:
                pass
        return pnl


class BinanceError(Exception):
    def __init__(self, code, msg):
        super().__init__(f"{code}: {msg}")
        self.code, self.msg = code, msg


# ------------------------------------------------ bot ile entegrasyon
def new_state():
    return {"positions": {}, "pending": {}, "closed": [], "paused": False, "day": None, "day_start": None, "curve": [], "errors": []}


def _risk_gate(D, ds, sym, msgs):
    ds.setdefault("pending", {})
    if ds["paused"] or sym in ds["positions"] or sym in ds["pending"] or len(ds["positions"]) + len(ds["pending"]) >= CFG["max_pos"]:
        return None
    D.load_info()
    if sym not in D.info:
        return None
    eq, avail = D.balance()
    if ds.get("day_start") and eq < ds["day_start"] * (1 - CFG["daily_loss"]):
        if not ds.get("halted"):
            msgs.append(f"🧪⛔ DEMO günlük zarar limiti (%{CFG['daily_loss']*100:.0f}) aşıldı; bugün yeni işlem yok.")
        ds["halted"] = True
        return None
    try:
        D.req("POST", "/fapi/v1/marginType", {"symbol": sym, "marginType": "ISOLATED"})
    except BinanceError as e:
        if e.code != -4046:
            ds["errors"].append(f"marginType {sym}: {e}")
    D.req("POST", "/fapi/v1/leverage", {"symbol": sym, "leverage": CFG["lev"]})
    return min(eq * CFG["margin_frac"], avail * 0.9)


def place_limit(D, ds, sym, d, plan, msgs):
    """Geri çekilme stratejisi: giriş seviyesine LIMIT emir. Dolunca sync() stop/hedefleri koyar."""
    margin = _risk_gate(D, ds, sym, msgs)
    if not margin:
        return
    price = D.rp(sym, plan["entry"])
    qty = D.rq(sym, margin * CFG["lev"] / price)
    if qty < D.info[sym]["minq"] or qty * price < D.info[sym]["notional"]:
        ds["errors"].append(f"{sym}: limit miktarı çok küçük ({qty})")
        return
    o = D.req("POST", "/fapi/v1/order", {"symbol": sym, "side": "BUY" if d > 0 else "SELL", "type": "LIMIT", "timeInForce": "GTC",
                                          "quantity": qty, "price": price})
    ds["pending"][sym] = {"orderId": o["orderId"], "dir": d, "qty": qty, "entry": price, "sl": plan["sl"], "tp1": plan["tp1"], "tp2": plan["tp2"],
                          "expire_t": plan["expire_t"], "until_ms": plan["until_ms"], "score": plan["score"], "created": int(time.time() * 1000)}
    msgs.append(f"🧪⏳ DEMO limit {'ALIŞ' if d > 0 else 'SATIŞ'} {sym.replace('USDT', '')} {qty} @ {price:g} (stop {D.rp(sym, plan['sl']):g})")


def protect(D, ds, sym, pos, msgs):
    """Dolmuş pozisyona borsa tarafında SL + TP1 (yarısı) + TP2 koy. Konamazsa güvenlik için kapat."""
    close_side = "SELL" if pos["dir"] > 0 else "BUY"
    try:
        pos["orders"]["sl"] = D.cond(sym, close_side, "STOP_MARKET", pos["sl"], close=True)
        half = D.rq(sym, pos["qty"] / 2)
        if half >= D.info[sym]["minq"]:
            pos["orders"]["tp1"] = D.cond(sym, close_side, "TAKE_PROFIT_MARKET", pos["tp1"], qty=half)
        pos["orders"]["tp2"] = D.cond(sym, close_side, "TAKE_PROFIT_MARKET", pos["tp2"], close=True)
        return True
    except BinanceError as e:
        ds["errors"].append(f"{sym} koruma emri hatası: {e} → pozisyon kapatıldı")
        D.cancel_all(sym)
        amt, _ = D.position(sym)
        if amt:
            D.req("POST", "/fapi/v1/order", {"symbol": sym, "side": close_side, "type": "MARKET", "quantity": abs(amt), "reduceOnly": "true"})
        msgs.append(f"🧪⚠️ DEMO {sym}: stop/hedef konamadı (fiyat seviyeyi geçmiş olabilir), güvenlik için kapatıldı ({e.msg})")
        return False


def open_trade(D, ds, sym, d, plan, msgs):
    """plan: {'sl','tp1','tp2','until','score'} (bot hesaplar). Demo hesapta gerçek emirle açar."""
    if ds["paused"] or sym in ds["positions"] or len(ds["positions"]) >= CFG["max_pos"]:
        return
    D.load_info()
    if sym not in D.info:
        return
    eq, avail = D.balance()
    if ds.get("day_start") and eq < ds["day_start"] * (1 - CFG["daily_loss"]):
        if not ds.get("halted"):
            msgs.append(f"🧪⛔ DEMO günlük zarar limiti (%{CFG['daily_loss']*100:.0f}) aşıldı; bugün yeni işlem yok.")
        ds["halted"] = True
        return
    margin = min(eq * CFG["margin_frac"], avail * 0.9)
    lev = CFG["lev"]
    try:
        D.req("POST", "/fapi/v1/marginType", {"symbol": sym, "marginType": "ISOLATED"})
    except BinanceError as e:
        if e.code != -4046:  # zaten isolated
            ds["errors"].append(f"marginType {sym}: {e}")
    D.req("POST", "/fapi/v1/leverage", {"symbol": sym, "leverage": lev})
    price = plan["entry"]
    qty = D.rq(sym, margin * lev / price)
    if qty < D.info[sym]["minq"] or qty * price < D.info[sym]["notional"]:
        ds["errors"].append(f"{sym}: miktar çok küçük ({qty})")
        return
    side, close_side = ("BUY", "SELL") if d > 0 else ("SELL", "BUY")
    o = D.req("POST", "/fapi/v1/order", {"symbol": sym, "side": side, "type": "MARKET", "quantity": qty, "newOrderRespType": "RESULT"})
    fill = float(o.get("avgPrice") or 0)
    if not fill or not float(o.get("executedQty") or 0):  # bazı demo sunucuları dolum bilgisini dönmüyor → pozisyondan oku
        time.sleep(0.5)
        amt, ep = D.position(sym)
        fill, qty = (ep or price), (abs(amt) or qty)
    else:
        qty = float(o["executedQty"])
    # planı gerçek dolum fiyatına kaydır (ATR mesafeleri aynı kalır)
    shift = fill - price
    sl, tp1, tp2 = plan["sl"] + shift, plan["tp1"] + shift, plan["tp2"] + shift
    pos = {"dir": d, "qty": qty, "entry": fill, "sl": sl, "tp1": tp1, "tp2": tp2, "opened": int(time.time() * 1000),
           "until": plan["until"], "score": plan["score"], "tp1_done": False, "orders": {}, "slippage": round((fill / price - 1) * d * 100, 3)}
    try:
        pos["orders"]["sl"] = D.cond(sym, close_side, "STOP_MARKET", sl, close=True)
        half = D.rq(sym, qty / 2)
        if half >= D.info[sym]["minq"]:
            pos["orders"]["tp1"] = D.cond(sym, close_side, "TAKE_PROFIT_MARKET", tp1, qty=half)
        pos["orders"]["tp2"] = D.cond(sym, close_side, "TAKE_PROFIT_MARKET", tp2, close=True)
    except BinanceError as e:
        ds["errors"].append(f"{sym} koruma emri hatası: {e} → pozisyon kapatıldı")
        D.cancel_all(sym)
        D.req("POST", "/fapi/v1/order", {"symbol": sym, "side": close_side, "type": "MARKET", "quantity": qty, "reduceOnly": "true"})
        msgs.append(f"🧪⚠️ DEMO {sym}: stop/hedef emri konamadı, güvenlik için kapatıldı ({e.msg})")
        return
    ds["positions"][sym] = pos
    msgs.append(f"🧪 DEMO {'LONG' if d > 0 else 'SHORT'} {sym.replace('USDT', '')} {lev}x · {qty} adet @ {fill:g} (kayma %{pos['slippage']}) · "
                f"SL {D.rp(sym, sl):g} TP1 {D.rp(sym, tp1):g} TP2 {D.rp(sym, tp2):g}")


def sync(D, ds, msgs, close_all=False):
    now = int(time.time() * 1000)
    eq, _ = D.balance()
    day = time.strftime("%Y-%m-%d", time.gmtime(now / 1000 + 3 * 3600))
    if ds.get("day") != day:
        ds.update(day=day, day_start=eq, halted=False)
    ds.setdefault("pending", {})
    D.load_info()
    for sym in list(ds["pending"]):
        q = ds["pending"][sym]
        try:
            o = D.req("GET", "/fapi/v1/order", {"symbol": sym, "orderId": q["orderId"]})
        except BinanceError as e:
            ds["errors"].append(f"{sym} limit sorgu: {e}"); continue
        st_, exq = o.get("status"), float(o.get("executedQty") or 0)
        expired = now >= q["expire_t"] or close_all
        if st_ in ("NEW", "PARTIALLY_FILLED") and expired:
            try:
                D.req("DELETE", "/fapi/v1/order", {"symbol": sym, "orderId": q["orderId"]})
            except BinanceError:
                pass
            st_ = "CANCELED"
        if st_ == "FILLED" or (st_ in ("CANCELED", "EXPIRED") and exq > 0):
            amt, ep = D.position(sym)
            fill = float(o.get("avgPrice") or 0) or ep or q["entry"]
            pos = {"dir": q["dir"], "qty": abs(amt) or exq, "entry": fill, "sl": q["sl"], "tp1": q["tp1"], "tp2": q["tp2"], "opened": int(o.get("updateTime") or now),
                   "until": int(o.get("updateTime") or now) + q["until_ms"], "score": q["score"], "tp1_done": False, "orders": {},
                   "slippage": round((fill / q["entry"] - 1) * q["dir"] * 100, 3), "limit": True}
            del ds["pending"][sym]
            if protect(D, ds, sym, pos, msgs):
                ds["positions"][sym] = pos
                msgs.append(f"🧪✅ DEMO limit doldu: {'LONG' if pos['dir'] > 0 else 'SHORT'} {sym.replace('USDT', '')} {pos['qty']} @ {fill:g} · SL {q['sl']:g} TP1 {q['tp1']:g} TP2 {q['tp2']:g}")
        elif st_ in ("CANCELED", "EXPIRED", "REJECTED"):
            del ds["pending"][sym]
            ds["expired"] = ds.get("expired", 0) + 1
    for sym in list(ds["positions"]):
        p = ds["positions"][sym]
        amt, _ = D.position(sym)
        close_side = "SELL" if p["dir"] > 0 else "BUY"
        if amt != 0 and (close_all or now >= p["until"]):
            D.cancel_all(sym)
            D.req("POST", "/fapi/v1/order", {"symbol": sym, "side": close_side, "type": "MARKET", "quantity": abs(amt), "reduceOnly": "true"})
            amt = 0
            p["reason"] = "/kapat" if close_all else "SÜRE"
        if amt == 0:
            D.cancel_all(sym)
            time.sleep(0.5)
            pnl = D.realized(sym, p["opened"] - 1000)
            margin = p["qty"] * p["entry"] / CFG["lev"]
            reason = p.get("reason") or ("TP2" if p["tp1_done"] and pnl > 0 else "TP1→BE" if p["tp1_done"] else ("SL" if pnl < 0 else "TP2"))
            ds["closed"].append({"sym": sym, "dir": p["dir"], "entry": p["entry"], "opened": p["opened"], "closed": now, "pnl": round(pnl, 2),
                                 "roe": round(pnl / margin * 100, 2) if margin else None, "reason": reason, "score": p["score"], "slippage": p["slippage"]})
            ds["closed"] = ds["closed"][-500:]
            del ds["positions"][sym]
            msgs.append(f"🧪 DEMO {sym.replace('USDT', '')} kapandı: {reason} · {pnl:+.2f}$ (ROE {pnl / margin * 100 if margin else 0:+.1f}%)")
            continue
        if not p["tp1_done"] and abs(amt) < p["qty"] * 0.75:  # TP1 doldu → stop girişe
            p["tp1_done"] = True
            if "sl" in p["orders"]:
                D.cancel(sym, p["orders"]["sl"])
            be = p["entry"] * (1 + 0.0008 * p["dir"])  # komisyonu karşılayacak kadar üstü
            p["sl"] = be
            try:
                p["orders"]["sl"] = D.cond(sym, close_side, "STOP_MARKET", be, close=True)
                msgs.append(f"🧪 DEMO {sym.replace('USDT', '')}: TP1 alındı, stop girişe çekildi")
            except BinanceError as e:
                # Fiyat girişin gerisine dönmüşse borsa stop'u reddeder (ör. -2021 "hemen tetiklenir"). Eski stop iptal
                # edildiği için pozisyon korumasız kalmasın: kalan miktarı piyasa emriyle kapat (≈ giriş seviyesi).
                p["orders"].pop("sl", None)
                ds["errors"].append(f"{sym} başa-baş stop konamadı: {e} → kalan pozisyon kapatıldı")
                D.cancel_all(sym)
                D.req("POST", "/fapi/v1/order", {"symbol": sym, "side": close_side, "type": "MARKET", "quantity": abs(amt), "reduceOnly": "true"})
                p["reason"] = "TP1→BE"
                msgs.append(f"🧪⚠️ DEMO {sym.replace('USDT', '')}: TP1 alındı ama başa-baş stop konamadı ({e.msg}); kalan pozisyon güvenlik için kapatıldı")
    eq, _ = D.balance()
    ds["equity"] = round(eq, 2)
    ds["curve"].append([now, round(eq, 2)])
    ds["curve"] = ds["curve"][-3000:]
    ds["errors"] = ds["errors"][-50:]


def status(ds):
    cl = ds["closed"]
    w = sum(1 for x in cl if x["pnl"] > 0)
    return (f"🧪 <b>DEMO hesap</b> ({CFG['tf']} {CFG['lev']}x) — bakiye {ds.get('equity', 0):.2f} USDT"
            f"{' · ⏸ DURAKLATILDI' if ds['paused'] else ''}\nAçık: {len(ds['positions'])} · Bekleyen limit: {len(ds.get('pending', {}))} · Kapanan: {len(cl)} · Kazanma: "
            f"{'%' + format(w / len(cl) * 100, '.0f') if cl else '-'} · Toplam: {sum(x['pnl'] for x in cl):+.2f}$")
