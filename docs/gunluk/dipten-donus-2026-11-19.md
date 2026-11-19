# 🚀 Dipten Dönüş Raporu — 19.11.2026

120 coin, son 120 gün, 1 saatlik mumlar. 747 dip tetiği (yeni 30g dip + dipten %3 dönüş); bunların %12.4'i 7 gün içinde dibin %20 üstüne çıktı (başarılı dönüş). Eğitim/TEST ayrımı 08.11.2026.

## Başarılı dönüşlerden önce ne oluyor? (başarısız diplerle kıyas, medyan)

| Öncü işaret | Başarılı | Başarısız | Etki (eğitim) | Etki (test) | Kalıcı |
|---|---|---|---|---|---|
| BTC son 24s % | 0.247 | -0.39 | +0.37 | -0.83 | ✗ |
| Likidite avı (7g dibin altına fitil, üstünde kapanış) | 0.0 | 0.0 | -0.35 | -0.43 | ✓ |
| BTC son 7g % | -2.237 | -2.237 | +0.34 | -0.80 | ✗ |
| Global L/S 24s değişim | -0.054 | -0.025 | -0.30 | +0.12 | ✗ |
| Top trader L/S | 2.103 | 2.107 | -0.23 | +0.29 | ✗ |
| Stop mesafesi % | 4.05 | 3.961 | +0.22 | +0.27 | ✓ |
| OI değişimi son 24s % | -5.553 | -3.274 | -0.19 | -0.54 | ✓ |
| Global L/S | 1.223 | 1.075 | +0.18 | +0.38 | ✓ |
| Funding (son) | 0.005 | 0.002 | -0.17 | None | ✗ |
| Dip mumunun alt fitil oranı | 0.389 | 0.429 | -0.11 | +0.12 | ✗ |
| 30 günlük tepeden düşüş % | -30.507 | -30.956 | +0.08 | -0.33 | ✗ |
| RSI pozitif uyumsuzluk (dip daha alçak, RSI daha yüksek) | 0.0 | 0.0 | -0.08 | -0.26 | ✗ |
| Dipten bu yana saat | 4.0 | 3.0 | +0.08 | -0.27 | ✗ |
| RSI(14s) tetikte | 45.023 | 46.876 | +0.07 | -0.57 | ✗ |

Etki: standart fark (+ = başarılı dönüşlerde daha yüksek). Kalıcı ✓: eğitim ve test döneminde aynı yönde ve belirgin.

## Strateji simülasyonu (tetikte gir, stop dibin altı, hedef 1,5R + 3R, en çok 7 gün)

Her dipte körlemesine giriş — TEST: 231 işlem, kazanma %29.4, ort -0.322R, 3x ort ROE %-3.74, PF 0.56

| Kural (yalnız canlı verilebilen işaretler) | Eğitim ort R (n, başarılı %) | TEST n / kazanma / ort R / PF | 3x ort ROE | 5x ort ROE |
|---|---|---|---|---|
| BTC son 24s % ≥ 0.432 VE Likidite avı (7g dibin altına fitil, üstünde kapanış) ≤ 0 VE 30 günlük tepeden düşüş % ≤ -24.3 | 0.731 (62, %35.5) | 1 / %0.0 / -1.021 / 0.0 | %-14.84 | %-24.74 |
| BTC son 24s % ≥ 0.432 VE Likidite avı (7g dibin altına fitil, üstünde kapanış) ≤ 0 | 0.612 (86, %31.4) | 1 / %0.0 / -1.021 / 0.0 | %-14.84 | %-24.74 |
| BTC son 24s % ≥ 0.432 VE Likidite avı (7g dibin altına fitil, üstünde kapanış) ≤ 0 VE Son 24s hacim / önceki 7g ort. ≤ 1.06 | 0.749 (45, %33.3) | 0 / %None / None / None | %None | %None |
| Son 24s hacim / önceki 7g ort. ≤ 0.763 VE BTC son 7g % ≤ -2.24 VE BTC son 24s % ≥ -2.45 | 0.693 (51, %19.6) | 28 / %28.6 / -0.267 / 0.55 | %-3.46 | %-5.77 |
| BTC son 24s % ≥ 0.432 VE Likidite avı (7g dibin altına fitil, üstünde kapanış) ≤ 0 VE Stop mesafesi % ≥ 3.97 | 0.714 (47, %31.9) | 1 / %0.0 / -1.021 / 0.0 | %-14.84 | %-24.74 |

Futures verisi (OI, funding, L/S) de dahil edilince:

| Kural | Eğitim ort R (n) | TEST n / ort R / PF |
|---|---|---|
| BTC son 24s % ≥ 0.432 VE Likidite avı (7g dibin altına fitil, üstünde kapanış) ≤ 0 VE 30 günlük tepeden düşüş % ≤ -24.3 | 0.731 (62) | 1 / -1.021 / 0.0 |
| BTC son 24s % ≥ 0.432 VE Likidite avı (7g dibin altına fitil, üstünde kapanış) ≤ 0 | 0.612 (86) | 1 / -1.021 / 0.0 |
| BTC son 24s % ≥ 0.432 VE Likidite avı (7g dibin altına fitil, üstünde kapanış) ≤ 0 VE Funding (son) ≥ -0.0014 | 0.786 (43) | 0 / None / None |

Karar: ❌ hiçbir kural TEST dönemini yeterince geçemedi; kâğıt hesapta ileri test olarak izleniyor

## Son 120 günün en büyük dipten dönüşleri

- HEI 30.07.2026 18:00: dipten +%594.2 (öncesinde 30g tepeden %-49.3, RVOL 0.82, OI 72s %None, funding 0.005)
- BMT 18.10.2026 20:00: dipten +%216.5 (öncesinde 30g tepeden %-29.2, RVOL 0.76, OI 72s %-8.8, funding 0.005)
- SHELL 13.11.2026 03:00: dipten +%172.5 (öncesinde 30g tepeden %-34.9, RVOL 1.36, OI 72s %-4.9, funding None)
- SHELL 08.11.2026 21:00: dipten +%165.9 (öncesinde 30g tepeden %-33.2, RVOL 0.69, OI 72s %-0.9, funding None)
- MMT 13.11.2026 03:00: dipten +%154.0 (öncesinde 30g tepeden %-36.5, RVOL 1.34, OI 72s %-7.0, funding None)
- BREV 17.11.2026 01:00: dipten +%147.0 (öncesinde 30g tepeden %-43.8, RVOL 1.55, OI 72s %-6.5, funding None)
- ONE 05.11.2026 15:00: dipten +%141.5 (öncesinde 30g tepeden %-56.0, RVOL 1.39, OI 72s %-16.2, funding None)
- BREV 14.11.2026 21:00: dipten +%141.2 (öncesinde 30g tepeden %-42.4, RVOL 1.41, OI 72s %-14.0, funding None)
- ONE 03.11.2026 03:00: dipten +%130.2 (öncesinde 30g tepeden %-55.8, RVOL 0.79, OI 72s %-2.2, funding None)
- SOPH 08.11.2026 21:00: dipten +%123.4 (öncesinde 30g tepeden %-69.4, RVOL 0.61, OI 72s %-3.0, funding None)
- BREV 11.11.2026 23:00: dipten +%113.2 (öncesinde 30g tepeden %-34.9, RVOL 1.06, OI 72s %2.5, funding None)
- BARD 10.11.2026 13:00: dipten +%91.8 (öncesinde 30g tepeden %-28.4, RVOL 2.78, OI 72s %-13.2, funding None)

## Şu an dipten dönen coinler (son 48 saat)

- APT: dip 0.4205, şimdi 0.434 (3 saat önce tetik), 30g düşüş %-50.3, RVOL 1.03
- STRK: dip 0.03148, şimdi 0.03346 (12 saat önce tetik), 30g düşüş %-52.3, RVOL 0.71 · ✅ kurala uyuyor
- 牛来: dip 0.0425, şimdi 0.0438 (12 saat önce tetik), 30g düşüş %-42.4, RVOL 0.4 · ✅ kurala uyuyor
- S: dip 0.0304, şimdi 0.0313 (12 saat önce tetik), 30g düşüş %-49.1, RVOL 0.96
- ENA: dip 0.1076, şimdi 0.1118 (13 saat önce tetik), 30g düşüş %-52.4, RVOL 0.96
- ZRO: dip 1.283, şimdi 1.43 (13 saat önce tetik), 30g düşüş %-40.0, RVOL 1.18
- AAOIB: dip 39.32, şimdi 42.3 (24 saat önce tetik), 30g düşüş %-55.4, RVOL 2.57
- PLUME: dip 0.01146, şimdi 0.01183 (34 saat önce tetik), 30g düşüş %-40.2, RVOL 0.6 · ✅ kurala uyuyor
- PEPE: dip 3.65e-06, şimdi 3.81e-06 (35 saat önce tetik), 30g düşüş %-35.7, RVOL 0.55 · ✅ kurala uyuyor
- FIL: dip 0.575, şimdi 0.5711 (35 saat önce tetik), 30g düşüş %-47.4, RVOL 0.84
- EIGEN: dip 0.1232, şimdi 0.1299 (35 saat önce tetik), 30g düşüş %-50.9, RVOL 0.8
- PENGU: dip 0.004446, şimdi 0.004742 (36 saat önce tetik), 30g düşüş %-47.1, RVOL 1.02 · 🔥 CoinGecko trend
- SKHYB: dip 117.5, şimdi 128.22 (37 saat önce tetik), 30g düşüş %-29.3, RVOL 1.2
- OP: dip 0.0739, şimdi 0.0767 (37 saat önce tetik), 30g düşüş %-45.6, RVOL 2.13
- PUMP: dip 0.002713, şimdi 0.002686 (43 saat önce tetik), 30g düşüş %-48.1, RVOL 1.07
- SNXXB: dip 2.77, şimdi 2.9 (43 saat önce tetik), 30g düşüş %-74.6, RVOL 1.35 · ✅ kurala uyuyor
- MUBARAK: dip 0.02668, şimdi 0.02611 (45 saat önce tetik), 30g düşüş %-53.5, RVOL 0.84

CoinGecko'da şu an trend olanlar: PEARL, BTC, PENGU, IRYS, VVV, LUNC, SOL, MON, HBAR, PONS, AERO, SKY, KNTQ, TAO, ICP

## İleri test defteri (canlı kaydedilen dipler, 7 gün sonra sonuçlanır; açık: 56)

- Tümü: 52 dip, %21.2 başarılı dönüş, ort -0.335R
- Kurala uyanlar: 2 dip, %0.0 başarılı, ort -1.017R
- İnternette trend olan (CoinGecko): 7 dip, %14.3 başarılı, ort -0.561R · trend olmayan: 45 dip, %22.2, ort -0.3R

Simülasyon/araştırmadır, yatırım tavsiyesi değildir.