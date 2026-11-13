import os
import time
import requests

TOKEN = os.environ.get("TELEGRAM_TOKEN", "").strip()
API = f"https://api.telegram.org/bot{TOKEN}"


def enabled():
    return bool(TOKEN)


def _call(method, **kw):
    """Telegram çağrısı, bağlantı koparsa 4 kez dener."""
    for i in range(4):
        try:
            r = requests.post(f"{API}/{method}", data=kw, timeout=20)
            return r.json()
        except Exception as e:  # bildirim hatası botu durdurmasın
            print(f"telegram {method} hata ({i+1}/4):", e)
            time.sleep(2 + i * 3)
    return {}


def updates(offset=None):
    if not TOKEN:
        return []
    r = _call("getUpdates", offset=offset or "", timeout=0)
    if not r.get("ok"):
        print("telegram getUpdates cevap:", {k: v for k, v in r.items() if k != "result"})
    else:
        print(f"telegram: {len(r['result'])} yeni mesaj")
    return r.get("result", [])


def send(chat_id, text):
    if not TOKEN or not chat_id:
        print("[telegram kapalı]\n" + text)
        return False
    for chunk in [text[i:i + 3900] for i in range(0, len(text), 3900)]:
        r = _call("sendMessage", chat_id=chat_id, text=chunk, parse_mode="HTML", disable_web_page_preview="true")
        if not r.get("ok"):
            print("telegram send cevap:", r)
            return False
    return True
