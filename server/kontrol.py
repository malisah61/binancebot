"""Sunucu kontrolü — YALNIZ OKUR, hiçbir emir göndermez.
1) Binance Futures'a bu sunucudan erişilebiliyor mu (ABD/engelli bölge değil mi)?
2) Anahtar girildiyse: para çekme izni KAPALI mı, futures izni açık mı, IP kısıtlaması var mı, USDT bakiyesi."""
import hashlib, hmac, os, time, urllib.parse
import requests

def ok(m): print("✅", m)
def bad(m): print("❌", m)

try:
    r = requests.get("https://fapi.binance.com/fapi/v1/time", timeout=10)
    if r.status_code == 200:
        ok(f"Binance Futures erişimi var (gecikme {r.elapsed.total_seconds()*1000:.0f} ms)")
    else:
        bad(f"Binance Futures erişimi YOK (HTTP {r.status_code}). Sunucu konumu engelli olabilir — ABD dışı (Almanya/Finlandiya) seçin.")
except Exception as e:
    bad(f"Binance'e bağlanılamadı: {e}")
ip = requests.get("https://api.ipify.org", timeout=10).text
print(f"ℹ️ Sunucunun IP adresi: {ip}  ← Binance API anahtarında 'IP kısıtlaması'na bunu yazın")

K, S = os.environ.get("BINANCE_REAL_KEY"), os.environ.get("BINANCE_REAL_SECRET")
if not K or not S:
    print("ℹ️ API anahtarı henüz girilmedi.")
    raise SystemExit
def signed(base, path):
    q = urllib.parse.urlencode({"timestamp": int(time.time() * 1000), "recvWindow": 10000})
    sig = hmac.new(S.encode(), q.encode(), hashlib.sha256).hexdigest()
    return requests.get(f"{base}{path}?{q}&signature={sig}", headers={"X-MBX-APIKEY": K}, timeout=10)
r = signed("https://api.binance.com", "/sapi/v1/account/apiRestrictions")
if r.status_code != 200:
    bad(f"Anahtar okunamadı: {r.text[:200]}"); raise SystemExit
p = r.json()
(bad("PARA ÇEKME İZNİ AÇIK — Binance'te bu izni hemen kapatın! Bot bu anahtarla çalışmayacak.") if p.get("enableWithdrawals") else ok("Para çekme izni kapalı"))
(ok("Futures izni açık") if p.get("enableFutures") else bad("Futures izni kapalı — anahtar ayarlarından 'Enable Futures' açın"))
(ok("IP kısıtlaması var") if p.get("ipRestrict") else bad("IP kısıtlaması yok — anahtarı yalnız bu sunucunun IP'sine kısıtlayın"))
r = signed("https://fapi.binance.com", "/fapi/v2/balance")
if r.status_code == 200:
    u = next((x for x in r.json() if x["asset"] == "USDT"), None)
    ok(f"Futures USDT bakiyesi: {float(u['balance']):.2f}" if u else "Futures cüzdanında USDT yok")
else:
    bad(f"Futures bakiyesi okunamadı: {r.text[:200]}")
