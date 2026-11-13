# V5 Araştırma Raporu — 13.11.2026 15:43 UTC

40 coin · değerlendirme 15.08.2026'dan bugüne (90 gün) · eğitim/TEST ayrımı 17.10.2026

## 1. Mevcut model: kaldıraçlı işlem sonuçları (tüm dönem)

| Periyot | Kaldıraç | İşlem | Kazanma | Ort. ROE | PF | Ort. R | Likidasyon | 100$ marjla net | Maks. DD |
|---|---|---|---|---|---|---|---|---|---|
| 15m | 5x | 29650 | %49.3 | %-0.49 | 0.84 | 0.002 | 0 | -14499.0$ | 16091.0$ |
| 15m | 10x | 29650 | %49.3 | %-0.98 | 0.84 | 0.002 | 11 | -29045.0$ | 32213.0$ |
| 30m | 5x | 14272 | %50.3 | %-0.36 | 0.91 | 0.016 | 0 | -5199.0$ | 7457.0$ |
| 30m | 10x | 14275 | %50.3 | %-0.73 | 0.91 | 0.016 | 16 | -10391.0$ | 14833.0$ |
| 1h | 5x | 7026 | %50.1 | %-0.34 | 0.94 | 0.017 | 1 | -2420.0$ | 4708.0$ |
| 1h | 10x | 7038 | %50.0 | %-0.74 | 0.94 | 0.017 | 30 | -5207.0$ | 9818.0$ |
| 4h | 5x | 1834 | %55.0 | %1.48 | 1.14 | 0.124 | 4 | 2714.0$ | 2174.0$ |
| 4h | 10x | 1845 | %54.7 | %3.06 | 1.14 | 0.124 | 42 | 5648.0$ | 4100.0$ |

PF = kâr faktörü (toplam kazanç / toplam kayıp, 1 üstü kârlı). R = risk birimi (stop mesafesi).

## 2. Göstergelerin doğruluğu (TEST dönemi)

### 15m

| Bileşen | IC | İsabet | ↑ dediğinde yükseldi | ↓ dediğinde düştü | İşlemde aynı yöndeyken kazanma | Ters yöndeyken kazanma |
|---|---|---|---|---|---|---|
| Trend | -0.083 | %47.4 | %41.9 | %50.7 | %48.3 (7143) | %56.9 (313) |
| Momentum | -0.023 | %47.7 | %44.1 | %51.8 | %49.4 (5447) | %47.7 (1460) |
| Hacim | -0.039 | %48.8 | %44.8 | %50.9 | %49.9 (4790) | %47.8 (766) |
| Funding+L/S | -0.025 | %41.4 | %41.4 | %- | %46.7 (629) | %48.6 (759) |
| FVG+Likidite avı | -0.013 | %50.3 | %47.2 | %54.0 | %49.2 (3345) | %49.1 (2683) |
| VWAP | -0.047 | %47.6 | %42.3 | %51.4 | %48.6 (7596) | %50.9 (409) |

Ham göstergeler (IC, büyükten küçüğe): EMA dizilimi -0.092, Üst periyot trendi -0.082, Fiyat>EMA200 -0.068, VWAP üstü/altı -0.058, RSI -0.056, FVG -0.046, Z-Score -0.044, OBV yönü -0.026, Taker alım -0.018, MACD yönü -0.017

### 30m

| Bileşen | IC | İsabet | ↑ dediğinde yükseldi | ↓ dediğinde düştü | İşlemde aynı yöndeyken kazanma | Ters yöndeyken kazanma |
|---|---|---|---|---|---|---|
| Trend | -0.106 | %48.5 | %40.3 | %52.4 | %45.4 (3381) | %54.8 (217) |
| Momentum | -0.049 | %46.8 | %41.9 | %52.1 | %49.4 (2797) | %47.3 (550) |
| Hacim | -0.092 | %46.9 | %40.5 | %49.7 | %46.3 (2363) | %49.0 (204) |
| Funding+L/S | -0.038 | %39.9 | %39.9 | %- | %47.3 (279) | %47.5 (394) |
| FVG+Likidite avı | 0.006 | %52.3 | %46.9 | %58.8 | %46.8 (1639) | %47.0 (1369) |
| VWAP | -0.063 | %47.5 | %40.7 | %52.2 | %45.9 (3441) | %55.0 (191) |

Ham göstergeler (IC, büyükten küçüğe): Üst periyot trendi -0.101, EMA dizilimi -0.092, RSI -0.088, Fiyat>EMA200 -0.087, OBV yönü -0.080, Z-Score -0.079, VWAP üstü/altı -0.069, FVG -0.053, Likidite avı +0.046, MACD yönü -0.046

### 1h

| Bileşen | IC | İsabet | ↑ dediğinde yükseldi | ↓ dediğinde düştü | İşlemde aynı yöndeyken kazanma | Ters yöndeyken kazanma |
|---|---|---|---|---|---|---|
| Trend | -0.11 | %50.0 | %37.9 | %54.1 | %48.9 (1580) | %48.5 (97) |
| Momentum | -0.08 | %45.4 | %38.8 | %52.4 | %47.0 (1434) | %56.7 (194) |
| Hacim | -0.102 | %46.5 | %37.9 | %49.2 | %45.7 (1116) | %67.2 (64) |
| Funding+L/S | -0.053 | %43.6 | %43.6 | %- | %39.0 (123) | %46.0 (200) |
| FVG+Likidite avı | 0.05 | %54.7 | %46.0 | %66.5 | %50.9 (796) | %43.6 (608) |
| VWAP | -0.076 | %47.3 | %39.3 | %52.8 | %45.0 (1470) | %69.1 (165) |

Ham göstergeler (IC, büyükten küçüğe): RSI -0.125, Fiyat>EMA200 -0.115, Üst periyot trendi -0.107, Z-Score -0.097, EMA dizilimi -0.096, Taker alım -0.071, Likidite avı +0.069, VWAP üstü/altı -0.061, OBV yönü -0.049, MACD yönü -0.037

### 4h

| Bileşen | IC | İsabet | ↑ dediğinde yükseldi | ↓ dediğinde düştü | İşlemde aynı yöndeyken kazanma | Ters yöndeyken kazanma |
|---|---|---|---|---|---|---|
| Trend | -0.152 | %53.1 | %34.7 | %56.0 | %54.2 (384) | %30.8 (26) |
| Momentum | -0.156 | %43.3 | %36.5 | %49.8 | %47.7 (331) | %67.9 (53) |
| Hacim | -0.201 | %45.3 | %30.0 | %48.0 | %44.7 (206) | %57.9 (19) |
| Funding+L/S | -0.041 | %41.0 | %41.0 | %- | %41.2 (34) | %45.3 (53) |
| FVG+Likidite avı | 0.067 | %57.4 | %51.2 | %66.5 | %51.0 (202) | %49.7 (155) |
| VWAP | -0.179 | %47.1 | %29.8 | %54.0 | %43.5 (315) | %59.0 (39) |

Ham göstergeler (IC, büyükten küçüğe): Z-Score -0.220, RSI -0.207, VWAP üstü/altı -0.151, OBV yönü -0.146, Likidite avı +0.135, Fiyat>EMA200 -0.125, Taker alım -0.118, RVOL +0.114, MACD yönü -0.092, FVG -0.088

## 3. Öğrenme: yeni ağırlıklar (eğitimde bulundu, TEST'te sınandı)

| Periyot | Yöntem | Eşik | Mevcut model TEST ort. R / kazanma | Yeni model TEST ort. R / kazanma | Karar |
|---|---|---|---|---|---|
| 15m | IC+ | 74/26 | -0.0 / %49.3 (8949) | -0.037 / %47.4 (5028) | ❌ mevcut kalır |
| 30m | IC+ | 55/45 | -0.043 / %47.3 (4321) | -0.055 / %46.6 (4587) | ❌ mevcut kalır |
| 1h | IC+ | 55/45 | -0.004 / %48.9 (2052) | -0.06 / %46.8 (2225) | ❌ mevcut kalır |
| 4h | mevcut | 58/42 | 0.022 / %50.3 (477) | 0.04 / %52.5 (516) | ✅ benimsendi |

Ağırlıklar:
- 15m: FVG+Likidite avı 70.3, VWAP 29.7
- 30m: Hacim 16.1, FVG+Likidite avı 5.2, VWAP 78.7
- 1h: Momentum 10.5, Hacim 54.8, VWAP 34.7
- 4h: Trend 20, Momentum 18, Open Interest 15, Hacim 10, Funding+L/S 10, FVG+Likidite avı 10, VWAP 5

## 4. Strateji yarışması (yalnız canlı botun da görebildiği veriler; eğitimde seçildi, TEST'te sınandı)

### 15m — 99 strateji denendi · ❌ hiçbiri yeterince iyi değil, mevcut kalır

Mevcut (trend, filtresiz) TEST: 9075 işlem, kazanma %49.3, ort R -0.0, PF 0.82

| # | Strateji | Eğitim ort R (n) | TEST ort R | TEST kazanma | TEST PF | 5x ort ROE | 10x ort ROE | 10x likidasyon |
|---|---|---|---|---|---|---|---|---|
| 1 | Likidite avı tersine dönüş +üst trend yönünde, SL1.0/TP1.5-2.5 | 0.053 (3913) | 0.032 | %41.0 (1667) | 0.8 | %-0.5 | %-1.0 | 1 |
| 2 | Ortalamaya dönüş (|Z|≥2.0, RSI 30/70), SL1.0/TP1.5-2.5 | 0.049 (3596) | 0.037 | %40.7 (1337) | 0.88 | %-0.32 | %-0.64 | 0 |
| 3 | Likidite avı tersine dönüş +üst trend yönünde, SL1.5/TP1.5-3.0 | 0.043 (3574) | 0.022 | %50.2 (1537) | 0.8 | %-0.6 | %-1.15 | 3 |
| 4 | Ortalamaya dönüş (|Z|≥2.5, RSI 30/70), SL1.0/TP1.5-2.5 | 0.039 (2142) | 0.044 | %40.8 (736) | 0.82 | %-0.49 | %-0.99 | 0 |
| 5 | Likidite avı tersine dönüş +üst trend yönünde, SL2.0/TP1.0-2.0 | 0.023 (3643) | 0.015 | %64.9 (1569) | 0.85 | %-0.39 | %-1.09 | 3 |

### 30m — 99 strateji denendi · ❌ hiçbiri yeterince iyi değil, mevcut kalır

Mevcut (trend, filtresiz) TEST: 4395 işlem, kazanma %47.7, ort R -0.034, PF 0.82

| # | Strateji | Eğitim ort R (n) | TEST ort R | TEST kazanma | TEST PF | 5x ort ROE | 10x ort ROE | 10x likidasyon |
|---|---|---|---|---|---|---|---|---|
| 1 | Ortalamaya dönüş (|Z|≥2.5, RSI 25/75, likidite avı şart), SL1.0/TP1.5-2.5 | 0.095 (274) | 0.127 | %43.0 (100) | 1.04 | %0.16 | %0.32 | 0 |
| 2 | Trend takibi (skor ≥58 / ≤42, VWAP'tan ≤2.0 ATR), SL1.5/TP1.5-3.0 | 0.027 (3374) | -0.018 | %48.8 (1448) | 0.85 | %-0.63 | %-1.24 | 2 |
| 3 | Trend takibi (skor ≥58 / ≤42, VWAP'tan ≤2.0 ATR) +üst trend yönünde, SL1.5/TP1.5-3.0 | 0.026 (3298) | -0.028 | %48.2 (1418) | 0.84 | %-0.7 | %-1.39 | 2 |
| 4 | Trend takibi (skor ≥66 / ≤34, VWAP'tan ≤2.0 ATR), SL1.5/TP1.5-3.0 | 0.024 (3339) | -0.013 | %49.1 (1422) | 0.86 | %-0.58 | %-1.15 | 2 |
| 5 | Trend takibi (skor ≥58 / ≤42, VWAP'tan ≤2.0 ATR), SL2.0/TP1.0-2.0 | 0.023 (3528) | -0.015 | %64.4 (1543) | 0.86 | %-0.53 | %-1.01 | 2 |

### 1h — 99 strateji denendi · ❌ hiçbiri yeterince iyi değil, mevcut kalır

Mevcut (trend, filtresiz) TEST: 2110 işlem, kazanma %48.9, ort R 0.0, PF 0.89

| # | Strateji | Eğitim ort R (n) | TEST ort R | TEST kazanma | TEST PF | 5x ort ROE | 10x ort ROE | 10x likidasyon |
|---|---|---|---|---|---|---|---|---|
| 1 | Trend takibi (skor ≥58 / ≤42, VWAP'tan ≤2.0 ATR) +üst trend yönünde, SL1.5/TP1.5-3.0 | 0.046 (1763) | 0.014 | %51.1 (759) | 0.86 | %-0.84 | %-1.51 | 4 |
| 2 | Trend takibi (skor ≥66 / ≤34, VWAP'tan ≤2.0 ATR) +üst trend yönünde, SL1.5/TP1.5-3.0 | 0.044 (1761) | 0.014 | %51.1 (756) | 0.86 | %-0.84 | %-1.5 | 4 |
| 3 | Trend takibi (skor ≥58 / ≤42, VWAP'tan ≤2.0 ATR), SL1.5/TP1.5-3.0 | 0.043 (1770) | 0.027 | %51.6 (772) | 0.89 | %-0.63 | %-1.1 | 4 |
| 4 | Trend takibi (skor ≥66 / ≤34, VWAP'tan ≤2.0 ATR), SL1.5/TP1.5-3.0 | 0.042 (1770) | 0.024 | %51.4 (769) | 0.89 | %-0.67 | %-1.17 | 4 |
| 5 | Trend takibi (skor ≥74 / ≤26), SL2.0/TP1.0-2.0 | 0.039 (1934) | 0.027 | %66.7 (781) | 0.94 | %-0.31 | %-0.51 | 5 |

### 4h — 87 strateji denendi · ✅ kazanan benimsendi

Mevcut (trend, filtresiz) TEST: 529 işlem, kazanma %52.4, ort R 0.04, PF 0.96

| # | Strateji | Eğitim ort R (n) | TEST ort R | TEST kazanma | TEST PF | 5x ort ROE | 10x ort ROE | 10x likidasyon |
|---|---|---|---|---|---|---|---|---|
| 1 | Trend takibi (skor ≥66 / ≤34, VWAP'tan ≤1.0 ATR), SL1.0/TP1.5-2.5 | 0.061 (493) | 0.151 | %47.0 (236) | 1.21 | %1.71 | %3.59 | 2 |
| 2 | Trend takibi (skor ≥58 / ≤42, VWAP'tan ≤1.0 ATR), SL1.0/TP1.5-2.5 | 0.059 (512) | 0.16 | %47.7 (241) | 1.22 | %1.78 | %3.72 | 2 |
| 3 | Trend takibi (skor ≥66 / ≤34, VWAP'tan ≤1.0 ATR) +üst trend yönünde, SL1.0/TP1.5-2.5 | 0.052 (492) | 0.174 | %47.9 (234) | 1.24 | %1.94 | %4.04 | 2 |
| 4 | Trend takibi (skor ≥58 / ≤42, VWAP'tan ≤1.0 ATR) +üst trend yönünde, SL1.0/TP1.5-2.5 | 0.049 (508) | 0.187 | %48.7 (238) | 1.27 | %2.16 | %4.48 | 2 |
| 5 | Trend takibi (skor ≥74 / ≤26) +üst trend yönünde, SL1.0/TP1.5-2.5 | 0.029 (516) | 0.123 | %44.8 (212) | 1.15 | %1.28 | %2.7 | 2 |


IC (bilgi katsayısı): gösterge puanı ile sonraki getiri arasındaki sıralama korelasyonu. Piyasada 0.02–0.05 bile anlamlıdır; negatif ise gösterge ters çalışıyor demektir.
Geçmiş performans geleceği garanti etmez.