# V5 Araştırma Raporu — 23.11.2026 10:56 UTC

40 coin · değerlendirme 25.08.2026'dan bugüne (90 gün) · eğitim/TEST ayrımı 27.10.2026

## 1. Mevcut model: kaldıraçlı işlem sonuçları (tüm dönem)

| Periyot | Kaldıraç | İşlem | Kazanma | Ort. ROE | PF | Ort. R | Likidasyon | 100$ marjla net | Maks. DD |
|---|---|---|---|---|---|---|---|---|---|
| 15m | 5x | 28971 | %49.7 | %-0.53 | 0.83 | 0.002 | 0 | -15366.0$ | 16049.0$ |
| 15m | 10x | 28973 | %49.7 | %-1.05 | 0.83 | 0.002 | 6 | -30559.0$ | 32163.0$ |
| 30m | 5x | 14230 | %49.9 | %-0.57 | 0.87 | 0.002 | 0 | -8163.0$ | 8383.0$ |
| 30m | 10x | 14232 | %49.9 | %-1.12 | 0.87 | 0.003 | 19 | -15918.0$ | 16617.0$ |
| 1h | 5x | 6987 | %49.5 | %-0.54 | 0.91 | 0.003 | 0 | -3805.0$ | 4477.0$ |
| 1h | 10x | 7000 | %49.4 | %-1.14 | 0.91 | 0.003 | 26 | -7952.0$ | 9315.0$ |
| 4h | 5x | 1838 | %51.1 | %0.31 | 1.03 | 0.044 | 1 | 572.0$ | 3292.0$ |
| 4h | 10x | 1845 | %51.0 | %0.56 | 1.02 | 0.044 | 33 | 1033.0$ | 6774.0$ |

PF = kâr faktörü (toplam kazanç / toplam kayıp, 1 üstü kârlı). R = risk birimi (stop mesafesi).

## 2. Göstergelerin doğruluğu (TEST dönemi)

### 15m

| Bileşen | IC | İsabet | ↑ dediğinde yükseldi | ↓ dediğinde düştü | İşlemde aynı yöndeyken kazanma | Ters yöndeyken kazanma |
|---|---|---|---|---|---|---|
| Trend | -0.088 | %46.2 | %39.7 | %50.0 | %50.5 (6693) | %57.0 (446) |
| Momentum | -0.032 | %47.0 | %43.7 | %50.8 | %50.6 (5738) | %52.2 (870) |
| Open Interest | -0.019 | %46.0 | %45.7 | %46.7 | %54.3 (2455) | %47.4 (329) |
| Hacim | -0.023 | %48.8 | %44.9 | %51.0 | %52.6 (4791) | %48.1 (648) |
| Funding+L/S | -0.012 | %47.2 | %46.6 | %55.4 | %46.7 (2290) | %54.9 (2821) |
| FVG+Likidite avı | -0.008 | %51.5 | %48.0 | %55.7 | %50.7 (3186) | %52.1 (2566) |
| VWAP | -0.054 | %46.9 | %41.4 | %51.0 | %51.1 (7258) | %49.5 (384) |

Ham göstergeler (IC, büyükten küçüğe): EMA dizilimi -0.090, Üst periyot trendi -0.088, Fiyat>EMA200 -0.086, RSI -0.070, VWAP üstü/altı -0.061, Z-Score -0.054, Funding -0.047, FVG -0.042, Bollinger sıkışma -0.027, RVOL -0.025

### 30m

| Bileşen | IC | İsabet | ↑ dediğinde yükseldi | ↓ dediğinde düştü | İşlemde aynı yöndeyken kazanma | Ters yöndeyken kazanma |
|---|---|---|---|---|---|---|
| Trend | -0.102 | %47.7 | %37.9 | %51.8 | %47.2 (3204) | %56.0 (332) |
| Momentum | -0.054 | %46.0 | %40.9 | %51.7 | %48.9 (2979) | %50.5 (305) |
| Open Interest | -0.044 | %45.1 | %45.0 | %45.2 | %48.9 (1760) | %44.2 (206) |
| Hacim | -0.076 | %46.3 | %40.8 | %48.6 | %48.1 (2397) | %46.5 (202) |
| Funding+L/S | -0.018 | %46.0 | %45.3 | %55.8 | %46.5 (1038) | %49.4 (1543) |
| FVG+Likidite avı | 0.002 | %52.4 | %47.9 | %58.3 | %49.3 (1483) | %48.9 (1373) |
| VWAP | -0.061 | %46.7 | %39.6 | %51.9 | %47.9 (3486) | %47.3 (146) |

Ham göstergeler (IC, büyükten küçüğe): Üst periyot trendi -0.097, Fiyat>EMA200 -0.097, RSI -0.090, EMA dizilimi -0.083, Z-Score -0.079, VWAP üstü/altı -0.065, OBV yönü -0.060, FVG -0.057, MACD yönü -0.046, Likidite avı +0.041

### 1h

| Bileşen | IC | İsabet | ↑ dediğinde yükseldi | ↓ dediğinde düştü | İşlemde aynı yöndeyken kazanma | Ters yöndeyken kazanma |
|---|---|---|---|---|---|---|
| Trend | -0.098 | %50.3 | %34.5 | %54.3 | %48.8 (1576) | %52.9 (189) |
| Momentum | -0.042 | %46.7 | %39.0 | %55.0 | %48.9 (1549) | %53.0 (100) |
| Open Interest | -0.082 | %42.6 | %38.1 | %48.1 | %46.4 (1203) | %55.8 (138) |
| Hacim | -0.067 | %49.0 | %35.0 | %52.6 | %46.4 (1182) | %51.4 (70) |
| Funding+L/S | -0.02 | %44.5 | %43.6 | %56.9 | %41.4 (481) | %51.0 (777) |
| FVG+Likidite avı | 0.02 | %52.0 | %44.0 | %64.5 | %49.6 (789) | %45.8 (671) |
| VWAP | -0.044 | %47.9 | %37.9 | %54.6 | %47.1 (1640) | %63.4 (112) |

Ham göstergeler (IC, büyükten küçüğe): Üst periyot trendi -0.097, RSI -0.090, Fiyat>EMA200 -0.088, EMA dizilimi -0.085, OI değişimi -0.075, Z-Score -0.060, OI rejimi +0.052, Taker alım -0.052, VWAP üstü/altı -0.043, Likidite avı +0.035

### 4h

| Bileşen | IC | İsabet | ↑ dediğinde yükseldi | ↓ dediğinde düştü | İşlemde aynı yöndeyken kazanma | Ters yöndeyken kazanma |
|---|---|---|---|---|---|---|
| Trend | -0.073 | %56.7 | %31.9 | %59.3 | %56.7 (439) | %25.0 (44) |
| Momentum | -0.133 | %43.3 | %31.3 | %53.5 | %50.7 (373) | %74.1 (27) |
| Open Interest | -0.12 | %45.5 | %33.3 | %52.9 | %52.5 (375) | %52.2 (46) |
| Hacim | -0.178 | %46.4 | %30.2 | %48.4 | %54.9 (275) | %63.6 (11) |
| Funding+L/S | -0.01 | %40.8 | %39.3 | %61.0 | %37.9 (87) | %57.7 (208) |
| FVG+Likidite avı | 0.06 | %55.1 | %48.5 | %70.1 | %58.2 (225) | %44.3 (158) |
| VWAP | -0.184 | %47.1 | %26.0 | %53.9 | %49.0 (400) | %64.7 (17) |

Ham göstergeler (IC, büyükten küçüğe): Z-Score -0.185, RSI -0.177, MACD yönü -0.168, VWAP üstü/altı -0.150, OI değişimi -0.139, Likidite avı +0.116, OI rejimi +0.100, OBV yönü -0.085, RVOL +0.082, Taker alım -0.079

## 3. Öğrenme: yeni ağırlıklar (eğitimde bulundu, TEST'te sınandı)

| Periyot | Yöntem | Eşik | Mevcut model TEST ort. R / kazanma | Yeni model TEST ort. R / kazanma | Karar |
|---|---|---|---|---|---|
| 15m | mevcut | 74/26 | 0.025 / %51.3 (8551) | -0.023 / %49.0 (3174) | ❌ mevcut kalır |
| 30m | mevcut | 55/45 | -0.009 / %49.0 (4213) | -0.017 / %48.8 (4412) | ❌ mevcut kalır |
| 1h | IC+ | 74/26 | -0.006 / %48.7 (2100) | -0.164 / %41.9 (248) | ❌ mevcut kalır |
| 4h | IC+ | 55/45 | 0.122 / %52.4 (532) | 0.118 / %57.3 (555) | ❌ mevcut kalır |

Ağırlıklar:
- 15m: Trend 20, Momentum 18, Open Interest 15, Hacim 10, Funding+L/S 10, FVG+Likidite avı 10, VWAP 5
- 30m: Trend 20, Momentum 18, Open Interest 15, Hacim 10, Funding+L/S 10, FVG+Likidite avı 10, VWAP 5
- 1h: Open Interest 31.6, Hacim 4.2, Funding+L/S 24.0, FVG+Likidite avı 40.2
- 4h: Funding+L/S 18.3, FVG+Likidite avı 81.7

## 4. Strateji yarışması (yalnız canlı botun da görebildiği veriler; eğitimde seçildi, TEST'te sınandı)

### 15m — 207 strateji denendi · ❌ hiçbiri yeterince iyi değil, mevcut kalır

Mevcut (trend, filtresiz) TEST: 2957 işlem, kazanma %48.3, ort R -0.023, PF 0.78

| # | Strateji | Eğitim ort R (n) | TEST ort R | TEST kazanma | TEST PF | 5x ort ROE | 10x ort ROE | 10x likidasyon |
|---|---|---|---|---|---|---|---|---|
| 1 | Trend takibi (skor ≥58 / ≤42) +FVG/likidite aynı yönde +BTC trendi aynı yönde, SL1.0/TP1.5-2.5 | 0.034 (7535) | -0.056 | %37.6 (3177) | 0.71 | %-0.76 | %-1.51 | 0 |
| 2 | Trend takibi (skor ≥66 / ≤34) +FVG/likidite aynı yönde +BTC trendi aynı yönde, SL1.0/TP1.5-2.5 | 0.034 (7270) | -0.05 | %37.9 (3040) | 0.72 | %-0.72 | %-1.43 | 0 |
| 3 | Trend takibi (skor ≥66 / ≤34) +üst trend yönünde +FVG/likidite aynı yönde +BTC trendi aynı yönde, SL1.0/TP1.5-2.5 | 0.033 (7184) | -0.054 | %37.8 (3008) | 0.72 | %-0.71 | %-1.41 | 0 |
| 4 | Trend takibi (skor ≥58 / ≤42) +üst trend yönünde +FVG/likidite aynı yönde +BTC trendi aynı yönde, SL1.0/TP1.5-2.5 | 0.03 (7401) | -0.055 | %37.6 (3128) | 0.71 | %-0.74 | %-1.48 | 0 |
| 5 | Geri çekilmede limit giriş (skor ≥66 / ≤34, dip-tepe aralığının en fazla %50'inde, 0.5 Fibonacci geri çekilmesine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) +üst trend yönünde +BTC trendi aynı yönde | 0.068 (1384) | -0.114 | %36.2 (558) | 0.65 | %-1.54 | %-3.08 | 0 |

### 30m — 207 strateji denendi · ❌ hiçbiri yeterince iyi değil, mevcut kalır

Mevcut (trend, filtresiz) TEST: 1454 işlem, kazanma %49.7, ort R 0.012, PF 0.81

| # | Strateji | Eğitim ort R (n) | TEST ort R | TEST kazanma | TEST PF | 5x ort ROE | 10x ort ROE | 10x likidasyon |
|---|---|---|---|---|---|---|---|---|
| 1 | Ortalamaya dönüş (|Z|≥3.0, RSI 30/70, likidite avı şart), SL1.0/TP1.5-2.5 | 0.183 (186) | -0.27 | %31.0 (87) | 0.55 | %-1.99 | %-3.98 | 0 |
| 2 | Ortalamaya dönüş (|Z|≥2.5, RSI 25/75, likidite avı şart), SL1.0/TP1.5-2.5 | 0.14 (274) | -0.18 | %32.8 (119) | 0.64 | %-1.68 | %-3.36 | 0 |
| 3 | Ortalamaya dönüş (|Z|≥3.0, RSI 25/75, likidite avı şart), SL1.0/TP1.5-2.5 | 0.189 (113) | -0.348 | %27.5 (51) | 0.44 | %-2.91 | %-5.82 | 0 |
| 4 | Ortalamaya dönüş (|Z|≥3.0, RSI 25/75), SL1.5/TP1.5-3.0 | 0.112 (312) | -0.031 | %48.7 (113) | 0.8 | %-1.14 | %-2.27 | 0 |
| 5 | Ortalamaya dönüş (|Z|≥3.0, RSI 25/75), SL1.0/TP1.5-2.5 | 0.107 (313) | -0.033 | %37.7 (114) | 0.8 | %-0.93 | %-1.87 | 0 |

### 1h — 217 strateji denendi · ❌ hiçbiri yeterince iyi değil, mevcut kalır

Mevcut (trend, filtresiz) TEST: 727 işlem, kazanma %52.4, ort R 0.096, PF 0.99

| # | Strateji | Eğitim ort R (n) | TEST ort R | TEST kazanma | TEST PF | 5x ort ROE | 10x ort ROE | 10x likidasyon |
|---|---|---|---|---|---|---|---|---|
| 1 | Kazanan ortak noktaları kuralı (skor ≥55 / ≤45 VE Dip-tepe konumu (yön) ≤ 0.49 VE VWAP bileşeni (yön) ≥ 0.23 VE Agresif alım-satım (yön) ≤ 0.05), fiyatın 0.5 ATR gerisine limit emirle giriş (6 mum geçerli), SL1.0/TP1.5-2.5 | 0.189 (385) | 0.042 | %43.7 (126) | 0.94 | %-0.22 | %-0.45 | 0 |
| 2 | Kazanan ortak noktaları kuralı (skor ≥55 / ≤45 VE Dip-tepe konumu (yön) ≤ 0.49 VE VWAP'tan uzaklık ATR (yön) ≥ 0.47 VE Agresif alım-satım (yön) ≤ 0.05), fiyatın 0.5 ATR gerisine limit emirle giriş (6 mum geçerli), SL1.0/TP1.5-2.5 | 0.189 (385) | 0.042 | %43.7 (126) | 0.94 | %-0.22 | %-0.45 | 0 |
| 3 | Kazanan ortak noktaları kuralı (skor ≥55 / ≤45 VE Dip-tepe konumu (yön) ≤ 0.49 VE VWAP bileşeni (yön) ≥ 0.23), fiyatın 0.5 ATR gerisine limit emirle giriş (6 mum geçerli), SL1.0/TP1.5-2.5 | 0.16 (422) | -0.015 | %41.7 (132) | 0.88 | %-0.48 | %-0.95 | 0 |
| 4 | Kazanan ortak noktaları kuralı (skor ≥55 / ≤45 VE FVG+Likidite (yön) ≤ -0.60 VE Saat (UTC) ≥ 12.00 VE RVOL ≤ 1.39), SL1.0/TP1.5-2.5 | 0.124 (699) | 0.169 | %46.5 (288) | 1.09 | %0.39 | %0.91 | 1 |
| 5 | Ortalamaya dönüş (|Z|≥3.0, RSI 25/75), SL1.0/TP1.5-2.5 | 0.225 (170) | 0.254 | %48.3 (58) | 1.57 | %2.96 | %5.92 | 0 |

### 4h — 194 strateji denendi · ❌ hiçbiri yeterince iyi değil, mevcut kalır

Mevcut (trend, filtresiz) TEST: 197 işlem, kazanma %57.9, ort R 0.234, PF 1.41

| # | Strateji | Eğitim ort R (n) | TEST ort R | TEST kazanma | TEST PF | 5x ort ROE | 10x ort ROE | 10x likidasyon |
|---|---|---|---|---|---|---|---|---|
| 1 | Likidite avı tersine dönüş, SL1.5/TP1.5-3.0 | 0.064 (478) | -0.014 | %48.8 (201) | 0.91 | %-1.17 | %-2.21 | 3 |
| 2 | Ortalamaya dönüş (|Z|≥2.0, RSI 30/70), SL2.0/TP1.0-2.0 | 0.082 (231) | -0.071 | %61.0 (82) | 0.76 | %-3.0 | %-7.22 | 5 |
| 3 | Likidite avı tersine dönüş +üst trende karşı, SL1.5/TP1.5-3.0 | 0.049 (403) | -0.225 | %40.4 (161) | 0.63 | %-5.35 | %-10.61 | 2 |
| 4 | Ortalamaya dönüş (|Z|≥2.5, RSI 30/70), SL2.0/TP1.0-2.0 | 0.077 (136) | 0.023 | %68.5 (54) | 0.89 | %-1.23 | %-3.55 | 6 |
| 5 | Ortalamaya dönüş (|Z|≥2.5, RSI 30/70), SL1.5/TP1.5-3.0 | 0.068 (133) | -0.12 | %43.4 (53) | 0.59 | %-6.55 | %-11.94 | 4 |


## 5. 15m (piyasa girişli): kazananlar ve kaybedenler

Tüm olaylar: kazanma %39.5 (eğitim) / %39.2 (test); ort. net R -0.162 / -0.159

**Kazanan vs kaybeden girişte o anki durum** (etki = standart fark; ✓ = test döneminde de aynı yönde)

| Özellik | Kazananlarda | Kaybedenlerde | Etki (eğitim) | Etki (test) | |
|---|---|---|---|---|---|
| BTC 1s yönü (yön) | 0.142 | 0.191 | -0.050 | -0.022 | ✗ |
| Momentum (yön) | 0.242 | 0.254 | -0.028 | -0.035 | ✓ |
| Z-Score (yön) | 0.845 | 0.871 | -0.026 | -0.047 | ✓ |
| VWAP bileşeni (yön) | 0.69 | 0.682 | +0.023 | +0.007 | ✗ |
| VWAP'tan uzaklık ATR (yön) | 2.586 | 2.549 | +0.019 | -0.009 | ✗ |
| Dip-tepe konumu (yön) | 0.719 | 0.722 | -0.017 | -0.022 | ✗ |
| Agresif alım-satım (yön) | 0.015 | 0.016 | -0.013 | +0.027 | ✗ |
| RSI (yön, 50 merkez) | 8.819 | 8.896 | -0.010 | -0.041 | ✓ |
| Üst trend (yön) | 0.663 | 0.66 | +0.008 | -0.001 | ✗ |
| Likidite avı (yön) | -0.2 | -0.205 | +0.008 | +0.033 | ✓ |

| Kural | Eğitim ort R (n) | Eğitim 1./2. yarı | TEST olay ort R (n) |
|---|---|---|---|

## 5. 15m (limit girişli): kazananlar ve kaybedenler

Tüm olaylar: kazanma %40.0 (eğitim) / %38.7 (test); ort. net R -0.147 / -0.171

**Kazanan vs kaybeden girişte o anki durum** (etki = standart fark; ✓ = test döneminde de aynı yönde)

| Özellik | Kazananlarda | Kaybedenlerde | Etki (eğitim) | Etki (test) | |
|---|---|---|---|---|---|
| Momentum (yön) | 0.254 | 0.27 | -0.037 | -0.026 | ✗ |
| VWAP bileşeni (yön) | 0.694 | 0.681 | +0.036 | -0.006 | ✗ |
| Z-Score (yön) | 0.879 | 0.911 | -0.032 | -0.033 | ✓ |
| BTC 1s yönü (yön) | 0.183 | 0.214 | -0.032 | -0.048 | ✓ |
| VWAP'tan uzaklık ATR (yön) | 2.613 | 2.558 | +0.028 | -0.014 | ✗ |
| Dip-tepe konumu (yön) | 0.722 | 0.727 | -0.026 | -0.019 | ✗ |
| RSI (yön, 50 merkez) | 9.013 | 9.156 | -0.018 | -0.045 | ✓ |
| RVOL | 1.113 | 1.134 | -0.016 | +0.002 | ✗ |
| Agresif alım-satım (yön) | 0.016 | 0.017 | -0.016 | +0.032 | ✗ |
| Likidite avı (yön) | -0.208 | -0.216 | +0.014 | +0.023 | ✗ |

| Kural | Eğitim ort R (n) | Eğitim 1./2. yarı | TEST olay ort R (n) |
|---|---|---|---|

## 5. 1h (piyasa girişli): kazananlar ve kaybedenler

Tüm olaylar: kazanma %40.5 (eğitim) / %40.0 (test); ort. net R -0.049 / -0.037

**Kazanan vs kaybeden girişte o anki durum** (etki = standart fark; ✓ = test döneminde de aynı yönde)

| Özellik | Kazananlarda | Kaybedenlerde | Etki (eğitim) | Etki (test) | |
|---|---|---|---|---|---|
| Hacim (yön) | 0.182 | 0.169 | +0.056 | -0.001 | ✗ |
| VWAP'tan uzaklık ATR (yön) | 1.089 | 1.03 | +0.056 | +0.025 | ✗ |
| VWAP bileşeni (yön) | 0.415 | 0.394 | +0.055 | +0.022 | ✗ |
| Likidite avı (yön) | -0.235 | -0.211 | -0.041 | +0.008 | ✗ |
| RSI (yön, 50 merkez) | 9.772 | 9.527 | +0.032 | +0.004 | ✗ |
| Z-Score (yön) | 0.98 | 0.959 | +0.022 | -0.013 | ✗ |
| Üst trend (yön) | 0.636 | 0.624 | +0.022 | +0.108 | ✓ |
| Trend (yön) | 0.747 | 0.741 | +0.015 | +0.098 | ✓ |
| FVG+Likidite (yön) | -0.006 | -0.0 | -0.013 | +0.043 | ✗ |
| RVOL | 1.066 | 1.08 | -0.013 | -0.021 | ✗ |

| Kural | Eğitim ort R (n) | Eğitim 1./2. yarı | TEST olay ort R (n) |
|---|---|---|---|
| VWAP bileşeni (yön) ≥ 0.57 VE Dip-tepe konumu (yön) ≤ 0.70 VE Trend (yön) ≥ 0.43 | 0.172 (1861) | 0.16 / 0.182 | 0.051 (509) |
| VWAP bileşeni (yön) ≥ 0.57 VE Dip-tepe konumu (yön) ≤ 0.70 VE Üst trend (yön) ≥ 0.33 | 0.164 (1968) | 0.142 / 0.183 | 0.022 (530) |
| VWAP'tan uzaklık ATR (yön) ≥ 1.28 VE Dip-tepe konumu (yön) ≤ 0.64 VE Üst trend (yön) ≥ -0.33 | 0.151 (1741) | 0.116 / 0.183 | 0.098 (438) |
| FVG+Likidite (yön) ≤ -0.60 VE Saat (UTC) ≥ 12.00 VE RVOL ≤ 1.39 | 0.151 (1657) | 0.155 / 0.148 | 0.129 (709) |
| VWAP bileşeni (yön) ≥ 0.57 VE Dip-tepe konumu (yön) ≤ 0.64 | 0.113 (2049) | 0.059 / 0.163 | 0.044 (547) |

## 5. 1h (limit girişli): kazananlar ve kaybedenler

Tüm olaylar: kazanma %41.4 (eğitim) / %38.8 (test); ort. net R -0.03 / -0.082

**Kazanan vs kaybeden girişte o anki durum** (etki = standart fark; ✓ = test döneminde de aynı yönde)

| Özellik | Kazananlarda | Kaybedenlerde | Etki (eğitim) | Etki (test) | |
|---|---|---|---|---|---|
| Hacim (yön) | 0.183 | 0.169 | +0.057 | -0.039 | ✗ |
| Dip-tepe konumu (yön) | 0.724 | 0.731 | -0.044 | -0.005 | ✗ |
| Likidite avı (yön) | -0.235 | -0.216 | -0.033 | +0.021 | ✗ |
| ATR % | 1.489 | 1.461 | +0.032 | -0.077 | ✗ |
| VWAP'tan uzaklık ATR (yön) | 1.09 | 1.057 | +0.031 | -0.018 | ✗ |
| VWAP bileşeni (yön) | 0.414 | 0.404 | +0.027 | -0.034 | ✗ |
| RVOL | 1.092 | 1.118 | -0.024 | -0.022 | ✗ |
| BTC 1s yönü (yön) | 0.25 | 0.228 | +0.023 | -0.028 | ✗ |
| Z-Score (yön) | 1.009 | 0.991 | +0.019 | -0.023 | ✗ |
| Momentum (yön) | 0.302 | 0.308 | -0.015 | +0.022 | ✗ |

| Kural | Eğitim ort R (n) | Eğitim 1./2. yarı | TEST olay ort R (n) |
|---|---|---|---|
| Dip-tepe konumu (yön) ≤ 0.49 VE VWAP bileşeni (yön) ≥ 0.23 VE Agresif alım-satım (yön) ≤ 0.05 | 0.316 (1214) | 0.573 / 0.069 | -0.02 (330) |
| Dip-tepe konumu (yön) ≤ 0.49 VE VWAP'tan uzaklık ATR (yön) ≥ 0.47 VE Agresif alım-satım (yön) ≤ 0.05 | 0.316 (1214) | 0.573 / 0.069 | -0.02 (330) |
| Dip-tepe konumu (yön) ≤ 0.49 VE VWAP bileşeni (yön) ≥ 0.23 VE ATR % ≥ 0.63 | 0.28 (1190) | 0.531 / 0.043 | 0.001 (338) |
| Dip-tepe konumu (yön) ≤ 0.49 VE VWAP'tan uzaklık ATR (yön) ≥ 0.47 VE ATR % ≥ 0.63 | 0.28 (1190) | 0.531 / 0.043 | 0.001 (338) |
| Dip-tepe konumu (yön) ≤ 0.49 VE VWAP bileşeni (yön) ≥ 0.23 | 0.26 (1368) | 0.515 / 0.037 | -0.008 (389) |

IC (bilgi katsayısı): gösterge puanı ile sonraki getiri arasındaki sıralama korelasyonu. Piyasada 0.02–0.05 bile anlamlıdır; negatif ise gösterge ters çalışıyor demektir.
Geçmiş performans geleceği garanti etmez.