"""Sahte Binance demo sunucusuyla emir akışı testi (ağ yok)."""
import json, os, sys, threading, time
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
os.environ["BINANCE_DEMO_KEY"] = "k"; os.environ["BINANCE_DEMO_SECRET"] = "s"
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "bot"))
POS = {}; ORD = []; ALGO = {}; INC = []
PRICE = {"XRPUSDT": 2.0}


class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def send(self, code, obj):
        b = json.dumps(obj).encode(); self.send_response(code); self.send_header("Content-Type", "application/json"); self.end_headers(); self.wfile.write(b)

    def handle_any(self):
        u = urlparse(self.path); q = {k: v[0] for k, v in parse_qs(u.query).items()}; p = u.path; m = self.command
        if p != "/fapi/v1/time" and p != "/fapi/v1/exchangeInfo" and "signature" not in q:
            return self.send(400, {"code": -1102, "msg": "imza yok"})
        if p == "/fapi/v1/time": return self.send(200, {"serverTime": int(time.time() * 1000)})
        if p == "/fapi/v1/exchangeInfo":
            return self.send(200, {"symbols": [{"symbol": "XRPUSDT", "contractType": "PERPETUAL", "status": "TRADING", "filters": [
                {"filterType": "LOT_SIZE", "stepSize": "0.1", "minQty": "0.1"}, {"filterType": "PRICE_FILTER", "tickSize": "0.0001"}, {"filterType": "MIN_NOTIONAL", "notional": "5"}]}]})
        if p == "/fapi/v2/balance": return self.send(200, [{"asset": "USDT", "balance": "5000", "crossUnPnl": "0", "availableBalance": "4800"}])
        if p == "/fapi/v2/positionRisk":
            s = q["symbol"]; return self.send(200, [{"positionAmt": str(POS.get(s, (0, 0))[0]), "entryPrice": str(POS.get(s, (0, 0))[1])}])
        if p in ("/fapi/v1/marginType", "/fapi/v1/leverage"): return self.send(200, {})
        if p == "/fapi/v1/order" and m == "POST":
            s = q["symbol"]
            if q["type"] == "LIMIT":
                i = 1000 + len(ORD); ORD.append({"orderId": i, "status": "NEW", "executedQty": "0", "price": q["price"], "symbol": s, "qty": q["quantity"], "side": q["side"]})
                return self.send(200, {"orderId": i})
            if q["type"] == "MARKET":
                qty = float(q["quantity"]) * (1 if q["side"] == "BUY" else -1)
                cur = POS.get(s, (0, 0))[0]; POS[s] = (round(cur + qty, 6), PRICE[s])
                return self.send(200, {"orderId": len(ORD), "avgPrice": str(PRICE[s]), "executedQty": q["quantity"]})
            return self.send(400, {"code": -4120, "msg": "Order type not supported for this endpoint. Please use the Algo Order API."})
        if p == "/fapi/v1/algoOrder" and m == "POST":
            i = len(ALGO) + 1; ALGO[i] = q; return self.send(200, {"algoId": i})
        if p == "/fapi/v1/algoOrder" and m == "DELETE":
            ALGO.pop(int(q["algoId"]), None); return self.send(200, {})
        if p == "/fapi/v1/openAlgoOrders": return self.send(200, [{"algoId": k} for k, v in ALGO.items() if v["symbol"] == q["symbol"]])
        if p == "/fapi/v1/allOpenOrders": return self.send(200, {})
        if p == "/fapi/v1/order" and m == "GET":
            o = next(x for x in ORD if str(x["orderId"]) == q["orderId"]); return self.send(200, {**o, "avgPrice": o["price"] if o["status"] == "FILLED" else "0", "updateTime": int(time.time() * 1000)})
        if p == "/fapi/v1/order" and m == "DELETE":
            for x in ORD:
                if "orderId" in q and str(x["orderId"]) == q["orderId"]: x["status"] = "CANCELED"
            return self.send(200, {})
        if p == "/fapi/v1/income": return self.send(200, [x for x in INC if x["kind"] == q["incomeType"]])
        return self.send(404, {"code": -1, "msg": p})
    do_GET = do_POST = do_DELETE = handle_any


srv = HTTPServer(("127.0.0.1", 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
import executor
executor.DEMO_HOSTS[:] = [f"http://127.0.0.1:{srv.server_port}"]; executor.ALLOWED = ("127.0.0.1",)
D = executor.Demo(); ds = executor.new_state(); msgs = []
executor.open_trade(D, ds, "XRPUSDT", 1, {"entry": 2.0, "sl": 1.9, "tp1": 2.15, "tp2": 2.3, "until": int(time.time() * 1000) + 10**7, "score": 70}, msgs)
assert "XRPUSDT" in ds["positions"], msgs
assert D.algo is True and len(ALGO) == 3, ALGO   # klasik uç reddetti → algo ucuna geçti
q = ds["positions"]["XRPUSDT"]["qty"]; print("açıldı", q, msgs[-1])
POS["XRPUSDT"] = (round(q / 2, 6), 2.0)           # TP1 doldu
executor.sync(D, ds, msgs); assert ds["positions"]["XRPUSDT"]["tp1_done"]; print(msgs[-1])
POS["XRPUSDT"] = (0, 0); INC += [{"kind": "REALIZED_PNL", "income": "12.5"}, {"kind": "COMMISSION", "income": "-0.8"}]
executor.sync(D, ds, msgs); assert not ds["positions"] and ds["closed"][-1]["pnl"] == 11.7; print(msgs[-1])
ds["paused"] = True; executor.open_trade(D, ds, "XRPUSDT", 1, {"entry": 2.0, "sl": 1.9, "tp1": 2.1, "tp2": 2.2, "until": 0, "score": 70}, msgs)
assert not ds["positions"]
# LIMIT akışı
ds["paused"] = False; ALGO.clear()
executor.place_limit(D, ds, "XRPUSDT", 1, {"entry": 1.95, "sl": 1.88, "tp1": 2.02, "tp2": 2.09, "expire_t": int(time.time() * 1000) + 10**7, "until_ms": 10**7, "score": 70}, msgs)
assert "XRPUSDT" in ds["pending"], msgs; print(msgs[-1])
executor.sync(D, ds, msgs); assert "XRPUSDT" in ds["pending"]           # henüz dolmadı
o = ORD[-1]; o["status"] = "FILLED"; o["executedQty"] = o["qty"]; POS["XRPUSDT"] = (float(o["qty"]), 1.95)
executor.sync(D, ds, msgs); assert "XRPUSDT" in ds["positions"] and len(ALGO) == 3, (ds, ALGO); print(msgs[-1])
# süresi dolan limit
POS["XRPUSDT"] = (0, 0); INC.clear(); INC.append({"kind": "REALIZED_PNL", "income": "-7"}); executor.sync(D, ds, msgs)
executor.place_limit(D, ds, "XRPUSDT", -1, {"entry": 2.1, "sl": 2.2, "tp1": 2.0, "tp2": 1.9, "expire_t": int(time.time() * 1000) - 1, "until_ms": 10**7, "score": 30}, msgs)
executor.sync(D, ds, msgs); assert not ds["pending"] and ORD[-1]["status"] == "CANCELED"; print("süresi dolan limit iptal edildi")
print("DEMO EMİR TESTİ GEÇTİ")
