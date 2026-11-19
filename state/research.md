# V5 Araştırma Raporu — 19.11.2026 10:30 UTC

40 coin · değerlendirme 21.08.2026'dan bugüne (90 gün) · eğitim/TEST ayrımı 23.10.2026

## 1. Mevcut model: kaldıraçlı işlem sonuçları (tüm dönem)

| Periyot | Kaldıraç | İşlem | Kazanma | Ort. ROE | PF | Ort. R | Likidasyon | 100$ marjla net | Maks. DD |
|---|---|---|---|---|---|---|---|---|---|
| 15m | 5x | 29299 | %49.8 | %-0.47 | 0.85 | 0.007 | 0 | -13626.0$ | 15400.0$ |
| 15m | 10x | 29302 | %49.8 | %-0.94 | 0.85 | 0.007 | 11 | -27654.0$ | 31202.0$ |
| 30m | 5x | 14213 | %50.5 | %-0.4 | 0.91 | 0.02 | 1 | -5742.0$ | 7512.0$ |
| 30m | 10x | 14216 | %50.5 | %-0.8 | 0.91 | 0.02 | 16 | -11336.0$ | 14986.0$ |
| 1h | 5x | 7046 | %50.6 | %-0.32 | 0.95 | 0.025 | 0 | -2263.0$ | 4920.0$ |
| 1h | 10x | 7052 | %50.5 | %-0.68 | 0.95 | 0.025 | 25 | -4777.0$ | 10072.0$ |
| 4h | 5x | 1876 | %53.0 | %1.09 | 1.09 | 0.082 | 3 | 2043.0$ | 2349.0$ |
| 4h | 10x | 1880 | %53.0 | %2.63 | 1.12 | 0.085 | 41 | 4944.0$ | 4834.0$ |

PF = kâr faktörü (toplam kazanç / toplam kayıp, 1 üstü kârlı). R = risk birimi (stop mesafesi).

## 2. Göstergelerin doğruluğu (TEST dönemi)

### 15m

| Bileşen | IC | İsabet | ↑ dediğinde yükseldi | ↓ dediğinde düştü | İşlemde aynı yöndeyken kazanma | Ters yöndeyken kazanma |
|---|---|---|---|---|---|---|
| Trend | -0.076 | %47.1 | %39.1 | %51.3 | %49.5 (6770) | %55.9 (487) |
| Momentum | -0.035 | %47.3 | %43.0 | %52.1 | %49.6 (5882) | %51.8 (884) |
| Open Interest | -0.02 | %46.6 | %44.0 | %51.9 | %52.2 (2563) | %46.3 (354) |
| Hacim | -0.027 | %49.4 | %44.4 | %52.1 | %52.0 (4880) | %44.3 (641) |
| Funding+L/S | -0.027 | %44.7 | %44.1 | %55.0 | %46.0 (2145) | %54.5 (2599) |
| FVG+Likidite avı | 0.001 | %51.4 | %47.4 | %56.3 | %48.4 (3243) | %51.1 (2624) |
| VWAP | -0.041 | %47.6 | %40.8 | %52.3 | %49.8 (7348) | %50.4 (421) |

Ham göstergeler (IC, büyükten küçüğe): EMA dizilimi -0.076, Üst periyot trendi -0.072, Fiyat>EMA200 -0.071, RSI -0.069, Z-Score -0.058, VWAP üstü/altı -0.057, MACD yönü -0.039, FVG -0.036, Likidite avı +0.027, Funding -0.026

### 30m

| Bileşen | IC | İsabet | ↑ dediğinde yükseldi | ↓ dediğinde düştü | İşlemde aynı yöndeyken kazanma | Ters yöndeyken kazanma |
|---|---|---|---|---|---|---|
| Trend | -0.088 | %49.8 | %38.6 | %53.8 | %47.9 (3258) | %50.7 (359) |
| Momentum | -0.057 | %46.1 | %39.7 | %52.9 | %49.4 (3078) | %53.0 (279) |
| Open Interest | -0.041 | %45.5 | %43.1 | %49.3 | %48.8 (1819) | %45.0 (218) |
| Hacim | -0.078 | %47.0 | %37.3 | %50.9 | %48.9 (2387) | %50.5 (208) |
| Funding+L/S | -0.035 | %43.5 | %42.8 | %54.8 | %45.0 (965) | %50.8 (1390) |
| FVG+Likidite avı | 0.018 | %53.1 | %47.5 | %60.6 | %49.4 (1541) | %48.2 (1362) |
| VWAP | -0.047 | %47.6 | %38.6 | %53.5 | %47.7 (3462) | %50.0 (170) |

Ham göstergeler (IC, büyükten küçüğe): RSI -0.084, Üst periyot trendi -0.074, Z-Score -0.073, Fiyat>EMA200 -0.069, EMA dizilimi -0.064, OBV yönü -0.062, VWAP üstü/altı -0.061, Likidite avı +0.049, MACD yönü -0.047, FVG -0.047

### 1h

| Bileşen | IC | İsabet | ↑ dediğinde yükseldi | ↓ dediğinde düştü | İşlemde aynı yöndeyken kazanma | Ters yöndeyken kazanma |
|---|---|---|---|---|---|---|
| Trend | -0.078 | %53.3 | %36.4 | %57.2 | %51.4 (1583) | %45.2 (208) |
| Momentum | -0.051 | %46.2 | %37.4 | %55.7 | %48.4 (1540) | %54.9 (113) |
| Open Interest | -0.073 | %43.7 | %37.4 | %51.0 | %46.4 (1170) | %57.1 (147) |
| Hacim | -0.072 | %49.4 | %33.8 | %53.5 | %45.4 (1178) | %55.3 (76) |
| Funding+L/S | -0.038 | %42.5 | %41.7 | %54.9 | %43.2 (454) | %53.8 (664) |
| FVG+Likidite avı | 0.014 | %51.5 | %42.9 | %64.4 | %50.7 (787) | %47.3 (659) |
| VWAP | -0.04 | %48.7 | %36.5 | %56.3 | %46.6 (1553) | %77.2 (136) |

Ham göstergeler (IC, büyükten küçüğe): RSI -0.089, Üst periyot trendi -0.079, Taker alım -0.064, OI değişimi -0.063, Z-Score -0.062, EMA dizilimi -0.058, Fiyat>EMA200 -0.056, OI rejimi +0.043, VWAP üstü/altı -0.037, Funding +0.037

### 4h

| Bileşen | IC | İsabet | ↑ dediğinde yükseldi | ↓ dediğinde düştü | İşlemde aynı yöndeyken kazanma | Ters yöndeyken kazanma |
|---|---|---|---|---|---|---|
| Trend | -0.083 | %58.8 | %36.3 | %61.4 | %61.6 (396) | %37.7 (53) |
| Momentum | -0.115 | %45.5 | %33.0 | %55.8 | %56.3 (350) | %68.8 (32) |
| Open Interest | -0.085 | %48.7 | %34.6 | %57.1 | %57.0 (363) | %72.7 (33) |
| Hacim | -0.13 | %53.3 | %37.5 | %55.2 | %60.8 (265) | %58.8 (17) |
| Funding+L/S | -0.034 | %40.1 | %39.0 | %58.2 | %47.8 (90) | %66.7 (174) |
| FVG+Likidite avı | 0.033 | %51.8 | %45.0 | %68.0 | %58.7 (213) | %56.1 (148) |
| VWAP | -0.111 | %53.0 | %30.2 | %59.0 | %55.4 (370) | %63.2 (19) |

Ham göstergeler (IC, büyükten küçüğe): Z-Score -0.156, RSI -0.142, MACD yönü -0.092, VWAP üstü/altı -0.092, Fiyat>EMA200 -0.090, Likidite avı +0.083, OI değişimi -0.081, OI rejimi +0.079, Taker alım -0.074, RVOL +0.067

## 3. Öğrenme: yeni ağırlıklar (eğitimde bulundu, TEST'te sınandı)

| Periyot | Yöntem | Eşik | Mevcut model TEST ort. R / kazanma | Yeni model TEST ort. R / kazanma | Karar |
|---|---|---|---|---|---|
| 15m | mevcut | 74/26 | 0.006 / %50.1 (8723) | -0.007 / %49.7 (3240) | ❌ mevcut kalır |
| 30m | IC+ | 58/42 | -0.014 / %48.9 (4278) | -0.081 / %46.2 (3147) | ❌ mevcut kalır |
| 1h | IC+ | 55/45 | 0.015 / %49.9 (2081) | -0.085 / %45.2 (2147) | ❌ mevcut kalır |
| 4h | mevcut | 55/45 | 0.183 / %58.5 (491) | 0.165 / %57.2 (547) | ❌ mevcut kalır |

Ağırlıklar:
- 15m: Trend 20, Momentum 18, Open Interest 15, Hacim 10, Funding+L/S 10, FVG+Likidite avı 10, VWAP 5
- 30m: Funding+L/S 68.7, VWAP 31.3
- 1h: Momentum 0.2, Open Interest 9.4, Hacim 48.1, Funding+L/S 26.7, VWAP 15.7
- 4h: Trend 20, Momentum 18, Open Interest 15, Hacim 10, Funding+L/S 10, FVG+Likidite avı 10, VWAP 5

## 4. Strateji yarışması (yalnız canlı botun da görebildiği veriler; eğitimde seçildi, TEST'te sınandı)

### 15m — 217 strateji denendi · ❌ hiçbiri yeterince iyi değil, mevcut kalır

Mevcut (trend, filtresiz) TEST: 2930 işlem, kazanma %49.6, ort R -0.001, PF 0.82

| # | Strateji | Eğitim ort R (n) | TEST ort R | TEST kazanma | TEST PF | 5x ort ROE | 10x ort ROE | 10x likidasyon |
|---|---|---|---|---|---|---|---|---|
| 1 | Geri çekilmede limit giriş (skor ≥66 / ≤34, dip-tepe aralığının en fazla %50'inde, 0.382 Fibonacci geri çekilmesine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) | 0.114 (1914) | -0.027 | %39.0 (784) | 0.82 | %-0.83 | %-1.95 | 5 |
| 2 | Geri çekilmede limit giriş (skor ≥66 / ≤34, dip-tepe aralığının en fazla %50'inde, 0.5 Fibonacci geri çekilmesine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) | 0.114 (1914) | -0.027 | %39.0 (784) | 0.82 | %-0.83 | %-1.95 | 5 |
| 3 | Geri çekilmede limit giriş (skor ≥66 / ≤34, dip-tepe aralığının en fazla %50'inde, 0.382 Fibonacci geri çekilmesine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) +üst trend yönünde | 0.112 (1884) | -0.014 | %39.4 (767) | 0.84 | %-0.73 | %-1.77 | 5 |
| 4 | Geri çekilmede limit giriş (skor ≥66 / ≤34, dip-tepe aralığının en fazla %50'inde, 0.5 Fibonacci geri çekilmesine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) +üst trend yönünde | 0.112 (1884) | -0.014 | %39.4 (767) | 0.84 | %-0.73 | %-1.77 | 5 |
| 5 | Geri çekilmede limit giriş (skor ≥58 / ≤42, dip-tepe aralığının en fazla %70'inde, 0.5 Fibonacci geri çekilmesine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) | 0.087 (2822) | 0.036 | %40.0 (1276) | 0.9 | %-0.41 | %-0.74 | 4 |

### 30m — 207 strateji denendi · ❌ hiçbiri yeterince iyi değil, mevcut kalır

Mevcut (trend, filtresiz) TEST: 1440 işlem, kazanma %51.0, ort R 0.032, PF 0.92

| # | Strateji | Eğitim ort R (n) | TEST ort R | TEST kazanma | TEST PF | 5x ort ROE | 10x ort ROE | 10x likidasyon |
|---|---|---|---|---|---|---|---|---|
| 1 | Geri çekilmede limit giriş (skor ≥58 / ≤42, dip-tepe aralığının en fazla %70'inde, 0.382 Fibonacci geri çekilmesine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) | 0.067 (1591) | 0.056 | %42.7 (698) | 0.99 | %-0.05 | %-0.29 | 7 |
| 2 | Geri çekilmede limit giriş (skor ≥58 / ≤42, dip-tepe aralığının en fazla %70'inde, 0.382 Fibonacci geri çekilmesine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.0R / 2.0R) | 0.061 (1807) | 0.033 | %50.4 (788) | 0.93 | %-0.37 | %-0.82 | 6 |
| 3 | Geri çekilmede limit giriş (skor ≥66 / ≤34, dip-tepe aralığının en fazla %70'inde, 0.382 Fibonacci geri çekilmesine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) | 0.064 (1502) | 0.026 | %41.3 (653) | 0.92 | %-0.53 | %-1.26 | 7 |
| 4 | Geri çekilmede limit giriş (skor ≥58 / ≤42, dip-tepe aralığının en fazla %70'inde, 0.382 Fibonacci geri çekilmesine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.0R / 2.0R) +üst trend yönünde | 0.051 (1827) | 0.034 | %50.3 (783) | 0.92 | %-0.48 | %-1.03 | 6 |
| 5 | Geri çekilmede limit giriş (skor ≥66 / ≤34, dip-tepe aralığının en fazla %70'inde, 0.382 Fibonacci geri çekilmesine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.0R / 2.0R) | 0.052 (1697) | 0.022 | %50.0 (736) | 0.9 | %-0.58 | %-1.24 | 6 |

### 1h — 213 strateji denendi · ❌ hiçbiri yeterince iyi değil, mevcut kalır

Mevcut (trend, filtresiz) TEST: 738 işlem, kazanma %54.5, ort R 0.13, PF 1.09

| # | Strateji | Eğitim ort R (n) | TEST ort R | TEST kazanma | TEST PF | 5x ort ROE | 10x ort ROE | 10x likidasyon |
|---|---|---|---|---|---|---|---|---|
| 1 | Kazanan ortak noktaları kuralı (skor ≥55 / ≤45 VE Dip-tepe konumu (yön) ≤ 0.49 VE Hacim (yön) ≥ 0.11 VE Agresif alım-satım (yön) ≤ 0.05), fiyatın 0.5 ATR gerisine limit emirle giriş (6 mum geçerli), SL1.0/TP1.5-2.5 | 0.224 (431) | 0.07 | %42.5 (193) | 0.9 | %-0.44 | %-0.88 | 0 |
| 2 | Kazanan ortak noktaları kuralı (skor ≥55 / ≤45 VE Dip-tepe konumu (yön) ≤ 0.49 VE VWAP bileşeni (yön) ≥ 0.24 VE Agresif alım-satım (yön) ≤ 0.05), fiyatın 0.5 ATR gerisine limit emirle giriş (6 mum geçerli), SL1.0/TP1.5-2.5 | 0.221 (375) | 0.001 | %40.4 (136) | 0.88 | %-0.6 | %-1.19 | 0 |
| 3 | Kazanan ortak noktaları kuralı (skor ≥55 / ≤45 VE Dip-tepe konumu (yön) ≤ 0.49 VE VWAP'tan uzaklık ATR (yön) ≥ 0.49 VE Agresif alım-satım (yön) ≤ 0.05), fiyatın 0.5 ATR gerisine limit emirle giriş (6 mum geçerli), SL1.0/TP1.5-2.5 | 0.221 (375) | 0.001 | %40.4 (136) | 0.88 | %-0.6 | %-1.19 | 0 |
| 4 | Kazanan ortak noktaları kuralı (skor ≥55 / ≤45 VE Dip-tepe konumu (yön) ≤ 0.49 VE VWAP bileşeni (yön) ≥ 0.24 VE Hacim (yön) ≥ -0.15), fiyatın 0.5 ATR gerisine limit emirle giriş (6 mum geçerli), SL1.0/TP1.5-2.5 | 0.21 (385) | -0.073 | %38.3 (141) | 0.75 | %-1.21 | %-2.41 | 0 |
| 5 | Kazanan ortak noktaları kuralı (skor ≥55 / ≤45 VE Dip-tepe konumu (yön) ≤ 0.49 VE VWAP'tan uzaklık ATR (yön) ≥ 0.49 VE Hacim (yön) ≥ -0.15), fiyatın 0.5 ATR gerisine limit emirle giriş (6 mum geçerli), SL1.0/TP1.5-2.5 | 0.21 (385) | -0.073 | %38.3 (141) | 0.75 | %-1.21 | %-2.41 | 0 |

### 4h — 194 strateji denendi · ✅ kazanan benimsendi

Mevcut (trend, filtresiz) TEST: 197 işlem, kazanma %61.4, ort R 0.24, PF 1.4

| # | Strateji | Eğitim ort R (n) | TEST ort R | TEST kazanma | TEST PF | 5x ort ROE | 10x ort ROE | 10x likidasyon |
|---|---|---|---|---|---|---|---|---|
| 1 | Geri çekilmede limit giriş (skor ≥58 / ≤42, dip-tepe aralığının en fazla %50'inde, 0.382 Fibonacci geri çekilmesine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) | 0.18 (177) | 0.409 | %54.5 (66) | 1.29 | %5.32 | %12.24 | 13 |
| 2 | Geri çekilmede limit giriş (skor ≥58 / ≤42, dip-tepe aralığının en fazla %50'inde, 0.5 Fibonacci geri çekilmesine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) | 0.18 (177) | 0.409 | %54.5 (66) | 1.29 | %5.32 | %12.24 | 13 |
| 3 | Geri çekilmede limit giriş (skor ≥58 / ≤42, dip-tepe aralığının en fazla %50'inde, 0.382 Fibonacci geri çekilmesine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) +üst trend yönünde | 0.147 (167) | 0.482 | %56.1 (57) | 1.4 | %6.83 | %13.71 | 11 |
| 4 | Geri çekilmede limit giriş (skor ≥58 / ≤42, dip-tepe aralığının en fazla %50'inde, 0.5 Fibonacci geri çekilmesine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) +üst trend yönünde | 0.147 (167) | 0.482 | %56.1 (57) | 1.4 | %6.83 | %13.71 | 11 |
| 5 | Geri çekilmede limit giriş (skor ≥66 / ≤34, dip-tepe aralığının en fazla %50'inde, fiyatın 0.5 ATR gerisine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) | 0.183 (100) | 0.19 | %50.0 (24) | 0.72 | %-5.59 | %-5.51 | 5 |


## 5. 15m (piyasa girişli): kazananlar ve kaybedenler

Tüm olaylar: kazanma %40.0 (eğitim) / %39.6 (test); ort. net R -0.137 / -0.142

**Kazanan vs kaybeden girişte o anki durum** (etki = standart fark; ✓ = test döneminde de aynı yönde)

| Özellik | Kazananlarda | Kaybedenlerde | Etki (eğitim) | Etki (test) | |
|---|---|---|---|---|---|
| BTC 1s yönü (yön) | 0.15 | 0.192 | -0.043 | -0.032 | ✓ |
| Z-Score (yön) | 0.847 | 0.877 | -0.030 | -0.040 | ✓ |
| Dip-tepe konumu (yön) | 0.721 | 0.726 | -0.030 | -0.017 | ✗ |
| Momentum (yön) | 0.244 | 0.255 | -0.024 | -0.026 | ✗ |
| Saat (UTC) | 11.416 | 11.585 | -0.024 | +0.015 | ✗ |
| VWAP bileşeni (yön) | 0.697 | 0.689 | +0.022 | +0.028 | ✗ |
| Hacim (yön) | 0.172 | 0.178 | -0.020 | +0.019 | ✗ |
| RSI (yön, 50 merkez) | 8.883 | 9.018 | -0.017 | -0.028 | ✗ |
| Üst trend (yön) | 0.67 | 0.664 | +0.013 | +0.027 | ✗ |
| VWAP'tan uzaklık ATR (yön) | 2.639 | 2.614 | +0.012 | +0.057 | ✓ |

| Kural | Eğitim ort R (n) | Eğitim 1./2. yarı | TEST olay ort R (n) |
|---|---|---|---|
| ATR % ≥ 1.23 VE Dip-tepe konumu (yön) ≤ 0.70 VE Hacim (yön) ≥ -0.20 | 0.054 (6659) | 0.087 / 0.014 | -0.058 (2722) |
| ATR % ≥ 0.99 VE Dip-tepe konumu (yön) ≤ 0.58 VE Likidite avı (yön) ≤ 0.00 | 0.047 (7328) | 0.061 / 0.03 | -0.114 (2577) |
| ATR % ≥ 0.99 VE Dip-tepe konumu (yön) ≤ 0.58 VE FVG+Likidite (yön) ≤ 0.30 | 0.044 (7084) | 0.053 / 0.033 | -0.111 (2510) |
| ATR % ≥ 0.99 VE Dip-tepe konumu (yön) ≤ 0.58 | 0.033 (8368) | 0.056 / 0.006 | -0.109 (3013) |
| ATR % ≥ 1.23 VE VWAP bileşeni (yön) ≤ 0.75 | 0.018 (8090) | 0.029 / 0.005 | -0.108 (3543) |

## 5. 15m (limit girişli): kazananlar ve kaybedenler

Tüm olaylar: kazanma %40.3 (eğitim) / %39.1 (test); ort. net R -0.128 / -0.155

**Kazanan vs kaybeden girişte o anki durum** (etki = standart fark; ✓ = test döneminde de aynı yönde)

| Özellik | Kazananlarda | Kaybedenlerde | Etki (eğitim) | Etki (test) | |
|---|---|---|---|---|---|
| VWAP bileşeni (yön) | 0.704 | 0.687 | +0.046 | +0.019 | ✗ |
| Z-Score (yön) | 0.885 | 0.92 | -0.034 | -0.024 | ✗ |
| BTC 1s yönü (yön) | 0.183 | 0.216 | -0.034 | -0.056 | ✓ |
| Momentum (yön) | 0.257 | 0.271 | -0.033 | -0.018 | ✗ |
| Hacim (yön) | 0.177 | 0.186 | -0.031 | +0.027 | ✗ |
| Dip-tepe konumu (yön) | 0.726 | 0.73 | -0.029 | -0.031 | ✓ |
| VWAP'tan uzaklık ATR (yön) | 2.679 | 2.625 | +0.027 | +0.050 | ✓ |
| RSI (yön, 50 merkez) | 9.112 | 9.302 | -0.024 | -0.041 | ✓ |
| Agresif alım-satım (yön) | 0.015 | 0.016 | -0.023 | +0.039 | ✗ |
| ATR % | 0.739 | 0.73 | +0.020 | +0.001 | ✗ |

| Kural | Eğitim ort R (n) | Eğitim 1./2. yarı | TEST olay ort R (n) |
|---|---|---|---|
| ATR % ≥ 1.22 VE Hacim (yön) ≤ 0.18 VE Saat (UTC) ≥ 9.00 | 0.103 (5482) | 0.144 / 0.054 | -0.079 (1991) |
| ATR % ≥ 1.22 VE Agresif alım-satım (yön) ≤ 0.00 VE Saat (UTC) ≥ 7.00 | 0.087 (5095) | 0.083 / 0.092 | -0.035 (1835) |
| ATR % ≥ 1.22 VE Hacim (yön) ≤ 0.10 VE FVG+Likidite (yön) ≥ 0.00 | 0.085 (4781) | 0.123 / 0.041 | -0.132 (1943) |
| ATR % ≥ 1.22 VE Hacim (yön) ≤ 0.10 | 0.067 (6189) | 0.088 / 0.043 | -0.102 (2477) |
| ATR % ≥ 1.22 VE Agresif alım-satım (yön) ≤ 0.00 | 0.064 (6738) | 0.078 / 0.048 | -0.106 (2577) |

## 5. 1h (piyasa girişli): kazananlar ve kaybedenler

Tüm olaylar: kazanma %40.8 (eğitim) / %42.6 (test); ort. net R -0.037 / 0.031

**Kazanan vs kaybeden girişte o anki durum** (etki = standart fark; ✓ = test döneminde de aynı yönde)

| Özellik | Kazananlarda | Kaybedenlerde | Etki (eğitim) | Etki (test) | |
|---|---|---|---|---|---|
| VWAP bileşeni (yön) | 0.43 | 0.399 | +0.083 | -0.032 | ✗ |
| VWAP'tan uzaklık ATR (yön) | 1.127 | 1.052 | +0.070 | -0.022 | ✗ |
| RSI (yön, 50 merkez) | 10.092 | 9.755 | +0.043 | -0.053 | ✗ |
| Likidite avı (yön) | -0.242 | -0.218 | -0.042 | +0.061 | ✗ |
| Hacim (yön) | 0.172 | 0.163 | +0.039 | -0.038 | ✗ |
| Z-Score (yön) | 1.009 | 0.974 | +0.037 | -0.086 | ✗ |
| Saat (UTC) | 11.414 | 11.637 | -0.032 | +0.028 | ✗ |
| Agresif alım-satım (yön) | 0.008 | 0.009 | -0.028 | +0.027 | ✗ |
| Dip-tepe konumu (yön) | 0.729 | 0.725 | +0.028 | +0.023 | ✗ |
| RVOL | 1.073 | 1.106 | -0.024 | -0.080 | ✓ |

| Kural | Eğitim ort R (n) | Eğitim 1./2. yarı | TEST olay ort R (n) |
|---|---|---|---|
| RSI (yön, 50 merkez) ≥ 16.20 VE Saat (UTC) ≤ 7.00 VE ATR % ≤ 1.78 | 0.248 (1880) | 0.417 / 0.039 | -0.108 (794) |

## 5. 1h (limit girişli): kazananlar ve kaybedenler

Tüm olaylar: kazanma %41.9 (eğitim) / %41.0 (test); ort. net R -0.012 / -0.021

**Kazanan vs kaybeden girişte o anki durum** (etki = standart fark; ✓ = test döneminde de aynı yönde)

| Özellik | Kazananlarda | Kaybedenlerde | Etki (eğitim) | Etki (test) | |
|---|---|---|---|---|---|
| VWAP bileşeni (yön) | 0.429 | 0.406 | +0.062 | -0.076 | ✗ |
| VWAP'tan uzaklık ATR (yön) | 1.132 | 1.077 | +0.050 | -0.053 | ✗ |
| Saat (UTC) | 11.374 | 11.663 | -0.042 | +0.063 | ✗ |
| Hacim (yön) | 0.173 | 0.164 | +0.040 | -0.044 | ✗ |
| Z-Score (yön) | 1.04 | 1.003 | +0.040 | -0.084 | ✗ |
| Likidite avı (yön) | -0.243 | -0.221 | -0.037 | +0.049 | ✗ |
| RSI (yön, 50 merkez) | 10.252 | 10.013 | +0.030 | -0.052 | ✗ |
| RVOL | 1.108 | 1.146 | -0.027 | -0.051 | ✓ |
| BTC 1s yönü (yön) | 0.262 | 0.237 | +0.025 | -0.039 | ✗ |
| ATR % | 1.532 | 1.516 | +0.019 | -0.015 | ✗ |

| Kural | Eğitim ort R (n) | Eğitim 1./2. yarı | TEST olay ort R (n) |
|---|---|---|---|
| Dip-tepe konumu (yön) ≤ 0.49 VE Hacim (yön) ≥ 0.11 VE Agresif alım-satım (yön) ≤ 0.05 | 0.27 (1202) | 0.292 / 0.252 | -0.003 (529) |
| Dip-tepe konumu (yön) ≤ 0.49 VE VWAP bileşeni (yön) ≥ 0.24 VE Agresif alım-satım (yön) ≤ 0.05 | 0.262 (1212) | 0.332 / 0.199 | -0.089 (349) |
| Dip-tepe konumu (yön) ≤ 0.49 VE VWAP'tan uzaklık ATR (yön) ≥ 0.49 VE Agresif alım-satım (yön) ≤ 0.05 | 0.262 (1212) | 0.332 / 0.199 | -0.089 (349) |
| Dip-tepe konumu (yön) ≤ 0.49 VE VWAP bileşeni (yön) ≥ 0.24 VE Hacim (yön) ≥ -0.15 | 0.232 (1278) | 0.303 / 0.173 | -0.078 (378) |
| Dip-tepe konumu (yön) ≤ 0.49 VE VWAP'tan uzaklık ATR (yön) ≥ 0.49 VE Hacim (yön) ≥ -0.15 | 0.232 (1278) | 0.303 / 0.173 | -0.078 (378) |

IC (bilgi katsayısı): gösterge puanı ile sonraki getiri arasındaki sıralama korelasyonu. Piyasada 0.02–0.05 bile anlamlıdır; negatif ise gösterge ters çalışıyor demektir.
Geçmiş performans geleceği garanti etmez.