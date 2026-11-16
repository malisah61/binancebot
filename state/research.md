# V5 Araştırma Raporu — 16.11.2026 00:00 UTC

40 coin · değerlendirme 18.08.2026'dan bugüne (90 gün) · eğitim/TEST ayrımı 20.10.2026

## 1. Mevcut model: kaldıraçlı işlem sonuçları (tüm dönem)

| Periyot | Kaldıraç | İşlem | Kazanma | Ort. ROE | PF | Ort. R | Likidasyon | 100$ marjla net | Maks. DD |
|---|---|---|---|---|---|---|---|---|---|
| 15m | 5x | 29111 | %50.1 | %-0.35 | 0.89 | 0.019 | 0 | -10101.0$ | 13607.0$ |
| 15m | 10x | 29118 | %50.1 | %-0.71 | 0.88 | 0.019 | 23 | -20754.0$ | 27529.0$ |
| 30m | 5x | 14277 | %50.9 | %-0.21 | 0.95 | 0.032 | 1 | -3044.0$ | 6773.0$ |
| 30m | 10x | 14295 | %50.8 | %-0.47 | 0.95 | 0.031 | 36 | -6745.0$ | 13906.0$ |
| 1h | 5x | 7089 | %51.4 | %0.16 | 1.03 | 0.049 | 1 | 1112.0$ | 3475.0$ |
| 1h | 10x | 7115 | %51.3 | %0.12 | 1.01 | 0.048 | 42 | 854.0$ | 7371.0$ |
| 4h | 5x | 1926 | %53.7 | %1.73 | 1.16 | 0.115 | 6 | 3339.0$ | 2495.0$ |
| 4h | 10x | 1938 | %53.4 | %3.33 | 1.15 | 0.116 | 50 | 6459.0$ | 5134.0$ |

PF = kâr faktörü (toplam kazanç / toplam kayıp, 1 üstü kârlı). R = risk birimi (stop mesafesi).

## 2. Göstergelerin doğruluğu (TEST dönemi)

### 15m

| Bileşen | IC | İsabet | ↑ dediğinde yükseldi | ↓ dediğinde düştü | İşlemde aynı yöndeyken kazanma | Ters yöndeyken kazanma |
|---|---|---|---|---|---|---|
| Trend | -0.059 | %47.8 | %41.3 | %51.7 | %49.4 (6787) | %59.2 (397) |
| Momentum | -0.007 | %48.5 | %44.4 | %53.2 | %49.8 (5704) | %49.8 (918) |
| Open Interest | 0.002 | %47.6 | %45.4 | %52.2 | %53.6 (2442) | %46.2 (305) |
| Hacim | -0.012 | %50.0 | %45.6 | %52.4 | %51.7 (4801) | %45.9 (649) |
| Funding+L/S | -0.025 | %46.7 | %46.1 | %54.3 | %45.9 (1920) | %53.3 (2380) |
| FVG+Likidite avı | -0.009 | %49.6 | %45.6 | %54.4 | %48.8 (3192) | %51.3 (2611) |
| VWAP | -0.016 | %48.3 | %42.1 | %52.7 | %49.6 (7371) | %51.6 (351) |

Ham göstergeler (IC, büyükten küçüğe): EMA dizilimi -0.073, Üst periyot trendi -0.061, Fiyat>EMA200 -0.054, VWAP üstü/altı -0.040, RSI -0.030, OI değişimi +0.021, Top trader L/S +0.020, Z-Score -0.019, OI rejimi -0.018, FVG -0.015

### 30m

| Bileşen | IC | İsabet | ↑ dediğinde yükseldi | ↓ dediğinde düştü | İşlemde aynı yöndeyken kazanma | Ters yöndeyken kazanma |
|---|---|---|---|---|---|---|
| Trend | -0.081 | %49.8 | %40.5 | %54.0 | %48.2 (3267) | %52.9 (325) |
| Momentum | -0.034 | %47.4 | %41.4 | %53.9 | %50.5 (2999) | %51.0 (288) |
| Open Interest | -0.011 | %47.1 | %43.8 | %52.2 | %49.1 (1777) | %43.8 (201) |
| Hacim | -0.072 | %47.9 | %39.5 | %51.6 | %47.9 (2382) | %54.5 (211) |
| Funding+L/S | -0.033 | %45.6 | %44.8 | %54.3 | %44.9 (900) | %50.6 (1251) |
| FVG+Likidite avı | 0.01 | %51.7 | %45.7 | %59.5 | %50.0 (1530) | %48.4 (1350) |
| VWAP | -0.03 | %48.1 | %39.8 | %53.7 | %48.1 (3477) | %55.1 (136) |

Ham göstergeler (IC, büyükten küçüğe): Üst periyot trendi -0.071, EMA dizilimi -0.067, OBV yönü -0.066, Fiyat>EMA200 -0.066, RSI -0.058, Z-Score -0.057, VWAP üstü/altı -0.052, MACD yönü -0.035, Likidite avı +0.033, FVG -0.027

### 1h

| Bileşen | IC | İsabet | ↑ dediğinde yükseldi | ↓ dediğinde düştü | İşlemde aynı yöndeyken kazanma | Ters yöndeyken kazanma |
|---|---|---|---|---|---|---|
| Trend | -0.076 | %51.1 | %37.9 | %55.6 | %50.8 (1569) | %50.0 (186) |
| Momentum | -0.049 | %46.8 | %38.9 | %55.1 | %49.5 (1554) | %49.0 (96) |
| Open Interest | -0.061 | %45.0 | %38.2 | %53.3 | %49.7 (1184) | %56.4 (140) |
| Hacim | -0.068 | %48.7 | %37.2 | %52.4 | %48.3 (1154) | %57.7 (71) |
| Funding+L/S | -0.033 | %43.8 | %42.9 | %54.6 | %40.6 (434) | %53.2 (600) |
| FVG+Likidite avı | 0.044 | %53.0 | %44.2 | %65.3 | %52.9 (804) | %46.4 (647) |
| VWAP | -0.045 | %48.3 | %38.7 | %54.7 | %47.6 (1579) | %76.0 (121) |

Ham göstergeler (IC, büyükten küçüğe): Fiyat>EMA200 -0.094, RSI -0.086, Üst periyot trendi -0.079, EMA dizilimi -0.072, Taker alım -0.064, Z-Score -0.057, Funding +0.052, Likidite avı +0.045, OI değişimi -0.043, VWAP üstü/altı -0.042

### 4h

| Bileşen | IC | İsabet | ↑ dediğinde yükseldi | ↓ dediğinde düştü | İşlemde aynı yöndeyken kazanma | Ters yöndeyken kazanma |
|---|---|---|---|---|---|---|
| Trend | -0.086 | %56.3 | %35.7 | %59.7 | %59.7 (365) | %41.9 (62) |
| Momentum | -0.156 | %43.6 | %34.1 | %52.2 | %51.2 (377) | %82.6 (23) |
| Open Interest | -0.129 | %45.6 | %32.9 | %54.9 | %56.1 (374) | %55.2 (29) |
| Hacim | -0.146 | %48.5 | %27.6 | %52.7 | %57.5 (219) | %50.0 (16) |
| Funding+L/S | -0.015 | %44.4 | %43.2 | %57.6 | %42.7 (89) | %72.1 (136) |
| FVG+Likidite avı | 0.087 | %54.5 | %46.5 | %66.9 | %57.9 (183) | %50.9 (169) |
| VWAP | -0.139 | %49.6 | %28.2 | %57.8 | %53.1 (373) | %50.0 (16) |

Ham göstergeler (IC, büyükten küçüğe): Z-Score -0.182, RSI -0.150, VWAP üstü/altı -0.125, OI değişimi -0.124, Likidite avı +0.115, OI rejimi +0.107, Taker alım -0.105, Bollinger sıkışma +0.103, MACD yönü -0.090, OBV yönü -0.087

## 3. Öğrenme: yeni ağırlıklar (eğitimde bulundu, TEST'te sınandı)

| Periyot | Yöntem | Eşik | Mevcut model TEST ort. R / kazanma | Yeni model TEST ort. R / kazanma | Karar |
|---|---|---|---|---|---|
| 15m | mevcut | 74/26 | 0.023 / %50.2 (8574) | 0.01 / %49.7 (3241) | ❌ mevcut kalır |
| 30m | IC± | 62/38 | 0.008 / %49.3 (4232) | 0.007 / %48.7 (3264) | ❌ mevcut kalır |
| 1h | IC± | 66/34 | 0.036 / %50.7 (2084) | 0.017 / %49.1 (1687) | ❌ mevcut kalır |
| 4h | mevcut | 55/45 | 0.124 / %55.1 (492) | 0.044 / %51.1 (546) | ❌ mevcut kalır |

Ağırlıklar:
- 15m: Trend 20, Momentum 18, Open Interest 15, Hacim 10, Funding+L/S 10, FVG+Likidite avı 10, VWAP 5
- 30m: Trend 12.5, Momentum -44.6, Open Interest -13.9, VWAP 17.1
- 1h: Trend 8.3, Momentum 4.1, Open Interest 12.3, Hacim 32.6, FVG+Likidite avı -11.0, VWAP 29.1
- 4h: Trend 20, Momentum 18, Open Interest 15, Hacim 10, Funding+L/S 10, FVG+Likidite avı 10, VWAP 5

## 4. Strateji yarışması (yalnız canlı botun da görebildiği veriler; eğitimde seçildi, TEST'te sınandı)

### 15m — 217 strateji denendi · ❌ hiçbiri yeterince iyi değil, mevcut kalır

Mevcut (trend, filtresiz) TEST: 2907 işlem, kazanma %48.3, ort R -0.005, PF 0.85

| # | Strateji | Eğitim ort R (n) | TEST ort R | TEST kazanma | TEST PF | 5x ort ROE | 10x ort ROE | 10x likidasyon |
|---|---|---|---|---|---|---|---|---|
| 1 | Kazanan ortak noktaları kuralı (skor ≥55 / ≤45 VE Z-Score (yön) ≤ -0.52 VE ATR % ≥ 0.49 VE Saat (UTC) ≥ 12.00), SL1.0/TP1.5-2.5 | 0.159 (2084) | -0.014 | %38.7 (822) | 0.82 | %-0.56 | %-1.13 | 1 |
| 2 | Kazanan ortak noktaları kuralı (skor ≥55 / ≤45 VE Z-Score (yön) ≤ -0.52 VE ATR % ≥ 0.49 VE FVG+Likidite (yön) ≤ 0.00), SL1.0/TP1.5-2.5 | 0.143 (2535) | -0.001 | %39.1 (989) | 0.85 | %-0.47 | %-0.93 | 0 |
| 3 | Geri çekilmede limit giriş (skor ≥58 / ≤42, dip-tepe aralığının en fazla %70'inde, 0.382 Fibonacci geri çekilmesine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) +üst trend yönünde | 0.085 (3276) | -0.035 | %37.8 (1377) | 0.78 | %-0.95 | %-1.85 | 8 |
| 4 | Geri çekilmede limit giriş (skor ≥66 / ≤34, dip-tepe aralığının en fazla %70'inde, 0.382 Fibonacci geri çekilmesine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) | 0.086 (3141) | -0.033 | %38.3 (1280) | 0.79 | %-0.94 | %-1.73 | 7 |
| 5 | Geri çekilmede limit giriş (skor ≥66 / ≤34, dip-tepe aralığının en fazla %50'inde, 0.5 Fibonacci geri çekilmesine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) +üst trend yönünde +BTC trendi aynı yönde | 0.127 (1366) | 0.023 | %42.1 (554) | 0.93 | %-0.24 | %-0.5 | 1 |

### 30m — 207 strateji denendi · ✅ kazanan benimsendi

Mevcut (trend, filtresiz) TEST: 1438 işlem, kazanma %50.9, ort R 0.039, PF 0.98

| # | Strateji | Eğitim ort R (n) | TEST ort R | TEST kazanma | TEST PF | 5x ort ROE | 10x ort ROE | 10x likidasyon |
|---|---|---|---|---|---|---|---|---|
| 1 | Geri çekilmede limit giriş (skor ≥58 / ≤42, dip-tepe aralığının en fazla %70'inde, 0.382 Fibonacci geri çekilmesine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) | 0.089 (1632) | 0.066 | %43.0 (647) | 1.06 | %0.34 | %0.31 | 7 |
| 2 | Geri çekilmede limit giriş (skor ≥58 / ≤42, dip-tepe aralığının en fazla %70'inde, 0.382 Fibonacci geri çekilmesine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) +üst trend yönünde | 0.078 (1650) | 0.067 | %42.7 (653) | 1.04 | %0.24 | %0.12 | 7 |
| 3 | Geri çekilmede limit giriş (skor ≥66 / ≤34, dip-tepe aralığının en fazla %70'inde, 0.382 Fibonacci geri çekilmesine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) | 0.078 (1532) | 0.048 | %42.5 (610) | 1.01 | %0.04 | %-0.18 | 6 |
| 4 | Trend takibi (skor ≥58 / ≤42, VWAP'tan ≤2.0 ATR) +üst trend yönünde, SL1.5/TP1.5-3.0 | 0.051 (3289) | 0.002 | %49.2 (1365) | 0.9 | %-0.44 | %-0.91 | 3 |
| 5 | Geri çekilmede limit giriş (skor ≥66 / ≤34, dip-tepe aralığının en fazla %70'inde, 0.382 Fibonacci geri çekilmesine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) +üst trend yönünde | 0.069 (1536) | 0.058 | %42.8 (608) | 1.0 | %-0.03 | %-0.31 | 6 |

### 1h — 217 strateji denendi · ❌ hiçbiri yeterince iyi değil, mevcut kalır

Mevcut (trend, filtresiz) TEST: 739 işlem, kazanma %52.6, ort R 0.072, PF 1.07

| # | Strateji | Eğitim ort R (n) | TEST ort R | TEST kazanma | TEST PF | 5x ort ROE | 10x ort ROE | 10x likidasyon |
|---|---|---|---|---|---|---|---|---|
| 1 | Kazanan ortak noktaları kuralı (skor ≥55 / ≤45 VE RSI (yön, 50 merkez) ≥ 13.37 VE Agresif alım-satım (yön) ≤ -0.01 VE RVOL ≤ 1.13), SL1.0/TP1.5-2.5 | 0.368 (664) | 0.057 | %41.5 (200) | 0.88 | %-0.56 | %-1.12 | 0 |
| 2 | Kazanan ortak noktaları kuralı (skor ≥55 / ≤45 VE RSI (yön, 50 merkez) ≥ 16.39 VE Momentum (yön) ≤ 0.09 VE ATR % ≤ 2.51), SL1.0/TP1.5-2.5 | 0.344 (458) | -0.068 | %36.8 (133) | 0.81 | %-0.88 | %-1.76 | 0 |
| 3 | Kazanan ortak noktaları kuralı (skor ≥55 / ≤45 VE RSI (yön, 50 merkez) ≥ 16.70 VE Momentum (yön) ≤ 0.14 VE ATR % ≤ 2.50), fiyatın 0.5 ATR gerisine limit emirle giriş (6 mum geçerli), SL1.0/TP1.5-2.5 | 0.415 (293) | 0.157 | %44.4 (99) | 1.18 | %0.71 | %1.41 | 0 |
| 4 | Kazanan ortak noktaları kuralı (skor ≥55 / ≤45 VE RSI (yön, 50 merkez) ≥ 13.37 VE Momentum (yön) ≤ 0.09 VE Agresif alım-satım (yön) ≤ 0.02), SL1.0/TP1.5-2.5 | 0.289 (604) | -0.033 | %39.0 (154) | 0.8 | %-1.46 | %-2.89 | 2 |
| 5 | Kazanan ortak noktaları kuralı (skor ≥55 / ≤45 VE RSI (yön, 50 merkez) ≥ 16.70 VE Momentum (yön) ≤ 0.14 VE ATR % ≥ 0.65), fiyatın 0.5 ATR gerisine limit emirle giriş (6 mum geçerli), SL1.0/TP1.5-2.5 | 0.378 (338) | 0.126 | %42.1 (114) | 1.19 | %1.36 | %2.85 | 2 |

### 4h — 194 strateji denendi · ✅ kazanan benimsendi

Mevcut (trend, filtresiz) TEST: 191 işlem, kazanma %55.0, ort R 0.125, PF 1.1

| # | Strateji | Eğitim ort R (n) | TEST ort R | TEST kazanma | TEST PF | 5x ort ROE | 10x ort ROE | 10x likidasyon |
|---|---|---|---|---|---|---|---|---|
| 1 | Trend takibi (skor ≥58 / ≤42), SL1.0/TP1.5-2.5 | 0.143 (541) | 0.183 | %46.3 (214) | 1.18 | %1.49 | %3.12 | 2 |
| 2 | Trend takibi (skor ≥66 / ≤34), SL1.0/TP1.5-2.5 | 0.143 (541) | 0.183 | %46.3 (214) | 1.18 | %1.49 | %3.12 | 2 |
| 3 | Trend takibi (skor ≥58 / ≤42) +üst trend yönünde, SL1.0/TP1.5-2.5 | 0.142 (543) | 0.183 | %46.3 (214) | 1.17 | %1.46 | %3.07 | 2 |
| 4 | Trend takibi (skor ≥66 / ≤34) +üst trend yönünde, SL1.0/TP1.5-2.5 | 0.142 (543) | 0.183 | %46.3 (214) | 1.17 | %1.46 | %3.07 | 2 |
| 5 | Trend takibi (skor ≥74 / ≤26), SL1.0/TP1.5-2.5 | 0.146 (512) | 0.186 | %46.4 (211) | 1.17 | %1.44 | %3.02 | 2 |


## 5. 15m (piyasa girişli): kazananlar ve kaybedenler

Tüm olaylar: kazanma %40.2 (eğitim) / %40.2 (test); ort. net R -0.134 / -0.131

**Kazanan vs kaybeden girişte o anki durum** (etki = standart fark; ✓ = test döneminde de aynı yönde)

| Özellik | Kazananlarda | Kaybedenlerde | Etki (eğitim) | Etki (test) | |
|---|---|---|---|---|---|
| BTC 1s yönü (yön) | 0.147 | 0.191 | -0.045 | -0.034 | ✓ |
| Z-Score (yön) | 0.835 | 0.879 | -0.043 | -0.004 | ✗ |
| Üst trend (yön) | 0.683 | 0.665 | +0.035 | -0.000 | ✗ |
| Dip-tepe konumu (yön) | 0.718 | 0.724 | -0.034 | +0.007 | ✗ |
| Momentum (yön) | 0.24 | 0.254 | -0.032 | -0.003 | ✗ |
| VWAP bileşeni (yön) | 0.701 | 0.69 | +0.032 | +0.036 | ✓ |
| RSI (yön, 50 merkez) | 8.796 | 9.033 | -0.030 | +0.015 | ✗ |
| Agresif alım-satım (yön) | 0.014 | 0.015 | -0.027 | +0.035 | ✗ |
| Hacim (yön) | 0.168 | 0.175 | -0.026 | +0.029 | ✗ |
| Trend (yön) | 0.783 | 0.775 | +0.025 | -0.004 | ✗ |

| Kural | Eğitim ort R (n) | Eğitim 1./2. yarı | TEST olay ort R (n) |
|---|---|---|---|
| Z-Score (yön) ≤ -0.52 VE ATR % ≥ 0.49 VE FVG+Likidite (yön) ≤ 0.00 | 0.108 (6897) | 0.153 / 0.064 | -0.074 (2699) |
| Z-Score (yön) ≤ -0.52 VE ATR % ≥ 0.49 VE Saat (UTC) ≥ 12.00 | 0.094 (7343) | 0.186 / 0.018 | -0.132 (2995) |
| ATR % ≥ 1.26 VE Z-Score (yön) ≤ 0.68 VE FVG+Likidite (yön) ≥ 0.00 | 0.075 (6810) | 0.101 / 0.055 | -0.097 (1791) |
| Z-Score (yön) ≤ -0.52 VE ATR % ≥ 0.40 VE VWAP bileşeni (yön) ≥ 0.84 | 0.071 (6552) | 0.145 / 0.003 | 0.133 (2054) |
| ATR % ≥ 1.26 VE Z-Score (yön) ≤ 0.68 | 0.044 (8245) | 0.058 / 0.033 | -0.051 (2253) |

## 5. 15m (limit girişli): kazananlar ve kaybedenler

Tüm olaylar: kazanma %40.6 (eğitim) / %39.4 (test); ort. net R -0.123 / -0.153

**Kazanan vs kaybeden girişte o anki durum** (etki = standart fark; ✓ = test döneminde de aynı yönde)

| Özellik | Kazananlarda | Kaybedenlerde | Etki (eğitim) | Etki (test) | |
|---|---|---|---|---|---|
| VWAP bileşeni (yön) | 0.706 | 0.688 | +0.050 | +0.010 | ✗ |
| Z-Score (yön) | 0.882 | 0.922 | -0.040 | -0.001 | ✗ |
| RSI (yön, 50 merkez) | 9.071 | 9.336 | -0.033 | -0.012 | ✗ |
| Agresif alım-satım (yön) | 0.014 | 0.016 | -0.033 | +0.023 | ✗ |
| Momentum (yön) | 0.257 | 0.27 | -0.030 | -0.008 | ✗ |
| Hacim (yön) | 0.174 | 0.183 | -0.030 | +0.027 | ✗ |
| Dip-tepe konumu (yön) | 0.724 | 0.729 | -0.030 | -0.027 | ✗ |
| ATR % | 0.756 | 0.739 | +0.030 | +0.001 | ✗ |
| BTC 1s yönü (yön) | 0.185 | 0.214 | -0.029 | -0.055 | ✓ |
| Trend (yön) | 0.783 | 0.774 | +0.027 | -0.025 | ✗ |

| Kural | Eğitim ort R (n) | Eğitim 1./2. yarı | TEST olay ort R (n) |
|---|---|---|---|
| ATR % ≥ 1.25 VE Z-Score (yön) ≤ 0.98 VE Saat (UTC) ≥ 9.00 | 0.1 (5229) | 0.174 / 0.041 | -0.004 (1407) |
| ATR % ≥ 1.25 VE Z-Score (yön) ≤ 0.98 VE Momentum (yön) ≥ -0.37 | 0.085 (6432) | 0.104 / 0.069 | -0.041 (1728) |
| ATR % ≥ 1.25 VE RSI (yön, 50 merkez) ≤ 12.64 VE Saat (UTC) ≥ 11.00 | 0.084 (5801) | 0.127 / 0.05 | -0.043 (1521) |
| ATR % ≥ 1.25 VE Dip-tepe konumu (yön) ≤ 0.70 VE Saat (UTC) ≥ 4.00 | 0.085 (4961) | 0.114 / 0.059 | 0.059 (1212) |
| ATR % ≥ 1.25 VE Dip-tepe konumu (yön) ≤ 0.70 VE Momentum (yön) ≥ -0.37 | 0.085 (4906) | 0.099 / 0.073 | 0.042 (1197) |

## 5. 1h (piyasa girişli): kazananlar ve kaybedenler

Tüm olaylar: kazanma %41.5 (eğitim) / %42.9 (test); ort. net R -0.013 / 0.035

**Kazanan vs kaybeden girişte o anki durum** (etki = standart fark; ✓ = test döneminde de aynı yönde)

| Özellik | Kazananlarda | Kaybedenlerde | Etki (eğitim) | Etki (test) | |
|---|---|---|---|---|---|
| VWAP bileşeni (yön) | 0.434 | 0.401 | +0.088 | -0.003 | ✗ |
| RSI (yön, 50 merkez) | 10.395 | 9.796 | +0.075 | -0.031 | ✗ |
| VWAP'tan uzaklık ATR (yön) | 1.141 | 1.06 | +0.074 | +0.020 | ✗ |
| Likidite avı (yön) | -0.249 | -0.206 | -0.073 | +0.069 | ✗ |
| Üst trend (yön) | 0.656 | 0.629 | +0.050 | +0.085 | ✓ |
| Agresif alım-satım (yön) | 0.008 | 0.009 | -0.049 | +0.032 | ✗ |
| Trend (yön) | 0.761 | 0.743 | +0.047 | +0.069 | ✓ |
| Hacim (yön) | 0.172 | 0.161 | +0.044 | -0.016 | ✗ |
| Dip-tepe konumu (yön) | 0.731 | 0.724 | +0.041 | +0.029 | ✗ |
| Z-Score (yön) | 1.013 | 0.976 | +0.039 | -0.049 | ✗ |

| Kural | Eğitim ort R (n) | Eğitim 1./2. yarı | TEST olay ort R (n) |
|---|---|---|---|
| RSI (yön, 50 merkez) ≥ 13.37 VE Momentum (yön) ≤ 0.09 VE Agresif alım-satım (yön) ≤ 0.02 | 0.332 (2152) | 0.526 / 0.079 | -0.02 (396) |
| RSI (yön, 50 merkez) ≥ 13.37 VE Agresif alım-satım (yön) ≤ -0.01 VE RVOL ≤ 1.13 | 0.344 (1939) | 0.504 / 0.134 | 0.055 (402) |
| RSI (yön, 50 merkez) ≥ 13.37 VE Momentum (yön) ≤ 0.09 | 0.276 (2975) | 0.444 / 0.054 | -0.058 (678) |
| RSI (yön, 50 merkez) ≥ 13.37 VE Agresif alım-satım (yön) ≤ -0.01 | 0.261 (3059) | 0.397 / 0.082 | 0.01 (618) |
| RSI (yön, 50 merkez) ≥ 16.39 VE Momentum (yön) ≤ 0.09 VE ATR % ≤ 2.51 | 0.337 (1816) | 0.518 / 0.075 | -0.097 (366) |

## 5. 1h (limit girişli): kazananlar ve kaybedenler

Tüm olaylar: kazanma %42.5 (eğitim) / %40.2 (test); ort. net R 0.011 / -0.041

**Kazanan vs kaybeden girişte o anki durum** (etki = standart fark; ✓ = test döneminde de aynı yönde)

| Özellik | Kazananlarda | Kaybedenlerde | Etki (eğitim) | Etki (test) | |
|---|---|---|---|---|---|
| VWAP bileşeni (yön) | 0.435 | 0.408 | +0.075 | -0.060 | ✗ |
| RSI (yön, 50 merkez) | 10.575 | 9.984 | +0.073 | -0.055 | ✗ |
| VWAP'tan uzaklık ATR (yön) | 1.158 | 1.082 | +0.068 | -0.023 | ✗ |
| Likidite avı (yön) | -0.245 | -0.211 | -0.056 | +0.062 | ✗ |
| Hacim (yön) | 0.173 | 0.162 | +0.043 | -0.025 | ✗ |
| Üst trend (yön) | 0.656 | 0.634 | +0.041 | +0.082 | ✓ |
| Z-Score (yön) | 1.043 | 1.005 | +0.039 | -0.082 | ✗ |
| Agresif alım-satım (yön) | 0.008 | 0.01 | -0.034 | +0.009 | ✗ |
| Trend (yön) | 0.76 | 0.747 | +0.032 | +0.077 | ✓ |
| FVG+Likidite (yön) | -0.016 | -0.004 | -0.031 | +0.083 | ✗ |

| Kural | Eğitim ort R (n) | Eğitim 1./2. yarı | TEST olay ort R (n) |
|---|---|---|---|
| RSI (yön, 50 merkez) ≥ 16.70 VE Momentum (yön) ≤ 0.14 VE ATR % ≥ 0.65 | 0.376 (1394) | 0.56 / 0.103 | 0.104 (294) |
| RSI (yön, 50 merkez) ≥ 16.70 VE Momentum (yön) ≤ 0.14 VE ATR % ≤ 2.50 | 0.398 (1202) | 0.588 / 0.089 | 0.022 (264) |
| RSI (yön, 50 merkez) ≥ 21.24 VE Z-Score (yön) ≤ 1.81 VE ATR % ≥ 0.65 | 0.378 (1261) | 0.61 / 0.06 | 0.183 (404) |
| RSI (yön, 50 merkez) ≥ 16.70 VE Momentum (yön) ≤ 0.14 VE RVOL ≤ 1.46 | 0.38 (1220) | 0.556 / 0.113 | 0.064 (252) |
| RSI (yön, 50 merkez) ≥ 16.70 VE Momentum (yön) ≤ 0.14 | 0.338 (1473) | 0.514 / 0.078 | 0.077 (318) |

IC (bilgi katsayısı): gösterge puanı ile sonraki getiri arasındaki sıralama korelasyonu. Piyasada 0.02–0.05 bile anlamlıdır; negatif ise gösterge ters çalışıyor demektir.
Geçmiş performans geleceği garanti etmez.