# V5 Araştırma Raporu — 15.11.2026 08:13 UTC

40 coin · değerlendirme 17.08.2026'dan bugüne (90 gün) · eğitim/TEST ayrımı 19.10.2026

## 1. Mevcut model: kaldıraçlı işlem sonuçları (tüm dönem)

| Periyot | Kaldıraç | İşlem | Kazanma | Ort. ROE | PF | Ort. R | Likidasyon | 100$ marjla net | Maks. DD |
|---|---|---|---|---|---|---|---|---|---|
| 15m | 5x | 29716 | %49.6 | %-0.44 | 0.86 | 0.009 | 0 | -12978.0$ | 15990.0$ |
| 15m | 10x | 29721 | %49.6 | %-0.89 | 0.86 | 0.009 | 19 | -26334.0$ | 32165.0$ |
| 30m | 5x | 14322 | %50.7 | %-0.27 | 0.94 | 0.028 | 0 | -3796.0$ | 7366.0$ |
| 30m | 10x | 14334 | %50.7 | %-0.56 | 0.93 | 0.028 | 28 | -8077.0$ | 14942.0$ |
| 1h | 5x | 7103 | %50.7 | %-0.1 | 0.98 | 0.036 | 1 | -699.0$ | 4248.0$ |
| 1h | 10x | 7118 | %50.6 | %-0.3 | 0.98 | 0.036 | 35 | -2125.0$ | 9040.0$ |
| 4h | 5x | 1872 | %55.9 | %2.35 | 1.22 | 0.157 | 4 | 4407.0$ | 1963.0$ |
| 4h | 10x | 1882 | %55.6 | %4.63 | 1.22 | 0.157 | 36 | 8722.0$ | 4027.0$ |

PF = kâr faktörü (toplam kazanç / toplam kayıp, 1 üstü kârlı). R = risk birimi (stop mesafesi).

## 2. Göstergelerin doğruluğu (TEST dönemi)

### 15m

| Bileşen | IC | İsabet | ↑ dediğinde yükseldi | ↓ dediğinde düştü | İşlemde aynı yöndeyken kazanma | Ters yöndeyken kazanma |
|---|---|---|---|---|---|---|
| Trend | -0.066 | %47.4 | %41.4 | %51.2 | %48.7 (7236) | %58.7 (303) |
| Momentum | -0.013 | %48.3 | %44.2 | %52.9 | %49.4 (5529) | %48.2 (1455) |
| Hacim | -0.018 | %49.6 | %45.2 | %52.0 | %50.8 (4934) | %45.5 (770) |
| Funding+L/S | -0.02 | %40.2 | %40.2 | %- | %47.0 (457) | %46.6 (551) |
| FVG+Likidite avı | -0.009 | %50.0 | %46.1 | %54.4 | %49.4 (3414) | %49.1 (2724) |
| VWAP | -0.025 | %47.8 | %42.0 | %52.2 | %49.0 (7739) | %51.3 (390) |

Ham göstergeler (IC, büyükten küçüğe): EMA dizilimi -0.079, Üst periyot trendi -0.067, Fiyat>EMA200 -0.059, VWAP üstü/altı -0.045, RSI -0.037, Z-Score -0.025, FVG -0.022, Bollinger sıkışma -0.014, MACD yönü -0.009, OBV yönü -0.009

### 30m

| Bileşen | IC | İsabet | ↑ dediğinde yükseldi | ↓ dediğinde düştü | İşlemde aynı yöndeyken kazanma | Ters yöndeyken kazanma |
|---|---|---|---|---|---|---|
| Trend | -0.086 | %49.1 | %40.1 | %53.3 | %47.0 (3444) | %51.1 (223) |
| Momentum | -0.036 | %47.3 | %41.8 | %53.3 | %49.7 (2875) | %47.1 (535) |
| Hacim | -0.073 | %47.7 | %39.3 | %51.4 | %47.8 (2407) | %47.3 (220) |
| Funding+L/S | -0.042 | %35.5 | %35.5 | %- | %42.6 (190) | %45.1 (284) |
| FVG+Likidite avı | 0.013 | %51.8 | %45.9 | %59.0 | %49.4 (1630) | %47.6 (1390) |
| VWAP | -0.038 | %47.6 | %39.9 | %53.3 | %47.0 (3492) | %56.3 (190) |

Ham göstergeler (IC, büyükten küçüğe): Üst periyot trendi -0.080, EMA dizilimi -0.073, OBV yönü -0.072, Fiyat>EMA200 -0.071, RSI -0.064, Z-Score -0.062, VWAP üstü/altı -0.056, MACD yönü -0.034, Likidite avı +0.034, FVG -0.024

### 1h

| Bileşen | IC | İsabet | ↑ dediğinde yükseldi | ↓ dediğinde düştü | İşlemde aynı yöndeyken kazanma | Ters yöndeyken kazanma |
|---|---|---|---|---|---|---|
| Trend | -0.081 | %50.8 | %37.7 | %55.2 | %50.3 (1661) | %50.0 (96) |
| Momentum | -0.055 | %46.3 | %38.8 | %54.5 | %48.6 (1469) | %56.7 (203) |
| Hacim | -0.068 | %48.4 | %37.5 | %51.9 | %48.5 (1165) | %63.2 (68) |
| Funding+L/S | -0.085 | %35.0 | %35.0 | %- | %32.5 (80) | %46.0 (150) |
| FVG+Likidite avı | 0.044 | %53.6 | %44.3 | %65.7 | %53.4 (830) | %45.2 (644) |
| VWAP | -0.05 | %47.7 | %38.5 | %54.4 | %46.6 (1503) | %68.3 (183) |

Ham göstergeler (IC, büyükten küçüğe): Fiyat>EMA200 -0.094, RSI -0.093, Üst periyot trendi -0.080, EMA dizilimi -0.074, Z-Score -0.063, Taker alım -0.060, Funding +0.058, Likidite avı +0.049, VWAP üstü/altı -0.043, OBV yönü -0.019

### 4h

| Bileşen | IC | İsabet | ↑ dediğinde yükseldi | ↓ dediğinde düştü | İşlemde aynı yöndeyken kazanma | Ters yöndeyken kazanma |
|---|---|---|---|---|---|---|
| Trend | -0.102 | %55.3 | %34.6 | %58.3 | %57.9 (404) | %42.3 (26) |
| Momentum | -0.15 | %43.6 | %35.3 | %51.7 | %50.6 (342) | %70.7 (58) |
| Hacim | -0.158 | %48.2 | %26.3 | %51.9 | %52.2 (224) | %63.2 (19) |
| Funding+L/S | -0.063 | %36.7 | %36.7 | %- | %35.7 (14) | %56.0 (50) |
| FVG+Likidite avı | 0.083 | %55.2 | %47.2 | %67.5 | %58.4 (219) | %50.0 (164) |
| VWAP | -0.144 | %48.9 | %29.1 | %56.6 | %49.6 (341) | %64.9 (37) |

Ham göstergeler (IC, büyükten küçüğe): Z-Score -0.186, RSI -0.158, VWAP üstü/altı -0.129, Likidite avı +0.117, OBV yönü -0.103, Bollinger sıkışma +0.097, Taker alım -0.097, RVOL +0.095, MACD yönü -0.087, Fiyat>EMA200 -0.073

## 3. Öğrenme: yeni ağırlıklar (eğitimde bulundu, TEST'te sınandı)

| Periyot | Yöntem | Eşik | Mevcut model TEST ort. R / kazanma | Yeni model TEST ort. R / kazanma | Karar |
|---|---|---|---|---|---|
| 15m | IC± | 74/26 | 0.01 / %49.7 (9065) | 0.013 / %49.0 (2004) | ✅ benimsendi |
| 30m | IC± | 62/38 | -0.02 / %48.1 (4394) | -0.049 / %46.6 (3483) | ❌ mevcut kalır |
| 1h | IC+ | 70/30 | 0.024 / %50.1 (2131) | 0.019 / %49.9 (1614) | ❌ mevcut kalır |
| 4h | mevcut | 58/42 | 0.115 / %54.0 (506) | 0.086 / %53.0 (521) | ❌ mevcut kalır |

Ağırlıklar:
- 15m: Momentum -34.7, Hacim -19.8, Funding+L/S -18.1, FVG+Likidite avı 10.1, VWAP 13.2
- 30m: Trend 9.9, Momentum -38.7, Funding+L/S -20.1, VWAP 22.1
- 1h: Trend 3.3, Momentum 10.6, Hacim 45.1, VWAP 41.0
- 4h: Trend 20, Momentum 18, Open Interest 15, Hacim 10, Funding+L/S 10, FVG+Likidite avı 10, VWAP 5

## 4. Strateji yarışması (yalnız canlı botun da görebildiği veriler; eğitimde seçildi, TEST'te sınandı)

### 15m — 173 strateji denendi · ❌ hiçbiri yeterince iyi değil, mevcut kalır

Mevcut (trend, filtresiz) TEST: 2991 işlem, kazanma %47.7, ort R -0.021, PF 0.81

| # | Strateji | Eğitim ort R (n) | TEST ort R | TEST kazanma | TEST PF | 5x ort ROE | 10x ort ROE | 10x likidasyon |
|---|---|---|---|---|---|---|---|---|
| 1 | Kazanan ortak noktaları kuralı (skor ≥55 / ≤45 VE Z-Score (yön) ≤ -0.52 VE ATR % ≥ 0.48 VE FVG+Likidite (yön) ≤ 0.00), SL1.0/TP1.5-2.5 | 0.157 (2490) | -0.047 | %37.8 (1018) | 0.78 | %-0.68 | %-1.37 | 0 |
| 2 | Kazanan ortak noktaları kuralı (skor ≥55 / ≤45 VE Z-Score (yön) ≤ -0.52 VE ATR % ≥ 0.39), SL1.0/TP1.5-2.5 | 0.107 (4308) | -0.015 | %39.1 (1785) | 0.76 | %-0.72 | %-1.43 | 1 |
| 3 | Kazanan ortak noktaları kuralı (skor ≥55 / ≤45 VE Z-Score (yön) ≤ -0.52 VE ATR % ≥ 0.48 VE Saat (UTC) ≥ 12.00), SL1.0/TP1.5-2.5 | 0.147 (2051) | -0.023 | %38.5 (855) | 0.8 | %-0.64 | %-1.28 | 1 |
| 4 | Kazanan ortak noktaları kuralı (skor ≥55 / ≤45 VE Z-Score (yön) ≤ -0.52 VE ATR % ≥ 0.39 VE VWAP bileşeni (yön) ≥ 0.84), SL1.0/TP1.5-2.5 | 0.15 (1732) | 0.141 | %44.8 (683) | 1.02 | %0.04 | %0.08 | 0 |
| 5 | Kazanan ortak noktaları kuralı (skor ≥55 / ≤45 VE Z-Score (yön) ≤ -0.52 VE ATR % ≥ 0.39 VE VWAP'tan uzaklık ATR (yön) ≥ 2.41), SL1.0/TP1.5-2.5 | 0.15 (1732) | 0.141 | %44.8 (683) | 1.02 | %0.04 | %0.08 | 0 |

### 30m — 163 strateji denendi · ❌ hiçbiri yeterince iyi değil, mevcut kalır

Mevcut (trend, filtresiz) TEST: 1469 işlem, kazanma %50.2, ort R 0.015, PF 0.92

| # | Strateji | Eğitim ort R (n) | TEST ort R | TEST kazanma | TEST PF | 5x ort ROE | 10x ort ROE | 10x likidasyon |
|---|---|---|---|---|---|---|---|---|
| 1 | Geri çekilmede limit giriş (skor ≥66 / ≤34, dip-tepe aralığının en fazla %50'inde, fiyatın 1.0 ATR gerisine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) | 0.126 (553) | -0.061 | %37.8 (230) | 0.89 | %-0.4 | %-0.8 | 0 |
| 2 | Geri çekilmede limit giriş (skor ≥58 / ≤42, dip-tepe aralığının en fazla %70'inde, 0.382 Fibonacci geri çekilmesine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) | 0.073 (1630) | 0.023 | %41.4 (672) | 0.93 | %-0.4 | %-0.98 | 5 |
| 3 | Geri çekilmede limit giriş (skor ≥66 / ≤34, dip-tepe aralığının en fazla %50'inde, fiyatın 1.0 ATR gerisine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) +üst trend yönünde | 0.122 (542) | -0.069 | %37.7 (223) | 0.89 | %-0.39 | %-0.77 | 0 |
| 4 | Geri çekilmede limit giriş (skor ≥66 / ≤34, dip-tepe aralığının en fazla %70'inde, fiyatın 1.0 ATR gerisine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) +üst trend yönünde | 0.075 (1257) | -0.034 | %39.8 (525) | 0.85 | %-0.68 | %-1.17 | 1 |
| 5 | Geri çekilmede limit giriş (skor ≥66 / ≤34, dip-tepe aralığının en fazla %70'inde, fiyatın 1.0 ATR gerisine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) | 0.073 (1263) | -0.013 | %40.6 (540) | 0.87 | %-0.61 | %-1.04 | 1 |

### 1h — 173 strateji denendi · ❌ hiçbiri yeterince iyi değil, mevcut kalır

Mevcut (trend, filtresiz) TEST: 752 işlem, kazanma %52.1, ort R 0.076, PF 1.06

| # | Strateji | Eğitim ort R (n) | TEST ort R | TEST kazanma | TEST PF | 5x ort ROE | 10x ort ROE | 10x likidasyon |
|---|---|---|---|---|---|---|---|---|
| 1 | Kazanan ortak noktaları kuralı (skor ≥55 / ≤45 VE RSI (yön, 50 merkez) ≥ 16.53 VE Momentum (yön) ≤ 0.09 VE RVOL ≤ 1.14), SL1.0/TP1.5-2.5 | 0.418 (434) | -0.144 | %35.0 (123) | 0.58 | %-2.59 | %-5.18 | 1 |
| 2 | Kazanan ortak noktaları kuralı (skor ≥55 / ≤45 VE RSI (yön, 50 merkez) ≥ 16.53 VE Momentum (yön) ≤ 0.09 VE ATR % ≤ 2.07), SL1.0/TP1.5-2.5 | 0.434 (382) | -0.09 | %37.0 (119) | 0.78 | %-0.96 | %-1.92 | 0 |
| 3 | Kazanan ortak noktaları kuralı (skor ≥55 / ≤45 VE RSI (yön, 50 merkez) ≥ 16.87 VE Momentum (yön) ≤ 0.14 VE ATR % ≥ 0.62), fiyatın 0.5 ATR gerisine limit emirle giriş (6 mum geçerli), SL1.0/TP1.5-2.5 | 0.447 (337) | 0.114 | %42.5 (113) | 1.12 | %0.84 | %1.83 | 2 |
| 4 | Kazanan ortak noktaları kuralı (skor ≥55 / ≤45 VE RSI (yön, 50 merkez) ≥ 16.53 VE Momentum (yön) ≤ 0.09 VE Hacim (yön) ≤ 0.36), SL1.0/TP1.5-2.5 | 0.369 (466) | -0.137 | %34.6 (104) | 0.52 | %-3.73 | %-7.78 | 3 |
| 5 | Kazanan ortak noktaları kuralı (skor ≥55 / ≤45 VE RSI (yön, 50 merkez) ≥ 16.87 VE Momentum (yön) ≤ 0.14), fiyatın 0.5 ATR gerisine limit emirle giriş (6 mum geçerli), SL1.0/TP1.5-2.5 | 0.411 (354) | 0.138 | %44.3 (122) | 1.12 | %0.81 | %1.75 | 2 |

### 4h — 151 strateji denendi · ✅ kazanan benimsendi

Mevcut (trend, filtresiz) TEST: 194 işlem, kazanma %55.7, ort R 0.139, PF 1.05

| # | Strateji | Eğitim ort R (n) | TEST ort R | TEST kazanma | TEST PF | 5x ort ROE | 10x ort ROE | 10x likidasyon |
|---|---|---|---|---|---|---|---|---|
| 1 | Trend takibi (skor ≥58 / ≤42) +üst trend yönünde, SL1.0/TP1.5-2.5 | 0.151 (534) | 0.16 | %45.0 (222) | 1.11 | %0.95 | %2.05 | 2 |
| 2 | Trend takibi (skor ≥66 / ≤34) +üst trend yönünde, SL1.0/TP1.5-2.5 | 0.151 (534) | 0.16 | %45.0 (222) | 1.11 | %0.95 | %2.05 | 2 |
| 3 | Trend takibi (skor ≥74 / ≤26) +üst trend yönünde, SL1.0/TP1.5-2.5 | 0.151 (499) | 0.149 | %44.5 (220) | 1.12 | %0.99 | %2.12 | 2 |
| 4 | Trend takibi (skor ≥74 / ≤26), SL1.0/TP1.5-2.5 | 0.144 (503) | 0.149 | %44.5 (220) | 1.12 | %1.01 | %2.17 | 2 |
| 5 | Trend takibi (skor ≥58 / ≤42), SL1.0/TP1.5-2.5 | 0.138 (537) | 0.16 | %45.0 (222) | 1.12 | %1.04 | %2.22 | 2 |


## 5. 15m (piyasa girişli): kazananlar ve kaybedenler

Tüm olaylar: kazanma %40.3 (eğitim) / %39.8 (test); ort. net R -0.133 / -0.146

**Kazanan vs kaybeden girişte o anki durum** (etki = standart fark; ✓ = test döneminde de aynı yönde)

| Özellik | Kazananlarda | Kaybedenlerde | Etki (eğitim) | Etki (test) | |
|---|---|---|---|---|---|
| BTC 1s yönü (yön) | 0.145 | 0.195 | -0.051 | -0.030 | ✓ |
| Z-Score (yön) | 0.831 | 0.882 | -0.050 | -0.008 | ✗ |
| Momentum (yön) | 0.238 | 0.256 | -0.039 | -0.005 | ✗ |
| Dip-tepe konumu (yön) | 0.717 | 0.724 | -0.038 | -0.001 | ✗ |
| Üst trend (yön) | 0.683 | 0.666 | +0.035 | -0.009 | ✗ |
| VWAP bileşeni (yön) | 0.703 | 0.691 | +0.034 | +0.023 | ✗ |
| RSI (yön, 50 merkez) | 8.763 | 9.025 | -0.033 | +0.011 | ✗ |
| Trend (yön) | 0.783 | 0.775 | +0.026 | -0.012 | ✗ |
| Hacim (yön) | 0.169 | 0.176 | -0.023 | +0.027 | ✗ |
| Agresif alım-satım (yön) | 0.014 | 0.015 | -0.019 | +0.038 | ✗ |

| Kural | Eğitim ort R (n) | Eğitim 1./2. yarı | TEST olay ort R (n) |
|---|---|---|---|
| Z-Score (yön) ≤ -0.52 VE ATR % ≥ 0.48 VE FVG+Likidite (yön) ≤ 0.00 | 0.124 (6817) | 0.165 / 0.084 | -0.117 (2762) |
| Z-Score (yön) ≤ -0.52 VE ATR % ≥ 0.48 VE Saat (UTC) ≥ 12.00 | 0.102 (7350) | 0.175 / 0.043 | -0.14 (3065) |
| Z-Score (yön) ≤ -0.52 VE ATR % ≥ 0.39 VE VWAP bileşeni (yön) ≥ 0.84 | 0.105 (6540) | 0.164 / 0.051 | 0.1 (2168) |
| Z-Score (yön) ≤ -0.52 VE ATR % ≥ 0.39 VE VWAP'tan uzaklık ATR (yön) ≥ 2.41 | 0.105 (6540) | 0.164 / 0.051 | 0.1 (2168) |
| Z-Score (yön) ≤ -0.52 VE ATR % ≥ 0.39 | 0.047 (17318) | 0.092 / 0.006 | -0.079 (7024) |

## 5. 15m (limit girişli): kazananlar ve kaybedenler

Tüm olaylar: kazanma %40.7 (eğitim) / %39.3 (test); ort. net R -0.121 / -0.161

**Kazanan vs kaybeden girişte o anki durum** (etki = standart fark; ✓ = test döneminde de aynı yönde)

| Özellik | Kazananlarda | Kaybedenlerde | Etki (eğitim) | Etki (test) | |
|---|---|---|---|---|---|
| VWAP bileşeni (yön) | 0.708 | 0.689 | +0.052 | -0.002 | ✗ |
| Z-Score (yön) | 0.877 | 0.925 | -0.047 | -0.010 | ✗ |
| RSI (yön, 50 merkez) | 9.027 | 9.329 | -0.038 | -0.015 | ✗ |
| Momentum (yön) | 0.255 | 0.271 | -0.035 | -0.015 | ✗ |
| BTC 1s yönü (yön) | 0.184 | 0.218 | -0.035 | -0.050 | ✓ |
| Hacim (yön) | 0.174 | 0.184 | -0.033 | +0.021 | ✗ |
| Dip-tepe konumu (yön) | 0.723 | 0.729 | -0.032 | -0.033 | ✓ |
| Agresif alım-satım (yön) | 0.014 | 0.016 | -0.029 | +0.020 | ✗ |
| Trend (yön) | 0.783 | 0.774 | +0.024 | -0.028 | ✗ |
| Likidite avı (yön) | -0.202 | -0.216 | +0.024 | +0.009 | ✗ |

| Kural | Eğitim ort R (n) | Eğitim 1./2. yarı | TEST olay ort R (n) |
|---|---|---|---|
| ATR % ≥ 1.27 VE Z-Score (yön) ≤ 0.98 VE Saat (UTC) ≥ 9.00 | 0.092 (5177) | 0.138 / 0.053 | -0.035 (1390) |
| ATR % ≥ 1.27 VE Saat (UTC) ≥ 14.00 VE Hacim (yön) ≤ 0.33 | 0.085 (5544) | 0.106 / 0.068 | -0.06 (1730) |
| ATR % ≥ 1.27 VE Saat (UTC) ≥ 14.00 VE Üst trend (yön) ≥ 1.00 | 0.086 (5264) | 0.147 / 0.042 | -0.0 (1911) |
| ATR % ≥ 1.27 VE Saat (UTC) ≥ 14.00 VE Trend (yön) ≥ 1.00 | 0.08 (5067) | 0.132 / 0.044 | -0.003 (1837) |
| ATR % ≥ 1.27 VE Saat (UTC) ≥ 16.00 VE Agresif alım-satım (yön) ≤ 0.06 | 0.076 (5157) | 0.144 / 0.022 | -0.072 (1806) |

## 5. 1h (piyasa girişli): kazananlar ve kaybedenler

Tüm olaylar: kazanma %41.5 (eğitim) / %42.3 (test); ort. net R -0.012 / 0.012

**Kazanan vs kaybeden girişte o anki durum** (etki = standart fark; ✓ = test döneminde de aynı yönde)

| Özellik | Kazananlarda | Kaybedenlerde | Etki (eğitim) | Etki (test) | |
|---|---|---|---|---|---|
| VWAP bileşeni (yön) | 0.438 | 0.401 | +0.102 | -0.031 | ✗ |
| VWAP'tan uzaklık ATR (yön) | 1.157 | 1.059 | +0.091 | -0.008 | ✗ |
| RSI (yön, 50 merkez) | 10.49 | 9.818 | +0.084 | -0.053 | ✗ |
| Likidite avı (yön) | -0.25 | -0.205 | -0.076 | +0.077 | ✗ |
| Z-Score (yön) | 1.022 | 0.971 | +0.054 | -0.064 | ✗ |
| Hacim (yön) | 0.175 | 0.164 | +0.048 | -0.014 | ✗ |
| Dip-tepe konumu (yön) | 0.734 | 0.726 | +0.047 | +0.003 | ✗ |
| Agresif alım-satım (yön) | 0.008 | 0.009 | -0.045 | +0.047 | ✗ |
| FVG+Likidite (yön) | -0.014 | 0.003 | -0.044 | +0.107 | ✗ |
| Üst trend (yön) | 0.656 | 0.633 | +0.043 | +0.089 | ✓ |

| Kural | Eğitim ort R (n) | Eğitim 1./2. yarı | TEST olay ort R (n) |
|---|---|---|---|
| RSI (yön, 50 merkez) ≥ 13.47 VE Momentum (yön) ≤ 0.09 VE Agresif alım-satım (yön) ≤ 0.02 | 0.361 (2150) | 0.497 / 0.218 | -0.098 (374) |
| RSI (yön, 50 merkez) ≥ 13.47 VE Momentum (yön) ≤ 0.09 | 0.292 (2982) | 0.388 / 0.189 | -0.12 (653) |
| RSI (yön, 50 merkez) ≥ 16.53 VE Momentum (yön) ≤ 0.09 VE ATR % ≤ 2.07 | 0.37 (1565) | 0.463 / 0.258 | -0.154 (301) |
| RSI (yön, 50 merkez) ≥ 16.53 VE Momentum (yön) ≤ 0.09 VE RVOL ≤ 1.14 | 0.36 (1596) | 0.457 / 0.245 | -0.055 (294) |
| RSI (yön, 50 merkez) ≥ 16.53 VE Momentum (yön) ≤ 0.09 VE Hacim (yön) ≤ 0.36 | 0.347 (1621) | 0.487 / 0.203 | -0.123 (246) |

## 5. 1h (limit girişli): kazananlar ve kaybedenler

Tüm olaylar: kazanma %42.4 (eğitim) / %40.2 (test); ort. net R 0.01 / -0.052

**Kazanan vs kaybeden girişte o anki durum** (etki = standart fark; ✓ = test döneminde de aynı yönde)

| Özellik | Kazananlarda | Kaybedenlerde | Etki (eğitim) | Etki (test) | |
|---|---|---|---|---|---|
| VWAP bileşeni (yön) | 0.44 | 0.407 | +0.091 | -0.091 | ✗ |
| VWAP'tan uzaklık ATR (yön) | 1.174 | 1.079 | +0.086 | -0.057 | ✗ |
| RSI (yön, 50 merkez) | 10.689 | 9.999 | +0.085 | -0.079 | ✗ |
| Likidite avı (yön) | -0.244 | -0.209 | -0.059 | +0.081 | ✗ |
| Z-Score (yön) | 1.053 | 0.997 | +0.057 | -0.092 | ✗ |
| Hacim (yön) | 0.177 | 0.165 | +0.049 | -0.019 | ✗ |
| FVG+Likidite (yön) | -0.013 | 0.001 | -0.036 | +0.082 | ✗ |
| Üst trend (yön) | 0.656 | 0.638 | +0.035 | +0.101 | ✓ |
| Agresif alım-satım (yön) | 0.009 | 0.01 | -0.032 | +0.017 | ✗ |
| Trend (yön) | 0.76 | 0.752 | +0.020 | +0.086 | ✓ |

| Kural | Eğitim ort R (n) | Eğitim 1./2. yarı | TEST olay ort R (n) |
|---|---|---|---|
| RSI (yön, 50 merkez) ≥ 16.87 VE Momentum (yön) ≤ 0.14 VE ATR % ≥ 0.62 | 0.414 (1388) | 0.482 / 0.34 | 0.051 (284) |
| RSI (yön, 50 merkez) ≥ 21.30 VE Z-Score (yön) ≤ 1.81 VE ATR % ≥ 0.62 | 0.406 (1298) | 0.481 / 0.333 | 0.083 (392) |
| RSI (yön, 50 merkez) ≥ 16.87 VE Momentum (yön) ≤ 0.14 VE ATR % ≤ 2.52 | 0.407 (1212) | 0.521 / 0.273 | 0.01 (249) |
| RSI (yön, 50 merkez) ≥ 16.87 VE Momentum (yön) ≤ 0.14 | 0.37 (1461) | 0.44 / 0.295 | 0.035 (307) |
| Dip-tepe konumu (yön) ≤ 0.49 VE VWAP bileşeni (yön) ≥ 0.25 VE ATR % ≥ 0.62 | 0.41 (1166) | 0.245 / 0.554 | -0.145 (405) |

IC (bilgi katsayısı): gösterge puanı ile sonraki getiri arasındaki sıralama korelasyonu. Piyasada 0.02–0.05 bile anlamlıdır; negatif ise gösterge ters çalışıyor demektir.
Geçmiş performans geleceği garanti etmez.