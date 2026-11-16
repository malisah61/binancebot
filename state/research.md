# V5 Araştırma Raporu — 16.11.2026 09:56 UTC

40 coin · değerlendirme 18.08.2026'dan bugüne (90 gün) · eğitim/TEST ayrımı 20.10.2026

## 1. Mevcut model: kaldıraçlı işlem sonuçları (tüm dönem)

| Periyot | Kaldıraç | İşlem | Kazanma | Ort. ROE | PF | Ort. R | Likidasyon | 100$ marjla net | Maks. DD |
|---|---|---|---|---|---|---|---|---|---|
| 15m | 5x | 29098 | %50.2 | %-0.36 | 0.88 | 0.019 | 0 | -10547.0$ | 13514.0$ |
| 15m | 10x | 29107 | %50.1 | %-0.74 | 0.88 | 0.019 | 28 | -21619.0$ | 27336.0$ |
| 30m | 5x | 14308 | %50.7 | %-0.27 | 0.94 | 0.029 | 2 | -3827.0$ | 6703.0$ |
| 30m | 10x | 14328 | %50.7 | %-0.59 | 0.93 | 0.029 | 44 | -8384.0$ | 13841.0$ |
| 1h | 5x | 7133 | %51.0 | %0.04 | 1.01 | 0.041 | 1 | 310.0$ | 3104.0$ |
| 1h | 10x | 7159 | %50.9 | %-0.08 | 0.99 | 0.041 | 44 | -606.0$ | 6880.0$ |
| 4h | 5x | 1974 | %53.2 | %1.33 | 1.12 | 0.103 | 8 | 2626.0$ | 2213.0$ |
| 4h | 10x | 1986 | %52.9 | %2.72 | 1.12 | 0.105 | 54 | 5399.0$ | 4554.0$ |

PF = kâr faktörü (toplam kazanç / toplam kayıp, 1 üstü kârlı). R = risk birimi (stop mesafesi).

## 2. Göstergelerin doğruluğu (TEST dönemi)

### 15m

| Bileşen | IC | İsabet | ↑ dediğinde yükseldi | ↓ dediğinde düştü | İşlemde aynı yöndeyken kazanma | Ters yöndeyken kazanma |
|---|---|---|---|---|---|---|
| Trend | -0.063 | %47.7 | %41.5 | %51.2 | %49.9 (6903) | %59.6 (458) |
| Momentum | -0.011 | %48.4 | %44.8 | %52.5 | %50.2 (5812) | %51.2 (918) |
| Open Interest | -0.001 | %47.9 | %45.7 | %52.2 | %53.9 (2474) | %47.6 (319) |
| Hacim | -0.016 | %49.7 | %45.6 | %52.0 | %52.0 (4889) | %47.2 (657) |
| Funding+L/S | -0.019 | %46.5 | %45.9 | %54.3 | %47.0 (2033) | %53.8 (2502) |
| FVG+Likidite avı | -0.005 | %50.0 | %46.2 | %54.5 | %49.2 (3237) | %51.3 (2631) |
| VWAP | -0.018 | %48.5 | %42.8 | %52.4 | %50.3 (7466) | %50.7 (381) |

Ham göstergeler (IC, büyükten küçüğe): EMA dizilimi -0.074, Üst periyot trendi -0.065, Fiyat>EMA200 -0.056, RSI -0.039, VWAP üstü/altı -0.037, Z-Score -0.026, FVG -0.017, OI değişimi +0.017, OI rejimi -0.013, Top trader L/S +0.012

### 30m

| Bileşen | IC | İsabet | ↑ dediğinde yükseldi | ↓ dediğinde düştü | İşlemde aynı yöndeyken kazanma | Ters yöndeyken kazanma |
|---|---|---|---|---|---|---|
| Trend | -0.084 | %49.8 | %41.1 | %53.4 | %48.3 (3319) | %53.5 (344) |
| Momentum | -0.033 | %47.5 | %42.0 | %53.4 | %49.9 (3044) | %49.7 (302) |
| Open Interest | -0.017 | %47.0 | %44.6 | %50.8 | %49.3 (1763) | %43.1 (216) |
| Hacim | -0.075 | %47.6 | %39.5 | %51.1 | %48.3 (2426) | %54.0 (215) |
| Funding+L/S | -0.026 | %45.2 | %44.6 | %54.3 | %45.8 (937) | %50.0 (1343) |
| FVG+Likidite avı | 0.018 | %52.2 | %46.6 | %59.5 | %50.3 (1551) | %48.4 (1352) |
| VWAP | -0.029 | %48.5 | %40.8 | %53.7 | %48.3 (3541) | %50.0 (142) |

Ham göstergeler (IC, büyükten küçüğe): Üst periyot trendi -0.076, EMA dizilimi -0.069, OBV yönü -0.069, Fiyat>EMA200 -0.063, RSI -0.063, Z-Score -0.057, VWAP üstü/altı -0.046, Likidite avı +0.037, MACD yönü -0.031, FVG -0.027

### 1h

| Bileşen | IC | İsabet | ↑ dediğinde yükseldi | ↓ dediğinde düştü | İşlemde aynı yöndeyken kazanma | Ters yöndeyken kazanma |
|---|---|---|---|---|---|---|
| Trend | -0.079 | %51.4 | %38.3 | %55.4 | %49.4 (1643) | %50.3 (191) |
| Momentum | -0.033 | %47.6 | %39.8 | %55.7 | %49.6 (1587) | %46.7 (105) |
| Open Interest | -0.056 | %45.3 | %39.5 | %52.1 | %49.6 (1192) | %53.9 (154) |
| Hacim | -0.064 | %49.1 | %39.0 | %52.1 | %47.1 (1212) | %55.9 (68) |
| Funding+L/S | -0.027 | %43.5 | %42.8 | %54.9 | %41.3 (446) | %51.6 (680) |
| FVG+Likidite avı | 0.043 | %52.4 | %44.3 | %64.4 | %52.0 (812) | %45.4 (661) |
| VWAP | -0.034 | %49.2 | %39.7 | %55.3 | %47.7 (1626) | %67.9 (131) |

Ham göstergeler (IC, büyükten küçüğe): Fiyat>EMA200 -0.091, RSI -0.085, Üst periyot trendi -0.081, EMA dizilimi -0.074, Taker alım -0.056, Funding +0.051, Z-Score -0.046, Likidite avı +0.041, OI değişimi -0.040, VWAP üstü/altı -0.028

### 4h

| Bileşen | IC | İsabet | ↑ dediğinde yükseldi | ↓ dediğinde düştü | İşlemde aynı yöndeyken kazanma | Ters yöndeyken kazanma |
|---|---|---|---|---|---|---|
| Trend | -0.086 | %57.1 | %33.9 | %60.3 | %56.5 (416) | %46.3 (67) |
| Momentum | -0.132 | %45.1 | %34.6 | %54.0 | %51.7 (414) | %81.8 (22) |
| Open Interest | -0.124 | %46.5 | %33.0 | %55.5 | %54.0 (422) | %58.6 (29) |
| Hacim | -0.137 | %50.1 | %28.5 | %53.9 | %53.4 (266) | %44.4 (18) |
| Funding+L/S | -0.022 | %41.9 | %40.9 | %58.2 | %45.7 (92) | %65.2 (178) |
| FVG+Likidite avı | 0.074 | %53.2 | %45.1 | %67.5 | %56.5 (209) | %48.6 (183) |
| VWAP | -0.126 | %50.7 | %28.9 | %58.2 | %51.8 (425) | %41.2 (17) |

Ham göstergeler (IC, büyükten küçüğe): Z-Score -0.168, RSI -0.135, OI değişimi -0.113, VWAP üstü/altı -0.109, Likidite avı +0.102, Bollinger sıkışma +0.101, Taker alım -0.100, OI rejimi +0.097, MACD yönü -0.092, RVOL +0.086

## 3. Öğrenme: yeni ağırlıklar (eğitimde bulundu, TEST'te sınandı)

| Periyot | Yöntem | Eşik | Mevcut model TEST ort. R / kazanma | Yeni model TEST ort. R / kazanma | Karar |
|---|---|---|---|---|---|
| 15m | mevcut | 74/26 | 0.029 / %50.7 (8722) | 0.019 / %50.0 (3283) | ❌ mevcut kalır |
| 30m | IC± | 70/30 | 0.004 / %49.3 (4310) | 0.018 / %49.8 (2002) | ✅ benimsendi |
| 1h | IC+ | 70/30 | 0.015 / %49.8 (2158) | 0.021 / %49.9 (1615) | ✅ benimsendi |
| 4h | IC+ | 66/34 | 0.1 / %53.8 (548) | 0.015 / %49.3 (540) | ❌ mevcut kalır |

Ağırlıklar:
- 15m: Trend 20, Momentum 18, Open Interest 15, Hacim 10, Funding+L/S 10, FVG+Likidite avı 10, VWAP 5
- 30m: Trend 13.8, Momentum -40.7, Open Interest -10.1, Funding+L/S -10.9, VWAP 18.1
- 1h: Trend 10.4, Momentum 7.3, Open Interest 13.2, Hacim 35.3, VWAP 33.8
- 4h: Hacim 8.6, VWAP 91.4

## 4. Strateji yarışması (yalnız canlı botun da görebildiği veriler; eğitimde seçildi, TEST'te sınandı)

### 15m — 216 strateji denendi · ❌ hiçbiri yeterince iyi değil, mevcut kalır

Mevcut (trend, filtresiz) TEST: 2978 işlem, kazanma %48.1, ort R -0.014, PF 0.84

| # | Strateji | Eğitim ort R (n) | TEST ort R | TEST kazanma | TEST PF | 5x ort ROE | 10x ort ROE | 10x likidasyon |
|---|---|---|---|---|---|---|---|---|
| 1 | Kazanan ortak noktaları kuralı (skor ≥55 / ≤45 VE Z-Score (yön) ≤ -0.52 VE ATR % ≥ 0.48 VE Saat (UTC) ≥ 12.00), SL1.0/TP1.5-2.5 | 0.161 (2050) | 0.019 | %40.0 (848) | 0.88 | %-0.38 | %-0.77 | 1 |
| 2 | Kazanan ortak noktaları kuralı (skor ≥55 / ≤45 VE Z-Score (yön) ≤ -0.52 VE ATR % ≥ 0.48 VE FVG+Likidite (yön) ≤ 0.00), SL1.0/TP1.5-2.5 | 0.137 (2557) | 0.022 | %40.1 (1024) | 0.89 | %-0.34 | %-0.68 | 0 |
| 3 | Geri çekilmede limit giriş (skor ≥58 / ≤42, dip-tepe aralığının en fazla %70'inde, 0.382 Fibonacci geri çekilmesine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) +üst trend yönünde | 0.082 (3248) | 0.024 | %39.8 (1416) | 0.86 | %-0.63 | %-1.09 | 8 |
| 4 | Geri çekilmede limit giriş (skor ≥58 / ≤42, dip-tepe aralığının en fazla %70'inde, 0.382 Fibonacci geri çekilmesine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) | 0.081 (3239) | 0.041 | %40.7 (1398) | 0.88 | %-0.55 | %-0.92 | 8 |
| 5 | Geri çekilmede limit giriş (skor ≥66 / ≤34, dip-tepe aralığının en fazla %70'inde, 0.382 Fibonacci geri çekilmesine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) | 0.081 (3112) | 0.022 | %40.1 (1322) | 0.85 | %-0.69 | %-1.11 | 7 |

### 30m — 207 strateji denendi · ❌ hiçbiri yeterince iyi değil, mevcut kalır

Mevcut (trend, filtresiz) TEST: 1450 işlem, kazanma %51.4, ort R 0.049, PF 0.97

| # | Strateji | Eğitim ort R (n) | TEST ort R | TEST kazanma | TEST PF | 5x ort ROE | 10x ort ROE | 10x likidasyon |
|---|---|---|---|---|---|---|---|---|
| 1 | Trend takibi (skor ≥58 / ≤42) +FVG/likidite aynı yönde, SL1.5/TP1.5-3.0 | 0.046 (3648) | 0.053 | %51.1 (1514) | 1.05 | %0.2 | %0.32 | 5 |
| 2 | Trend takibi (skor ≥66 / ≤34) +FVG/likidite aynı yönde, SL1.5/TP1.5-3.0 | 0.046 (3629) | 0.05 | %51.0 (1504) | 1.05 | %0.21 | %0.33 | 5 |
| 3 | Trend takibi (skor ≥58 / ≤42) +üst trend yönünde +FVG/likidite aynı yönde, SL1.5/TP1.5-3.0 | 0.046 (3592) | 0.055 | %51.4 (1480) | 1.08 | %0.31 | %0.53 | 5 |
| 4 | Trend takibi (skor ≥66 / ≤34) +üst trend yönünde +FVG/likidite aynı yönde, SL1.5/TP1.5-3.0 | 0.046 (3572) | 0.052 | %51.3 (1465) | 1.06 | %0.26 | %0.44 | 5 |
| 5 | Trend takibi (skor ≥58 / ≤42, VWAP'tan ≤2.0 ATR) +üst trend yönünde, SL1.5/TP1.5-3.0 | 0.044 (3274) | 0.005 | %49.0 (1385) | 0.88 | %-0.51 | %-1.07 | 4 |

### 1h — 217 strateji denendi · ❌ hiçbiri yeterince iyi değil, mevcut kalır

Mevcut (trend, filtresiz) TEST: 746 işlem, kazanma %54.0, ort R 0.104, PF 1.09

| # | Strateji | Eğitim ort R (n) | TEST ort R | TEST kazanma | TEST PF | 5x ort ROE | 10x ort ROE | 10x likidasyon |
|---|---|---|---|---|---|---|---|---|
| 1 | Kazanan ortak noktaları kuralı (skor ≥55 / ≤45 VE RSI (yön, 50 merkez) ≥ 13.39 VE Agresif alım-satım (yön) ≤ -0.01 VE RVOL ≤ 1.13), SL1.0/TP1.5-2.5 | 0.371 (675) | 0.028 | %40.4 (213) | 0.83 | %-0.75 | %-1.5 | 0 |
| 2 | Kazanan ortak noktaları kuralı (skor ≥55 / ≤45 VE RSI (yön, 50 merkez) ≥ 13.39 VE Agresif alım-satım (yön) ≤ -0.01), SL1.0/TP1.5-2.5 | 0.254 (915) | 0.029 | %40.8 (289) | 0.87 | %-0.62 | %-1.23 | 0 |
| 3 | Kazanan ortak noktaları kuralı (skor ≥55 / ≤45 VE RSI (yön, 50 merkez) ≥ 13.39 VE Momentum (yön) ≤ 0.09 VE Agresif alım-satım (yön) ≤ 0.02), SL1.0/TP1.5-2.5 | 0.301 (594) | -0.046 | %38.8 (165) | 0.76 | %-1.81 | %-3.59 | 2 |
| 4 | Kazanan ortak noktaları kuralı (skor ≥55 / ≤45 VE RSI (yön, 50 merkez) ≥ 16.76 VE Momentum (yön) ≤ 0.14 VE ATR % ≥ 0.64), fiyatın 0.5 ATR gerisine limit emirle giriş (6 mum geçerli), SL1.0/TP1.5-2.5 | 0.389 (342) | 0.02 | %38.1 (126) | 0.96 | %-0.3 | %-1.01 | 3 |
| 5 | Kazanan ortak noktaları kuralı (skor ≥55 / ≤45 VE RSI (yön, 50 merkez) ≥ 16.76 VE Momentum (yön) ≤ 0.14 VE ATR % ≤ 2.50), fiyatın 0.5 ATR gerisine limit emirle giriş (6 mum geçerli), SL1.0/TP1.5-2.5 | 0.412 (301) | 0.056 | %40.7 (108) | 0.98 | %-0.08 | %-0.16 | 0 |

### 4h — 194 strateji denendi · ✅ kazanan benimsendi

Mevcut (trend, filtresiz) TEST: 196 işlem, kazanma %51.5, ort R 0.094, PF 1.03

| # | Strateji | Eğitim ort R (n) | TEST ort R | TEST kazanma | TEST PF | 5x ort ROE | 10x ort ROE | 10x likidasyon |
|---|---|---|---|---|---|---|---|---|
| 1 | Trend takibi (skor ≥66 / ≤34) +üst trend yönünde +BTC trendi aynı yönde, SL1.0/TP1.5-2.5 | 0.166 (502) | 0.314 | %51.0 (202) | 1.44 | %3.2 | %6.57 | 1 |
| 2 | Trend takibi (skor ≥74 / ≤26), SL1.0/TP1.5-2.5 | 0.164 (513) | 0.127 | %43.0 (223) | 1.09 | %0.81 | %1.76 | 2 |
| 3 | Trend takibi (skor ≥58 / ≤42), SL1.0/TP1.5-2.5 | 0.16 (535) | 0.14 | %43.7 (222) | 1.1 | %0.88 | %1.91 | 2 |
| 4 | Trend takibi (skor ≥66 / ≤34), SL1.0/TP1.5-2.5 | 0.16 (535) | 0.14 | %43.7 (222) | 1.1 | %0.88 | %1.91 | 2 |
| 5 | Trend takibi (skor ≥74 / ≤26) +üst trend yönünde, SL1.0/TP1.5-2.5 | 0.161 (512) | 0.132 | %43.2 (222) | 1.1 | %0.89 | %1.92 | 2 |


## 5. 15m (piyasa girişli): kazananlar ve kaybedenler

Tüm olaylar: kazanma %40.1 (eğitim) / %40.3 (test); ort. net R -0.137 / -0.13

**Kazanan vs kaybeden girişte o anki durum** (etki = standart fark; ✓ = test döneminde de aynı yönde)

| Özellik | Kazananlarda | Kaybedenlerde | Etki (eğitim) | Etki (test) | |
|---|---|---|---|---|---|
| Z-Score (yön) | 0.833 | 0.879 | -0.045 | -0.018 | ✗ |
| BTC 1s yönü (yön) | 0.145 | 0.186 | -0.041 | -0.044 | ✓ |
| Momentum (yön) | 0.239 | 0.255 | -0.036 | -0.012 | ✗ |
| Üst trend (yön) | 0.682 | 0.665 | +0.035 | +0.004 | ✗ |
| Dip-tepe konumu (yön) | 0.718 | 0.724 | -0.034 | -0.012 | ✗ |
| VWAP bileşeni (yön) | 0.699 | 0.688 | +0.032 | +0.051 | ✓ |
| RSI (yön, 50 merkez) | 8.793 | 9.005 | -0.027 | -0.002 | ✗ |
| Trend (yön) | 0.783 | 0.774 | +0.026 | +0.001 | ✗ |
| Agresif alım-satım (yön) | 0.014 | 0.016 | -0.026 | +0.029 | ✗ |
| Hacim (yön) | 0.171 | 0.177 | -0.021 | +0.020 | ✗ |

| Kural | Eğitim ort R (n) | Eğitim 1./2. yarı | TEST olay ort R (n) |
|---|---|---|---|
| Z-Score (yön) ≤ -0.52 VE ATR % ≥ 0.48 VE FVG+Likidite (yön) ≤ 0.00 | 0.09 (6880) | 0.142 / 0.041 | -0.052 (2799) |
| Z-Score (yön) ≤ -0.52 VE ATR % ≥ 0.48 VE Saat (UTC) ≥ 12.00 | 0.086 (7381) | 0.166 / 0.019 | -0.093 (3003) |
| ATR % ≥ 1.26 VE Z-Score (yön) ≤ 0.68 | 0.026 (8215) | 0.015 / 0.035 | -0.054 (2764) |
| ATR % ≥ 1.26 VE Dip-tepe konumu (yön) ≤ 0.69 | 0.021 (7997) | 0.035 / 0.007 | -0.064 (2261) |

## 5. 15m (limit girişli): kazananlar ve kaybedenler

Tüm olaylar: kazanma %40.6 (eğitim) / %39.8 (test); ort. net R -0.123 / -0.146

**Kazanan vs kaybeden girişte o anki durum** (etki = standart fark; ✓ = test döneminde de aynı yönde)

| Özellik | Kazananlarda | Kaybedenlerde | Etki (eğitim) | Etki (test) | |
|---|---|---|---|---|---|
| VWAP bileşeni (yön) | 0.705 | 0.686 | +0.052 | +0.037 | ✓ |
| Z-Score (yön) | 0.878 | 0.925 | -0.047 | -0.009 | ✗ |
| Momentum (yön) | 0.255 | 0.272 | -0.037 | -0.011 | ✗ |
| RSI (yön, 50 merkez) | 9.051 | 9.324 | -0.034 | -0.022 | ✗ |
| Agresif alım-satım (yön) | 0.015 | 0.017 | -0.034 | +0.019 | ✗ |
| Hacim (yön) | 0.176 | 0.185 | -0.032 | +0.016 | ✗ |
| Trend (yön) | 0.783 | 0.773 | +0.030 | -0.019 | ✗ |
| Dip-tepe konumu (yön) | 0.723 | 0.729 | -0.030 | -0.033 | ✓ |
| Üst trend (yön) | 0.677 | 0.663 | +0.028 | -0.008 | ✗ |
| BTC 1s yönü (yön) | 0.182 | 0.209 | -0.028 | -0.066 | ✓ |

| Kural | Eğitim ort R (n) | Eğitim 1./2. yarı | TEST olay ort R (n) |
|---|---|---|---|
| ATR % ≥ 1.24 VE Üst trend (yön) ≥ 1.00 VE Saat (UTC) ≥ 9.00 | 0.078 (7527) | 0.118 / 0.045 | 0.091 (2610) |
| ATR % ≥ 1.24 VE Z-Score (yön) ≤ 0.98 VE Saat (UTC) ≥ 9.00 | 0.086 (5276) | 0.145 / 0.034 | 0.024 (1539) |
| ATR % ≥ 1.24 VE Z-Score (yön) ≤ 0.98 VE Momentum (yön) ≥ -0.37 | 0.075 (6401) | 0.08 / 0.071 | -0.066 (1998) |
| ATR % ≥ 1.24 VE Agresif alım-satım (yön) ≤ 0.00 VE Üst trend (yön) ≥ 1.00 | 0.08 (5197) | 0.034 / 0.118 | -0.075 (1598) |
| ATR % ≥ 1.24 VE Agresif alım-satım (yön) ≤ 0.00 VE Trend (yön) ≥ 1.00 | 0.082 (4867) | 0.045 / 0.112 | -0.085 (1509) |

## 5. 1h (piyasa girişli): kazananlar ve kaybedenler

Tüm olaylar: kazanma %41.5 (eğitim) / %42.5 (test); ort. net R -0.011 / 0.024

**Kazanan vs kaybeden girişte o anki durum** (etki = standart fark; ✓ = test döneminde de aynı yönde)

| Özellik | Kazananlarda | Kaybedenlerde | Etki (eğitim) | Etki (test) | |
|---|---|---|---|---|---|
| VWAP bileşeni (yön) | 0.433 | 0.4 | +0.091 | +0.039 | ✓ |
| RSI (yön, 50 merkez) | 10.428 | 9.804 | +0.078 | -0.040 | ✗ |
| VWAP'tan uzaklık ATR (yön) | 1.14 | 1.055 | +0.078 | +0.050 | ✓ |
| Likidite avı (yön) | -0.245 | -0.206 | -0.068 | +0.042 | ✗ |
| Hacim (yön) | 0.177 | 0.164 | +0.054 | -0.014 | ✗ |
| Üst trend (yön) | 0.658 | 0.632 | +0.051 | +0.047 | ✓ |
| Dip-tepe konumu (yön) | 0.732 | 0.724 | +0.049 | +0.022 | ✗ |
| Trend (yön) | 0.762 | 0.744 | +0.048 | +0.032 | ✓ |
| Z-Score (yön) | 1.014 | 0.974 | +0.043 | -0.013 | ✗ |
| Agresif alım-satım (yön) | 0.008 | 0.01 | -0.038 | +0.035 | ✗ |

| Kural | Eğitim ort R (n) | Eğitim 1./2. yarı | TEST olay ort R (n) |
|---|---|---|---|
| RSI (yön, 50 merkez) ≥ 13.39 VE Momentum (yön) ≤ 0.09 VE Agresif alım-satım (yön) ≤ 0.02 | 0.338 (2109) | 0.521 / 0.099 | -0.082 (432) |
| RSI (yön, 50 merkez) ≥ 13.39 VE Agresif alım-satım (yön) ≤ -0.01 VE RVOL ≤ 1.13 | 0.339 (1922) | 0.522 / 0.094 | 0.004 (435) |
| RSI (yön, 50 merkez) ≥ 13.39 VE Agresif alım-satım (yön) ≤ -0.01 | 0.269 (3030) | 0.416 / 0.076 | -0.022 (658) |
| RSI (yön, 50 merkez) ≥ 13.39 VE Momentum (yön) ≤ 0.09 | 0.271 (2943) | 0.425 / 0.067 | -0.117 (743) |
| RSI (yön, 50 merkez) ≥ 16.44 VE Momentum (yön) ≤ 0.09 VE ATR % ≤ 2.51 | 0.325 (1805) | 0.493 / 0.088 | -0.146 (393) |

## 5. 1h (limit girişli): kazananlar ve kaybedenler

Tüm olaylar: kazanma %42.5 (eğitim) / %39.9 (test); ort. net R 0.01 / -0.051

**Kazanan vs kaybeden girişte o anki durum** (etki = standart fark; ✓ = test döneminde de aynı yönde)

| Özellik | Kazananlarda | Kaybedenlerde | Etki (eğitim) | Etki (test) | |
|---|---|---|---|---|---|
| VWAP bileşeni (yön) | 0.434 | 0.406 | +0.077 | -0.016 | ✗ |
| RSI (yön, 50 merkez) | 10.597 | 10.007 | +0.073 | -0.054 | ✗ |
| VWAP'tan uzaklık ATR (yön) | 1.152 | 1.078 | +0.067 | +0.007 | ✗ |
| Likidite avı (yön) | -0.243 | -0.21 | -0.056 | +0.052 | ✗ |
| Z-Score (yön) | 1.045 | 1.001 | +0.046 | -0.043 | ✗ |
| Hacim (yön) | 0.176 | 0.166 | +0.044 | -0.008 | ✗ |
| Üst trend (yön) | 0.659 | 0.637 | +0.042 | +0.068 | ✓ |
| Trend (yön) | 0.761 | 0.749 | +0.032 | +0.061 | ✓ |
| FVG+Likidite (yön) | -0.015 | -0.004 | -0.029 | +0.077 | ✗ |
| Agresif alım-satım (yön) | 0.009 | 0.01 | -0.029 | +0.016 | ✗ |

| Kural | Eğitim ort R (n) | Eğitim 1./2. yarı | TEST olay ort R (n) |
|---|---|---|---|
| RSI (yön, 50 merkez) ≥ 16.76 VE Agresif alım-satım (yön) ≤ -0.01 VE ATR % ≥ 0.64 | 0.388 (1288) | 0.487 / 0.238 | -0.169 (220) |
| RSI (yön, 50 merkez) ≥ 16.76 VE Momentum (yön) ≤ 0.14 VE ATR % ≥ 0.64 | 0.367 (1393) | 0.519 / 0.155 | -0.085 (349) |
| RSI (yön, 50 merkez) ≥ 16.76 VE Agresif alım-satım (yön) ≤ -0.01 VE Trend (yön) ≥ 0.73 | 0.369 (1279) | 0.458 / 0.23 | -0.157 (227) |
| RSI (yön, 50 merkez) ≥ 16.76 VE Momentum (yön) ≤ 0.14 VE ATR % ≤ 2.50 | 0.372 (1200) | 0.53 / 0.129 | -0.091 (293) |
| RSI (yön, 50 merkez) ≥ 16.76 VE Agresif alım-satım (yön) ≤ -0.01 | 0.35 (1344) | 0.446 / 0.2 | -0.178 (255) |

IC (bilgi katsayısı): gösterge puanı ile sonraki getiri arasındaki sıralama korelasyonu. Piyasada 0.02–0.05 bile anlamlıdır; negatif ise gösterge ters çalışıyor demektir.
Geçmiş performans geleceği garanti etmez.