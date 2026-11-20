# 🚀 Dipten Dönüş Raporu — 20.11.2026

116 coin, son 120 gün, 1 saatlik mumlar. 757 dip tetiği (yeni 30g dip + dipten %3 dönüş); bunların %10.3'i 7 gün içinde dibin %20 üstüne çıktı (başarılı dönüş). Eğitim/TEST ayrımı 08.11.2026.

## Başarılı dönüşlerden önce ne oluyor? (başarısız diplerle kıyas, medyan)

| Öncü işaret | Başarılı | Başarısız | Etki (eğitim) | Etki (test) | Kalıcı |
|---|---|---|---|---|---|
| Likidite avı (7g dibin altına fitil, üstünde kapanış) | 0.0 | 0.0 | -0.43 | -0.48 | ✓ |
| BTC son 7g % | -1.641 | -2.237 | +0.40 | -0.88 | ✗ |
| BTC son 24s % | 0.197 | -0.39 | +0.25 | -0.69 | ✗ |
| Stop mesafesi % | 4.005 | 3.961 | +0.21 | +0.30 | ✓ |
| Son 24s hacim / önceki 7g ort. | 1.1 | 1.064 | +0.19 | +0.52 | ✓ |
| OI değişimi son 24s % | -5.553 | -3.604 | -0.19 | -0.70 | ✓ |
| Agresif alım değişimi (24s - önceki 72s) | -0.007 | -0.009 | +0.11 | -0.59 | ✗ |
| OI değişimi dipten önceki 72s % | -11.332 | -8.985 | -0.10 | -0.47 | ✗ |
| Top trader L/S | 2.03 | 2.105 | -0.08 | -0.03 | ✗ |
| Dip mumunun alt fitil oranı | 0.406 | 0.423 | -0.07 | +0.20 | ✗ |
| Global L/S 24s değişim | -0.046 | -0.027 | -0.07 | +0.15 | ✗ |
| Dibe son 24s'te düşüş % | -7.42 | -8.445 | -0.07 | -0.86 | ✗ |
| Dipten bu yana saat | 4.5 | 3.0 | +0.07 | -0.58 | ✗ |
| Global L/S | 1.244 | 1.148 | +0.06 | +0.41 | ✗ |

Etki: standart fark (+ = başarılı dönüşlerde daha yüksek). Kalıcı ✓: eğitim ve test döneminde aynı yönde ve belirgin.

## Strateji simülasyonu (tetikte gir, stop dibin altı, hedef 1,5R + 3R, en çok 7 gün)

Her dipte körlemesine giriş — TEST: 233 işlem, kazanma %30.0, ort -0.361R, 3x ort ROE %-4.28, PF 0.49

| Kural (yalnız canlı verilebilen işaretler) | Eğitim ort R (n, başarılı %) | TEST n / kazanma / ort R / PF | 3x ort ROE | 5x ort ROE |
|---|---|---|---|---|
| BTC son 24s % ≥ -0.332 VE Likidite avı (7g dibin altına fitil, üstünde kapanış) ≤ 0 VE Dibe son 24s'te düşüş % ≥ -8.32 | 0.61 (81, %23.5) | 4 / %25.0 / -0.213 / 0.75 | %-2.33 | %-3.88 |
| BTC son 24s % ≥ 0.433 VE Likidite avı (7g dibin altına fitil, üstünde kapanış) ≤ 0 VE Son 24s agresif alım oranı ≤ 0.484 | 0.635 (57, %31.6) | 1 / %0.0 / -1.029 / 0.0 | %-10.75 | %-17.91 |
| BTC son 24s % ≥ 0.433 VE Likidite avı (7g dibin altına fitil, üstünde kapanış) ≤ 0 | 0.512 (83, %24.1) | 2 / %0.0 / -1.025 / 0.0 | %-12.79 | %-21.32 |
| BTC son 24s % ≥ -0.332 VE Likidite avı (7g dibin altına fitil, üstünde kapanış) ≤ 0 VE Hacim eğilimi (son 3g / önceki 7g) ≤ 0.815 | 0.617 (52, %17.3) | 1 / %0.0 / -1.029 / 0.0 | %-10.75 | %-17.91 |
| BTC son 24s % ≥ 0.433 VE Likidite avı (7g dibin altına fitil, üstünde kapanış) ≤ 0 VE Oynaklık sıkışması (24s ATR / 7g ATR) ≥ 0.829 | 0.599 (55, %29.1) | 1 / %0.0 / -1.021 / 0.0 | %-14.84 | %-24.74 |

Futures verisi (OI, funding, L/S) de dahil edilince:

| Kural | Eğitim ort R (n) | TEST n / ort R / PF |
|---|---|---|
| BTC son 24s % ≥ 0.433 VE Likidite avı (7g dibin altına fitil, üstünde kapanış) ≤ 0 VE Son 24s agresif alım oranı ≤ 0.484 | 0.635 (57) | 1 / -1.029 / 0.0 |
| BTC son 24s % ≥ 0.433 VE Likidite avı (7g dibin altına fitil, üstünde kapanış) ≤ 0 | 0.512 (83) | 2 / -1.025 / 0.0 |
| BTC son 24s % ≥ 0.433 VE Likidite avı (7g dibin altına fitil, üstünde kapanış) ≤ 0 VE Oynaklık sıkışması (24s ATR / 7g ATR) ≥ 0.829 | 0.599 (55) | 1 / -1.021 / 0.0 |

Karar: ❌ hiçbir kural TEST dönemini yeterince geçemedi; kâğıt hesapta ileri test olarak izleniyor

## Son 120 günün en büyük dipten dönüşleri

- HEI 30.07.2026 18:00: dipten +%594.2 (öncesinde 30g tepeden %-49.3, RVOL 0.82, OI 72s %None, funding 0.005)
- BMT 18.10.2026 20:00: dipten +%216.5 (öncesinde 30g tepeden %-29.2, RVOL 0.76, OI 72s %-8.8, funding 0.005)
- MMT 13.11.2026 03:00: dipten +%184.8 (öncesinde 30g tepeden %-36.5, RVOL 1.34, OI 72s %-7.0, funding None)
- BREV 17.11.2026 01:00: dipten +%147.0 (öncesinde 30g tepeden %-43.8, RVOL 1.55, OI 72s %-6.5, funding None)
- ONE 05.11.2026 15:00: dipten +%141.5 (öncesinde 30g tepeden %-56.0, RVOL 1.39, OI 72s %-16.2, funding None)
- BREV 14.11.2026 21:00: dipten +%141.2 (öncesinde 30g tepeden %-42.4, RVOL 1.41, OI 72s %-14.0, funding None)
- ONE 03.11.2026 03:00: dipten +%130.2 (öncesinde 30g tepeden %-55.8, RVOL 0.79, OI 72s %-2.2, funding None)
- SOPH 08.11.2026 21:00: dipten +%123.4 (öncesinde 30g tepeden %-69.4, RVOL 0.61, OI 72s %-3.0, funding None)
- BREV 11.11.2026 23:00: dipten +%113.2 (öncesinde 30g tepeden %-34.9, RVOL 1.06, OI 72s %2.5, funding None)
- BARD 10.11.2026 13:00: dipten +%91.8 (öncesinde 30g tepeden %-28.4, RVOL 2.78, OI 72s %-13.2, funding None)
- RARE 13.11.2026 03:00: dipten +%88.9 (öncesinde 30g tepeden %-39.9, RVOL 1.62, OI 72s %0.3, funding None)
- SOPH 26.10.2026 10:00: dipten +%81.9 (öncesinde 30g tepeden %-66.0, RVOL 0.51, OI 72s %-37.1, funding -0.164)

## Şu an dipten dönen coinler (son 48 saat)

- PUMP: dip 0.002498, şimdi 0.002562 (1 saat önce tetik), 30g düşüş %-52.2, RVOL 0.86
- JTO: dip 0.2438, şimdi 0.2442 (7 saat önce tetik), 30g düşüş %-50.7, RVOL 1.08
- FIL: dip 0.553, şimdi 0.5578 (12 saat önce tetik), 30g düşüş %-49.4, RVOL 0.76
- CRV: dip 0.193, şimdi 0.1928 (17 saat önce tetik), 30g düşüş %-52.9, RVOL 0.79
- CFG: dip 0.0631, şimdi 0.0594 (22 saat önce tetik), 30g düşüş %-49.8, RVOL 2.65
- APT: dip 0.4205, şimdi 0.4066 (27 saat önce tetik), 30g düşüş %-50.3, RVOL 1.03
- 牛来: dip 0.0425, şimdi 0.03502 (36 saat önce tetik), 30g düşüş %-42.4, RVOL 0.4
- STRK: dip 0.03148, şimdi 0.0318 (36 saat önce tetik), 30g düşüş %-52.3, RVOL 0.71
- ENA: dip 0.1076, şimdi 0.105 (37 saat önce tetik), 30g düşüş %-52.4, RVOL 0.96
- ZRO: dip 1.283, şimdi 1.27 (37 saat önce tetik), 30g düşüş %-40.0, RVOL 1.18
- IRENB: dip 15, şimdi 14.02 (37 saat önce tetik), 30g düşüş %-48.7, RVOL 1.35

CoinGecko'da şu an trend olanlar: BTC, ETH, PEARL, XMR, EVAA, SKY, HYPE, QTC, AAVE, SPX, CARDS, LINK, BP, SOL, TRUMP

## İleri test defteri (canlı kaydedilen dipler, 7 gün sonra sonuçlanır; açık: 44)

- Tümü: 70 dip, %18.6 başarılı dönüş, ort -0.457R
- Kurala uyanlar: 3 dip, %0.0 başarılı, ort -1.02R
- İnternette trend olan (CoinGecko): 10 dip, %10.0 başarılı, ort -0.699R · trend olmayan: 60 dip, %20.0, ort -0.417R

Simülasyon/araştırmadır, yatırım tavsiyesi değildir.