# 📊 Kripto Analiz + Simülasyon Botu

Binance'te hacimce ilk 100 USDT çiftini 16 gösterge ile puanlayan **Android uygulaması** ve
aynı motorla **sanal parayla** al-sat yapıp **Telegram'a bildirim** atan GitHub botu.

> ⚠️ Gerçek para kullanılmaz, Binance hesabına bağlanmaz. Skor, göstergelerin ne kadar aynı yönü
> gösterdiğinin ölçüsüdür; kesin tahmin veya yatırım tavsiyesi değildir.

## Göstergeler ve ağırlıkları

| Bileşen | Ağırlık | Ne ölçer |
|---|---|---|
| Trend EMA 20/50/200 | 2.0 | Ana trend yönü |
| Üst zaman dilimi (4s) EMA 21/55 | 1.5 | Büyük resim |
| MACD 12/26/9 | 1.5 | Momentum, kesişimler |
| Alıcı/Satıcı baskısı | 1.5 | Agresif (taker) alım oranı |
| RSI 14 | 1.0 | Momentum, aşırı alım/satım |
| ADX / DMI | 1.0 | Trend gücü ve yönü |
| OBV | 1.0 | Hacim birikimi / dağıtım |
| Hacim patlaması | 1.0 | Ortalamanın üstünde hacim + yön |
| Destek/Direnç | 1.0 | Pivot kümeleri + hacim profili (POC) |
| Emir defteri ±%2 | 1.0 | Bekleyen alış/satış duvarları |
| Büyük işlemler | 1.0 | Balina alım/satımları (son 1000 işlem, ilk %5) |
| Stoch RSI, Bollinger, MFI, VWAP, Fibonacci | 0.5 | Destekleyici sinyaller |

Skor 0-100: **≥65 yükseliş ihtimali yüksek**, **≤35 düşüş ihtimali yüksek**.
İşlem planı ATR'ye göre: stop = fiyat − 1.5×ATR (yakın destek varsa altı), hedef 1 = en yakın direnç, hedef 2 = +3.5×ATR.

## Kurulum

1. **APK:** `Actions → APK derle` bitince **Releases** bölümünden `KriptoAnaliz.apk` indir, kur.
2. **Telegram:** @BotFather → `/newbot` → token'ı al. Repo → *Settings → Secrets and variables → Actions → New repository secret* → ad: `TELEGRAM_TOKEN`.
3. Telegram'da kendi botuna herhangi bir mesaj yaz. Bot bir sonraki çalışmada (≤15 dk) seni bulur ve "✅ Bağlandı" yazar.
4. İstersen `Actions → Simülasyon botu → Run workflow` ile hemen çalıştır.

## Telegram komutları (en geç 15 dk içinde yanıt)
- `/durum` — portföy
- `/sinyal` — en yüksek / en düşük skorlu 5'er coin
- `/coin SOL` — tek coinin tam analizi

## Bot kuralları (`bot/bot.py` → `CFG`)
- Başlangıç 1000$ sanal, en fazla 5 pozisyon, her biri varlığın %19'u, komisyon %0.1
- AL: skor ≥68, göstergelerin ≥%60'ı aynı yönde, 4s trend yukarı, RSI <78, 24s hacim ≥20M$
- SAT: stop / iz süren stop (tepe − 2.2×ATR), hedef 1'de yarısı, hedef 2'de tamamı, skor ≤42
- Her pazartesi **geriye dönük test**: skorun geçmişte gerçekten işe yarayıp yaramadığını ölçer

## Klasörler
- `app/www/` — uygulama (HTML/JS), `analysis.js` analiz motoru
- `android/` — WebView kabuğu (GitHub Actions derler)
- `bot/` — Python bot, `analysis.py` (JS ile aynı motor), `backtest.py`
- `state/` — botun portföyü ve son tarama (bot yazar)
- `tests/test_bot.py` — ağsız test: `python tests/test_bot.py`
