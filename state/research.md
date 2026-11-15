# V5 Araştırma Raporu — 15.11.2026 08:05 UTC

40 coin · değerlendirme 17.08.2026'dan bugüne (90 gün) · eğitim/TEST ayrımı 19.10.2026

## 1. Mevcut model: kaldıraçlı işlem sonuçları (tüm dönem)

| Periyot | Kaldıraç | İşlem | Kazanma | Ort. ROE | PF | Ort. R | Likidasyon | 100$ marjla net | Maks. DD |
|---|---|---|---|---|---|---|---|---|---|
| 15m | 5x | 29477 | %49.5 | %-0.47 | 0.85 | 0.005 | 0 | -13752.0$ | 15993.0$ |
| 15m | 10x | 29479 | %49.5 | %-0.94 | 0.85 | 0.005 | 14 | -27663.0$ | 32173.0$ |
| 30m | 5x | 14186 | %50.5 | %-0.32 | 0.93 | 0.022 | 0 | -4496.0$ | 7304.0$ |
| 30m | 10x | 14193 | %50.5 | %-0.64 | 0.93 | 0.022 | 20 | -9149.0$ | 14733.0$ |
| 1h | 5x | 7030 | %50.5 | %-0.2 | 0.97 | 0.027 | 1 | -1419.0$ | 4254.0$ |
| 1h | 10x | 7043 | %50.4 | %-0.47 | 0.96 | 0.028 | 29 | -3317.0$ | 9025.0$ |
| 4h | 5x | 1853 | %55.6 | %2.1 | 1.2 | 0.146 | 4 | 3893.0$ | 1941.0$ |
| 4h | 10x | 1863 | %55.3 | %4.14 | 1.2 | 0.145 | 33 | 7712.0$ | 4015.0$ |

PF = kâr faktörü (toplam kazanç / toplam kayıp, 1 üstü kârlı). R = risk birimi (stop mesafesi).

## 2. Göstergelerin doğruluğu (TEST dönemi)

### 15m

| Bileşen | IC | İsabet | ↑ dediğinde yükseldi | ↓ dediğinde düştü | İşlemde aynı yöndeyken kazanma | Ters yöndeyken kazanma |
|---|---|---|---|---|---|---|
| Trend | -0.084 | %46.7 | %41.6 | %50.0 | %48.1 (7014) | %59.3 (297) |
| Momentum | -0.019 | %48.0 | %44.5 | %51.9 | %49.1 (5387) | %47.7 (1417) |
| Hacim | -0.029 | %48.8 | %45.4 | %50.7 | %50.3 (4762) | %45.5 (761) |
| Funding+L/S | -0.02 | %40.2 | %40.2 | %- | %47.0 (457) | %46.6 (551) |
| FVG+Likidite avı | -0.009 | %50.6 | %47.4 | %54.1 | %49.0 (3321) | %48.6 (2630) |
| VWAP | -0.046 | %47.0 | %42.2 | %50.9 | %48.5 (7516) | %51.3 (384) |

Ham göstergeler (IC, büyükten küçüğe): EMA dizilimi -0.096, Üst periyot trendi -0.083, Fiyat>EMA200 -0.072, VWAP üstü/altı -0.061, RSI -0.056, Z-Score -0.039, FVG -0.038, OBV yönü -0.019, Bollinger sıkışma -0.017, Likidite avı +0.016

### 30m

| Bileşen | IC | İsabet | ↑ dediğinde yükseldi | ↓ dediğinde düştü | İşlemde aynı yöndeyken kazanma | Ters yöndeyken kazanma |
|---|---|---|---|---|---|---|
| Trend | -0.103 | %48.3 | %40.3 | %52.2 | %45.9 (3316) | %51.8 (218) |
| Momentum | -0.049 | %46.8 | %42.2 | %52.1 | %49.0 (2781) | %46.9 (522) |
| Hacim | -0.086 | %46.8 | %39.8 | %50.0 | %46.6 (2303) | %47.5 (217) |
| Funding+L/S | -0.042 | %35.5 | %35.5 | %- | %42.6 (190) | %45.1 (284) |
| FVG+Likidite avı | 0.016 | %52.6 | %47.3 | %58.9 | %48.4 (1585) | %46.8 (1331) |
| VWAP | -0.058 | %46.8 | %40.1 | %52.0 | %46.1 (3370) | %55.6 (187) |

Ham göstergeler (IC, büyükten küçüğe): Üst periyot trendi -0.093, EMA dizilimi -0.087, RSI -0.085, OBV yönü -0.085, Fiyat>EMA200 -0.083, Z-Score -0.081, VWAP üstü/altı -0.072, MACD yönü -0.047, Likidite avı +0.047, FVG -0.039

### 1h

| Bileşen | IC | İsabet | ↑ dediğinde yükseldi | ↓ dediğinde düştü | İşlemde aynı yöndeyken kazanma | Ters yöndeyken kazanma |
|---|---|---|---|---|---|---|
| Trend | -0.096 | %50.0 | %37.8 | %54.0 | %49.3 (1590) | %49.5 (95) |
| Momentum | -0.067 | %45.9 | %39.2 | %53.4 | %47.5 (1412) | %56.3 (199) |
| Hacim | -0.077 | %47.7 | %37.6 | %50.9 | %47.2 (1109) | %63.1 (65) |
| Funding+L/S | -0.085 | %35.0 | %35.0 | %- | %32.5 (80) | %46.0 (150) |
| FVG+Likidite avı | 0.047 | %54.3 | %45.6 | %65.5 | %52.7 (809) | %43.0 (603) |
| VWAP | -0.062 | %47.2 | %39.0 | %53.2 | %45.4 (1440) | %67.8 (180) |

Ham göstergeler (IC, büyükten küçüğe): RSI -0.107, Fiyat>EMA200 -0.106, Üst periyot trendi -0.094, EMA dizilimi -0.087, Z-Score -0.077, Taker alım -0.062, Likidite avı +0.058, Funding +0.058, VWAP üstü/altı -0.052, OBV yönü -0.027

### 4h

| Bileşen | IC | İsabet | ↑ dediğinde yükseldi | ↓ dediğinde düştü | İşlemde aynı yöndeyken kazanma | Ters yöndeyken kazanma |
|---|---|---|---|---|---|---|
| Trend | -0.117 | %54.6 | %34.3 | %57.5 | %56.8 (387) | %42.3 (26) |
| Momentum | -0.155 | %43.5 | %35.5 | %51.1 | %50.3 (334) | %67.9 (53) |
| Hacim | -0.173 | %46.9 | %24.1 | %50.8 | %51.2 (213) | %66.7 (18) |
| Funding+L/S | -0.063 | %36.7 | %36.7 | %- | %35.7 (14) | %56.0 (50) |
| FVG+Likidite avı | 0.084 | %56.0 | %48.6 | %67.3 | %56.7 (208) | %49.4 (160) |
| VWAP | -0.156 | %48.1 | %29.0 | %55.7 | %49.1 (330) | %66.7 (36) |

Ham göstergeler (IC, büyükten küçüğe): Z-Score -0.199, RSI -0.174, VWAP üstü/altı -0.140, Likidite avı +0.127, OBV yönü -0.114, Taker alım -0.105, RVOL +0.099, Bollinger sıkışma +0.093, MACD yönü -0.092, Fiyat>EMA200 -0.082

## 3. Öğrenme: yeni ağırlıklar (eğitimde bulundu, TEST'te sınandı)

| Periyot | Yöntem | Eşik | Mevcut model TEST ort. R / kazanma | Yeni model TEST ort. R / kazanma | Karar |
|---|---|---|---|---|---|
| 15m | IC± | 74/26 | -0.003 / %49.2 (8826) | 0.012 / %49.1 (1966) | ✅ benimsendi |
| 30m | IC± | 62/38 | -0.042 / %47.3 (4258) | -0.069 / %46.0 (3373) | ❌ mevcut kalır |
| 1h | IC+ | 70/30 | -0.005 / %49.3 (2058) | -0.017 / %49.0 (1546) | ❌ mevcut kalır |
| 4h | mevcut | 58/42 | 0.07 / %53.0 (487) | 0.041 / %51.9 (503) | ❌ mevcut kalır |

Ağırlıklar:
- 15m: Momentum -34.7, Hacim -19.8, Funding+L/S -18.1, FVG+Likidite avı 10.1, VWAP 13.2
- 30m: Trend 9.9, Momentum -38.7, Funding+L/S -20.1, VWAP 22.1
- 1h: Trend 3.3, Momentum 10.6, Hacim 45.1, VWAP 41.0
- 4h: Trend 20, Momentum 18, Open Interest 15, Hacim 10, Funding+L/S 10, FVG+Likidite avı 10, VWAP 5

## 4. Strateji yarışması (yalnız canlı botun da görebildiği veriler; eğitimde seçildi, TEST'te sınandı)

### 15m — 168 strateji denendi · ❌ hiçbiri yeterince iyi değil, mevcut kalır

Mevcut (trend, filtresiz) TEST: 2932 işlem, kazanma %47.6, ort R -0.026, PF 0.79

| # | Strateji | Eğitim ort R (n) | TEST ort R | TEST kazanma | TEST PF | 5x ort ROE | 10x ort ROE | 10x likidasyon |
|---|---|---|---|---|---|---|---|---|
| 1 | Kazanan ortak noktaları kuralı (skor ≥55 / ≤45 VE Z-Score (yön) ≤ -0.52 VE ATR % ≥ 0.48 VE FVG+Likidite (yön) ≤ 0.00), SL1.0/TP1.5-2.5 | 0.157 (2490) | -0.045 | %37.9 (997) | 0.81 | %-0.58 | %-1.15 | 0 |
| 2 | Kazanan ortak noktaları kuralı (skor ≥55 / ≤45 VE Z-Score (yön) ≤ -0.52 VE ATR % ≥ 0.39), SL1.0/TP1.5-2.5 | 0.107 (4308) | -0.017 | %39.1 (1754) | 0.77 | %-0.65 | %-1.3 | 0 |
| 3 | Kazanan ortak noktaları kuralı (skor ≥55 / ≤45 VE Z-Score (yön) ≤ -0.52 VE ATR % ≥ 0.48 VE Saat (UTC) ≥ 12.00), SL1.0/TP1.5-2.5 | 0.147 (2051) | -0.025 | %38.4 (841) | 0.82 | %-0.54 | %-1.07 | 0 |
| 4 | Kazanan ortak noktaları kuralı (skor ≥55 / ≤45 VE Z-Score (yön) ≤ -0.52 VE ATR % ≥ 0.39 VE VWAP bileşeni (yön) ≥ 0.84), SL1.0/TP1.5-2.5 | 0.15 (1732) | 0.144 | %44.9 (661) | 1.02 | %0.06 | %0.12 | 0 |
| 5 | Kazanan ortak noktaları kuralı (skor ≥55 / ≤45 VE Z-Score (yön) ≤ -0.52 VE ATR % ≥ 0.39 VE VWAP'tan uzaklık ATR (yön) ≥ 2.41), SL1.0/TP1.5-2.5 | 0.15 (1732) | 0.144 | %44.9 (661) | 1.02 | %0.06 | %0.12 | 0 |

### 30m — 163 strateji denendi · ❌ hiçbiri yeterince iyi değil, mevcut kalır

Mevcut (trend, filtresiz) TEST: 1437 işlem, kazanma %50.0, ort R 0.008, PF 0.9

| # | Strateji | Eğitim ort R (n) | TEST ort R | TEST kazanma | TEST PF | 5x ort ROE | 10x ort ROE | 10x likidasyon |
|---|---|---|---|---|---|---|---|---|
| 1 | Geri çekilmede limit giriş (skor ≥66 / ≤34, dip-tepe aralığının en fazla %50'inde, fiyatın 1.0 ATR gerisine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) | 0.126 (553) | -0.092 | %37.4 (227) | 0.82 | %-0.63 | %-1.26 | 0 |
| 2 | Geri çekilmede limit giriş (skor ≥58 / ≤42, dip-tepe aralığının en fazla %70'inde, 0.382 Fibonacci geri çekilmesine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) | 0.073 (1630) | -0.01 | %40.7 (656) | 0.81 | %-1.15 | %-2.39 | 3 |
| 3 | Geri çekilmede limit giriş (skor ≥66 / ≤34, dip-tepe aralığının en fazla %50'inde, fiyatın 1.0 ATR gerisine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) +üst trend yönünde | 0.122 (542) | -0.1 | %37.3 (220) | 0.82 | %-0.63 | %-1.26 | 0 |
| 4 | Geri çekilmede limit giriş (skor ≥66 / ≤34, dip-tepe aralığının en fazla %70'inde, fiyatın 1.0 ATR gerisine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) +üst trend yönünde | 0.075 (1257) | -0.051 | %39.7 (522) | 0.77 | %-1.04 | %-1.9 | 1 |
| 5 | Geri çekilmede limit giriş (skor ≥66 / ≤34, dip-tepe aralığının en fazla %70'inde, fiyatın 1.0 ATR gerisine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) | 0.073 (1263) | -0.03 | %40.4 (537) | 0.79 | %-0.97 | %-1.75 | 1 |

### 1h — 163 strateji denendi · ❌ hiçbiri yeterince iyi değil, mevcut kalır

Mevcut (trend, filtresiz) TEST: 735 işlem, kazanma %51.3, ort R 0.051, PF 1.01

| # | Strateji | Eğitim ort R (n) | TEST ort R | TEST kazanma | TEST PF | 5x ort ROE | 10x ort ROE | 10x likidasyon |
|---|---|---|---|---|---|---|---|---|
| 1 | Trend takibi (skor ≥66 / ≤34, VWAP'tan ≤2.0 ATR) +üst trend yönünde, SL1.0/TP1.5-2.5 | 0.075 (2073) | 0.044 | %41.6 (854) | 0.92 | %-0.38 | %-0.75 | 1 |
| 2 | Trend takibi (skor ≥58 / ≤42, VWAP'tan ≤2.0 ATR) +üst trend yönünde, SL1.0/TP1.5-2.5 | 0.074 (2079) | 0.039 | %41.4 (858) | 0.91 | %-0.4 | %-0.79 | 1 |
| 3 | Trend takibi (skor ≥66 / ≤34, VWAP'tan ≤2.0 ATR), SL1.0/TP1.5-2.5 | 0.072 (2088) | 0.048 | %41.8 (866) | 0.92 | %-0.36 | %-0.71 | 1 |
| 4 | Trend takibi (skor ≥58 / ≤42, VWAP'tan ≤2.0 ATR), SL1.0/TP1.5-2.5 | 0.07 (2093) | 0.049 | %41.8 (868) | 0.92 | %-0.36 | %-0.71 | 1 |
| 5 | Trend takibi (skor ≥58 / ≤42, VWAP'tan ≤2.0 ATR) +üst trend yönünde, SL1.5/TP1.5-3.0 | 0.076 (1765) | 0.01 | %50.3 (741) | 0.86 | %-0.81 | %-1.48 | 4 |

### 4h — 151 strateji denendi · ❌ hiçbiri yeterince iyi değil, mevcut kalır

Mevcut (trend, filtresiz) TEST: 189 işlem, kazanma %54.0, ort R 0.086, PF 0.95

| # | Strateji | Eğitim ort R (n) | TEST ort R | TEST kazanma | TEST PF | 5x ort ROE | 10x ort ROE | 10x likidasyon |
|---|---|---|---|---|---|---|---|---|
| 1 | Trend takibi (skor ≥58 / ≤42) +üst trend yönünde, SL1.0/TP1.5-2.5 | 0.151 (534) | 0.093 | %43.3 (217) | 1.0 | %0.02 | %0.19 | 2 |
| 2 | Trend takibi (skor ≥66 / ≤34) +üst trend yönünde, SL1.0/TP1.5-2.5 | 0.151 (534) | 0.093 | %43.3 (217) | 1.0 | %0.02 | %0.19 | 2 |
| 3 | Trend takibi (skor ≥74 / ≤26) +üst trend yönünde, SL1.0/TP1.5-2.5 | 0.151 (499) | 0.081 | %42.8 (215) | 1.01 | %0.05 | %0.25 | 2 |
| 4 | Trend takibi (skor ≥74 / ≤26), SL1.0/TP1.5-2.5 | 0.144 (503) | 0.081 | %42.8 (215) | 1.01 | %0.07 | %0.3 | 2 |
| 5 | Trend takibi (skor ≥58 / ≤42), SL1.0/TP1.5-2.5 | 0.138 (537) | 0.093 | %43.3 (217) | 1.01 | %0.11 | %0.37 | 2 |


## 5. 15dk: kazanan işlemlerin ortak noktaları (eğitimde bulundu)

Tüm olaylar: eğitim ort. net R -0.133 (214611 olay), test -0.162 (89386 olay)

| Kural | Eğitim ort R (n) | Eğitim 1./2. yarı | TEST olay ort R (n) |
|---|---|---|---|
| Z-Score (yön) ≤ -0.52 VE ATR % ≥ 0.48 VE FVG+Likidite (yön) ≤ 0.00 | 0.124 (6817) | 0.165 / 0.084 | -0.115 (2694) |
| Z-Score (yön) ≤ -0.52 VE ATR % ≥ 0.48 VE Saat (UTC) ≥ 12.00 | 0.102 (7350) | 0.175 / 0.043 | -0.136 (3030) |
| Z-Score (yön) ≤ -0.52 VE ATR % ≥ 0.39 VE VWAP bileşeni (yön) ≥ 0.84 | 0.105 (6540) | 0.164 / 0.051 | 0.093 (2094) |
| Z-Score (yön) ≤ -0.52 VE ATR % ≥ 0.39 VE VWAP'tan uzaklık ATR (yön) ≥ 2.41 | 0.105 (6540) | 0.164 / 0.051 | 0.093 (2094) |
| Z-Score (yön) ≤ -0.52 VE ATR % ≥ 0.39 | 0.047 (17318) | 0.092 / 0.006 | -0.081 (6901) |

IC (bilgi katsayısı): gösterge puanı ile sonraki getiri arasındaki sıralama korelasyonu. Piyasada 0.02–0.05 bile anlamlıdır; negatif ise gösterge ters çalışıyor demektir.
Geçmiş performans geleceği garanti etmez.