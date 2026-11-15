# 🚀 Dipten Dönüş Raporu — 15.11.2026

120 coin, son 120 gün, 1 saatlik mumlar. 728 dip tetiği (yeni 30g dip + dipten %3 dönüş); bunların %8.7'i 7 gün içinde dibin %20 üstüne çıktı (başarılı dönüş). Eğitim/TEST ayrımı 03.11.2026.

## Başarılı dönüşlerden önce ne oluyor? (başarısız diplerle kıyas, medyan)

| Öncü işaret | Başarılı | Başarısız | Etki (eğitim) | Etki (test) | Kalıcı |
|---|---|---|---|---|---|
| BTC son 24s % | 0.322 | -0.316 | +0.48 | -0.12 | ✗ |
| Stop mesafesi % | 3.869 | 3.946 | +0.41 | -0.12 | ✗ |
| BTC son 7g % | -1.652 | -1.834 | +0.26 | +0.01 | ✗ |
| Agresif alım değişimi (24s - önceki 72s) | -0.006 | -0.009 | +0.24 | +0.35 | ✓ |
| RSI(14s) tetikte | 50.277 | 47.296 | +0.23 | -0.42 | ✗ |
| Likidite avı (7g dibin altına fitil, üstünde kapanış) | 0.0 | 0.0 | -0.20 | -0.57 | ✓ |
| Son 24s agresif alım oranı | 0.48 | 0.474 | +0.16 | +0.07 | ✗ |
| Dipten bu yana saat | 5.0 | 4.0 | +0.16 | -0.55 | ✗ |
| Son 24s hacim / önceki 7g ort. | 1.055 | 1.073 | +0.09 | -0.30 | ✗ |
| Funding (son) | 0.005 | 0.002 | +0.08 | None | ✗ |
| 30 günlük tepeden düşüş % | -29.238 | -30.457 | +0.06 | -0.97 | ✗ |
| RSI pozitif uyumsuzluk (dip daha alçak, RSI daha yüksek) | 0.0 | 0.0 | -0.04 | -0.30 | ✗ |
| Dibe son 24s'te düşüş % | -6.847 | -7.784 | -0.02 | -0.17 | ✗ |
| Dip mumunun alt fitil oranı | 0.412 | 0.436 | +0.02 | -0.40 | ✗ |

Etki: standart fark (+ = başarılı dönüşlerde daha yüksek). Kalıcı ✓: eğitim ve test döneminde aynı yönde ve belirgin.

## Strateji simülasyonu (tetikte gir, stop dibin altı, hedef 1,5R + 3R, en çok 7 gün)

Her dipte körlemesine giriş — TEST: 221 işlem, kazanma %25.8, ort -0.497R, 3x ort ROE %-5.99, PF 0.35

| Kural (yalnız canlı verilebilen işaretler) | Eğitim ort R (n, başarılı %) | TEST n / kazanma / ort R / PF | 3x ort ROE | 5x ort ROE |
|---|---|---|---|---|
| Stop mesafesi % ≤ 3.64 VE BTC son 24s % ≥ -1.08 VE Hacim eğilimi (son 3g / önceki 7g) ≤ 1.09 | 0.764 (47, %25.5) | 5 / %20.0 / -0.679 / 0.18 | %-7.0 | %-11.67 |
| Stop mesafesi % ≤ 3.64 VE BTC son 24s % ≥ -0.217 VE Dipten bu yana saat ≥ 2 | 0.752 (47, %23.4) | 3 / %0.0 / -1.029 / 0.0 | %-10.65 | %-17.76 |
| Stop mesafesi % ≤ 3.64 VE BTC son 24s % ≥ -0.217 VE BTC son 7g % ≥ -3.11 | 0.683 (47, %21.3) | 0 / %None / None / None | %None | %None |
| Stop mesafesi % ≤ 3.64 VE BTC son 24s % ≥ -0.217 | 0.645 (50, %22.0) | 3 / %0.0 / -1.029 / 0.0 | %-10.65 | %-17.76 |
| Stop mesafesi % ≤ 3.64 VE BTC son 24s % ≥ -1.08 VE Oynaklık sıkışması (24s ATR / 7g ATR) ≤ 1 | 0.659 (44, %22.7) | 5 / %20.0 / -0.679 / 0.18 | %-7.04 | %-11.74 |

Futures verisi (OI, funding, L/S) de dahil edilince:

| Kural | Eğitim ort R (n) | TEST n / ort R / PF |
|---|---|---|
| Stop mesafesi % ≤ 3.64 VE BTC son 24s % ≥ -1.08 VE Hacim eğilimi (son 3g / önceki 7g) ≤ 1.09 | 0.764 (47) | 5 / -0.679 / 0.18 |
| Stop mesafesi % ≤ 3.64 VE BTC son 24s % ≥ -0.217 VE Dipten bu yana saat ≥ 2 | 0.752 (47) | 3 / -1.029 / 0.0 |
| Stop mesafesi % ≤ 3.64 VE BTC son 24s % ≥ -0.217 VE BTC son 7g % ≥ -3.11 | 0.683 (47) | 0 / None / None |

Karar: ❌ hiçbir kural TEST dönemini yeterince geçemedi; kâğıt hesapta ileri test olarak izleniyor

## Son 120 günün en büyük dipten dönüşleri

- BMT 18.10.2026 20:00: dipten +%216.5 (öncesinde 30g tepeden %-29.2, RVOL 0.76, OI 72s %None, funding 0.005)
- SHELL 13.11.2026 03:00: dipten +%172.5 (öncesinde 30g tepeden %-34.9, RVOL 1.36, OI 72s %None, funding None)
- SHELL 08.11.2026 21:00: dipten +%165.9 (öncesinde 30g tepeden %-33.2, RVOL 0.69, OI 72s %None, funding None)
- ONE 05.11.2026 15:00: dipten +%141.5 (öncesinde 30g tepeden %-56.0, RVOL 1.39, OI 72s %None, funding None)
- HOME 30.07.2026 17:00: dipten +%139.8 (öncesinde 30g tepeden %-73.3, RVOL 0.68, OI 72s %None, funding 0.005)
- ONE 03.11.2026 03:00: dipten +%130.2 (öncesinde 30g tepeden %-55.8, RVOL 0.79, OI 72s %None, funding None)
- SOPH 08.11.2026 21:00: dipten +%123.4 (öncesinde 30g tepeden %-69.4, RVOL 0.61, OI 72s %None, funding None)
- ERA 19.07.2026 14:00: dipten +%122.1 (öncesinde 30g tepeden %-34.6, RVOL 1.39, OI 72s %None, funding -0.0)
- LSK 25.10.2026 08:00: dipten +%98.2 (öncesinde 30g tepeden %-57.0, RVOL 1.4, OI 72s %None, funding 0.0047)
- BARD 10.11.2026 13:00: dipten +%91.8 (öncesinde 30g tepeden %-28.4, RVOL 2.78, OI 72s %None, funding None)
- ALLO 16.09.2026 17:00: dipten +%82.0 (öncesinde 30g tepeden %-40.8, RVOL 0.71, OI 72s %None, funding 0.005)
- SOPH 26.10.2026 10:00: dipten +%81.9 (öncesinde 30g tepeden %-66.0, RVOL 0.51, OI 72s %None, funding -0.164)

## Şu an dipten dönen coinler (son 48 saat)

- BTC: dip 62006, şimdi 64012.6 (5 saat önce tetik), 30g düşüş %-27.0, RVOL 1.88 · 🔥 CoinGecko trend
- AVAX: dip 6.743, şimdi 7.16 (5 saat önce tetik), 30g düşüş %-35.9, RVOL 1.38
- LTC: dip 42.67, şimdi 44.74 (5 saat önce tetik), 30g düşüş %-31.6, RVOL 1.96
- INJ: dip 6.56, şimdi 6.963 (5 saat önce tetik), 30g düşüş %-30.3, RVOL 1.88
- PUMP: dip 0.002726, şimdi 0.002897 (5 saat önce tetik), 30g düşüş %-47.8, RVOL 1.87
- PENDLE: dip 1.33, şimdi 1.402 (5 saat önce tetik), 30g düşüş %-40.1, RVOL 1.91
- SKY: dip 0.05042, şimdi 0.05589 (5 saat önce tetik), 30g düşüş %-34.8, RVOL 1.93
- BNCB: dip 3.67, şimdi 3.83 (5 saat önce tetik), 30g düşüş %-37.8, RVOL 0.91
- MORPHO: dip 1.691, şimdi 1.748 (5 saat önce tetik), 30g düşüş %-34.2, RVOL 1.54
- MUBARAK: dip 0.02784, şimdi 0.02828 (5 saat önce tetik), 30g düşüş %-52.8, RVOL 1.92
- NEAR: dip 2.87, şimdi 3.119 (8 saat önce tetik), 30g düşüş %-47.3, RVOL 1.59
- DOGE: dip 0.05543, şimdi 0.05757 (8 saat önce tetik), 30g düşüş %-33.9, RVOL 2.09 · 🔥 CoinGecko trend
- PEPE: dip 3.69e-06, şimdi 3.91e-06 (8 saat önce tetik), 30g düşüş %-35.0, RVOL 1.05 · 🔥 CoinGecko trend
- SUI: dip 0.6755, şimdi 0.7143 (8 saat önce tetik), 30g düşüş %-36.4, RVOL 1.72
- ADA: dip 0.1432, şimdi 0.1499 (8 saat önce tetik), 30g düşüş %-38.7, RVOL 2.16
- LINK: dip 8.574, şimdi 9.038 (8 saat önce tetik), 30g düşüş %-33.1, RVOL 1.76
- TAO: dip 177.5, şimdi 186.7 (8 saat önce tetik), 30g düşüş %-39.1, RVOL 2.1
- AAVE: dip 97.02, şimdi 104.61 (8 saat önce tetik), 30g düşüş %-41.5, RVOL 1.38
- XLM: dip 0.13, şimdi 0.1375 (8 saat önce tetik), 30g düşüş %-30.6, RVOL 1.59
- TRUMP: dip 0.891, şimdi 0.939 (8 saat önce tetik), 30g düşüş %-53.6, RVOL 1.75
- ZRO: dip 1.342, şimdi 1.453 (8 saat önce tetik), 30g düşüş %-41.2, RVOL 1.75
- FET: dip 0.1209, şimdi 0.1302 (8 saat önce tetik), 30g düşüş %-42.2, RVOL 1.49
- ARB: dip 0.124, şimdi 0.1323 (8 saat önce tetik), 30g düşüş %-39.2, RVOL 0.75
- ICP: dip 2.103, şimdi 2.172 (8 saat önce tetik), 30g düşüş %-32.6, RVOL 1.88
- XPL: dip 0.04034, şimdi 0.04344 (8 saat önce tetik), 30g düşüş %-53.5, RVOL 1.74
- APT: dip 0.4283, şimdi 0.4492 (8 saat önce tetik), 30g düşüş %-51.9, RVOL 2.38
- DOT: dip 0.683, şimdi 0.715 (8 saat önce tetik), 30g düşüş %-43.7, RVOL 2.27
- RENDER: dip 1.314, şimdi 1.364 (8 saat önce tetik), 30g düşüş %-34.3, RVOL 2.0
- TIA: dip 0.3278, şimdi 0.3454 (8 saat önce tetik), 30g düşüş %-57.4, RVOL 2.22
- STRK: dip 0.032, şimdi 0.03557 (8 saat önce tetik), 30g düşüş %-63.9, RVOL 1.71
- ETHFI: dip 0.4685, şimdi 0.5045 (8 saat önce tetik), 30g düşüş %-35.8, RVOL 1.45
- SHIB: dip 3.7e-06, şimdi 3.86e-06 (8 saat önce tetik), 30g düşüş %-29.8, RVOL 2.03
- BONK: dip 2.19e-06, şimdi 2.34e-06 (8 saat önce tetik), 30g düşüş %-35.0, RVOL 2.34
- OP: dip 0.0757, şimdi 0.0812 (8 saat önce tetik), 30g düşüş %-47.4, RVOL 2.24
- VIRTUAL: dip 0.4175, şimdi 0.4389 (8 saat önce tetik), 30g düşüş %-40.9, RVOL 1.96
- POL: dip 0.07616, şimdi 0.07975 (8 saat önce tetik), 30g düşüş %-23.9, RVOL 1.24
- RAY: dip 1.3048, şimdi 1.3682 (8 saat önce tetik), 30g düşüş %-37.5, RVOL 1.69
- SEI: dip 0.03631, şimdi 0.0383 (8 saat önce tetik), 30g düşüş %-46.3, RVOL 1.9
- EIGEN: dip 0.1246, şimdi 0.1328 (8 saat önce tetik), 30g düşüş %-55.8, RVOL 2.47
- CRV: dip 0.1959, şimdi 0.2072 (8 saat önce tetik), 30g düşüş %-52.2, RVOL 1.83
- ETC: dip 5.62, şimdi 5.83 (8 saat önce tetik), 30g düşüş %-31.5, RVOL 1.51
- PLUME: dip 0.01152, şimdi 0.01252 (8 saat önce tetik), 30g düşüş %-45.4, RVOL 1.56
- ZK: dip 0.00742, şimdi 0.00791 (8 saat önce tetik), 30g düşüş %-60.6, RVOL 2.08
- STX: dip 0.2531, şimdi 0.2629 (8 saat önce tetik), 30g düşüş %-41.9, RVOL 1.66
- ATOM: dip 1.218, şimdi 1.28 (8 saat önce tetik), 30g düşüş %-33.0, RVOL 1.72
- LDO: dip 0.2556, şimdi 0.2686 (8 saat önce tetik), 30g düşüş %-39.1, RVOL 1.6
- HOME: dip 0.00389, şimdi 0.00421 (8 saat önce tetik), 30g düşüş %-31.0, RVOL 2.56
- ZEN: dip 3.815, şimdi 4.084 (8 saat önce tetik), 30g düşüş %-41.7, RVOL 1.68
- CHIP: dip 0.025, şimdi 0.0276 (8 saat önce tetik), 30g düşüş %-56.6, RVOL 1.31
- CFX: dip 0.03226, şimdi 0.03408 (8 saat önce tetik), 30g düşüş %-43.5, RVOL 2.82
- JTO: dip 0.2549, şimdi 0.2679 (8 saat önce tetik), 30g düşüş %-48.5, RVOL 2.01
- ORDI: dip 2.553, şimdi 2.726 (8 saat önce tetik), 30g düşüş %-36.4, RVOL 1.9
- APE: dip 0.076, şimdi 0.0788 (8 saat önce tetik), 30g düşüş %-51.6, RVOL 1.71
- S: dip 0.03146, şimdi 0.03364 (8 saat önce tetik), 30g düşüş %-47.3, RVOL 1.43
- 0G: dip 0.1336, şimdi 0.1326 (8 saat önce tetik), 30g düşüş %-48.0, RVOL 1.35
- GALA: dip 0.001258, şimdi 0.001335 (8 saat önce tetik), 30g düşüş %-40.2, RVOL 1.99
- INIT: dip 0.09409, şimdi 0.12395 (10 saat önce tetik), 30g düşüş %-76.2, RVOL 0.58
- AR: dip 2.435, şimdi 2.599 (10 saat önce tetik), 30g düşüş %-40.2, RVOL 2.07
- MITO: dip 0.00611, şimdi 0.00639 (10 saat önce tetik), 30g düşüş %-58.0, RVOL 2.03
- STO: dip 0.0243, şimdi 0.0237 (14 saat önce tetik), 30g düşüş %-32.1, RVOL 5.24
- AERO: dip 0.435, şimdi 0.4351 (16 saat önce tetik), 30g düşüş %-55.6, RVOL 1.12 · 🔥 CoinGecko trend
- ASTER: dip 0.6171, şimdi 0.5288 (27 saat önce tetik), 30g düşüş %-15.8, RVOL 0.98
- NBISB: dip 109.2, şimdi 110.52 (27 saat önce tetik), 30g düşüş %-43.2, RVOL 1.43
- BNB: dip 622.41, şimdi 586.78 (42 saat önce tetik), 30g düşüş %-18.3, RVOL 1.81
- CAKE: dip 1.686, şimdi 1.607 (43 saat önce tetik), 30g düşüş %-26.4, RVOL 1.64
- ETH: dip 1895.95, şimdi 1782.25 (44 saat önce tetik), 30g düşüş %-25.0, RVOL 1.72 · 🔥 CoinGecko trend
- SOL: dip 77.92, şimdi 69.96 (45 saat önce tetik), 30g düşüş %-28.6, RVOL 1.77 · 🔥 CoinGecko trend
- HBAR: dip 0.06064, şimdi 0.05681 (45 saat önce tetik), 30g düşüş %-32.4, RVOL 1.85
- BCH: dip 214.1, şimdi 203.5 (45 saat önce tetik), 30g düşüş %-29.8, RVOL 0.85
- 币安人生: dip 0.4565, şimdi 0.4639 (45 saat önce tetik), 30g düşüş %-17.0, RVOL 1.4
- XRP: dip 0.9975, şimdi 0.9478 (47 saat önce tetik), 30g düşüş %-28.7, RVOL 1.19 · 🔥 CoinGecko trend

CoinGecko'da şu an trend olanlar: BTC, KAVA, HYPE, ETH, XRP, QTC, SOL, DOGE, ZEC, BDX, PI, AERO, PEPE, PENGU, WLFI

Simülasyon/araştırmadır, yatırım tavsiyesi değildir.