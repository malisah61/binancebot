"""Günlük (1d) grafik formasyonları — ileriye bakmadan (her olay, oluştuğu günün kapanışında bilinir).

Olay listesi (dir: +1 yükseliş beklentisi, -1 düşüş):
  OBO  (omuz-baş-omuz, -1) / TOBO (ters omuz-baş-omuz, +1): boyun çizgisi kapanışla kırılınca
  İKİLİ TEPE (-1) / İKİLİ DİP (+1): aradaki dip/tepe kapanışla kırılınca
  YUTAN (±1), ÇEKİÇ (+1), KAYAN YILDIZ (-1), SABAH YILDIZI (+1), AKŞAM YILDIZI (-1) — "bağlamlı" sürümleri:
      yükseliş mumu son 30 günün dibine 1 ATR yakınken, düşüş mumu tepesine yakınken
  BOĞA TUZAĞI (-1): 20 günlük tepenin üstünde kapanış, ertesi gün tekrar altında (sahte kırılım)
  AYI TUZAĞI (+1): 20 günlük dibin altında kapanış, ertesi gün tekrar üstünde
  KIRILIM (±1): 20 günlük tepe/dip kapanışla kırıldı ve ertesi gün de tuttu (tuzakların karşılaştırması)
  KARAKTER DEĞİŞİMİ (CHoCH, ±1): yükselen tepe/dip yapısında son dibin kapanışla kırılması (ve tersi)
Her olayda: stop (formasyonun ötesi) ve hedef (ölçülü hareket / 2R) önerisi.
"""
from __future__ import annotations

import numpy as np

NAMES = {"OBO": "Omuz-baş-omuz", "TOBO": "Ters omuz-baş-omuz", "IKILI_TEPE": "İkili tepe", "IKILI_DIP": "İkili dip",
         "YUTAN_BOGA": "Yükseliş yutan mum", "YUTAN_AYI": "Düşüş yutan mum", "CEKIC": "Çekiç", "KAYAN_YILDIZ": "Kayan yıldız",
         "SABAH_YILDIZI": "Sabah yıldızı", "AKSAM_YILDIZI": "Akşam yıldızı", "BOGA_TUZAGI": "Boğa tuzağı (sahte yukarı kırılım)",
         "AYI_TUZAGI": "Ayı tuzağı (sahte aşağı kırılım)", "KIRILIM_YUKARI": "Gerçek yukarı kırılım", "KIRILIM_ASAGI": "Gerçek aşağı kırılım",
         "CHOCH_BOGA": "Trend dönüşü (düşüş yapısı kırıldı)", "CHOCH_AYI": "Trend dönüşü (yükseliş yapısı kırıldı)"}
CANDLES = {"YUTAN_BOGA", "YUTAN_AYI", "CEKIC", "KAYAN_YILDIZ", "SABAH_YILDIZI", "AKSAM_YILDIZI"}


def atr(h, l, c, n=14):
    tr = np.maximum(h - l, np.maximum(np.abs(h - np.r_[c[0], c[:-1]]), np.abs(l - np.r_[c[0], c[:-1]])))
    out = np.empty_like(tr)
    out[0] = tr[0]
    for i in range(1, len(tr)):
        out[i] = out[i - 1] + (tr[i] - out[i - 1]) / n
    return out


def pivots(h, l, k=3):
    """(index, fiyat, tür) — pivot j, j+k gününde onaylanır."""
    P = []
    n = len(h)
    for j in range(k, n - k):
        # eşit tepelerde yalnız ilki pivot olsun (solundakilerden kesin büyük, sağındakilerden büyük-eşit)
        if h[j] > h[j - k:j].max() and h[j] >= h[j + 1:j + k + 1].max():
            P.append((j, h[j], "H"))
        if l[j] < l[j - k:j].min() and l[j] <= l[j + 1:j + k + 1].min():
            P.append((j, l[j], "L"))
    return P


def detect(o, h, l, c, k=3):
    """Tüm olaylar: [{'i', 'type', 'dir', 'stop', 'target', 'info'}] (i = olayın bilindiği gün)."""
    n = len(c)
    A = atr(h, l, c)
    ev = []
    P = pivots(h, l, k)
    by_conf = {}  # onay günü -> pivotlar
    for p in P:
        by_conf.setdefault(p[0] + k, []).append(p)
    highs, lows = [], []
    pending = []  # boyun çizgisi kırılımı bekleyen formasyonlar
    body = np.abs(c - o)
    rng = np.maximum(h - l, 1e-12)
    for i in range(n):
        for p in by_conf.get(i, []):
            (highs if p[2] == "H" else lows).append(p)
            # --- yeni pivotla formasyon adayı
            if p[2] == "H" and len(highs) >= 3:
                (p1, a, _), (p2, b, _), (p3, cc, _) = highs[-3:]
                lo1 = [x for x in lows if p1 < x[0] < p2]
                lo2 = [x for x in lows if p2 < x[0] < p3]
                if b > a and b > cc and lo1 and lo2 and 8 <= p3 - p1 <= 150:
                    n1 = min(lo1, key=lambda x: x[1]); n2 = min(lo2, key=lambda x: x[1])
                    height = b - max(n1[1], n2[1])
                    if abs(a - cc) <= 0.35 * height and b - max(a, cc) >= 0.5 * A[p2] and height > 1.5 * A[p2]:
                        pending.append({"type": "OBO", "dir": -1, "neck": (n1[0], n1[1], n2[0], n2[1]), "head": b, "stop": cc,
                                        "height": height, "until": i + 30, "info": f"sol omuz {a:.6g}, baş {b:.6g}, sağ omuz {cc:.6g}"})
            if p[2] == "L" and len(lows) >= 3:
                (p1, a, _), (p2, b, _), (p3, cc, _) = lows[-3:]
                hi1 = [x for x in highs if p1 < x[0] < p2]
                hi2 = [x for x in highs if p2 < x[0] < p3]
                if b < a and b < cc and hi1 and hi2 and 8 <= p3 - p1 <= 150:
                    n1 = max(hi1, key=lambda x: x[1]); n2 = max(hi2, key=lambda x: x[1])
                    height = min(n1[1], n2[1]) - b
                    if abs(a - cc) <= 0.35 * height and min(a, cc) - b >= 0.5 * A[p2] and height > 1.5 * A[p2]:
                        pending.append({"type": "TOBO", "dir": 1, "neck": (n1[0], n1[1], n2[0], n2[1]), "head": b, "stop": cc,
                                        "height": height, "until": i + 30, "info": f"sol omuz {a:.6g}, baş {b:.6g}, sağ omuz {cc:.6g}"})
            if p[2] == "H" and len(highs) >= 2:
                (p1, a, _), (p2, b, _) = highs[-2:]
                mid = [x for x in lows if p1 < x[0] < p2]
                if mid and 10 <= p2 - p1 <= 90 and abs(a - b) <= 0.6 * A[p2]:
                    t = min(mid, key=lambda x: x[1])
                    if max(a, b) - t[1] >= 2 * A[p2]:
                        pending.append({"type": "IKILI_TEPE", "dir": -1, "level": t[1], "stop": max(a, b), "height": max(a, b) - t[1],
                                        "until": i + 30, "info": f"tepeler {a:.6g} / {b:.6g}, boyun {t[1]:.6g}"})
            if p[2] == "L" and len(lows) >= 2:
                (p1, a, _), (p2, b, _) = lows[-2:]
                mid = [x for x in highs if p1 < x[0] < p2]
                if mid and 10 <= p2 - p1 <= 90 and abs(a - b) <= 0.6 * A[p2]:
                    t = max(mid, key=lambda x: x[1])
                    if t[1] - min(a, b) >= 2 * A[p2]:
                        pending.append({"type": "IKILI_DIP", "dir": 1, "level": t[1], "stop": min(a, b), "height": t[1] - min(a, b),
                                        "until": i + 30, "info": f"dipler {a:.6g} / {b:.6g}, boyun {t[1]:.6g}"})
        # --- bekleyen formasyonların kapanışla teyidi
        keep = []
        for f in pending:
            if i > f["until"]:
                continue
            if "neck" in f:
                x1, y1, x2, y2 = f["neck"]
                lvl = y1 + (y2 - y1) * (i - x1) / max(x2 - x1, 1)
                lvl_prev = y1 + (y2 - y1) * (i - 1 - x1) / max(x2 - x1, 1)
            else:
                lvl = lvl_prev = f["level"]
            d = f["dir"]
            if i > 0 and ((d < 0 and c[i] < lvl <= c[i - 1]) or (d > 0 and c[i] > lvl >= c[i - 1])):
                if (d < 0 and f["stop"] > c[i]) or (d > 0 and f["stop"] < c[i]):
                    ev.append({"i": i, "type": f["type"], "dir": d, "stop": float(f["stop"] + d * -0.25 * A[i]),
                               "target": float(lvl + d * f["height"]), "info": f["info"] + f", boyun {lvl:.6g} kırıldı"})
                continue
            if (d < 0 and c[i] > f["stop"]) or (d > 0 and c[i] < f["stop"]):
                continue  # formasyon bozuldu
            keep.append(f)
        pending = keep

        if i < 30:
            continue
        lo30, hi30 = l[i - 29:i + 1].min(), h[i - 29:i + 1].max()
        near_low = c[i] - lo30 <= 1.0 * A[i] or l[i] <= lo30 + 0.3 * A[i]
        near_high = hi30 - c[i] <= 1.0 * A[i] or h[i] >= hi30 - 0.3 * A[i]
        uw, lw = h[i] - max(o[i], c[i]), min(o[i], c[i]) - l[i]

        def cev(t, d, stop):
            risk = abs(c[i] - stop)
            if risk > 0:
                ev.append({"i": i, "type": t, "dir": d, "stop": float(stop), "target": float(c[i] + d * 2 * risk), "info": "", "context": True})

        # --- mum formasyonları (yalnız bağlamda: dipte yükseliş, tepede düşüş)
        if near_low and c[i - 1] < o[i - 1] and c[i] > o[i] and o[i] <= c[i - 1] and c[i] >= o[i - 1] and body[i] > body[i - 1]:
            cev("YUTAN_BOGA", 1, min(l[i], l[i - 1]) - 0.2 * A[i])
        if near_high and c[i - 1] > o[i - 1] and c[i] < o[i] and o[i] >= c[i - 1] and c[i] <= o[i - 1] and body[i] > body[i - 1]:
            cev("YUTAN_AYI", -1, max(h[i], h[i - 1]) + 0.2 * A[i])
        if near_low and lw >= 0.6 * rng[i] and (c[i] - l[i]) >= 0.7 * rng[i] and rng[i] >= 0.8 * A[i]:
            cev("CEKIC", 1, l[i] - 0.2 * A[i])
        if near_high and uw >= 0.6 * rng[i] and (h[i] - c[i]) >= 0.7 * rng[i] and rng[i] >= 0.8 * A[i]:
            cev("KAYAN_YILDIZ", -1, h[i] + 0.2 * A[i])
        if near_low and o[i - 2] - c[i - 2] > 0.6 * A[i] and body[i - 1] < 0.3 * A[i] and c[i] > o[i] and c[i] > (o[i - 2] + c[i - 2]) / 2:
            cev("SABAH_YILDIZI", 1, min(l[i - 2:i + 1]) - 0.2 * A[i])
        if near_high and c[i - 2] - o[i - 2] > 0.6 * A[i] and body[i - 1] < 0.3 * A[i] and c[i] < o[i] and c[i] < (o[i - 2] + c[i - 2]) / 2:
            cev("AKSAM_YILDIZI", -1, max(h[i - 2:i + 1]) + 0.2 * A[i])

        # --- sahte / gerçek kırılımlar (20 günlük seviye, dünkü kapanışla kırılmış)
        if i >= 23:
            hh = h[i - 21:i - 1].max()
            ll = l[i - 21:i - 1].min()
            if c[i - 1] > hh >= c[i - 2]:  # yalnız ilk kırılım günü (trend boyunca her gün tekrar sayılmasın)
                if c[i] < hh:
                    ev.append({"i": i, "type": "BOGA_TUZAGI", "dir": -1, "stop": float(max(h[i], h[i - 1]) + 0.2 * A[i]),
                               "target": float(ll + (hh - ll) * 0.5), "info": f"{hh:.6g} üstü kırılım geri alındı"})
                else:
                    ev.append({"i": i, "type": "KIRILIM_YUKARI", "dir": 1, "stop": float(hh - 1.0 * A[i]),
                               "target": float(c[i] + (hh - ll)), "info": f"{hh:.6g} üstü 2 gün kapanış"})
            if c[i - 1] < ll <= c[i - 2]:
                if c[i] > ll:
                    ev.append({"i": i, "type": "AYI_TUZAGI", "dir": 1, "stop": float(min(l[i], l[i - 1]) - 0.2 * A[i]),
                               "target": float(ll + (hh - ll) * 0.5), "info": f"{ll:.6g} altı kırılım geri alındı"})
                else:
                    ev.append({"i": i, "type": "KIRILIM_ASAGI", "dir": -1, "stop": float(ll + 1.0 * A[i]),
                               "target": float(c[i] - (hh - ll)), "info": f"{ll:.6g} altı 2 gün kapanış"})

        # --- piyasa yapısı: karakter değişimi (CHoCH)
        if len(highs) >= 2 and len(lows) >= 2:
            (_, h1, _), (_, h2, _) = highs[-2:]
            (_, l1, _), (_, l2, _) = lows[-2:]
            if h2 > h1 and l2 > l1 and c[i] < l2 <= c[i - 1]:
                ev.append({"i": i, "type": "CHOCH_AYI", "dir": -1, "stop": float(h2), "target": float(c[i] - (h2 - l2)),
                           "info": f"yükselen yapı: son dip {l2:.6g} kırıldı"})
            if h2 < h1 and l2 < l1 and c[i] > h2 >= c[i - 1]:
                ev.append({"i": i, "type": "CHOCH_BOGA", "dir": 1, "stop": float(l2), "target": float(c[i] + (h2 - l2)),
                           "info": f"düşen yapı: son tepe {h2:.6g} kırıldı"})
    return ev, A


def trade(h, l, c, e_i, d, stop, target, hold=30, fee=0.001):
    """Olay kapanışında gir; önce stop mu hedef mi? (aynı gün ikisi: stop). Dönen: (R, gün, sonuç)."""
    e = c[e_i]
    risk = abs(e - stop) / e
    if risk <= 0 or (d > 0 and stop >= e) or (d < 0 and stop <= e) or (d > 0 and target <= e) or (d < 0 and target >= e):
        return None
    n = len(c)
    for j in range(e_i + 1, min(n, e_i + 1 + hold)):
        if (d > 0 and l[j] <= stop) or (d < 0 and h[j] >= stop):
            return -1 - fee / risk, j - e_i, "stop"
        if (d > 0 and h[j] >= target) or (d < 0 and l[j] <= target):
            return abs(target / e - 1) / risk - fee / risk, j - e_i, "hedef"
    j = min(n - 1, e_i + hold)
    if j <= e_i:
        return None
    return d * (c[j] / e - 1) / risk - fee / risk, j - e_i, "süre"


def levels(h, l, c, v, tq=None, qv=None, look=180, bins=48):
    """Destek/direnç: hacim profili (POC, yüksek hacim düğümleri) + alıcıların toplandığı bölge (agresif alım ağırlıklı)."""
    m = min(look, len(c))
    hh, ll, cc, vv = h[-m:], l[-m:], c[-m:], v[-m:]
    lo, hi = ll.min(), hh.max()
    if hi <= lo:
        return {}
    tp = (hh + ll + cc) / 3
    idx = np.clip(((tp - lo) / (hi - lo) * bins).astype(int), 0, bins - 1)
    vol = np.zeros(bins); np.add.at(vol, idx, vv)
    buy = np.zeros(bins)
    if tq is not None and qv is not None:
        r = np.where(qv[-m:] > 0, tq[-m:] / np.maximum(qv[-m:], 1e-12), 0.5)
        np.add.at(buy, idx, vv * r)
    cen = lo + (np.arange(bins) + 0.5) * (hi - lo) / bins
    p = c[-1]
    order = np.argsort(-vol)
    hvn = [float(cen[k]) for k in order[:6]]
    poc = float(cen[order[0]])
    sup = sorted([x for x in hvn if x < p], reverse=True)[:3]
    res = sorted([x for x in hvn if x > p])[:3]
    acc = None
    if buy.any():
        ratio = np.where(vol > 0, buy / np.maximum(vol, 1e-12), 0)
        score = ratio * (vol / vol.max())
        k = int(np.argmax(np.where(cen < p, score, -1)))
        if cen[k] < p:
            acc = {"price": float(cen[k]), "buy_ratio": round(float(ratio[k]) * 100, 1)}
    y = min(365, len(c))
    return {"poc": poc, "support": sup, "resistance": res, "accumulation": acc,
            "range_hi": float(h[-y:].max()), "range_lo": float(l[-y:].min()),
            "range_pos": round(float((p - l[-y:].min()) / max(h[-y:].max() - l[-y:].min(), 1e-12)), 3),
            "from_hi": round(float(p / h[-y:].max() - 1) * 100, 1), "from_lo": round(float(p / l[-y:].min() - 1) * 100, 1)}


def trend_state(h, l, c):
    """Günlük trend: EMA50/200 + son pivot yapısı."""
    def ema(x, n):
        a = 2 / (n + 1); o = np.empty_like(x); o[0] = x[0]
        for i in range(1, len(x)):
            o[i] = a * x[i] + (1 - a) * o[i - 1]
        return o
    e50, e200 = ema(c, 50), ema(c, 200)
    P = pivots(h, l, 3)
    H = [p[1] for p in P if p[2] == "H"][-2:]
    L = [p[1] for p in P if p[2] == "L"][-2:]
    struct = "yatay"
    if len(H) == 2 and len(L) == 2:
        if H[1] > H[0] and L[1] > L[0]:
            struct = "yükselen tepeler/dipler (yükseliş)"
        elif H[1] < H[0] and L[1] < L[0]:
            struct = "alçalan tepeler/dipler (düşüş)"
    return {"ema50": float(e50[-1]), "ema200": float(e200[-1]), "above50": bool(c[-1] > e50[-1]), "above200": bool(c[-1] > e200[-1]),
            "structure": struct}
