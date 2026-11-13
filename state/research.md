# V5 Araştırma Raporu — 13.11.2026 18:54 UTC

40 coin · değerlendirme 15.08.2026'dan bugüne (90 gün) · eğitim/TEST ayrımı 17.10.2026

## 1. Mevcut model: kaldıraçlı işlem sonuçları (tüm dönem)

| Periyot | Kaldıraç | İşlem | Kazanma | Ort. ROE | PF | Ort. R | Likidasyon | 100$ marjla net | Maks. DD |
|---|---|---|---|---|---|---|---|---|---|
| 15m | 5x | 29627 | %49.6 | %-0.46 | 0.85 | 0.008 | 0 | -13582.0$ | 15306.0$ |
| 15m | 10x | 29629 | %49.6 | %-0.92 | 0.85 | 0.008 | 15 | -27345.0$ | 30808.0$ |
| 30m | 5x | 14252 | %50.4 | %-0.32 | 0.93 | 0.023 | 0 | -4557.0$ | 6926.0$ |
| 30m | 10x | 14259 | %50.4 | %-0.65 | 0.93 | 0.023 | 21 | -9271.0$ | 14020.0$ |
| 1h | 5x | 7007 | %50.5 | %-0.24 | 0.96 | 0.03 | 1 | -1681.0$ | 4021.0$ |
| 1h | 10x | 7024 | %50.5 | %-0.6 | 0.95 | 0.029 | 36 | -4239.0$ | 9024.0$ |
| 4h | 5x | 1842 | %55.0 | %1.61 | 1.14 | 0.132 | 6 | 2970.0$ | 2085.0$ |
| 4h | 10x | 1857 | %54.7 | %3.2 | 1.14 | 0.131 | 50 | 5949.0$ | 3894.0$ |

PF = kâr faktörü (toplam kazanç / toplam kayıp, 1 üstü kârlı). R = risk birimi (stop mesafesi).

## 2. Göstergelerin doğruluğu (TEST dönemi)

### 15m

| Bileşen | IC | İsabet | ↑ dediğinde yükseldi | ↓ dediğinde düştü | İşlemde aynı yöndeyken kazanma | Ters yöndeyken kazanma |
|---|---|---|---|---|---|---|
| Trend | -0.078 | %47.7 | %42.0 | %51.2 | %48.4 (7174) | %57.4 (310) |
| Momentum | -0.019 | %48.0 | %44.1 | %52.3 | %49.4 (5459) | %48.0 (1470) |
| Hacim | -0.036 | %48.9 | %44.5 | %51.4 | %50.0 (4765) | %47.9 (771) |
| Funding+L/S | -0.031 | %41.7 | %41.7 | %- | %46.5 (656) | %49.1 (794) |
| FVG+Likidite avı | -0.01 | %50.3 | %46.8 | %54.4 | %49.6 (3360) | %48.9 (2688) |
| VWAP | -0.037 | %48.1 | %42.5 | %52.0 | %48.9 (7643) | %49.4 (395) |

Ham göstergeler (IC, büyükten küçüğe): EMA dizilimi -0.089, Üst periyot trendi -0.078, Fiyat>EMA200 -0.064, RSI -0.049, VWAP üstü/altı -0.049, FVG -0.042, Z-Score -0.038, OBV yönü -0.024, Likidite avı +0.017, MACD yönü -0.016

### 30m

| Bileşen | IC | İsabet | ↑ dediğinde yükseldi | ↓ dediğinde düştü | İşlemde aynı yöndeyken kazanma | Ters yöndeyken kazanma |
|---|---|---|---|---|---|---|
| Trend | -0.101 | %49.0 | %40.5 | %53.0 | %45.7 (3379) | %54.0 (213) |
| Momentum | -0.045 | %47.1 | %41.8 | %52.8 | %49.8 (2782) | %46.1 (549) |
| Hacim | -0.087 | %47.5 | %40.7 | %50.5 | %46.3 (2340) | %47.8 (201) |
| Funding+L/S | -0.047 | %39.0 | %39.0 | %- | %46.0 (291) | %47.7 (415) |
| FVG+Likidite avı | 0.008 | %52.0 | %46.3 | %59.2 | %47.3 (1618) | %47.3 (1365) |
| VWAP | -0.051 | %48.1 | %40.9 | %53.0 | %46.3 (3440) | %55.2 (183) |

Ham göstergeler (IC, büyükten küçüğe): Üst periyot trendi -0.098, EMA dizilimi -0.088, Fiyat>EMA200 -0.084, RSI -0.080, OBV yönü -0.077, Z-Score -0.072, VWAP üstü/altı -0.060, FVG -0.048, Likidite avı +0.044, MACD yönü -0.044

### 1h

| Bileşen | IC | İsabet | ↑ dediğinde yükseldi | ↓ dediğinde düştü | İşlemde aynı yöndeyken kazanma | Ters yöndeyken kazanma |
|---|---|---|---|---|---|---|
| Trend | -0.107 | %50.3 | %37.8 | %54.5 | %49.3 (1575) | %50.0 (98) |
| Momentum | -0.074 | %45.8 | %38.8 | %53.1 | %47.3 (1430) | %58.0 (193) |
| Hacim | -0.094 | %46.9 | %38.6 | %49.6 | %46.2 (1109) | %63.9 (61) |
| Funding+L/S | -0.065 | %41.9 | %41.9 | %- | %38.8 (129) | %46.8 (205) |
| FVG+Likidite avı | 0.043 | %53.9 | %45.5 | %65.6 | %51.0 (796) | %44.1 (606) |
| VWAP | -0.064 | %48.1 | %39.7 | %53.8 | %46.1 (1470) | %66.7 (171) |

Ham göstergeler (IC, büyükten küçüğe): RSI -0.118, Fiyat>EMA200 -0.111, Üst periyot trendi -0.105, EMA dizilimi -0.098, Z-Score -0.089, Taker alım -0.069, Likidite avı +0.063, Funding +0.050, VWAP üstü/altı -0.049, OBV yönü -0.042

### 4h

| Bileşen | IC | İsabet | ↑ dediğinde yükseldi | ↓ dediğinde düştü | İşlemde aynı yöndeyken kazanma | Ters yöndeyken kazanma |
|---|---|---|---|---|---|---|
| Trend | -0.151 | %53.3 | %35.2 | %56.3 | %54.5 (378) | %34.6 (26) |
| Momentum | -0.161 | %43.2 | %36.3 | %49.7 | %47.1 (333) | %71.2 (52) |
| Hacim | -0.198 | %44.7 | %28.3 | %47.9 | %44.4 (207) | %65.0 (20) |
| Funding+L/S | -0.053 | %40.5 | %40.5 | %- | %41.7 (36) | %49.1 (57) |
| FVG+Likidite avı | 0.064 | %57.5 | %51.1 | %66.9 | %52.2 (203) | %49.4 (158) |
| VWAP | -0.176 | %47.4 | %29.6 | %54.2 | %43.9 (319) | %59.0 (39) |

Ham göstergeler (IC, büyükten küçüğe): Z-Score -0.218, RSI -0.198, VWAP üstü/altı -0.149, OBV yönü -0.140, Likidite avı +0.133, Taker alım -0.125, Fiyat>EMA200 -0.117, RVOL +0.107, MACD yönü -0.105, FVG -0.089

## 3. Öğrenme: yeni ağırlıklar (eğitimde bulundu, TEST'te sınandı)

| Periyot | Yöntem | Eşik | Mevcut model TEST ort. R / kazanma | Yeni model TEST ort. R / kazanma | Karar |
|---|---|---|---|---|---|
| 15m | IC± | 70/30 | 0.003 / %49.5 (8970) | 0.011 / %49.6 (3805) | ✅ benimsendi |
| 30m | IC± | 66/34 | -0.035 / %47.5 (4303) | 0.009 / %49.1 (2219) | ✅ benimsendi |
| 1h | IC+ | 66/34 | 0.004 / %49.3 (2046) | -0.031 / %47.6 (1911) | ❌ mevcut kalır |
| 4h | mevcut | 58/42 | 0.031 / %50.6 (476) | 0.053 / %53.1 (516) | ✅ benimsendi |

Ağırlıklar:
- 15m: Momentum -33.5, Hacim -20.7, Funding+L/S -26.0, FVG+Likidite avı 8.6, VWAP 10.6
- 30m: Momentum -37.8, Hacim 8.2, Funding+L/S -29.9, VWAP 18.5
- 1h: Momentum 15.3, Hacim 47.6, VWAP 37.1
- 4h: Trend 20, Momentum 18, Open Interest 15, Hacim 10, Funding+L/S 10, FVG+Likidite avı 10, VWAP 5

## 4. Strateji yarışması (yalnız canlı botun da görebildiği veriler; eğitimde seçildi, TEST'te sınandı)

### 15m — 163 strateji denendi · ❌ hiçbiri yeterince iyi değil, mevcut kalır

Mevcut (trend, filtresiz) TEST: 2988 işlem, kazanma %46.8, ort R -0.047, PF 0.78

| # | Strateji | Eğitim ort R (n) | TEST ort R | TEST kazanma | TEST PF | 5x ort ROE | 10x ort ROE | 10x likidasyon |
|---|---|---|---|---|---|---|---|---|
| 1 | Geri çekilmede limit giriş (skor ≥66 / ≤34, dip-tepe aralığının en fazla %50'inde, 0.382 Fibonacci geri çekilmesine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) | 0.105 (1862) | 0.067 | %42.8 (778) | 0.97 | %-0.14 | %-0.24 | 3 |
| 2 | Geri çekilmede limit giriş (skor ≥66 / ≤34, dip-tepe aralığının en fazla %50'inde, 0.5 Fibonacci geri çekilmesine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) | 0.105 (1862) | 0.067 | %42.8 (778) | 0.97 | %-0.14 | %-0.24 | 3 |
| 3 | Geri çekilmede limit giriş (skor ≥66 / ≤34, dip-tepe aralığının en fazla %50'inde, 0.382 Fibonacci geri çekilmesine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) +üst trend yönünde | 0.101 (1824) | 0.071 | %42.7 (761) | 0.98 | %-0.09 | %-0.13 | 3 |
| 4 | Geri çekilmede limit giriş (skor ≥66 / ≤34, dip-tepe aralığının en fazla %50'inde, 0.5 Fibonacci geri çekilmesine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) +üst trend yönünde | 0.101 (1824) | 0.071 | %42.7 (761) | 0.98 | %-0.09 | %-0.13 | 3 |
| 5 | Geri çekilmede limit giriş (skor ≥58 / ≤42, dip-tepe aralığının en fazla %70'inde, 0.5 Fibonacci geri çekilmesine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) +üst trend yönünde | 0.071 (2846) | -0.006 | %38.4 (1258) | 0.92 | %-0.31 | %-0.58 | 3 |

### 30m — 163 strateji denendi · ❌ hiçbiri yeterince iyi değil, mevcut kalır

Mevcut (trend, filtresiz) TEST: 1470 işlem, kazanma %49.5, ort R -0.005, PF 0.85

| # | Strateji | Eğitim ort R (n) | TEST ort R | TEST kazanma | TEST PF | 5x ort ROE | 10x ort ROE | 10x likidasyon |
|---|---|---|---|---|---|---|---|---|
| 1 | Geri çekilmede limit giriş (skor ≥58 / ≤42, dip-tepe aralığının en fazla %70'inde, fiyatın 0.5 ATR gerisine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) +üst trend yönünde | 0.056 (1573) | 0.005 | %41.8 (696) | 0.83 | %-0.97 | %-1.78 | 3 |
| 2 | Geri çekilmede limit giriş (skor ≥66 / ≤34, dip-tepe aralığının en fazla %70'inde, fiyatın 1.0 ATR gerisine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) | 0.061 (1245) | 0.005 | %41.4 (561) | 0.77 | %-1.15 | %-2.11 | 1 |
| 3 | Trend takibi (skor ≥58 / ≤42, VWAP'tan ≤2.0 ATR), SL1.5/TP1.5-3.0 | 0.036 (3381) | 0.008 | %49.8 (1435) | 0.91 | %-0.37 | %-0.73 | 2 |
| 4 | Trend takibi (skor ≥58 / ≤42, VWAP'tan ≤2.0 ATR) +üst trend yönünde, SL1.5/TP1.5-3.0 | 0.036 (3304) | -0.005 | %49.0 (1406) | 0.89 | %-0.5 | %-0.99 | 2 |
| 5 | Geri çekilmede limit giriş (skor ≥58 / ≤42, dip-tepe aralığının en fazla %70'inde, 0.382 Fibonacci geri çekilmesine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) | 0.051 (1616) | -0.03 | %40.5 (682) | 0.8 | %-1.39 | %-2.83 | 5 |

### 1h — 163 strateji denendi · ❌ hiçbiri yeterince iyi değil, mevcut kalır

Mevcut (trend, filtresiz) TEST: 731 işlem, kazanma %55.0, ort R 0.099, PF 1.05

| # | Strateji | Eğitim ort R (n) | TEST ort R | TEST kazanma | TEST PF | 5x ort ROE | 10x ort ROE | 10x likidasyon |
|---|---|---|---|---|---|---|---|---|
| 1 | Trend takibi (skor ≥58 / ≤42, VWAP'tan ≤2.0 ATR), SL1.5/TP1.5-3.0 | 0.072 (1774) | 0.033 | %51.4 (764) | 0.88 | %-0.75 | %-1.32 | 6 |
| 2 | Trend takibi (skor ≥58 / ≤42, VWAP'tan ≤2.0 ATR) +üst trend yönünde, SL1.5/TP1.5-3.0 | 0.072 (1756) | 0.023 | %51.1 (753) | 0.86 | %-0.91 | %-1.62 | 6 |
| 3 | Trend takibi (skor ≥66 / ≤34, VWAP'tan ≤2.0 ATR) +üst trend yönünde, SL1.5/TP1.5-3.0 | 0.072 (1753) | 0.025 | %51.2 (752) | 0.86 | %-0.89 | %-1.59 | 6 |
| 4 | Trend takibi (skor ≥66 / ≤34, VWAP'tan ≤2.0 ATR), SL1.5/TP1.5-3.0 | 0.071 (1769) | 0.033 | %51.4 (762) | 0.88 | %-0.75 | %-1.32 | 6 |
| 5 | Trend takibi (skor ≥66 / ≤34, VWAP'tan ≤2.0 ATR), SL1.0/TP1.5-2.5 | 0.056 (2058) | 0.06 | %42.1 (870) | 0.95 | %-0.25 | %-0.48 | 1 |

### 4h — 151 strateji denendi · ✅ kazanan benimsendi

Mevcut (trend, filtresiz) TEST: 189 işlem, kazanma %55.6, ort R 0.062, PF 0.95

| # | Strateji | Eğitim ort R (n) | TEST ort R | TEST kazanma | TEST PF | 5x ort ROE | 10x ort ROE | 10x likidasyon |
|---|---|---|---|---|---|---|---|---|
| 1 | Trend takibi (skor ≥66 / ≤34, VWAP'tan ≤1.0 ATR), SL1.0/TP1.5-2.5 | 0.114 (496) | 0.17 | %47.6 (231) | 1.28 | %2.3 | %4.77 | 2 |
| 2 | Trend takibi (skor ≥58 / ≤42, VWAP'tan ≤1.0 ATR), SL1.0/TP1.5-2.5 | 0.107 (517) | 0.168 | %47.9 (238) | 1.28 | %2.28 | %4.72 | 2 |
| 3 | Trend takibi (skor ≥66 / ≤34, VWAP'tan ≤1.0 ATR) +üst trend yönünde, SL1.0/TP1.5-2.5 | 0.099 (494) | 0.199 | %48.7 (228) | 1.34 | %2.71 | %5.58 | 2 |
| 4 | Trend takibi (skor ≥58 / ≤42, VWAP'tan ≤1.0 ATR) +üst trend yönünde, SL1.0/TP1.5-2.5 | 0.085 (514) | 0.203 | %49.4 (235) | 1.34 | %2.76 | %5.68 | 2 |
| 5 | Geri çekilmede limit giriş (skor ≥66 / ≤34, dip-tepe aralığının en fazla %70'inde, 0.5 Fibonacci geri çekilmesine limit emir, 6 mum geçerli, stop son 12 mumun dibinin/tepesinin ötesi, hedef 1.5R / 3.0R) | 0.126 (153) | 0.075 | %44.4 (63) | 0.84 | %-3.28 | %-2.31 | 11 |


IC (bilgi katsayısı): gösterge puanı ile sonraki getiri arasındaki sıralama korelasyonu. Piyasada 0.02–0.05 bile anlamlıdır; negatif ise gösterge ters çalışıyor demektir.
Geçmiş performans geleceği garanti etmez.