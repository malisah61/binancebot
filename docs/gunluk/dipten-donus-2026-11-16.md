# 🚀 Dipten Dönüş Raporu — 16.11.2026

119 coin, son 120 gün, 1 saatlik mumlar. 681 dip tetiği (yeni 30g dip + dipten %3 dönüş); bunların %8.7'i 7 gün içinde dibin %20 üstüne çıktı (başarılı dönüş). Eğitim/TEST ayrımı 03.11.2026.

## Başarılı dönüşlerden önce ne oluyor? (başarısız diplerle kıyas, medyan)

| Öncü işaret | Başarılı | Başarısız | Etki (eğitim) | Etki (test) | Kalıcı |
|---|---|---|---|---|---|
| BTC son 24s % | 0.322 | -0.304 | +0.56 | -0.25 | ✗ |
| Top trader L/S | 2.03 | 2.166 | -0.41 | -0.37 | ✓ |
| BTC son 7g % | -1.341 | -1.936 | +0.39 | -0.02 | ✗ |
| Likidite avı (7g dibin altına fitil, üstünde kapanış) | 0.0 | 0.0 | -0.33 | -0.55 | ✓ |
| Funding (son) | 0.003 | 0.002 | -0.26 | None | ✗ |
| RSI(14s) tetikte | 52.029 | 47.602 | +0.25 | -0.44 | ✗ |
| Stop mesafesi % | 4.002 | 3.93 | +0.24 | +0.11 | ✓ |
| Dip mumunun alt fitil oranı | 0.386 | 0.447 | -0.20 | -0.44 | ✓ |
| 30 günlük tepeden düşüş % | -30.344 | -30.738 | +0.14 | -1.23 | ✗ |
| Dipten bu yana saat | 5.0 | 4.0 | +0.14 | -0.53 | ✗ |
| Son 24s hacim / önceki 7g ort. | 0.995 | 1.045 | +0.13 | -0.10 | ✗ |
| Hacim eğilimi (son 3g / önceki 7g) | 0.974 | 0.921 | +0.13 | -0.16 | ✗ |
| RSI pozitif uyumsuzluk (dip daha alçak, RSI daha yüksek) | 0.0 | 0.0 | -0.12 | -0.28 | ✓ |
| Agresif alım değişimi (24s - önceki 72s) | -0.008 | -0.009 | +0.12 | +0.62 | ✓ |

Etki: standart fark (+ = başarılı dönüşlerde daha yüksek). Kalıcı ✓: eğitim ve test döneminde aynı yönde ve belirgin.

## Strateji simülasyonu (tetikte gir, stop dibin altı, hedef 1,5R + 3R, en çok 7 gün)

Her dipte körlemesine giriş — TEST: 208 işlem, kazanma %25.0, ort -0.514R, 3x ort ROE %-6.09, PF 0.34

| Kural (yalnız canlı verilebilen işaretler) | Eğitim ort R (n, başarılı %) | TEST n / kazanma / ort R / PF | 3x ort ROE | 5x ort ROE |
|---|---|---|---|---|
| Dip mumunun alt fitil oranı ≤ 0.256 VE BTC son 24s % ≥ -0.217 VE Son 24s hacim / önceki 7g ort. ≤ 1.25 | 0.72 (45, %17.8) | 0 / %None / None / None | %None | %None |
| BTC son 24s % ≥ -0.217 VE Stop mesafesi % ≤ 3.64 VE Dipten bu yana saat ≥ 2 | 0.72 (44, %22.7) | 2 / %0.0 / -1.029 / 0.0 | %-10.57 | %-17.62 |
| Dip mumunun alt fitil oranı ≤ 0.256 VE BTC son 24s % ≥ -0.217 VE Oynaklık sıkışması (24s ATR / 7g ATR) ≤ 0.987 | 0.77 (38, %13.2) | 0 / %None / None / None | %None | %None |
| BTC son 24s % ≥ -0.217 VE Stop mesafesi % ≤ 3.64 VE Hacim eğilimi (son 3g / önceki 7g) ≤ 1.26 | 0.754 (38, %23.7) | 3 / %0.0 / -1.029 / 0.0 | %-10.59 | %-17.65 |
| BTC son 24s % ≥ -0.217 VE Stop mesafesi % ≤ 3.64 VE RSI(14s) tetikte ≥ 36.8 | 0.754 (37, %24.3) | 3 / %0.0 / -1.029 / 0.0 | %-10.59 | %-17.65 |

Futures verisi (OI, funding, L/S) de dahil edilince:

| Kural | Eğitim ort R (n) | TEST n / ort R / PF |
|---|---|---|
| BTC son 24s % ≥ -0.217 VE Stop mesafesi % ≤ 3.64 VE Dipten bu yana saat ≥ 2 | 0.72 (44) | 2 / -1.029 / 0.0 |
| Dip mumunun alt fitil oranı ≤ 0.256 VE BTC son 24s % ≥ -0.217 VE Oynaklık sıkışması (24s ATR / 7g ATR) ≤ 0.987 | 0.77 (38) | 0 / None / None |
| Dip mumunun alt fitil oranı ≤ 0.256 VE Funding (son) ≤ 0.00188 VE RSI(14s) tetikte ≥ 36.8 | 0.768 (38) | 0 / None / None |

Karar: ❌ hiçbir kural TEST dönemini yeterince geçemedi; kâğıt hesapta ileri test olarak izleniyor

## Son 120 günün en büyük dipten dönüşleri

- BMT 18.10.2026 20:00: dipten +%216.5 (öncesinde 30g tepeden %-29.2, RVOL 0.76, OI 72s %-8.8, funding 0.005)
- SHELL 13.11.2026 03:00: dipten +%172.5 (öncesinde 30g tepeden %-34.9, RVOL 1.36, OI 72s %-4.9, funding None)
- SHELL 08.11.2026 21:00: dipten +%165.9 (öncesinde 30g tepeden %-33.2, RVOL 0.69, OI 72s %-0.9, funding None)
- ONE 05.11.2026 15:00: dipten +%141.5 (öncesinde 30g tepeden %-56.0, RVOL 1.39, OI 72s %-16.2, funding None)
- ONE 03.11.2026 03:00: dipten +%130.2 (öncesinde 30g tepeden %-55.8, RVOL 0.79, OI 72s %-2.2, funding None)
- SOPH 08.11.2026 21:00: dipten +%123.4 (öncesinde 30g tepeden %-69.4, RVOL 0.61, OI 72s %-3.0, funding None)
- ERA 19.07.2026 14:00: dipten +%122.1 (öncesinde 30g tepeden %-34.6, RVOL 1.39, OI 72s %None, funding -0.0)
- LSK 25.10.2026 08:00: dipten +%98.2 (öncesinde 30g tepeden %-57.0, RVOL 1.4, OI 72s %-14.8, funding 0.0047)
- BARD 10.11.2026 13:00: dipten +%91.8 (öncesinde 30g tepeden %-28.4, RVOL 2.78, OI 72s %-13.2, funding None)
- ALLO 16.09.2026 17:00: dipten +%82.0 (öncesinde 30g tepeden %-40.8, RVOL 0.71, OI 72s %-10.9, funding 0.005)
- SOPH 26.10.2026 10:00: dipten +%81.9 (öncesinde 30g tepeden %-66.0, RVOL 0.51, OI 72s %-37.1, funding -0.164)
- SOPH 24.10.2026 03:00: dipten +%67.4 (öncesinde 30g tepeden %-63.1, RVOL 3.55, OI 72s %-14.2, funding -0.1713)

## Şu an dipten dönen coinler (son 48 saat)

- SOPH: dip 0.00097, şimdi 0.00097 (4 saat önce tetik), 30g düşüş %-62.8, RVOL 2.01
- BERA: dip 0.0863, şimdi 0.0885 (4 saat önce tetik), 30g düşüş %-54.9, RVOL 0.68 · ✅ kurala uyuyor
- BTC: dip 62006, şimdi 64709.8 (28 saat önce tetik), 30g düşüş %-27.0, RVOL 1.88 · 🔥 CoinGecko trend
- LTC: dip 42.67, şimdi 44.76 (28 saat önce tetik), 30g düşüş %-31.6, RVOL 1.96
- AVAX: dip 6.743, şimdi 7.141 (28 saat önce tetik), 30g düşüş %-35.9, RVOL 1.38
- INJ: dip 6.56, şimdi 6.742 (28 saat önce tetik), 30g düşüş %-30.3, RVOL 1.88
- PUMP: dip 0.002726, şimdi 0.002867 (28 saat önce tetik), 30g düşüş %-47.8, RVOL 1.87 · 🔥 CoinGecko trend
- BNCB: dip 3.67, şimdi 3.72 (28 saat önce tetik), 30g düşüş %-37.8, RVOL 0.91
- SKY: dip 0.05042, şimdi 0.05361 (28 saat önce tetik), 30g düşüş %-34.8, RVOL 1.93
- JUV: dip 0.214, şimdi 0.226 (28 saat önce tetik), 30g düşüş %-34.4, RVOL 1.47
- PENDLE: dip 1.33, şimdi 1.446 (28 saat önce tetik), 30g düşüş %-40.1, RVOL 1.91
- NEAR: dip 2.87, şimdi 3.165 (31 saat önce tetik), 30g düşüş %-47.3, RVOL 1.59 · 🔥 CoinGecko trend
- DOGE: dip 0.05543, şimdi 0.05892 (31 saat önce tetik), 30g düşüş %-33.9, RVOL 2.09
- PEPE: dip 3.69e-06, şimdi 3.77e-06 (31 saat önce tetik), 30g düşüş %-35.0, RVOL 1.05
- SUI: dip 0.6755, şimdi 0.7222 (31 saat önce tetik), 30g düşüş %-36.4, RVOL 1.72
- ADA: dip 0.1432, şimdi 0.1529 (31 saat önce tetik), 30g düşüş %-38.7, RVOL 2.16
- LINK: dip 8.574, şimdi 9.136 (31 saat önce tetik), 30g düşüş %-33.1, RVOL 1.76
- RARE: dip 0.00822, şimdi 0.01287 (31 saat önce tetik), 30g düşüş %-44.1, RVOL 1.91
- AAVE: dip 97.02, şimdi 109.82 (31 saat önce tetik), 30g düşüş %-41.5, RVOL 1.38
- TAO: dip 177.5, şimdi 190.9 (31 saat önce tetik), 30g düşüş %-39.1, RVOL 2.1
- ZRO: dip 1.342, şimdi 1.38 (31 saat önce tetik), 30g düşüş %-41.2, RVOL 1.75
- XPL: dip 0.04034, şimdi 0.04294 (31 saat önce tetik), 30g düşüş %-53.5, RVOL 1.74
- XLM: dip 0.13, şimdi 0.1388 (31 saat önce tetik), 30g düşüş %-30.6, RVOL 1.59
- TRUMP: dip 0.891, şimdi 0.944 (31 saat önce tetik), 30g düşüş %-53.6, RVOL 1.75
- GLMR: dip 0.005414, şimdi 0.006629 (31 saat önce tetik), 30g düşüş %-52.6, RVOL 1.12
- FET: dip 0.1209, şimdi 0.1302 (31 saat önce tetik), 30g düşüş %-42.2, RVOL 1.49
- ARB: dip 0.124, şimdi 0.133 (31 saat önce tetik), 30g düşüş %-39.2, RVOL 0.75
- ICP: dip 2.103, şimdi 2.219 (31 saat önce tetik), 30g düşüş %-32.6, RVOL 1.88
- TLM: dip 0.000863, şimdi 0.00091 (31 saat önce tetik), 30g düşüş %-40.5, RVOL 1.39
- CRV: dip 0.1959, şimdi 0.2023 (31 saat önce tetik), 30g düşüş %-52.2, RVOL 1.83
- APT: dip 0.4283, şimdi 0.4567 (31 saat önce tetik), 30g düşüş %-51.9, RVOL 2.38
- STRK: dip 0.032, şimdi 0.03453 (31 saat önce tetik), 30g düşüş %-63.9, RVOL 1.71
- DOT: dip 0.683, şimdi 0.724 (31 saat önce tetik), 30g düşüş %-43.7, RVOL 2.27
- TIA: dip 0.3278, şimdi 0.3514 (31 saat önce tetik), 30g düşüş %-57.4, RVOL 2.22
- RENDER: dip 1.314, şimdi 1.37 (31 saat önce tetik), 30g düşüş %-34.3, RVOL 2.0
- SHIB: dip 3.7e-06, şimdi 3.89e-06 (31 saat önce tetik), 30g düşüş %-29.8, RVOL 2.03
- POL: dip 0.07616, şimdi 0.07945 (31 saat önce tetik), 30g düşüş %-23.9, RVOL 1.24
- BONK: dip 2.19e-06, şimdi 2.31e-06 (31 saat önce tetik), 30g düşüş %-35.0, RVOL 2.34
- OP: dip 0.0757, şimdi 0.0803 (31 saat önce tetik), 30g düşüş %-47.4, RVOL 2.24
- RAY: dip 1.3048, şimdi 1.3916 (31 saat önce tetik), 30g düşüş %-37.5, RVOL 1.69
- 0G: dip 0.1336, şimdi 0.1248 (31 saat önce tetik), 30g düşüş %-48.0, RVOL 1.35
- ETHFI: dip 0.4685, şimdi 0.4781 (31 saat önce tetik), 30g düşüş %-35.8, RVOL 1.45
- SAHARA: dip 0.00502, şimdi 0.00542 (31 saat önce tetik), 30g düşüş %-41.8, RVOL 2.07
- AUDIO: dip 0.01032, şimdi 0.01076 (31 saat önce tetik), 30g düşüş %-38.5, RVOL 3.23
- VIRTUAL: dip 0.4175, şimdi 0.4455 (31 saat önce tetik), 30g düşüş %-40.9, RVOL 1.96
- SEI: dip 0.03631, şimdi 0.03951 (31 saat önce tetik), 30g düşüş %-46.3, RVOL 1.9
- LDO: dip 0.2556, şimdi 0.2775 (31 saat önce tetik), 30g düşüş %-39.1, RVOL 1.6
- XEC: dip 4.83e-06, şimdi 5.2e-06 (31 saat önce tetik), 30g düşüş %-39.6, RVOL 1.55
- ZK: dip 0.00742, şimdi 0.00795 (31 saat önce tetik), 30g düşüş %-60.6, RVOL 2.08
- ATOM: dip 1.218, şimdi 1.297 (31 saat önce tetik), 30g düşüş %-33.0, RVOL 1.72
- CHIP: dip 0.025, şimdi 0.02706 (31 saat önce tetik), 30g düşüş %-56.6, RVOL 1.31
- STX: dip 0.2531, şimdi 0.2644 (31 saat önce tetik), 30g düşüş %-41.9, RVOL 1.66
- ORDI: dip 2.553, şimdi 2.785 (31 saat önce tetik), 30g düşüş %-36.4, RVOL 1.9
- INIT: dip 0.09409, şimdi 0.10171 (33 saat önce tetik), 30g düşüş %-76.2, RVOL 0.58
- AR: dip 2.435, şimdi 2.512 (33 saat önce tetik), 30g düşüş %-40.2, RVOL 2.07
- AERO: dip 0.435, şimdi 0.4175 (39 saat önce tetik), 30g düşüş %-55.6, RVOL 1.12

CoinGecko'da şu an trend olanlar: LIT, BTC, SKR, PENGU, SOL, ASTER, HYPE, PUMP, NEAR, VVV, ETH, ZEC, PEARL, XMR, AKE

## İleri test defteri (canlı kaydedilen dipler, 7 gün sonra sonuçlanır; açık: 64)

- Tümü: 16 dip, %6.2 başarılı dönüş, ort -0.822R
- Kurala uyanlar: 0 dip, %None başarılı, ort NoneR
- İnternette trend olan (CoinGecko): 4 dip, %0.0 başarılı, ort -1.027R · trend olmayan: 12 dip, %8.3, ort -0.754R

Simülasyon/araştırmadır, yatırım tavsiyesi değildir.