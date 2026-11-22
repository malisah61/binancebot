# 🚀 Dipten Dönüş Raporu — 22.11.2026

120 coin, son 120 gün, 1 saatlik mumlar. 768 dip tetiği (yeni 30g dip + dipten %3 dönüş); bunların %9.1'i 7 gün içinde dibin %20 üstüne çıktı (başarılı dönüş). Eğitim/TEST ayrımı 09.11.2026.

## Başarılı dönüşlerden önce ne oluyor? (başarısız diplerle kıyas, medyan)

| Öncü işaret | Başarılı | Başarısız | Etki (eğitim) | Etki (test) | Kalıcı |
|---|---|---|---|---|---|
| Likidite avı (7g dibin altına fitil, üstünde kapanış) | 0.0 | 0.0 | -0.45 | -0.20 | ✓ |
| BTC son 7g % | -2.237 | -2.237 | +0.31 | -0.81 | ✗ |
| BTC son 24s % | 0.106 | -0.451 | +0.24 | -0.71 | ✗ |
| Stop mesafesi % | 3.859 | 3.941 | +0.21 | +0.71 | ✓ |
| Dip mumunun alt fitil oranı | 0.381 | 0.429 | -0.21 | +0.34 | ✗ |
| Dipten bu yana saat | 5.0 | 3.0 | +0.19 | -0.13 | ✗ |
| Global L/S | 1.036 | 1.106 | -0.18 | +0.52 | ✗ |
| Son 24s hacim / önceki 7g ort. | 1.029 | 1.041 | +0.16 | +0.76 | ✓ |
| Dibe son 24s'te düşüş % | -8.302 | -8.331 | -0.12 | -1.00 | ✓ |
| RSI(14s) tetikte | 44.693 | 45.631 | +0.07 | -0.85 | ✗ |
| RSI pozitif uyumsuzluk (dip daha alçak, RSI daha yüksek) | 0.0 | 0.0 | -0.07 | -0.52 | ✗ |
| Top trader L/S | 2.231 | 2.301 | +0.07 | +0.26 | ✗ |
| OI değişimi son 24s % | -3.709 | -3.439 | -0.06 | -1.03 | ✗ |
| Funding (son) | 0.005 | 0.002 | -0.06 | None | ✗ |

Etki: standart fark (+ = başarılı dönüşlerde daha yüksek). Kalıcı ✓: eğitim ve test döneminde aynı yönde ve belirgin.

## Strateji simülasyonu (tetikte gir, stop dibin altı, hedef 1,5R + 3R, en çok 7 gün)

Her dipte körlemesine giriş — TEST: 243 işlem, kazanma %25.9, ort -0.433R, 3x ort ROE %-5.35, PF 0.35

| Kural (yalnız canlı verilebilen işaretler) | Eğitim ort R (n, başarılı %) | TEST n / kazanma / ort R / PF | 3x ort ROE | 5x ort ROE |
|---|---|---|---|---|
| BTC son 24s % ≥ 0.329 VE Likidite avı (7g dibin altına fitil, üstünde kapanış) ≤ 0 | 0.493 (82, %22.0) | 3 / %0.0 / -1.023 / 0.0 | %-13.47 | %-22.46 |
| Dip mumunun alt fitil oranı ≤ 0.243 VE BTC son 24s % ≥ -0.39 VE BTC son 7g % ≥ -3.14 | 0.634 (46, %17.4) | 0 / %None / None / None | %None | %None |
| Dip mumunun alt fitil oranı ≤ 0.243 VE BTC son 24s % ≥ -0.39 VE RSI(14s) tetikte ≥ 34.7 | 0.634 (46, %17.4) | 2 / %0.0 / -1.028 / 0.0 | %-10.85 | %-18.09 |
| Dip mumunun alt fitil oranı ≤ 0.243 VE BTC son 24s % ≥ -0.39 VE Dibe son 24s'te düşüş % ≥ -11.8 | 0.649 (43, %18.6) | 2 / %0.0 / -1.028 / 0.0 | %-10.85 | %-18.09 |
| Dip mumunun alt fitil oranı ≤ 0.243 VE Dibe son 24s'te düşüş % ≥ -10.2 VE BTC son 7g % ≥ -4.05 | 0.639 (43, %16.3) | 7 / %42.9 / -0.273 / 0.58 | %-3.16 | %-5.26 |

Futures verisi (OI, funding, L/S) de dahil edilince:

| Kural | Eğitim ort R (n) | TEST n / ort R / PF |
|---|---|---|
| BTC son 24s % ≥ 0.329 VE Likidite avı (7g dibin altına fitil, üstünde kapanış) ≤ 0 | 0.493 (82) | 3 / -1.023 / 0.0 |
| Dip mumunun alt fitil oranı ≤ 0.243 VE BTC son 24s % ≥ -0.39 VE BTC son 7g % ≥ -3.14 | 0.634 (46) | 0 / None / None |
| Dip mumunun alt fitil oranı ≤ 0.243 VE BTC son 24s % ≥ -0.39 VE RSI(14s) tetikte ≥ 34.7 | 0.634 (46) | 2 / -1.028 / 0.0 |

Karar: ❌ hiçbir kural TEST dönemini yeterince geçemedi; kâğıt hesapta ileri test olarak izleniyor

## Son 120 günün en büyük dipten dönüşleri

- BMT 18.10.2026 20:00: dipten +%216.5 (öncesinde 30g tepeden %-29.2, RVOL 0.76, OI 72s %-8.8, funding 0.005)
- MMT 13.11.2026 03:00: dipten +%184.8 (öncesinde 30g tepeden %-36.5, RVOL 1.34, OI 72s %-7.0, funding None)
- ONE 05.11.2026 15:00: dipten +%141.5 (öncesinde 30g tepeden %-56.0, RVOL 1.39, OI 72s %-16.2, funding None)
- ONE 03.11.2026 03:00: dipten +%130.2 (öncesinde 30g tepeden %-55.8, RVOL 0.79, OI 72s %-2.2, funding None)
- SOPH 08.11.2026 21:00: dipten +%123.4 (öncesinde 30g tepeden %-69.4, RVOL 0.61, OI 72s %-3.0, funding None)
- BARD 10.11.2026 13:00: dipten +%91.8 (öncesinde 30g tepeden %-28.4, RVOL 2.78, OI 72s %-13.2, funding None)
- RARE 13.11.2026 03:00: dipten +%88.9 (öncesinde 30g tepeden %-39.9, RVOL 1.62, OI 72s %0.3, funding None)
- SOPH 26.10.2026 10:00: dipten +%81.9 (öncesinde 30g tepeden %-66.0, RVOL 0.51, OI 72s %-37.1, funding -0.164)
- CYBER 05.11.2026 15:00: dipten +%79.5 (öncesinde 30g tepeden %-45.3, RVOL 0.68, OI 72s %-11.7, funding None)
- HOT 29.10.2026 07:00: dipten +%78.3 (öncesinde 30g tepeden %-29.0, RVOL 1.15, OI 72s %1.3, funding 0.01)
- HUMA 14.11.2026 21:00: dipten +%70.7 (öncesinde 30g tepeden %-80.2, RVOL 0.73, OI 72s %-14.0, funding None)
- YB 14.11.2026 21:00: dipten +%69.4 (öncesinde 30g tepeden %-43.7, RVOL 0.98, OI 72s %-20.6, funding None)

## Şu an dipten dönen coinler (son 48 saat)

- EWYB: dip 122.64, şimdi 126.14 (17 saat önce tetik), 30g düşüş %-26.6, RVOL 1.69
- LDO: dip 0.2202, şimdi 0.2307 (21 saat önce tetik), 30g düşüş %-45.0, RVOL 1.84
- ETH: dip 1538, şimdi 1663.32 (24 saat önce tetik), 30g düşüş %-37.2, RVOL 1.95 · 🔥 CoinGecko trend
- HYPE: dip 55.8, şimdi 60.14 (24 saat önce tetik), 30g düşüş %-42.9, RVOL 1.64 · 🔥 CoinGecko trend
- ASTER: dip 0.4672, şimdi 0.4898 (24 saat önce tetik), 30g düşüş %-36.2, RVOL 0.6
- ZRO: dip 1.062, şimdi 1.163 (24 saat önce tetik), 30g düşüş %-45.5, RVOL 1.5
- INIT: dip 0.08534, şimdi 0.09065 (24 saat önce tetik), 30g düşüş %-78.4, RVOL 0.57
- ONE: dip 0.000988, şimdi 0.00096 (24 saat önce tetik), 30g düşüş %-60.1, RVOL 0.76
- SC: dip 0.000531, şimdi 0.000586 (30 saat önce tetik), 30g düşüş %-45.1, RVOL 3.3
- SOL: dip 67.15, şimdi 69.2 (32 saat önce tetik), 30g düşüş %-37.6, RVOL 1.14
- NEAR: dip 2.764, şimdi 2.875 (32 saat önce tetik), 30g düşüş %-48.2, RVOL 1.41
- XRP: dip 0.8842, şimdi 0.9159 (32 saat önce tetik), 30g düşüş %-35.6, RVOL 1.15
- DOGE: dip 0.05254, şimdi 0.05423 (32 saat önce tetik), 30g düşüş %-36.2, RVOL 1.28
- SUI: dip 0.6317, şimdi 0.6401 (32 saat önce tetik), 30g düşüş %-39.1, RVOL 1.63
- LTC: dip 39.45, şimdi 39.04 (32 saat önce tetik), 30g düşüş %-36.3, RVOL 1.34
- WLD: dip 0.2247, şimdi 0.2253 (32 saat önce tetik), 30g düşüş %-61.9, RVOL 1.45
- AVAX: dip 6.398, şimdi 6.519 (32 saat önce tetik), 30g düşüş %-34.2, RVOL 0.94
- HBAR: dip 0.05005, şimdi 0.05063 (32 saat önce tetik), 30g düşüş %-40.9, RVOL 1.45
- XLM: dip 0.1249, şimdi 0.1273 (32 saat önce tetik), 30g düşüş %-32.3, RVOL 1.36
- GRAM: dip 0.956, şimdi 0.942 (32 saat önce tetik), 30g düşüş %-30.1, RVOL 1.09
- ICP: dip 1.974, şimdi 1.883 (32 saat önce tetik), 30g düşüş %-32.4, RVOL 1.15
- SKHYB: dip 102.69, şimdi 107.47 (32 saat önce tetik), 30g düşüş %-38.2, RVOL 1.07
- ETHFI: dip 0.4264, şimdi 0.4808 (32 saat önce tetik), 30g düşüş %-40.6, RVOL 0.97
- DASH: dip 32.35, şimdi 34.69 (32 saat önce tetik), 30g düşüş %-42.2, RVOL 1.39
- RAY: dip 1.256, şimdi 1.2961 (32 saat önce tetik), 30g düşüş %-36.9, RVOL 1.31
- POL: dip 0.07355, şimdi 0.07413 (32 saat önce tetik), 30g düşüş %-26.5, RVOL 1.83
- SHIB: dip 3.48e-06, şimdi 3.58e-06 (32 saat önce tetik), 30g düşüş %-32.8, RVOL 1.59
- ETC: dip 5.32, şimdi 5.46 (32 saat önce tetik), 30g düşüş %-34.6, RVOL 1.36
- PYTH: dip 0.04615, şimdi 0.04806 (32 saat önce tetik), 30g düşüş %-41.9, RVOL 1.16
- VANA: dip 0.552, şimdi 0.57 (32 saat önce tetik), 30g düşüş %-40.6, RVOL 1.36
- VIRTUAL: dip 0.3694, şimdi 0.3699 (32 saat önce tetik), 30g düşüş %-46.7, RVOL 1.16
- WIF: dip 0.1178, şimdi 0.1165 (32 saat önce tetik), 30g düşüş %-44.4, RVOL 1.31
- SEI: dip 0.0342, şimdi 0.03375 (32 saat önce tetik), 30g düşüş %-46.4, RVOL 1.54
- S: dip 0.02652, şimdi 0.02681 (32 saat önce tetik), 30g düşüş %-53.5, RVOL 1.29
- ATOM: dip 1.197, şimdi 1.15 (32 saat önce tetik), 30g düşüş %-34.2, RVOL 1.33
- EIGEN: dip 0.1105, şimdi 0.1143 (32 saat önce tetik), 30g düşüş %-55.1, RVOL 1.34
- MORPHO: dip 1.48, şimdi 1.544 (32 saat önce tetik), 30g düşüş %-41.0, RVOL 1.41
- ALGO: dip 0.0712, şimdi 0.0735 (32 saat önce tetik), 30g düşüş %-37.7, RVOL 1.47
- UNI: dip 4.313, şimdi 4.616 (33 saat önce tetik), 30g düşüş %-44.8, RVOL 1.11
- ENA: dip 0.0952, şimdi 0.0979 (33 saat önce tetik), 30g düşüş %-56.3, RVOL 1.31
- ADA: dip 0.1379, şimdi 0.1418 (33 saat önce tetik), 30g düşüş %-39.6, RVOL 1.24
- TAO: dip 173.2, şimdi 186 (33 saat önce tetik), 30g düşüş %-37.4, RVOL 1.37
- LINK: dip 8.246, şimdi 8.56 (33 saat önce tetik), 30g düşüş %-35.0, RVOL 1.35
- AAVE: dip 93.91, şimdi 95.81 (33 saat önce tetik), 30g düşüş %-40.1, RVOL 1.03
- INJ: dip 5.994, şimdi 5.957 (33 saat önce tetik), 30g düşüş %-31.5, RVOL 1.17
- ORCA: dip 1.041, şimdi 1.222 (33 saat önce tetik), 30g düşüş %-49.1, RVOL 1.49
- ONDO: dip 0.2719, şimdi 0.2775 (33 saat önce tetik), 30g düşüş %-41.7, RVOL 1.43
- BCH: dip 187.8, şimdi 195.6 (33 saat önce tetik), 30g düşüş %-38.4, RVOL 1.56
- RENDER: dip 1.231, şimdi 1.327 (33 saat önce tetik), 30g düşüş %-36.1, RVOL 1.63
- 牛来: dip 0.0328, şimdi 0.03515 (33 saat önce tetik), 30g düşüş %-55.6, RVOL 1.5
- DOT: dip 0.65, şimdi 0.645 (33 saat önce tetik), 30g düşüş %-46.0, RVOL 1.33
- STRK: dip 0.0293, şimdi 0.03005 (33 saat önce tetik), 30g düşüş %-50.9, RVOL 1.56
- TIA: dip 0.3124, şimdi 0.3216 (33 saat önce tetik), 30g düşüş %-49.6, RVOL 1.02
- OP: dip 0.068, şimdi 0.0699 (33 saat önce tetik), 30g düşüş %-48.1, RVOL 1.2
- BONK: dip 2.03e-06, şimdi 2.03e-06 (33 saat önce tetik), 30g düşüş %-39.8, RVOL 1.42
- AR: dip 2.124, şimdi 2.255 (33 saat önce tetik), 30g düşüş %-46.1, RVOL 1.24
- STX: dip 0.2361, şimdi 0.2485 (33 saat önce tetik), 30g düşüş %-40.8, RVOL 1.11
- 币安人生: dip 0.42, şimdi 0.4414 (33 saat önce tetik), 30g düşüş %-23.6, RVOL 1.3
- NBISB: dip 80.88, şimdi 85.04 (33 saat önce tetik), 30g düşüş %-56.2, RVOL 1.42
- GIGGLE: dip 19.95, şimdi 20.69 (33 saat önce tetik), 30g düşüş %-40.3, RVOL 1.06
- ZEC: dip 745.88, şimdi 785.04 (36 saat önce tetik), 30g düşüş %-46.7, RVOL 1.55 · 🔥 CoinGecko trend
- TRUMP: dip 0.814, şimdi 0.889 (36 saat önce tetik), 30g düşüş %-57.1, RVOL 1.49 · 🔥 CoinGecko trend
- PENGU: dip 0.004141, şimdi 0.004218 (36 saat önce tetik), 30g düşüş %-50.3, RVOL 0.64 · 🔥 CoinGecko trend
- PLUME: dip 0.0102, şimdi 0.01056 (36 saat önce tetik), 30g düşüş %-46.1, RVOL 1.41
- QNT: dip 134.96, şimdi 138.32 (38 saat önce tetik), 30g düşüş %-39.7, RVOL 0.95
- PARTI: dip 0.0309, şimdi 0.0362 (39 saat önce tetik), 30g düşüş %-53.1, RVOL 1.2
- PEPE: dip 3.51e-06, şimdi 3.33e-06 (44 saat önce tetik), 30g düşüş %-38.2, RVOL 1.27
- ARB: dip 0.1163, şimdi 0.1109 (47 saat önce tetik), 30g düşüş %-41.4, RVOL 1.17
- MARSCOIN: dip 0.0302, şimdi 0.0286 (47 saat önce tetik), 30g düşüş %-64.2, RVOL 0.95
- AERO: dip 0.4065, şimdi 0.3994 (47 saat önce tetik), 30g düşüş %-53.4, RVOL 1.29

CoinGecko'da şu an trend olanlar: TRUMP, BTC, PENGU, EVAA, AKE, PEARL, VVV, PIEVERSE, ETH, HYPE, ZEC, LIT, SKY, XAUT, BDX

## İleri test defteri (canlı kaydedilen dipler, 7 gün sonra sonuçlanır; açık: 22)

- Tümü: 171 dip, %8.8 başarılı dönüş, ort -0.578R
- Kurala uyanlar: 3 dip, %0.0 başarılı, ort -1.02R
- İnternette trend olan (CoinGecko): 18 dip, %5.6 başarılı, ort -0.844R · trend olmayan: 153 dip, %9.2, ort -0.547R

Simülasyon/araştırmadır, yatırım tavsiyesi değildir.