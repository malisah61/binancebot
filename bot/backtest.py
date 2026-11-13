"""Geriye dönük test: skor gerçekten işe yarıyor mu?

Hacimce ilk 40 coinin son ~1000 saatlik verisinde, her 4 saatte bir skoru
o anki veriyle hesaplar ve sonraki 12 saatteki fiyat değişimini ölçer.
Skor aralıklarına göre: kaç kez yükseldi, ortalama getiri ne oldu?
Sonuç state/backtest.json'a yazılır ve Telegram'a gönderilir.
"""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))
import numpy as np  # noqa: E402
import binance  # noqa: E402
import telegram  # noqa: E402
from analysis import analyze  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUCKETS = [(0, 35, "≤35 (güçlü düşüş)"), (35, 45, "35-45"), (45, 55, "45-55 (nötr)"), (55, 65, "55-65"), (65, 101, "≥65 (güçlü yükseliş)")]
HORIZON, STEP, WARM = 12, 4, 300


def run(n_coins=40):
    rows = []
    syms = [t["symbol"] for t in binance.top_usdt(n_coins)]
    for s in syms:
        try:
            k = binance.klines(s, "1h", 1000)[:-1]  # son (açık) mumu at
        except Exception as e:
            print("hata", s, e)
            continue
        c = [x["c"] for x in k]
        for i in range(WARM, len(k) - HORIZON, STEP):
            a = analyze(k[max(0, i - 600):i])
            rows.append((a["score"], c[i - 1 + HORIZON] / c[i - 1] - 1))
        print(s, len(rows))
    return rows


def report(rows):
    sc = np.array([r[0] for r in rows])
    fw = np.array([r[1] for r in rows])
    base = fw.mean()
    out = []
    for lo, hi, name in BUCKETS:
        m = (sc >= lo) & (sc < hi)
        if m.sum() == 0:
            continue
        out.append({"aralik": name, "n": int(m.sum()), "yukselme_orani": round(float((fw[m] > 0).mean()) * 100, 1),
                    "ort_getiri": round(float(fw[m].mean()) * 100, 3)})
    corr = float(np.corrcoef(sc, fw)[0, 1]) if len(rows) > 10 else 0.0
    return {"time": int(time.time() * 1000), "ornek": len(rows), "ufuk_saat": HORIZON,
            "genel_ort_getiri": round(float(base) * 100, 3), "genel_yukselme": round(float((fw > 0).mean()) * 100, 1),
            "korelasyon": round(corr, 3), "araliklar": out}


def main():
    res = report(run())
    os.makedirs(os.path.join(ROOT, "state"), exist_ok=True)
    with open(os.path.join(ROOT, "state", "backtest.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    lines = [f"🧪 <b>Geriye dönük test</b> ({res['ornek']} örnek, sonraki {HORIZON} saat)",
             f"Genel: %{res['genel_yukselme']} yükseldi, ort. {res['genel_ort_getiri']:+.3f}%",
             f"Skor–getiri korelasyonu: {res['korelasyon']:+.3f}"]
    lines += [f"• Skor {b['aralik']}: {b['n']} kez, %{b['yukselme_orani']} yükseldi, ort. {b['ort_getiri']:+.3f}%"
              for b in res["araliklar"]]
    print("\n".join(lines))
    pf_path = os.path.join(ROOT, "state", "portfolio.json")
    chat = os.environ.get("TELEGRAM_CHAT_ID")
    if not chat and os.path.exists(pf_path):
        chat = json.load(open(pf_path, encoding="utf-8")).get("chat_id")
    telegram.send(chat, "\n".join(lines))


if __name__ == "__main__":
    main()
