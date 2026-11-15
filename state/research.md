# V5 Araştırma Raporu — 15.11.2026 07:50 UTC

40 coin · değerlendirme 17.08.2026'dan bugüne (90 gün) · eğitim/TEST ayrımı 19.10.2026

## 1. Mevcut model: kaldıraçlı işlem sonuçları (tüm dönem)

| Periyot | Kaldıraç | İşlem | Kazanma | Ort. ROE | PF | Ort. R | Likidasyon | 100$ marjla net | Maks. DD |
|---|---|---|---|---|---|---|---|---|---|
| 15m | 5x | 29372 | %49.5 | %-0.47 | 0.84 | 0.004 | 0 | -13824.0$ | 15707.0$ |
| 15m | 10x | 29374 | %49.5 | %-0.95 | 0.84 | 0.004 | 11 | -27901.0$ | 31704.0$ |
| 30m | 5x | 14102 | %50.4 | %-0.35 | 0.92 | 0.02 | 0 | -4997.0$ | 7421.0$ |
| 30m | 10x | 14107 | %50.4 | %-0.71 | 0.92 | 0.02 | 16 | -9956.0$ | 14913.0$ |
| 1h | 5x | 7010 | %50.3 | %-0.28 | 0.95 | 0.023 | 0 | -1948.0$ | 4393.0$ |
| 1h | 10x | 7019 | %50.3 | %-0.63 | 0.95 | 0.023 | 22 | -4441.0$ | 9289.0$ |
| 4h | 5x | 1849 | %55.5 | %1.82 | 1.18 | 0.136 | 2 | 3369.0$ | 2127.0$ |
| 4h | 10x | 1856 | %55.3 | %3.56 | 1.17 | 0.136 | 26 | 6599.0$ | 4217.0$ |

PF = kâr faktörü (toplam kazanç / toplam kayıp, 1 üstü kârlı). R = risk birimi (stop mesafesi).

## 2. Göstergelerin doğruluğu (TEST dönemi)

### 15m

| Bileşen | IC | İsabet | ↑ dediğinde yükseldi | ↓ dediğinde düştü | İşlemde aynı yöndeyken kazanma | Ters yöndeyken kazanma |
|---|---|---|---|---|---|---|
| Trend | -0.098 | %46.2 | %41.5 | %49.3 | %47.6 (6933) | %59.6 (302) |
| Momentum | -0.021 | %47.8 | %44.7 | %51.4 | %48.9 (5343) | %47.5 (1383) |
| Hacim | -0.033 | %48.4 | %45.5 | %50.1 | %49.8 (4692) | %45.0 (765) |
| Funding+L/S | -0.017 | %40.0 | %40.0 | %- | %47.3 (448) | %46.7 (563) |
| FVG+Likidite avı | -0.01 | %50.7 | %47.8 | %53.8 | %49.0 (3276) | %48.2 (2611) |
| VWAP | -0.059 | %46.6 | %42.2 | %50.1 | %48.2 (7420) | %51.5 (390) |

Ham göstergeler (IC, büyükten küçüğe): EMA dizilimi -0.109, Üst periyot trendi -0.097, Fiyat>EMA200 -0.082, VWAP üstü/altı -0.070, RSI -0.064, Z-Score -0.044, FVG -0.043, OBV yönü -0.021, Likidite avı +0.019, Bollinger sıkışma -0.017

### 30m

| Bileşen | IC | İsabet | ↑ dediğinde yükseldi | ↓ dediğinde düştü | İşlemde aynı yöndeyken kazanma | Ters yöndeyken kazanma |
|---|---|---|---|---|---|---|
| Trend | -0.119 | %47.8 | %40.0 | %51.5 | %45.4 (3261) | %53.3 (214) |
| Momentum | -0.052 | %46.8 | %42.4 | %51.7 | %48.9 (2734) | %46.5 (520) |
| Hacim | -0.094 | %46.3 | %40.0 | %49.1 | %46.1 (2250) | %47.2 (212) |
| Funding+L/S | -0.041 | %34.5 | %34.5 | %- | %43.2 (183) | %45.2 (301) |
| FVG+Likidite avı | 0.014 | %53.0 | %47.9 | %58.7 | %47.4 (1552) | %46.6 (1309) |
| VWAP | -0.072 | %46.3 | %40.1 | %51.1 | %45.6 (3304) | %55.7 (192) |

Ham göstergeler (IC, büyükten küçüğe): Üst periyot trendi -0.108, EMA dizilimi -0.101, RSI -0.098, Fiyat>EMA200 -0.095, OBV yönü -0.092, Z-Score -0.090, VWAP üstü/altı -0.082, Likidite avı +0.052, FVG -0.050, MACD yönü -0.049

### 1h

| Bileşen | IC | İsabet | ↑ dediğinde yükseldi | ↓ dediğinde düştü | İşlemde aynı yöndeyken kazanma | Ters yöndeyken kazanma |
|---|---|---|---|---|---|---|
| Trend | -0.112 | %49.4 | %37.3 | %53.4 | %49.0 (1566) | %50.0 (96) |
| Momentum | -0.076 | %45.6 | %39.3 | %52.6 | %47.2 (1380) | %56.4 (202) |
| Hacim | -0.091 | %47.0 | %37.0 | %50.2 | %46.8 (1081) | %61.5 (65) |
| Funding+L/S | -0.085 | %33.0 | %33.0 | %- | %32.9 (76) | %46.2 (156) |
| FVG+Likidite avı | 0.05 | %54.9 | %46.4 | %66.0 | %52.4 (809) | %42.5 (588) |
| VWAP | -0.077 | %46.5 | %38.8 | %52.3 | %44.9 (1411) | %69.0 (187) |

Ham göstergeler (IC, büyükten küçüğe): RSI -0.126, Fiyat>EMA200 -0.121, Üst periyot trendi -0.110, EMA dizilimi -0.104, Z-Score -0.092, Taker alım -0.070, Likidite avı +0.068, VWAP üstü/altı -0.064, Funding +0.059, OBV yönü -0.037

### 4h

| Bileşen | IC | İsabet | ↑ dediğinde yükseldi | ↓ dediğinde düştü | İşlemde aynı yöndeyken kazanma | Ters yöndeyken kazanma |
|---|---|---|---|---|---|---|
| Trend | -0.137 | %54.2 | %31.3 | %57.0 | %56.8 (382) | %40.7 (27) |
| Momentum | -0.173 | %42.9 | %35.3 | %50.1 | %49.1 (328) | %66.7 (54) |
| Hacim | -0.202 | %45.1 | %20.7 | %48.9 | %49.5 (206) | %64.7 (17) |
| Funding+L/S | -0.055 | %34.2 | %34.2 | %- | %25.0 (12) | %55.8 (52) |
| FVG+Likidite avı | 0.092 | %56.6 | %49.2 | %68.0 | %56.3 (206) | %48.4 (153) |
| VWAP | -0.178 | %47.2 | %28.0 | %54.9 | %48.2 (326) | %70.6 (34) |

Ham göstergeler (IC, büyükten küçüğe): Z-Score -0.222, RSI -0.197, VWAP üstü/altı -0.160, Likidite avı +0.140, OBV yönü -0.130, Taker alım -0.120, RVOL +0.106, MACD yönü -0.104, Fiyat>EMA200 -0.100, Bollinger sıkışma +0.080

## 3. Öğrenme: yeni ağırlıklar (eğitimde bulundu, TEST'te sınandı)

| Periyot | Yöntem | Eşik | Mevcut model TEST ort. R / kazanma | Yeni model TEST ort. R / kazanma | Karar |
|---|---|---|---|---|---|
| 15m | IC± | 70/30 | -0.01 / %49.0 (8746) | -0.023 / %48.2 (3370) | ❌ mevcut kalır |
| 30m | IC± | 74/26 | -0.054 / %46.9 (4196) | 0.047 / %51.2 (1345) | ✅ benimsendi |
| 1h | IC+ | 62/38 | -0.016 / %49.2 (2032) | -0.078 / %46.3 (2011) | ❌ mevcut kalır |
| 4h | mevcut | 58/42 | 0.034 / %52.3 (480) | 0.003 / %51.0 (496) | ❌ mevcut kalır |

Ağırlıklar:
- 15m: Momentum -33.7, Hacim -19.7, Funding+L/S -16.6, FVG+Likidite avı 8.9, VWAP 15.7
- 30m: Trend 11.7, Momentum -36.9, Funding+L/S -18.3, VWAP 25.6
- 1h: Trend 2.5, Momentum 12.4, Hacim 43.9, VWAP 41.2
- 4h: Trend 20, Momentum 18, Open Interest 15, Hacim 10, Funding+L/S 10, FVG+Likidite avı 10, VWAP 5

## 4. Strateji yarışması (yalnız canlı botun da görebildiği veriler; eğitimde seçildi, TEST'te sınandı)

### 15m — 163 strateji denendi · ❌ hiçbiri yeterince iyi değil, mevcut kalır

Mevcut (trend, filtresiz) TEST: 2858 işlem, kazanma %46.9, ort R -0.047, PF 0.74

| # | Strateji | Eğitim ort R (n) | TEST ort R | TEST kazanma | TEST PF | 5x ort ROE | 10x ort ROE | 10x likidasyon |
|---|---|---|---|---|---|---|---|---|
| 1 | Geri çekilmede limit giriş (skor ≥66 / ≤34, dip-tepe aralığının en fazla %50'inde, 0.382 Fibonacci geri çekilmesine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) | 0.098 (1907) | 0.021 | %41.8 (749) | 0.9 | %-0.36 | %-0.72 | 0 |
| 2 | Geri çekilmede limit giriş (skor ≥66 / ≤34, dip-tepe aralığının en fazla %50'inde, 0.5 Fibonacci geri çekilmesine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) | 0.098 (1907) | 0.021 | %41.8 (749) | 0.9 | %-0.36 | %-0.72 | 0 |
| 3 | Geri çekilmede limit giriş (skor ≥66 / ≤34, dip-tepe aralığının en fazla %70'inde, 0.382 Fibonacci geri çekilmesine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) | 0.076 (3109) | -0.045 | %38.2 (1292) | 0.78 | %-0.95 | %-1.93 | 2 |
| 4 | Geri çekilmede limit giriş (skor ≥66 / ≤34, dip-tepe aralığının en fazla %50'inde, 0.382 Fibonacci geri çekilmesine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) +üst trend yönünde | 0.097 (1870) | 0.025 | %41.8 (734) | 0.91 | %-0.33 | %-0.66 | 0 |
| 5 | Geri çekilmede limit giriş (skor ≥66 / ≤34, dip-tepe aralığının en fazla %50'inde, 0.5 Fibonacci geri çekilmesine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) +üst trend yönünde | 0.097 (1870) | 0.025 | %41.8 (734) | 0.91 | %-0.33 | %-0.66 | 0 |

### 30m — 163 strateji denendi · ❌ hiçbiri yeterince iyi değil, mevcut kalır

Mevcut (trend, filtresiz) TEST: 1409 işlem, kazanma %48.3, ort R -0.036, PF 0.8

| # | Strateji | Eğitim ort R (n) | TEST ort R | TEST kazanma | TEST PF | 5x ort ROE | 10x ort ROE | 10x likidasyon |
|---|---|---|---|---|---|---|---|---|
| 1 | Geri çekilmede limit giriş (skor ≥58 / ≤42, dip-tepe aralığının en fazla %70'inde, 0.382 Fibonacci geri çekilmesine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) | 0.069 (1633) | -0.063 | %39.2 (658) | 0.73 | %-1.56 | %-3.12 | 0 |
| 2 | Geri çekilmede limit giriş (skor ≥66 / ≤34, dip-tepe aralığının en fazla %70'inde, fiyatın 1.0 ATR gerisine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) | 0.073 (1268) | -0.042 | %40.3 (543) | 0.76 | %-1.01 | %-2.02 | 0 |
| 3 | Geri çekilmede limit giriş (skor ≥66 / ≤34, dip-tepe aralığının en fazla %70'inde, fiyatın 1.0 ATR gerisine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) +üst trend yönünde | 0.073 (1268) | -0.059 | %39.5 (529) | 0.73 | %-1.12 | %-2.25 | 0 |
| 4 | Geri çekilmede limit giriş (skor ≥66 / ≤34, dip-tepe aralığının en fazla %70'inde, 0.382 Fibonacci geri çekilmesine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) | 0.063 (1532) | -0.063 | %39.2 (617) | 0.72 | %-1.66 | %-3.32 | 0 |
| 5 | Geri çekilmede limit giriş (skor ≥58 / ≤42, dip-tepe aralığının en fazla %70'inde, 0.382 Fibonacci geri çekilmesine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) +üst trend yönünde | 0.058 (1643) | -0.03 | %40.2 (662) | 0.76 | %-1.41 | %-2.83 | 0 |

### 1h — 163 strateji denendi · ❌ hiçbiri yeterince iyi değil, mevcut kalır

Mevcut (trend, filtresiz) TEST: 715 işlem, kazanma %49.8, ort R 0.01, PF 0.89

| # | Strateji | Eğitim ort R (n) | TEST ort R | TEST kazanma | TEST PF | 5x ort ROE | 10x ort ROE | 10x likidasyon |
|---|---|---|---|---|---|---|---|---|
| 1 | Trend takibi (skor ≥74 / ≤26), SL1.0/TP1.5-2.5 | 0.08 (2040) | -0.015 | %39.3 (782) | 0.84 | %-0.74 | %-1.47 | 0 |
| 2 | Trend takibi (skor ≥74 / ≤26) +üst trend yönünde, SL1.0/TP1.5-2.5 | 0.078 (2033) | -0.016 | %39.2 (778) | 0.84 | %-0.74 | %-1.48 | 0 |
| 3 | Trend takibi (skor ≥58 / ≤42), SL1.0/TP1.5-2.5 | 0.074 (2108) | -0.006 | %39.7 (817) | 0.85 | %-0.7 | %-1.4 | 0 |
| 4 | Trend takibi (skor ≥66 / ≤34), SL1.0/TP1.5-2.5 | 0.074 (2107) | -0.008 | %39.5 (817) | 0.84 | %-0.71 | %-1.42 | 0 |
| 5 | Trend takibi (skor ≥58 / ≤42) +üst trend yönünde, SL1.0/TP1.5-2.5 | 0.073 (2103) | -0.02 | %39.1 (814) | 0.83 | %-0.76 | %-1.53 | 0 |

### 4h — 151 strateji denendi · ❌ hiçbiri yeterince iyi değil, mevcut kalır

Mevcut (trend, filtresiz) TEST: 182 işlem, kazanma %51.6, ort R 0.007, PF 0.82

| # | Strateji | Eğitim ort R (n) | TEST ort R | TEST kazanma | TEST PF | 5x ort ROE | 10x ort ROE | 10x likidasyon |
|---|---|---|---|---|---|---|---|---|
| 1 | Trend takibi (skor ≥58 / ≤42) +üst trend yönünde, SL1.0/TP1.5-2.5 | 0.137 (532) | 0.022 | %41.4 (210) | 0.87 | %-1.16 | %-2.17 | 1 |
| 2 | Trend takibi (skor ≥66 / ≤34) +üst trend yönünde, SL1.0/TP1.5-2.5 | 0.137 (532) | 0.022 | %41.4 (210) | 0.87 | %-1.16 | %-2.17 | 1 |
| 3 | Trend takibi (skor ≥74 / ≤26) +üst trend yönünde, SL1.0/TP1.5-2.5 | 0.139 (496) | 0.022 | %41.7 (204) | 0.88 | %-1.05 | %-1.93 | 1 |
| 4 | Trend takibi (skor ≥58 / ≤42, VWAP'tan ≤2.0 ATR) +üst trend yönünde, SL1.0/TP1.5-2.5 | 0.127 (525) | 0.016 | %40.7 (214) | 0.88 | %-1.06 | %-1.96 | 1 |
| 5 | Trend takibi (skor ≥74 / ≤26), SL1.0/TP1.5-2.5 | 0.128 (501) | 0.022 | %41.7 (204) | 0.88 | %-1.02 | %-1.88 | 1 |


IC (bilgi katsayısı): gösterge puanı ile sonraki getiri arasındaki sıralama korelasyonu. Piyasada 0.02–0.05 bile anlamlıdır; negatif ise gösterge ters çalışıyor demektir.
Geçmiş performans geleceği garanti etmez.