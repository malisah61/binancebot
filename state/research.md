# V5 Araştırma Raporu — 15.11.2026 23:56 UTC

40 coin · değerlendirme 17.08.2026'dan bugüne (90 gün) · eğitim/TEST ayrımı 19.10.2026

## 1. Mevcut model: kaldıraçlı işlem sonuçları (tüm dönem)

| Periyot | Kaldıraç | İşlem | Kazanma | Ort. ROE | PF | Ort. R | Likidasyon | 100$ marjla net | Maks. DD |
|---|---|---|---|---|---|---|---|---|---|
| 15m | 5x | 29456 | %50.0 | %-0.36 | 0.88 | 0.015 | 0 | -10522.0$ | 13605.0$ |
| 15m | 10x | 29463 | %50.0 | %-0.73 | 0.88 | 0.015 | 23 | -21597.0$ | 27523.0$ |
| 30m | 5x | 14460 | %50.7 | %-0.23 | 0.95 | 0.027 | 1 | -3379.0$ | 6759.0$ |
| 30m | 10x | 14478 | %50.6 | %-0.51 | 0.94 | 0.027 | 36 | -7414.0$ | 13905.0$ |
| 1h | 5x | 7184 | %51.1 | %0.12 | 1.02 | 0.042 | 1 | 883.0$ | 3476.0$ |
| 1h | 10x | 7210 | %51.0 | %0.05 | 1.0 | 0.042 | 42 | 396.0$ | 7367.0$ |
| 4h | 5x | 1936 | %54.3 | %1.88 | 1.17 | 0.125 | 6 | 3634.0$ | 2450.0$ |
| 4h | 10x | 1948 | %53.9 | %3.63 | 1.17 | 0.126 | 51 | 7066.0$ | 5129.0$ |

PF = kâr faktörü (toplam kazanç / toplam kayıp, 1 üstü kârlı). R = risk birimi (stop mesafesi).

## 2. Göstergelerin doğruluğu (TEST dönemi)

### 15m

| Bileşen | IC | İsabet | ↑ dediğinde yükseldi | ↓ dediğinde düştü | İşlemde aynı yöndeyken kazanma | Ters yöndeyken kazanma |
|---|---|---|---|---|---|---|
| Trend | -0.061 | %47.7 | %41.3 | %51.7 | %49.3 (7021) | %58.3 (405) |
| Momentum | -0.011 | %48.3 | %44.0 | %53.2 | %49.5 (5894) | %49.9 (948) |
| Open Interest | -0.0 | %47.4 | %45.1 | %52.1 | %53.2 (2503) | %46.9 (318) |
| Hacim | -0.013 | %49.9 | %45.2 | %52.5 | %51.4 (4945) | %46.3 (670) |
| Funding+L/S | -0.027 | %46.6 | %45.9 | %54.3 | %45.6 (1977) | %53.3 (2435) |
| FVG+Likidite avı | -0.012 | %49.5 | %45.4 | %54.3 | %48.9 (3286) | %51.1 (2695) |
| VWAP | -0.019 | %48.0 | %41.9 | %52.6 | %49.5 (7584) | %53.4 (399) |

Ham göstergeler (IC, büyükten küçüğe): EMA dizilimi -0.075, Üst periyot trendi -0.062, Fiyat>EMA200 -0.055, VWAP üstü/altı -0.042, RSI -0.030, Z-Score -0.021, Top trader L/S +0.020, OI değişimi +0.019, FVG -0.019, OI rejimi -0.017

### 30m

| Bileşen | IC | İsabet | ↑ dediğinde yükseldi | ↓ dediğinde düştü | İşlemde aynı yöndeyken kazanma | Ters yöndeyken kazanma |
|---|---|---|---|---|---|---|
| Trend | -0.081 | %49.4 | %40.1 | %53.8 | %48.0 (3378) | %52.4 (336) |
| Momentum | -0.034 | %47.4 | %41.5 | %53.8 | %50.0 (3113) | %50.2 (299) |
| Open Interest | -0.009 | %47.4 | %44.3 | %52.2 | %48.8 (1823) | %43.8 (208) |
| Hacim | -0.072 | %47.8 | %39.6 | %51.5 | %47.7 (2446) | %53.2 (222) |
| Funding+L/S | -0.035 | %45.4 | %44.7 | %54.3 | %44.6 (929) | %50.7 (1278) |
| FVG+Likidite avı | 0.006 | %51.2 | %45.4 | %58.5 | %49.2 (1589) | %48.2 (1407) |
| VWAP | -0.032 | %47.8 | %39.7 | %53.6 | %47.7 (3581) | %57.2 (152) |

Ham göstergeler (IC, büyükten küçüğe): Üst periyot trendi -0.072, EMA dizilimi -0.068, OBV yönü -0.068, Fiyat>EMA200 -0.065, RSI -0.059, Z-Score -0.056, VWAP üstü/altı -0.054, MACD yönü -0.033, Likidite avı +0.027, FVG -0.025

### 1h

| Bileşen | IC | İsabet | ↑ dediğinde yükseldi | ↓ dediğinde düştü | İşlemde aynı yöndeyken kazanma | Ters yöndeyken kazanma |
|---|---|---|---|---|---|---|
| Trend | -0.076 | %51.3 | %37.8 | %55.8 | %50.8 (1617) | %48.1 (208) |
| Momentum | -0.056 | %46.1 | %38.2 | %54.6 | %49.3 (1623) | %49.0 (96) |
| Open Interest | -0.067 | %44.3 | %37.5 | %53.0 | %49.6 (1224) | %55.9 (143) |
| Hacim | -0.069 | %48.6 | %36.8 | %52.5 | %48.3 (1178) | %60.5 (76) |
| Funding+L/S | -0.035 | %43.6 | %42.7 | %54.6 | %40.5 (449) | %53.4 (614) |
| FVG+Likidite avı | 0.045 | %53.5 | %44.2 | %65.9 | %52.9 (815) | %46.3 (676) |
| VWAP | -0.048 | %47.8 | %38.0 | %54.7 | %47.5 (1626) | %74.4 (129) |

Ham göstergeler (IC, büyükten küçüğe): Fiyat>EMA200 -0.089, RSI -0.089, Üst periyot trendi -0.077, EMA dizilimi -0.067, Taker alım -0.067, Z-Score -0.063, Funding +0.058, OI değişimi -0.048, Likidite avı +0.047, VWAP üstü/altı -0.044

### 4h

| Bileşen | IC | İsabet | ↑ dediğinde yükseldi | ↓ dediğinde düştü | İşlemde aynı yöndeyken kazanma | Ters yöndeyken kazanma |
|---|---|---|---|---|---|---|
| Trend | -0.08 | %55.8 | %36.5 | %58.9 | %58.1 (382) | %42.2 (64) |
| Momentum | -0.15 | %43.5 | %34.8 | %51.8 | %50.4 (389) | %79.2 (24) |
| Open Interest | -0.114 | %46.1 | %34.7 | %54.8 | %55.4 (386) | %48.5 (33) |
| Hacim | -0.147 | %48.0 | %27.6 | %52.0 | %55.9 (229) | %50.0 (18) |
| Funding+L/S | -0.017 | %44.5 | %43.5 | %57.6 | %41.3 (92) | %71.4 (140) |
| FVG+Likidite avı | 0.085 | %54.5 | %46.6 | %66.9 | %57.5 (186) | %50.0 (172) |
| VWAP | -0.131 | %49.4 | %28.5 | %57.3 | %52.8 (381) | %52.9 (17) |

Ham göstergeler (IC, büyükten küçüğe): Z-Score -0.173, RSI -0.141, VWAP üstü/altı -0.120, OI değişimi -0.110, Likidite avı +0.110, Bollinger sıkışma +0.104, Taker alım -0.098, OI rejimi +0.094, OBV yönü -0.093, MACD yönü -0.082

## 3. Öğrenme: yeni ağırlıklar (eğitimde bulundu, TEST'te sınandı)

| Periyot | Yöntem | Eşik | Mevcut model TEST ort. R / kazanma | Yeni model TEST ort. R / kazanma | Karar |
|---|---|---|---|---|---|
| 15m | mevcut | 74/26 | 0.017 / %50.1 (8876) | 0.005 / %49.6 (3317) | ❌ mevcut kalır |
| 30m | IC+ | 66/34 | -0.003 / %48.9 (4388) | -0.022 / %48.0 (4169) | ❌ mevcut kalır |
| 1h | IC+ | 66/34 | 0.028 / %50.5 (2165) | 0.022 / %49.5 (1823) | ❌ mevcut kalır |
| 4h | mevcut | 55/45 | 0.102 / %53.9 (512) | 0.056 / %52.1 (547) | ❌ mevcut kalır |

Ağırlıklar:
- 15m: Trend 20, Momentum 18, Open Interest 15, Hacim 10, Funding+L/S 10, FVG+Likidite avı 10, VWAP 5
- 30m: Trend 32.1, FVG+Likidite avı 15.4, VWAP 52.5
- 1h: Trend 7.8, Momentum 6.1, Open Interest 15.0, Hacim 37.0, VWAP 34.2
- 4h: Trend 20, Momentum 18, Open Interest 15, Hacim 10, Funding+L/S 10, FVG+Likidite avı 10, VWAP 5

## 4. Strateji yarışması (yalnız canlı botun da görebildiği veriler; eğitimde seçildi, TEST'te sınandı)

### 15m — 217 strateji denendi · ❌ hiçbiri yeterince iyi değil, mevcut kalır

Mevcut (trend, filtresiz) TEST: 3010 işlem, kazanma %48.1, ort R -0.013, PF 0.83

| # | Strateji | Eğitim ort R (n) | TEST ort R | TEST kazanma | TEST PF | 5x ort ROE | 10x ort ROE | 10x likidasyon |
|---|---|---|---|---|---|---|---|---|
| 1 | Kazanan ortak noktaları kuralı (skor ≥55 / ≤45 VE Z-Score (yön) ≤ -0.52 VE ATR % ≥ 0.48 VE FVG+Likidite (yön) ≤ 0.00), SL1.0/TP1.5-2.5 | 0.144 (2526) | -0.01 | %38.9 (1040) | 0.84 | %-0.48 | %-0.96 | 0 |
| 2 | Kazanan ortak noktaları kuralı (skor ≥55 / ≤45 VE Z-Score (yön) ≤ -0.52 VE ATR % ≥ 0.48 VE Saat (UTC) ≥ 12.00), SL1.0/TP1.5-2.5 | 0.157 (2079) | -0.023 | %38.3 (858) | 0.81 | %-0.59 | %-1.18 | 1 |
| 3 | Geri çekilmede limit giriş (skor ≥58 / ≤42, dip-tepe aralığının en fazla %70'inde, 0.382 Fibonacci geri çekilmesine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) +üst trend yönünde | 0.085 (3270) | -0.043 | %37.4 (1421) | 0.77 | %-1.01 | %-1.97 | 8 |
| 4 | Geri çekilmede limit giriş (skor ≥66 / ≤34, dip-tepe aralığının en fazla %70'inde, 0.382 Fibonacci geri çekilmesine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) | 0.085 (3144) | -0.043 | %38.0 (1317) | 0.78 | %-1.02 | %-1.9 | 7 |
| 5 | Kazanan ortak noktaları kuralı (skor ≥55 / ≤45 VE Z-Score (yön) ≤ -0.52 VE ATR % ≥ 0.39 VE VWAP bileşeni (yön) ≥ 0.83), SL1.0/TP1.5-2.5 | 0.111 (1779) | 0.146 | %44.9 (704) | 1.04 | %0.11 | %0.21 | 0 |

### 30m — 207 strateji denendi · ❌ hiçbiri yeterince iyi değil, mevcut kalır

Mevcut (trend, filtresiz) TEST: 1483 işlem, kazanma %50.4, ort R 0.025, PF 0.96

| # | Strateji | Eğitim ort R (n) | TEST ort R | TEST kazanma | TEST PF | 5x ort ROE | 10x ort ROE | 10x likidasyon |
|---|---|---|---|---|---|---|---|---|
| 1 | Geri çekilmede limit giriş (skor ≥58 / ≤42, dip-tepe aralığının en fazla %70'inde, 0.382 Fibonacci geri çekilmesine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) | 0.1 (1629) | 0.048 | %42.4 (668) | 1.01 | %0.07 | %-0.21 | 7 |
| 2 | Geri çekilmede limit giriş (skor ≥58 / ≤42, dip-tepe aralığının en fazla %70'inde, 0.382 Fibonacci geri çekilmesine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) +üst trend yönünde | 0.086 (1647) | 0.051 | %42.2 (673) | 1.0 | %-0.0 | %-0.35 | 7 |
| 3 | Geri çekilmede limit giriş (skor ≥66 / ≤34, dip-tepe aralığının en fazla %70'inde, 0.382 Fibonacci geri çekilmesine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) | 0.088 (1529) | 0.036 | %42.1 (627) | 0.97 | %-0.2 | %-0.64 | 6 |
| 4 | Geri çekilmede limit giriş (skor ≥66 / ≤34, dip-tepe aralığının en fazla %70'inde, 0.382 Fibonacci geri çekilmesine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) +üst trend yönünde | 0.077 (1532) | 0.042 | %42.3 (627) | 0.96 | %-0.26 | %-0.77 | 6 |
| 5 | Trend takibi (skor ≥58 / ≤42, VWAP'tan ≤2.0 ATR) +üst trend yönünde, SL1.5/TP1.5-3.0 | 0.049 (3295) | -0.002 | %49.0 (1404) | 0.89 | %-0.46 | %-0.95 | 3 |

### 1h — 217 strateji denendi · ❌ hiçbiri yeterince iyi değil, mevcut kalır

Mevcut (trend, filtresiz) TEST: 759 işlem, kazanma %52.4, ort R 0.068, PF 1.08

| # | Strateji | Eğitim ort R (n) | TEST ort R | TEST kazanma | TEST PF | 5x ort ROE | 10x ort ROE | 10x likidasyon |
|---|---|---|---|---|---|---|---|---|
| 1 | Kazanan ortak noktaları kuralı (skor ≥55 / ≤45 VE RSI (yön, 50 merkez) ≥ 13.38 VE Agresif alım-satım (yön) ≤ -0.01 VE RVOL ≤ 1.13), SL1.0/TP1.5-2.5 | 0.357 (663) | 0.055 | %41.5 (205) | 0.88 | %-0.52 | %-1.04 | 0 |
| 2 | Kazanan ortak noktaları kuralı (skor ≥55 / ≤45 VE RSI (yön, 50 merkez) ≥ 16.42 VE Momentum (yön) ≤ 0.09 VE ATR % ≤ 2.51), SL1.0/TP1.5-2.5 | 0.348 (460) | -0.067 | %36.8 (136) | 0.82 | %-0.81 | %-1.63 | 0 |
| 3 | Kazanan ortak noktaları kuralı (skor ≥55 / ≤45 VE RSI (yön, 50 merkez) ≥ 16.76 VE Momentum (yön) ≤ 0.14 VE ATR % ≥ 0.63), fiyatın 0.5 ATR gerisine limit emirle giriş (6 mum geçerli), SL1.0/TP1.5-2.5 | 0.396 (335) | 0.115 | %42.1 (114) | 1.18 | %1.26 | %2.66 | 2 |
| 4 | Kazanan ortak noktaları kuralı (skor ≥55 / ≤45 VE RSI (yön, 50 merkez) ≥ 16.76 VE Momentum (yön) ≤ 0.14 VE ATR % ≤ 2.50), fiyatın 0.5 ATR gerisine limit emirle giriş (6 mum geçerli), SL1.0/TP1.5-2.5 | 0.424 (292) | 0.15 | %45.0 (100) | 1.15 | %0.6 | %1.2 | 0 |
| 5 | Kazanan ortak noktaları kuralı (skor ≥55 / ≤45 VE RSI (yön, 50 merkez) ≥ 13.38 VE Momentum (yön) ≤ 0.09 VE Agresif alım-satım (yön) ≤ 0.02), SL1.0/TP1.5-2.5 | 0.29 (604) | -0.019 | %39.2 (158) | 0.82 | %-1.32 | %-2.61 | 2 |

### 4h — 194 strateji denendi · ✅ kazanan benimsendi

Mevcut (trend, filtresiz) TEST: 196 işlem, kazanma %54.1, ort R 0.109, PF 1.03

| # | Strateji | Eğitim ort R (n) | TEST ort R | TEST kazanma | TEST PF | 5x ort ROE | 10x ort ROE | 10x likidasyon |
|---|---|---|---|---|---|---|---|---|
| 1 | Trend takibi (skor ≥58 / ≤42), SL1.0/TP1.5-2.5 | 0.14 (544) | 0.162 | %45.2 (219) | 1.13 | %1.14 | %2.43 | 2 |
| 2 | Trend takibi (skor ≥66 / ≤34), SL1.0/TP1.5-2.5 | 0.14 (544) | 0.162 | %45.2 (219) | 1.13 | %1.14 | %2.43 | 2 |
| 3 | Trend takibi (skor ≥58 / ≤42) +üst trend yönünde, SL1.0/TP1.5-2.5 | 0.139 (546) | 0.162 | %45.2 (219) | 1.13 | %1.12 | %2.38 | 2 |
| 4 | Trend takibi (skor ≥66 / ≤34) +üst trend yönünde, SL1.0/TP1.5-2.5 | 0.139 (546) | 0.162 | %45.2 (219) | 1.13 | %1.12 | %2.38 | 2 |
| 5 | Trend takibi (skor ≥74 / ≤26), SL1.0/TP1.5-2.5 | 0.143 (515) | 0.164 | %45.4 (216) | 1.13 | %1.14 | %2.43 | 2 |


## 5. 15m (piyasa girişli): kazananlar ve kaybedenler

Tüm olaylar: kazanma %40.2 (eğitim) / %40.0 (test); ort. net R -0.134 / -0.138

**Kazanan vs kaybeden girişte o anki durum** (etki = standart fark; ✓ = test döneminde de aynı yönde)

| Özellik | Kazananlarda | Kaybedenlerde | Etki (eğitim) | Etki (test) | |
|---|---|---|---|---|---|
| BTC 1s yönü (yön) | 0.144 | 0.19 | -0.047 | -0.029 | ✗ |
| Z-Score (yön) | 0.835 | 0.879 | -0.044 | -0.005 | ✗ |
| Dip-tepe konumu (yön) | 0.718 | 0.724 | -0.035 | +0.011 | ✗ |
| Üst trend (yön) | 0.684 | 0.666 | +0.034 | -0.000 | ✗ |
| VWAP bileşeni (yön) | 0.702 | 0.69 | +0.033 | +0.037 | ✓ |
| Momentum (yön) | 0.241 | 0.255 | -0.032 | -0.007 | ✗ |
| RSI (yön, 50 merkez) | 8.771 | 9.022 | -0.032 | +0.021 | ✗ |
| Agresif alım-satım (yön) | 0.014 | 0.015 | -0.026 | +0.032 | ✗ |
| Trend (yön) | 0.783 | 0.775 | +0.024 | -0.004 | ✗ |
| Hacim (yön) | 0.168 | 0.175 | -0.024 | +0.029 | ✗ |

| Kural | Eğitim ort R (n) | Eğitim 1./2. yarı | TEST olay ort R (n) |
|---|---|---|---|
| Z-Score (yön) ≤ -0.52 VE ATR % ≥ 0.48 VE FVG+Likidite (yön) ≤ 0.00 | 0.108 (6902) | 0.141 / 0.076 | -0.079 (2801) |
| Z-Score (yön) ≤ -0.52 VE ATR % ≥ 0.48 VE Saat (UTC) ≥ 12.00 | 0.094 (7355) | 0.17 / 0.033 | -0.14 (3089) |
| ATR % ≥ 1.26 VE Z-Score (yön) ≤ 0.68 VE FVG+Likidite (yön) ≥ 0.00 | 0.077 (6801) | 0.1 / 0.06 | -0.101 (1808) |
| Z-Score (yön) ≤ -0.52 VE ATR % ≥ 0.39 VE VWAP bileşeni (yön) ≥ 0.83 | 0.074 (6564) | 0.13 / 0.024 | 0.124 (2194) |
| ATR % ≥ 1.26 VE Z-Score (yön) ≤ 0.68 | 0.044 (8241) | 0.05 / 0.039 | -0.054 (2270) |

## 5. 15m (limit girişli): kazananlar ve kaybedenler

Tüm olaylar: kazanma %40.6 (eğitim) / %39.2 (test); ort. net R -0.123 / -0.16

**Kazanan vs kaybeden girişte o anki durum** (etki = standart fark; ✓ = test döneminde de aynı yönde)

| Özellik | Kazananlarda | Kaybedenlerde | Etki (eğitim) | Etki (test) | |
|---|---|---|---|---|---|
| VWAP bileşeni (yön) | 0.707 | 0.689 | +0.051 | +0.010 | ✗ |
| Z-Score (yön) | 0.881 | 0.922 | -0.040 | -0.004 | ✗ |
| RSI (yön, 50 merkez) | 9.036 | 9.329 | -0.036 | -0.005 | ✗ |
| BTC 1s yönü (yön) | 0.181 | 0.213 | -0.032 | -0.050 | ✓ |
| Dip-tepe konumu (yön) | 0.723 | 0.729 | -0.031 | -0.021 | ✗ |
| Momentum (yön) | 0.258 | 0.27 | -0.029 | -0.012 | ✗ |
| Agresif alım-satım (yön) | 0.014 | 0.016 | -0.029 | +0.017 | ✗ |
| ATR % | 0.753 | 0.736 | +0.029 | +0.005 | ✗ |
| Hacim (yön) | 0.174 | 0.183 | -0.028 | +0.026 | ✗ |
| Trend (yön) | 0.783 | 0.774 | +0.025 | -0.023 | ✗ |

| Kural | Eğitim ort R (n) | Eğitim 1./2. yarı | TEST olay ort R (n) |
|---|---|---|---|
| ATR % ≥ 1.25 VE Z-Score (yön) ≤ 0.98 VE Saat (UTC) ≥ 9.00 | 0.098 (5221) | 0.14 / 0.067 | -0.005 (1419) |
| ATR % ≥ 1.25 VE Z-Score (yön) ≤ 0.98 VE Momentum (yön) ≥ -0.37 | 0.084 (6426) | 0.081 / 0.086 | -0.04 (1743) |
| ATR % ≥ 1.25 VE Z-Score (yön) ≤ 0.73 VE FVG+Likidite (yön) ≥ 0.00 | 0.082 (4974) | 0.094 / 0.073 | -0.127 (1360) |
| ATR % ≥ 1.25 VE Dip-tepe konumu (yön) ≤ 0.70 VE Saat (UTC) ≥ 4.00 | 0.082 (4932) | 0.091 / 0.075 | 0.055 (1219) |
| ATR % ≥ 1.25 VE Dip-tepe konumu (yön) ≤ 0.70 VE Momentum (yön) ≥ -0.37 | 0.082 (4884) | 0.081 / 0.083 | 0.04 (1200) |

## 5. 1h (piyasa girişli): kazananlar ve kaybedenler

Tüm olaylar: kazanma %41.5 (eğitim) / %42.6 (test); ort. net R -0.012 / 0.021

**Kazanan vs kaybeden girişte o anki durum** (etki = standart fark; ✓ = test döneminde de aynı yönde)

| Özellik | Kazananlarda | Kaybedenlerde | Etki (eğitim) | Etki (test) | |
|---|---|---|---|---|---|
| VWAP bileşeni (yön) | 0.435 | 0.401 | +0.092 | -0.017 | ✗ |
| VWAP'tan uzaklık ATR (yön) | 1.146 | 1.059 | +0.080 | +0.007 | ✗ |
| Likidite avı (yön) | -0.25 | -0.206 | -0.075 | +0.071 | ✗ |
| RSI (yön, 50 merkez) | 10.402 | 9.812 | +0.074 | -0.033 | ✗ |
| Üst trend (yön) | 0.655 | 0.631 | +0.047 | +0.099 | ✓ |
| Agresif alım-satım (yön) | 0.008 | 0.009 | -0.046 | +0.032 | ✗ |
| Hacim (yön) | 0.172 | 0.162 | +0.045 | -0.016 | ✗ |
| Z-Score (yön) | 1.016 | 0.978 | +0.041 | -0.060 | ✗ |
| Trend (yön) | 0.761 | 0.745 | +0.040 | +0.085 | ✓ |
| FVG+Likidite (yön) | -0.015 | 0.001 | -0.040 | +0.101 | ✗ |

| Kural | Eğitim ort R (n) | Eğitim 1./2. yarı | TEST olay ort R (n) |
|---|---|---|---|
| RSI (yön, 50 merkez) ≥ 13.38 VE Momentum (yön) ≤ 0.09 VE Agresif alım-satım (yön) ≤ 0.02 | 0.333 (2147) | 0.465 / 0.2 | -0.011 (403) |
| RSI (yön, 50 merkez) ≥ 13.38 VE Momentum (yön) ≤ 0.09 | 0.277 (2975) | 0.376 / 0.174 | -0.061 (688) |
| RSI (yön, 50 merkez) ≥ 13.38 VE Agresif alım-satım (yön) ≤ -0.01 VE RVOL ≤ 1.13 | 0.341 (1931) | 0.457 / 0.211 | 0.041 (411) |
| RSI (yön, 50 merkez) ≥ 16.42 VE Momentum (yön) ≤ 0.09 VE ATR % ≤ 2.51 | 0.337 (1818) | 0.451 / 0.212 | -0.11 (369) |
| RSI (yön, 50 merkez) ≥ 13.38 VE Agresif alım-satım (yön) ≤ -0.01 | 0.258 (3045) | 0.351 / 0.155 | 0.007 (632) |

## 5. 1h (limit girişli): kazananlar ve kaybedenler

Tüm olaylar: kazanma %42.4 (eğitim) / %40.3 (test); ort. net R 0.01 / -0.046

**Kazanan vs kaybeden girişte o anki durum** (etki = standart fark; ✓ = test döneminde de aynı yönde)

| Özellik | Kazananlarda | Kaybedenlerde | Etki (eğitim) | Etki (test) | |
|---|---|---|---|---|---|
| VWAP bileşeni (yön) | 0.437 | 0.407 | +0.081 | -0.080 | ✗ |
| RSI (yön, 50 merkez) | 10.619 | 9.992 | +0.078 | -0.069 | ✗ |
| VWAP'tan uzaklık ATR (yön) | 1.164 | 1.08 | +0.076 | -0.044 | ✗ |
| Likidite avı (yön) | -0.247 | -0.211 | -0.060 | +0.069 | ✗ |
| Hacim (yön) | 0.174 | 0.163 | +0.044 | -0.030 | ✗ |
| Z-Score (yön) | 1.048 | 1.006 | +0.044 | -0.095 | ✗ |
| Üst trend (yön) | 0.655 | 0.636 | +0.036 | +0.099 | ✓ |
| ATR % | 1.553 | 1.52 | +0.033 | -0.007 | ✗ |
| Agresif alım-satım (yön) | 0.008 | 0.01 | -0.032 | +0.010 | ✗ |
| FVG+Likidite (yön) | -0.014 | -0.002 | -0.031 | +0.075 | ✗ |

| Kural | Eğitim ort R (n) | Eğitim 1./2. yarı | TEST olay ort R (n) |
|---|---|---|---|
| RSI (yön, 50 merkez) ≥ 16.76 VE Momentum (yön) ≤ 0.14 VE ATR % ≥ 0.63 | 0.382 (1396) | 0.442 / 0.321 | 0.092 (296) |
| RSI (yön, 50 merkez) ≥ 16.76 VE Momentum (yön) ≤ 0.14 VE ATR % ≤ 2.50 | 0.398 (1203) | 0.501 / 0.283 | 0.015 (266) |
| RSI (yön, 50 merkez) ≥ 16.76 VE Momentum (yön) ≤ 0.14 VE RVOL ≤ 1.47 | 0.381 (1220) | 0.434 / 0.327 | 0.059 (253) |
| Dip-tepe konumu (yön) ≤ 0.49 VE VWAP bileşeni (yön) ≥ 0.25 VE ATR % ≥ 0.63 | 0.384 (1171) | 0.208 / 0.534 | -0.129 (388) |
| Dip-tepe konumu (yön) ≤ 0.49 VE VWAP'tan uzaklık ATR (yön) ≥ 0.50 VE ATR % ≥ 0.63 | 0.384 (1171) | 0.208 / 0.534 | -0.129 (388) |

IC (bilgi katsayısı): gösterge puanı ile sonraki getiri arasındaki sıralama korelasyonu. Piyasada 0.02–0.05 bile anlamlıdır; negatif ise gösterge ters çalışıyor demektir.
Geçmiş performans geleceği garanti etmez.