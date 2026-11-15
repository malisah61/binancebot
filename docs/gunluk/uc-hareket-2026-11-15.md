# Uç hareketler: sert düşenler ve trend tersi yükselenler — 15.11.2026 12:03

295 coin (ilk 300 hacim; büyük 1-50, orta 51-150, küçük 151+), son 150 gün, 1s mum. Olaylar: 3779 sert düşüş, 1006 trend tersi pompa. Eğitim ilk %70, TEST son %30 (model görmeden).

## Sert düşüş — varyantlar (tüm coinler, en düşük eşik)

| Varyant | Eğitim | TEST |
|---|---|---|
| Sert düşüşte hemen LONG (tepki alımı) | 3010 işlem, %43.2 kazanç, ort 0.01R, PF 1.02, ort stop %6.7 · marjin/işlem 3x %-0.3 (19 tasfiye), 5x %-0.3 (97), 10x %-2.6 (400) | 1366 işlem, %40.8 kazanç, ort -0.101R, PF 0.84, ort stop %4.1 · marjin/işlem 3x %-1.3 (2 tasfiye), 5x %-2.3 (19), 10x %-5.8 (108) |
| Sert düşüşte 1 ATR aşağıya limit LONG | 1601 işlem, %47.3 kazanç, ort 0.053R, PF 1.11, ort stop %6.8 · marjin/işlem 3x %-0.3 (11 tasfiye), 5x %-0.5 (55), 10x %-1.7 (214) | 827 işlem, %33.9 kazanç, ort -0.304R, PF 0.58, ort stop %3.7 · marjin/işlem 3x %-2.3 (3 tasfiye), 5x %-3.7 (8), 10x %-10.4 (62) |
| Sert düşüşten sonra dönüş mumu gelince LONG | 2203 işlem, %39.7 kazanç, ort -0.064R, PF 0.88, ort stop %8.4 · marjin/işlem 3x %-1.0 (18 tasfiye), 5x %-1.9 (76), 10x %-5.1 (349) | 909 işlem, %33.9 kazanç, ort -0.246R, PF 0.59, ort stop %6.8 · marjin/işlem 3x %-4.4 (2 tasfiye), 5x %-7.1 (17), 10x %-16.3 (128) |
| Sert düşüşte hemen SHORT (devam) | 2821 işlem, %39.1 kazanç, ort -0.18R, PF 0.69, ort stop %8.2 · marjin/işlem 3x %-4.5 (28 tasfiye), 5x %-7.7 (125), 10x %-12.4 (546) | 1245 işlem, %49.2 kazanç, ort 0.039R, PF 1.09, ort stop %7.3 · marjin/işlem 3x %-0.2 (11 tasfiye), 5x %-0.4 (30), 10x %-0.6 (136) |
| Sert düşüşte 1.5 ATR tepki yukarısına limit SHORT | 1185 işlem, %38.1 kazanç, ort -0.138R, PF 0.79, ort stop %4.0 · marjin/işlem 3x %-1.9 (1 tasfiye), 5x %-3.8 (16), 10x %-8.9 (100) | 587 işlem, %33.7 kazanç, ort -0.273R, PF 0.63, ort stop %3.3 · marjin/işlem 3x %-2.8 (5 tasfiye), 5x %-4.6 (8), 10x %-8.7 (22) |
| Sert düşüşte tepki bitip kırılım gelince SHORT | 2084 işlem, %46.7 kazanç, ort -0.094R, PF 0.71, ort stop %16.4 · marjin/işlem 3x %-4.8 (41 tasfiye), 5x %-7.3 (166), 10x %-10.8 (826) | 839 işlem, %57.2 kazanç, ort 0.041R, PF 1.21, ort stop %16.2 · marjin/işlem 3x %1.2 (7 tasfiye), 5x %2.4 (39), 10x %-0.2 (240) |

### Sert düşüş — coin büyüklüğüne göre (TEST, en düşük eşik)

| Varyant | büyük | orta+küçük | küçük |
|---|---|---|---|
| Sert düşüşte hemen LONG (tepki alımı) | 209 işl, ort -0.228R, PF 0.68 | 1157 işl, ort -0.078R, PF 0.87 | 654 işl, ort -0.11R, PF 0.83 |
| Sert düşüşte 1 ATR aşağıya limit LONG | 145 işl, ort -0.3R, PF 0.57 | 682 işl, ort -0.305R, PF 0.58 | 369 işl, ort -0.353R, PF 0.54 |
| Sert düşüşten sonra dönüş mumu gelince LONG | 135 işl, ort -0.29R, PF 0.54 | 774 işl, ort -0.238R, PF 0.6 | 433 işl, ort -0.234R, PF 0.59 |
| Sert düşüşte hemen SHORT (devam) | 200 işl, ort 0.173R, PF 1.46 | 1045 işl, ort 0.013R, PF 1.03 | 588 işl, ort -0.069R, PF 0.85 |
| Sert düşüşte 1.5 ATR tepki yukarısına limit SHORT | 81 işl, ort -0.132R, PF 0.79 | 506 işl, ort -0.296R, PF 0.6 | 282 işl, ort -0.346R, PF 0.55 |
| Sert düşüşte tepki bitip kırılım gelince SHORT | 150 işl, ort 0.048R, PF 1.23 | 689 işl, ort 0.039R, PF 1.2 | 380 işl, ort 0.011R, PF 1.06 |

**Eğitimde seçilen:** Sert düşüşte 1 ATR aşağıya limit LONG, hareket ≥ %10, coinler: büyük → ❌ testte tutmadı → yalnız kâğıt ileri test
- Eğitim: 215 işlem, %50.7 kazanç, ort 0.164R, PF 1.35, ort stop %5.8 · marjin/işlem 3x %1.9 (1 tasfiye), 5x %2.2 (4), 10x %4.0 (18)
- TEST: 145 işlem, %33.1 kazanç, ort -0.3R, PF 0.57, ort stop %3.5 · marjin/işlem 3x %-2.8 (1 tasfiye), 5x %-4.7 (3), 10x %-11.0 (8)

Bu varyantta kazanan vs kaybeden işlemler (medyan; d = etki büyüklüğü, ✓ iki dönemde de aynı yönde ≥0.2):

| Özellik | Kazanan | Kaybeden | d eğitim / test | |
|---|---|---|---|---|
| Hareket / ATR | 5.5185 | 5.3093 | 0.16 / 0.05 |  |
| BTC son 24s % | -2.5218 | -3.041 | -0.16 / -0.15 |  |
| OI değişimi 24s % | -9.602 | -8.5832 | -0.16 / -0.03 |  |
| Hacim sırası (büyük = küçük coin) | 136.5 | 135.0 | -0.14 / 0.05 |  |
| Son 24s hacim / önceki 7g ort. | 1.2112 | 1.3166 | -0.11 / 0.0 |  |
| Top trader L/S | 1.8502 | 1.9423 | 0.11 / -0.06 |  |
| Son 24s agresif alım oranı | 0.4787 | 0.478 | -0.07 / -0.0 |  |
| Hareket büyüklüğü % | 10.7693 | 10.6232 | -0.06 / 0.07 |  |

## Trend tersi sert yükseliş — varyantlar (tüm coinler, en düşük eşik)

| Varyant | Eğitim | TEST |
|---|---|---|
| Trend tersi pompada hemen SHORT (geri sönme) | 870 işlem, %41.7 kazanç, ort -0.151R, PF 0.77, ort stop %12.8 · marjin/işlem 3x %-0.9 (5 tasfiye), 5x %-1.5 (12), 10x %-3.9 (49) | 392 işlem, %50.3 kazanç, ort 0.124R, PF 1.24, ort stop %4.4 · marjin/işlem 3x %0.3 (0 tasfiye), 5x %0.3 (3), 10x %0.0 (32) |
| Trend tersi pompada 1 ATR yukarıya limit SHORT | 558 işlem, %48.0 kazanç, ort -0.003R, PF 1.0, ort stop %2.6 · marjin/işlem 3x %-0.6 (2 tasfiye), 5x %-1.0 (5), 10x %-2.9 (23) | 216 işlem, %55.6 kazanç, ort 0.192R, PF 1.4, ort stop %4.1 · marjin/işlem 3x %1.1 (0 tasfiye), 5x %1.5 (2), 10x %0.9 (19) |
| Trend tersi pompadan sonra kırılım mumu gelince SHORT | 683 işlem, %40.1 kazanç, ort -0.144R, PF 0.74, ort stop %7.9 · marjin/işlem 3x %-1.7 (4 tasfiye), 5x %-2.8 (13), 10x %-6.9 (91) | 316 işlem, %65.5 kazanç, ort 0.387R, PF 2.2, ort stop %7.0 · marjin/işlem 3x %4.7 (1 tasfiye), 5x %7.6 (6), 10x %17.3 (26) |
| Trend tersi pompada hemen LONG (devam) | 921 işlem, %36.9 kazanç, ort -0.134R, PF 0.8, ort stop %5.5 · marjin/işlem 3x %-2.3 (3 tasfiye), 5x %-3.9 (8), 10x %-8.2 (39) | 444 işlem, %28.6 kazanç, ort -0.398R, PF 0.45, ort stop %4.1 · marjin/işlem 3x %-4.0 (0 tasfiye), 5x %-6.8 (1), 10x %-14.4 (16) |
| Trend tersi pompada 1.5 ATR geri çekilmeye limit LONG | 537 işlem, %43.6 kazanç, ort -0.028R, PF 0.95, ort stop %3.2 · marjin/işlem 3x %-0.6 (1 tasfiye), 5x %-1.4 (5), 10x %-2.7 (13) | 219 işlem, %33.3 kazanç, ort -0.317R, PF 0.57, ort stop %3.0 · marjin/işlem 3x %-2.2 (0 tasfiye), 5x %-3.6 (0), 10x %-8.9 (6) |
| Trend tersi pompada geri çekilme sonrası yeni tepe kırılımında LONG | 597 işlem, %37.9 kazanç, ort -0.042R, PF 0.88, ort stop %13.7 · marjin/işlem 3x %-2.1 (0 tasfiye), 5x %-3.6 (19), 10x %-5.8 (192) | 287 işlem, %24.0 kazanç, ort -0.317R, PF 0.35, ort stop %12.6 · marjin/işlem 3x %-10.7 (0 tasfiye), 5x %-18.1 (5), 10x %-37.5 (123) |

### Trend tersi sert yükseliş — coin büyüklüğüne göre (TEST, en düşük eşik)

| Varyant | büyük | orta+küçük | küçük |
|---|---|---|---|
| Trend tersi pompada hemen SHORT (geri sönme) | 56 işl, ort 0.099R, PF 1.19 | 336 işl, ort 0.128R, PF 1.25 | 194 işl, ort 0.063R, PF 1.11 |
| Trend tersi pompada 1 ATR yukarıya limit SHORT | 37 işl, ort 0.42R, PF 1.98 | 179 işl, ort 0.145R, PF 1.29 | 110 işl, ort 0.011R, PF 1.02 |
| Trend tersi pompadan sonra kırılım mumu gelince SHORT | 42 işl, ort 0.472R, PF 2.46 | 274 işl, ort 0.374R, PF 2.16 | 156 işl, ort 0.325R, PF 1.95 |
| Trend tersi pompada hemen LONG (devam) | 56 işl, ort -0.251R, PF 0.6 | 388 işl, ort -0.419R, PF 0.43 | 217 işl, ort -0.383R, PF 0.48 |
| Trend tersi pompada 1.5 ATR geri çekilmeye limit LONG | 27 işl, ort -0.419R, PF 0.49 | 192 işl, ort -0.303R, PF 0.58 | 105 işl, ort -0.19R, PF 0.72 |
| Trend tersi pompada geri çekilme sonrası yeni tepe kırılımında LONG | 40 işl, ort -0.227R, PF 0.55 | 247 işl, ort -0.331R, PF 0.32 | 144 işl, ort -0.312R, PF 0.36 |

**Eğitimde seçilen:** Trend tersi pompada 1 ATR yukarıya limit SHORT, hareket ≥ %10, coinler: büyük → ❌ testte tutmadı → yalnız kâğıt ileri test
- Eğitim: 66 işlem, %53.0 kazanç, ort 0.208R, PF 1.43, ort stop %3.1 · marjin/işlem 3x %0.1 (1 tasfiye), 5x %1.1 (1), 10x %3.7 (1)
- TEST: 37 işlem, %59.5 kazanç, ort 0.42R, PF 1.98, ort stop %4.3 · marjin/işlem 3x %2.9 (0 tasfiye), 5x %3.4 (1), 10x %2.5 (6)

Bu varyantta kazanan vs kaybeden işlemler (medyan; d = etki büyüklüğü, ✓ iki dönemde de aynı yönde ≥0.2):

| Özellik | Kazanan | Kaybeden | d eğitim / test | |
|---|---|---|---|---|
| Olay mumunun ters fitil oranı | 0.1689 | 0.2113 | -0.27 / -0.17 |  |
| Son 24s hacim / önceki 7g ort. | 1.4148 | 1.537 | -0.26 / -0.04 |  |
| Top trader L/S | 1.9784 | 1.6969 | -0.25 / 0.45 |  |
| OI değişimi 24s % | 2.1738 | 5.5909 | -0.16 / -0.34 |  |
| Hareket / ATR | 5.9648 | 5.9233 | -0.1 / -0.05 |  |
| Hareket büyüklüğü % | 10.5932 | 10.756 | -0.08 / -0.22 |  |
| Son 24s agresif alım oranı | 0.4896 | 0.4934 | 0.07 / -0.22 |  |
| 30 günlük getiri % | -24.3422 | -23.3087 | -0.04 / 0.01 |  |

## Testi geçen tüm kombinasyonlar (bilgi amaçlı — eğitimde seçilmedikçe benimsenmez)

- Sert düşüş · Sert düşüşte 1 ATR aşağıya limit LONG · ≥%15 · tümü · TEST 245 işlem, %53.1 kazanç, ort 0.273R, PF 1.56, ort stop %5.9 · marjin/işlem 3x %0.5 (4 tasfiye), 5x %1.9 (10), 10x %7.8 (26)
- Sert düşüş · Sert düşüşte 1 ATR aşağıya limit LONG · ≥%15 · küçük · TEST 106 işlem, %50.9 kazanç, ort 0.244R, PF 1.47, ort stop %6.0 · marjin/işlem 3x %0.1 (1 tasfiye), 5x %1.1 (4), 10x %5.8 (11)
- Sert düşüş · Sert düşüşte 1 ATR aşağıya limit LONG · ≥%15 · orta, küçük · TEST 204 işlem, %52.5 kazanç, ort 0.264R, PF 1.53, ort stop %5.9 · marjin/işlem 3x %-0.2 (3 tasfiye), 5x %0.9 (8), 10x %6.1 (21)
- Sert düşüş · Sert düşüşte 1 ATR aşağıya limit LONG · ≥%15 · büyük · TEST 41 işlem, %56.1 kazanç, ort 0.318R, PF 1.72, ort stop %5.9 · marjin/işlem 3x %4.3 (1 tasfiye), 5x %7.0 (2), 10x %16.3 (5)
- Sert düşüş · Sert düşüşte 1.5 ATR tepki yukarısına limit SHORT · ≥%15 · küçük · TEST 67 işlem, %49.3 kazanç, ort 0.128R, PF 1.24, ort stop %5.4 · marjin/işlem 3x %-0.8 (2 tasfiye), 5x %-2.3 (4), 10x %0.9 (6)
- Trend tersi sert yükseliş · Trend tersi pompada hemen SHORT (geri sönme) · ≥%15 · orta, küçük · TEST 92 işlem, %57.6 kazanç, ort 0.265R, PF 1.6, ort stop %5.1 · marjin/işlem 3x %2.8 (1 tasfiye), 5x %5.4 (1), 10x %7.0 (12)
- Trend tersi sert yükseliş · Trend tersi pompadan sonra kırılım mumu gelince SHORT · ≥%15 · orta, küçük · TEST 81 işlem, %58.0 kazanç, ort 0.164R, PF 1.46, ort stop %10.6 · marjin/işlem 3x %2.8 (1 tasfiye), 5x %4.5 (4), 10x %10.7 (19)

## Şu an (son 26 saat)

- KAVA [büyük] Sert düşüş %33.3, 23 saat önce, RVOL 11.68 → kâğıt: LONG (Sert düşüşte 1 ATR aşağıya limit LONG)
- 牛来 [büyük] Sert düşüş %31.3, 13 saat önce, RVOL 1.98
- SOPH [büyük] Sert düşüş %30.7, 18 saat önce, RVOL 11.31
- BERA [orta] Sert düşüş %30.4, 15 saat önce, RVOL 13.76
- REQ [küçük] Sert düşüş %22.2, 17 saat önce, RVOL 7.09
- AMP [küçük] Sert düşüş %21.9, 13 saat önce, RVOL 2.38
- WIN [küçük] Sert düşüş %21.2, 4 saat önce, RVOL 1.96
- MITO [orta] Sert düşüş %21.2, 14 saat önce, RVOL 1.89
- STO [orta] Sert düşüş %20.7, 23 saat önce, RVOL 25.22
- AUDIO [küçük] Sert düşüş %20.5, 8 saat önce, RVOL 5.12
- CHIP [orta] Sert düşüş %20.2, 13 saat önce, RVOL 1.01
- HOME [orta] Sert düşüş %20.0, 15 saat önce, RVOL 2.26
- STRAX [küçük] Sert düşüş %19.6, 8 saat önce, RVOL 0.96
- PYTH [orta] Sert düşüş %18.2, 13 saat önce, RVOL 1.13
- CFX [orta] Sert düşüş %18.1, 13 saat önce, RVOL 3.29
- APE [orta] Sert düşüş %17.6, 11 saat önce, RVOL 1.81
- VIRTUAL [orta] Sert düşüş %17.5, 13 saat önce, RVOL 1.92
- FORM [küçük] Sert düşüş %17.4, 13 saat önce, RVOL 2.08
- DOGS [küçük] Sert düşüş %17.3, 13 saat önce, RVOL 1.44
- FOGO [küçük] Sert düşüş %17.2, 13 saat önce, RVOL 1.01

## Kâğıt ileri test (açık: 40)

- Sert düşüş: işlem yok
- Trend tersi sert yükseliş: işlem yok

_Simülasyondur, yatırım tavsiyesi değildir. Küçük coinlerde kayma ve likidite riski yüksektir._