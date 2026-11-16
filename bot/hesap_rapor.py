"""Salt-okur hesap raporu (Actions'tan): DEMO hesabın açık pozisyonları, bekleyen emirleri, son 24 saatte kapanan işlemleri.
Gerçek hesap Actions'tan okunamaz (ABD engeli); onun durumu sunucudan Telegram'a gelir (/gercek)."""
import json, os, sys, time
from collections import defaultdict
sys.path.insert(0, os.path.dirname(__file__))
import executor, telegram  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    D = executor.Demo()
    now = int(time.time() * 1000)
    eq, av = D.balance()
    L = [f"🧪 <b>Demo hesap</b> — bakiye {eq:.2f} USDT (kullanılabilir {av:.2f})"]
    pos = [p for p in D.req("GET", "/fapi/v2/positionRisk") if float(p["positionAmt"]) != 0]
    L.append(f"\n<b>Açık pozisyonlar ({len(pos)})</b>")
    for p in pos:
        amt = float(p["positionAmt"]); ep = float(p["entryPrice"]); mk = float(p["markPrice"]); up = float(p["unRealizedProfit"])
        L.append(f"{'LONG' if amt > 0 else 'SHORT'} {p['symbol'].replace('USDT', '')} {abs(amt):g} @ {ep:g} → {mk:g} · {up:+.2f}$ ({p.get('leverage')}x)")
    oo = D.req("GET", "/fapi/v1/openOrders")
    lim = [o for o in oo if o["type"] == "LIMIT"]
    L.append(f"\n<b>Bekleyen limit emirler ({len(lim)})</b>")
    for o in lim:
        L.append(f"{'ALIŞ' if o['side'] == 'BUY' else 'SATIŞ'} {o['symbol'].replace('USDT', '')} {float(o['origQty']):g} @ {float(o['price']):g} · {time.strftime('%d.%m %H:%M', time.gmtime(o['time'] / 1000 + 3 * 3600))}")
    inc = D.req("GET", "/fapi/v1/income", {"startTime": now - 24 * 3600_000, "limit": 1000})
    by = defaultdict(float)
    for x in inc:
        if x["incomeType"] in ("REALIZED_PNL", "COMMISSION", "FUNDING_FEE"):
            by[x["symbol"]] += float(x["income"])
    L.append(f"\n<b>Son 24 saat gerçekleşen kâr/zarar</b> (komisyon + funding dahil): {sum(by.values()):+.2f}$")
    for s, v in sorted(by.items(), key=lambda kv: kv[1]):
        if s:
            L.append(f"{s.replace('USDT', '')}: {v:+.2f}$")
    txt = "\n".join(L)
    print(txt)
    if os.environ.get("RAPOR_TG") == "1":
        chat = os.environ.get("TELEGRAM_CHAT_ID") or json.load(open(os.path.join(ROOT, "state", "futures.json"))).get("chat_id")
        telegram.send(chat, txt)


if __name__ == "__main__":
    main()
