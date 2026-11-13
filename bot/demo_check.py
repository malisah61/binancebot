"""Demo hesap bağlantı testi: anahtar, bakiye ve tam emir akışı (aç → stop koy → iptal → kapat).
GitHub Actions → "Demo bağlantı testi" ile çalışır, sonucu Telegram'a yollar."""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(__file__))
import executor, telegram  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    L = ["🧪 <b>Demo bağlantı testi</b>"]
    if not executor.enabled():
        L.append("❌ BINANCE_DEMO_KEY / BINANCE_DEMO_SECRET secret'ları bulunamadı.")
    else:
        D = executor.Demo()
        try:
            eq, av = D.balance()
            L.append(f"✅ Sunucu: {D.base}\n✅ Anahtar geçerli, bakiye {eq:.2f} USDT (kullanılabilir {av:.2f})")
            D.load_info()
            sym = "XRPUSDT" if "XRPUSDT" in D.info else sorted(D.info)[0]
            px = float(D.req("GET", "/fapi/v1/ticker/price", {"symbol": sym}, signed=False)["price"])
            D.req("POST", "/fapi/v1/leverage", {"symbol": sym, "leverage": 2})
            qty = D.rq(sym, max(D.info[sym]["notional"] * 1.3, 6) / px)
            qty = max(qty, D.info[sym]["minq"])
            o = D.req("POST", "/fapi/v1/order", {"symbol": sym, "side": "BUY", "type": "MARKET", "quantity": qty, "newOrderRespType": "RESULT"})
            L.append(f"✅ Piyasa emri: {sym} {o.get('executedQty')} @ {o.get('avgPrice')}")
            ref = D.cond(sym, "SELL", "STOP_MARKET", px * 0.9, close=True)
            L.append(f"✅ Stop emri konuldu ({'algo ucu' if ref['kind'] == 'algo' else 'klasik uç'})")
            ref2 = D.cond(sym, "SELL", "TAKE_PROFIT_MARKET", px * 1.1, qty=D.rq(sym, qty / 2) or qty)
            L.append("✅ Hedef emri konuldu")
            D.cancel(sym, ref); D.cancel(sym, ref2); D.cancel_all(sym)
            amt, _ = D.position(sym)
            if amt:
                D.req("POST", "/fapi/v1/order", {"symbol": sym, "side": "SELL", "type": "MARKET", "quantity": abs(amt), "reduceOnly": "true"})
            L.append("✅ Emirler iptal edildi, test pozisyonu kapatıldı.\nBot artık 4s × 5x stratejisini demo hesapta gerçek emirle uygulayacak.")
        except Exception as e:
            L.append(f"❌ Hata: {e}")
            if D.log:
                L.append("Ayrıntı: " + " | ".join(D.log[-3:]))
    txt = "\n".join(L)
    print(txt)
    chat = os.environ.get("TELEGRAM_CHAT_ID")
    for f in ("futures.json", "portfolio.json"):
        p = os.path.join(ROOT, "state", f)
        if not chat and os.path.exists(p):
            chat = json.load(open(p, encoding="utf-8")).get("chat_id")
    telegram.send(chat, txt)


if __name__ == "__main__":
    main()
