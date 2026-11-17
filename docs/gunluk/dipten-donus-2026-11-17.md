# 🚀 Dipten Dönüş Raporu — 17.11.2026

117 coin, son 120 gün, 1 saatlik mumlar. 692 dip tetiği (yeni 30g dip + dipten %3 dönüş); bunların %9.1'i 7 gün içinde dibin %20 üstüne çıktı (başarılı dönüş). Eğitim/TEST ayrımı 05.11.2026.

## Başarılı dönüşlerden önce ne oluyor? (başarısız diplerle kıyas, medyan)

| Öncü işaret | Başarılı | Başarısız | Etki (eğitim) | Etki (test) | Kalıcı |
|---|---|---|---|---|---|
| Top trader L/S | 2.095 | 2.17 | -0.36 | +0.53 | ✗ |
| BTC son 24s % | 0.229 | -0.324 | +0.34 | -0.19 | ✗ |
| OI değişimi son 24s % | -3.46 | -1.999 | -0.33 | +0.04 | ✗ |
| Stop mesafesi % | 4.005 | 3.936 | +0.32 | -0.09 | ✗ |
| OI değişimi dipten önceki 72s % | -11.288 | -8.865 | -0.25 | +0.40 | ✗ |
| Likidite avı (7g dibin altına fitil, üstünde kapanış) | 0.0 | 0.0 | -0.25 | -0.06 | ✗ |
| BTC son 7g % | -1.974 | -2.109 | +0.21 | +0.09 | ✗ |
| Agresif alım değişimi (24s - önceki 72s) | -0.005 | -0.009 | +0.18 | +0.53 | ✓ |
| Global L/S 24s değişim | -0.04 | -0.025 | +0.17 | -0.06 | ✗ |
| Global L/S | 1.101 | 1.031 | +0.15 | -0.25 | ✗ |
| Son 24s hacim / önceki 7g ort. | 1.098 | 1.045 | +0.14 | -0.16 | ✗ |
| Dipten bu yana saat | 5.0 | 4.0 | +0.14 | +0.27 | ✓ |
| Dibe son 24s'te düşüş % | -7.278 | -7.658 | -0.12 | -0.23 | ✓ |
| Hacim eğilimi (son 3g / önceki 7g) | 0.975 | 0.918 | +0.12 | -0.21 | ✗ |

Etki: standart fark (+ = başarılı dönüşlerde daha yüksek). Kalıcı ✓: eğitim ve test döneminde aynı yönde ve belirgin.

## Strateji simülasyonu (tetikte gir, stop dibin altı, hedef 1,5R + 3R, en çok 7 gün)

Her dipte körlemesine giriş — TEST: 212 işlem, kazanma %34.9, ort -0.334R, 3x ort ROE %-3.73, PF 0.53

| Kural (yalnız canlı verilebilen işaretler) | Eğitim ort R (n, başarılı %) | TEST n / kazanma / ort R / PF | 3x ort ROE | 5x ort ROE |
|---|---|---|---|---|
| Stop mesafesi % ≤ 3.64 VE BTC son 24s % ≥ -1.03 VE Hacim eğilimi (son 3g / önceki 7g) ≤ 1.08 | 0.697 (42, %26.2) | 3 / %0.0 / -1.029 / 0.0 | %-10.69 | %-17.81 |
| Stop mesafesi % ≤ 3.64 VE Oynaklık sıkışması (24s ATR / 7g ATR) ≤ 0.986 VE BTC son 24s % ≥ -1.03 | 0.702 (38, %28.9) | 3 / %0.0 / -1.029 / 0.0 | %-10.73 | %-17.88 |
| Stop mesafesi % ≤ 3.64 VE BTC son 24s % ≥ -1.03 VE BTC son 7g % ≤ -1.18 | 0.669 (38, %23.7) | 5 / %0.0 / -1.029 / 0.0 | %-10.71 | %-17.85 |
| BTC son 24s % ≥ -0.239 VE Hacim eğilimi (son 3g / önceki 7g) ≤ 0.728 | 0.452 (50, %18.0) | 0 / %None / None / None | %None | %None |

Futures verisi (OI, funding, L/S) de dahil edilince:

| Kural | Eğitim ort R (n) | TEST n / ort R / PF |
|---|---|---|
| Stop mesafesi % ≤ 3.64 VE BTC son 24s % ≥ -1.03 VE Hacim eğilimi (son 3g / önceki 7g) ≤ 1.08 | 0.697 (42) | 3 / -1.029 / 0.0 |
| Stop mesafesi % ≤ 3.64 VE Oynaklık sıkışması (24s ATR / 7g ATR) ≤ 0.986 VE BTC son 24s % ≥ -1.03 | 0.702 (38) | 3 / -1.029 / 0.0 |
| Stop mesafesi % ≤ 3.64 VE BTC son 24s % ≥ -1.03 VE BTC son 7g % ≤ -1.18 | 0.669 (38) | 5 / -1.029 / 0.0 |

Karar: ❌ hiçbir kural TEST dönemini yeterince geçemedi; kâğıt hesapta ileri test olarak izleniyor

## Son 120 günün en büyük dipten dönüşleri

- HEI 30.07.2026 18:00: dipten +%594.2 (öncesinde 30g tepeden %-49.3, RVOL 0.82, OI 72s %None, funding 0.005)
- BMT 18.10.2026 20:00: dipten +%216.5 (öncesinde 30g tepeden %-29.2, RVOL 0.76, OI 72s %-8.8, funding 0.005)
- SHELL 13.11.2026 03:00: dipten +%172.5 (öncesinde 30g tepeden %-34.9, RVOL 1.36, OI 72s %-4.9, funding None)
- SHELL 08.11.2026 21:00: dipten +%165.9 (öncesinde 30g tepeden %-33.2, RVOL 0.69, OI 72s %-0.9, funding None)
- ONE 05.11.2026 15:00: dipten +%141.5 (öncesinde 30g tepeden %-56.0, RVOL 1.39, OI 72s %-16.2, funding None)
- HOME 30.07.2026 17:00: dipten +%139.8 (öncesinde 30g tepeden %-73.3, RVOL 0.68, OI 72s %None, funding 0.005)
- ONE 03.11.2026 03:00: dipten +%130.2 (öncesinde 30g tepeden %-55.8, RVOL 0.79, OI 72s %-2.2, funding None)
- SOPH 08.11.2026 21:00: dipten +%123.4 (öncesinde 30g tepeden %-69.4, RVOL 0.61, OI 72s %-3.0, funding None)
- AVA 11.09.2026 01:00: dipten +%120.9 (öncesinde 30g tepeden %-32.1, RVOL 0.43, OI 72s %-13.1, funding 0.005)
- BARD 10.11.2026 13:00: dipten +%91.8 (öncesinde 30g tepeden %-28.4, RVOL 2.78, OI 72s %-13.2, funding None)
- ALLO 16.09.2026 17:00: dipten +%82.0 (öncesinde 30g tepeden %-40.8, RVOL 0.71, OI 72s %-10.9, funding 0.005)
- SOPH 26.10.2026 10:00: dipten +%81.9 (öncesinde 30g tepeden %-66.0, RVOL 0.51, OI 72s %-37.1, funding -0.164)

## Şu an dipten dönen coinler (son 48 saat)

- KMNO: dip 0.02633, şimdi 0.02759 (1 saat önce tetik), 30g düşüş %-40.9, RVOL 2.73
- ETHFI: dip 0.4626, şimdi 0.4839 (3 saat önce tetik), 30g düşüş %-36.6, RVOL 0.99
- ALLO: dip 0.135, şimdi 0.1329 (3 saat önce tetik), 30g düşüş %-37.8, RVOL 1.13
- BNCB: dip 3.52, şimdi 3.58 (4 saat önce tetik), 30g düşüş %-40.3, RVOL 1.06
- MARSCOIN: dip 0.0313, şimdi 0.0337 (15 saat önce tetik), 30g düşüş %-62.9, RVOL 1.26
- NBISB: dip 104.66, şimdi 109.27 (15 saat önce tetik), 30g düşüş %-43.3, RVOL 1.57
- ZIL: dip 0.000976, şimdi 0.000926 (25 saat önce tetik), 30g düşüş %-61.6, RVOL 3.02
- SOPH: dip 0.00097, şimdi 0.00102 (29 saat önce tetik), 30g düşüş %-62.8, RVOL 2.01
- HUMA: dip 0.00631, şimdi 0.00852 (37 saat önce tetik), 30g düşüş %-80.1, RVOL 0.56

CoinGecko'da şu an trend olanlar: BP, ZEC, NEAR, EVAA, BTC, AERO, PENGU, SOL, INJ, ETH, LIT, LINK, BDX, HYPE, ADA

## İleri test defteri (canlı kaydedilen dipler, 7 gün sonra sonuçlanır; açık: 61)

- Tümü: 27 dip, %29.6 başarılı dönüş, ort -0.061R
- Kurala uyanlar: 0 dip, %None başarılı, ort NoneR
- İnternette trend olan (CoinGecko): 4 dip, %0.0 başarılı, ort -1.027R · trend olmayan: 23 dip, %34.8, ort 0.107R

Simülasyon/araştırmadır, yatırım tavsiyesi değildir.