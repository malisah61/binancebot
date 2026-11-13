# V5 Araştırma Raporu — 13.11.2026 13:50 UTC

38 coin · değerlendirme 15.08.2026'dan bugüne (90 gün) · eğitim/TEST ayrımı 17.10.2026

## 1. Mevcut model: kaldıraçlı işlem sonuçları (tüm dönem)

| Periyot | Kaldıraç | İşlem | Kazanma | Ort. ROE | PF | Ort. R | Likidasyon | 100$ marjla net | Maks. DD |
|---|---|---|---|---|---|---|---|---|---|
| 15m | 5x | 28435 | %48.8 | %-0.49 | 0.83 | 0.002 | 0 | -13946.0$ | 15618.0$ |
| 15m | 10x | 28435 | %48.8 | %-0.98 | 0.83 | 0.002 | 9 | -27947.0$ | 31299.0$ |
| 30m | 5x | 13655 | %50.2 | %-0.34 | 0.91 | 0.017 | 0 | -4641.0$ | 6964.0$ |
| 30m | 10x | 13661 | %50.2 | %-0.71 | 0.91 | 0.017 | 10 | -9661.0$ | 14337.0$ |
| 1h | 5x | 6719 | %50.0 | %-0.3 | 0.95 | 0.017 | 1 | -2042.0$ | 4456.0$ |
| 1h | 10x | 6726 | %50.0 | %-0.61 | 0.95 | 0.018 | 17 | -4106.0$ | 8962.0$ |
| 4h | 5x | 1771 | %55.1 | %1.75 | 1.17 | 0.128 | 2 | 3095.0$ | 1853.0$ |
| 4h | 10x | 1775 | %55.0 | %3.59 | 1.18 | 0.13 | 28 | 6365.0$ | 3804.0$ |

PF = kâr faktörü (toplam kazanç / toplam kayıp, 1 üstü kârlı). R = risk birimi (stop mesafesi).

## 2. Göstergelerin doğruluğu (TEST dönemi)

### 15m

| Bileşen | IC | İsabet | ↑ dediğinde yükseldi | ↓ dediğinde düştü | İşlemde aynı yöndeyken kazanma | Ters yöndeyken kazanma |
|---|---|---|---|---|---|---|
| Trend | -0.084 | %47.3 | %41.9 | %50.6 | %47.7 (6816) | %56.9 (297) |
| Momentum | -0.026 | %47.5 | %43.9 | %51.6 | %49.0 (5189) | %47.0 (1414) |
| Hacim | -0.04 | %48.6 | %44.8 | %50.7 | %49.7 (4604) | %45.6 (722) |
| Funding+L/S | -0.019 | %42.4 | %42.4 | %- | %46.2 (574) | %48.1 (727) |
| FVG+Likidite avı | -0.011 | %50.4 | %47.4 | %53.9 | %48.8 (3175) | %48.4 (2566) |
| VWAP | -0.048 | %47.6 | %42.4 | %51.4 | %48.0 (7247) | %50.6 (395) |

Ham göstergeler (IC, büyükten küçüğe): EMA dizilimi -0.094, Üst periyot trendi -0.084, Fiyat>EMA200 -0.067, VWAP üstü/altı -0.059, RSI -0.057, Z-Score -0.047, FVG -0.045, OBV yönü -0.026, MACD yönü -0.020, Likidite avı +0.019

### 30m

| Bileşen | IC | İsabet | ↑ dediğinde yükseldi | ↓ dediğinde düştü | İşlemde aynı yöndeyken kazanma | Ters yöndeyken kazanma |
|---|---|---|---|---|---|---|
| Trend | -0.106 | %48.5 | %40.2 | %52.4 | %45.0 (3218) | %53.6 (207) |
| Momentum | -0.047 | %46.8 | %41.9 | %52.1 | %49.3 (2668) | %46.7 (522) |
| Hacim | -0.092 | %46.9 | %40.4 | %49.7 | %45.8 (2265) | %48.2 (199) |
| Funding+L/S | -0.029 | %40.5 | %40.5 | %- | %46.8 (252) | %47.1 (359) |
| FVG+Likidite avı | 0.006 | %52.0 | %46.7 | %58.6 | %46.6 (1574) | %46.6 (1295) |
| VWAP | -0.063 | %47.5 | %40.8 | %52.2 | %45.6 (3287) | %54.2 (177) |

Ham göstergeler (IC, büyükten küçüğe): Üst periyot trendi -0.100, EMA dizilimi -0.092, RSI -0.087, Fiyat>EMA200 -0.083, OBV yönü -0.081, Z-Score -0.076, VWAP üstü/altı -0.070, FVG -0.048, Likidite avı +0.043, MACD yönü -0.040

### 1h

| Bileşen | IC | İsabet | ↑ dediğinde yükseldi | ↓ dediğinde düştü | İşlemde aynı yöndeyken kazanma | Ters yöndeyken kazanma |
|---|---|---|---|---|---|---|
| Trend | -0.107 | %49.9 | %37.7 | %54.1 | %48.7 (1500) | %47.9 (94) |
| Momentum | -0.081 | %45.4 | %39.0 | %52.4 | %46.4 (1368) | %55.9 (179) |
| Hacim | -0.103 | %46.5 | %37.3 | %49.4 | %45.0 (1065) | %68.9 (61) |
| Funding+L/S | -0.047 | %42.4 | %42.4 | %- | %36.2 (105) | %45.5 (189) |
| FVG+Likidite avı | 0.05 | %54.6 | %45.6 | %67.0 | %51.3 (748) | %42.8 (580) |
| VWAP | -0.079 | %47.3 | %39.3 | %52.8 | %44.8 (1405) | %68.2 (151) |

Ham göstergeler (IC, büyükten küçüğe): RSI -0.126, Fiyat>EMA200 -0.116, Üst periyot trendi -0.102, Z-Score -0.099, EMA dizilimi -0.088, Taker alım -0.071, Likidite avı +0.069, VWAP üstü/altı -0.065, OBV yönü -0.050, MACD yönü -0.039

### 4h

| Bileşen | IC | İsabet | ↑ dediğinde yükseldi | ↓ dediğinde düştü | İşlemde aynı yöndeyken kazanma | Ters yöndeyken kazanma |
|---|---|---|---|---|---|---|
| Trend | -0.14 | %53.5 | %35.4 | %56.4 | %55.0 (367) | %34.8 (23) |
| Momentum | -0.161 | %43.2 | %36.4 | %49.9 | %49.5 (307) | %68.6 (51) |
| Hacim | -0.194 | %45.3 | %26.4 | %48.4 | %46.7 (197) | %57.9 (19) |
| Funding+L/S | -0.031 | %38.0 | %38.0 | %- | %40.0 (25) | %46.0 (50) |
| FVG+Likidite avı | 0.082 | %58.0 | %51.6 | %67.3 | %53.2 (186) | %50.3 (145) |
| VWAP | -0.181 | %46.9 | %29.5 | %53.9 | %45.4 (295) | %57.5 (40) |

Ham göstergeler (IC, büyükten küçüğe): Z-Score -0.218, RSI -0.203, VWAP üstü/altı -0.155, OBV yönü -0.149, Likidite avı +0.139, Fiyat>EMA200 -0.114, RVOL +0.110, Taker alım -0.110, MACD yönü -0.106, FVG -0.077

## 3. Öğrenme: yeni ağırlıklar (eğitimde bulundu, TEST'te sınandı)

| Periyot | Yöntem | Eşik | Mevcut model TEST ort. R / kazanma | Yeni model TEST ort. R / kazanma | Karar |
|---|---|---|---|---|---|
| 15m | IC± | 70/30 | 0.001 / %48.8 (8527) | -0.009 / %48.4 (5066) | ❌ mevcut kalır |
| 30m | IC+ | 58/42 | -0.044 / %47.0 (4118) | -0.059 / %46.0 (4321) | ❌ mevcut kalır |
| 1h | IC+ | 70/30 | -0.008 / %48.5 (1951) | -0.025 / %48.6 (1480) | ❌ mevcut kalır |
| 4h | mevcut | 58/42 | 0.05 / %51.8 (450) | 0.06 / %53.7 (486) | ✅ benimsendi |

Ağırlıklar:
- 15m: Momentum -36.2, Hacim -21.8, Funding+L/S -22.2, FVG+Likidite avı 8.1, VWAP 6.3
- 30m: Hacim 32.5, VWAP 67.5
- 1h: Momentum 13.4, Hacim 51.8, VWAP 34.8
- 4h: Trend 20, Momentum 18, Open Interest 15, Hacim 10, Funding+L/S 10, FVG+Likidite avı 10, VWAP 5

IC (bilgi katsayısı): gösterge puanı ile sonraki getiri arasındaki sıralama korelasyonu. Piyasada 0.02–0.05 bile anlamlıdır; negatif ise gösterge ters çalışıyor demektir.
Geçmiş performans geleceği garanti etmez.