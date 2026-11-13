"""Canlı botun işlemlerini inceler: hangi kriterle açıldı, hangileri stop oldu, neden.
Kullanım: python bot/live_review.py [saat]   (varsayılan: tüm işlemler; saat verilirse son X saat)
Çıktı: markdown (stdout) + state/live_review.json
"""
from __future__ import annotations

import json
import os
import sys
import time
from collections import Counter, defaultdict

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMPS = ["trend", "momentum", "volume", "smc", "vwap"]
NM = {"trend": "Trend", "momentum": "Momentum", "volume": "Hacim", "smc": "FVG+Likidite", "vwap": "VWAP"}


def pct(a):
    return round(100 * float(np.mean(a)), 1) if len(a) else None


def main():
    hours = float(sys.argv[1]) if len(sys.argv) > 1 else None
    st = json.load(open(os.path.join(ROOT, "state", "futures.json"), encoding="utf-8"))
    since = (time.time() - hours * 3600) * 1000 if hours else 0
    cl = [dict(x, acc=k) for k, a in st["accounts"].items() for x in a["closed"] if x["closed"] >= since]
    op = [dict(x, acc=k) for k, a in st["accounts"].items() for x in a["positions"]]
    # 5x hesaplarını esas al (10x aynı işlemler, sadece kaldıraç farkı)
    c5 = [x for x in cl if x["acc"].endswith("_5x")]
    L = [f"## Canlı işlem incelemesi ({'son %g saat' % hours if hours else 'başlangıçtan beri'})", ""]
    L.append("| Hesap | Varlık | Açık | Kapanan | Kazanma | Ort. ROE | SL | TP2 | TP1→BE | Süre | Likidasyon |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for k, a in st["accounts"].items():
        x = [y for y in cl if y["acc"] == k]
        r = Counter(y["reason"] for y in x)
        L.append(f"| {k} | {a['equity']:.0f}$ | {len(a['positions'])} | {len(x)} | %{pct([y['pnl'] > 0 for y in x]) or '-'} | "
                 f"{(np.mean([y['roe'] for y in x]) if x else 0):+.1f}% | {r.get('SL', 0)} | {r.get('TP2', 0)} | {r.get('TP1→BE', 0)} | {r.get('SÜRE', 0)} | {r.get('LİKİDASYON', 0)} |")
    out = {"n": len(c5)}
    if c5:
        L += ["", "### 5x hesaplarında kırılım (10x aynı işlemlerin kaldıraçlı hali)", ""]
        for name, f in (("LONG", lambda y: y["dir"] > 0), ("SHORT", lambda y: y["dir"] < 0)):
            g = [y for y in c5 if f(y)]
            if g:
                L.append(f"- {name}: {len(g)} işlem, kazanma %{pct([y['pnl'] > 0 for y in g])}, ort R {np.mean([y['R'] for y in g]):+.2f}")
        # bileşen uyumu
        L += ["", "| Bileşen | Aynı yöndeyken kazanma (n) | Ters/nötrken kazanma (n) |", "|---|---|---|"]
        for k in COMPS:
            ag = [y for y in c5 if (y.get("snap") or {}).get(k) is not None and y["snap"][k] * y["dir"] > 0.2]
            ds = [y for y in c5 if (y.get("snap") or {}).get(k) is not None and y["snap"][k] * y["dir"] <= 0.2]
            L.append(f"| {NM[k]} | %{pct([y['pnl'] > 0 for y in ag]) or '-'} ({len(ag)}) | %{pct([y['pnl'] > 0 for y in ds]) or '-'} ({len(ds)}) |")
        # giriş anındaki uzama
        ext = [y for y in c5 if (y.get("snap") or {}).get("f_vwap_atr") is not None]
        if ext:
            far = [y for y in ext if abs(y["snap"]["f_vwap_atr"]) > 2]
            near = [y for y in ext if abs(y["snap"]["f_vwap_atr"]) <= 2]
            L.append(f"\nGirişte fiyat VWAP'tan >2 ATR uzaktaysa kazanma %{pct([y['pnl'] > 0 for y in far]) or '-'} ({len(far)}), yakınsa %{pct([y['pnl'] > 0 for y in near]) or '-'} ({len(near)})")
        else:
            vw = [y for y in c5 if (y.get("snap") or {}).get("vwap") is not None]
            far = [y for y in vw if abs(y["snap"]["vwap"]) > 0.9]
            L.append(f"\nGirişte VWAP bileşeni |>0.9| (fiyat VWAP'tan çok uzak) iken kazanma %{pct([y['pnl'] > 0 for y in far]) or '-'} ({len(far)})")
        # kümelenme: aynı hesap, aynı açılış zamanı
        grp = defaultdict(list)
        for y in c5:
            grp[(y["acc"], y["opened"])].append(y)
        big = [g for g in grp.values() if len(g) >= 3]
        if big:
            L.append(f"Aynı mumda 3+ işlem açılan küme: {len(big)} küme, {sum(len(g) for g in big)} işlem, kazanma %{pct([y['pnl'] > 0 for g in big for y in g])}")
        # stop olanlarda süre
        sl = [y for y in c5 if y["reason"] in ("SL", "LİKİDASYON")]
        if sl:
            dur = [(y["closed"] - y["opened"]) / 60000 for y in sl]
            L.append(f"Stop olan işlemlerin ortalama ömrü {np.mean(dur):.0f} dk (medyan {np.median(dur):.0f} dk)")
        coins = Counter(y["sym"] for y in sl)
        if coins:
            L.append("En çok stop olan coinler: " + ", ".join(f"{s.replace('USDT', '')} {n}" for s, n in coins.most_common(6)))
    if st.get("strategy"):
        L += ["", "Aktif stratejiler: " + "; ".join(f"{tf}: {n}" for tf, n in st["strategy"].items())]
    L.append(f"\nAçık pozisyon: {len(op)} (LONG {sum(1 for y in op if y['dir'] > 0)}, SHORT {sum(1 for y in op if y['dir'] < 0)})")
    md = "\n".join(L)
    with open(os.path.join(ROOT, "state", "live_review.json"), "w", encoding="utf-8") as f:
        json.dump({"time": int(time.time() * 1000), "closed": len(cl), "open": len(op), "md": md}, f, ensure_ascii=False)
    print(md)


if __name__ == "__main__":
    main()
