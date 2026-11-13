import os
import requests

TOKEN = os.environ.get("TELEGRAM_TOKEN", "").strip()
API = f"https://api.telegram.org/bot{TOKEN}"


def enabled():
    return bool(TOKEN)


def updates(offset=None):
    if not TOKEN:
        return []
    try:
        r = requests.get(API + "/getUpdates", params={"offset": offset, "timeout": 0}, timeout=15)
        return r.json().get("result", [])
    except Exception as e:  # bildirim hatası botu durdurmasın
        print("telegram getUpdates hata:", e)
        return []


def send(chat_id, text):
    if not TOKEN or not chat_id:
        print("[telegram kapalı]\n" + text)
        return False
    for chunk in [text[i:i + 3900] for i in range(0, len(text), 3900)]:
        try:
            requests.post(API + "/sendMessage", timeout=15, data={
                "chat_id": chat_id, "text": chunk, "parse_mode": "HTML", "disable_web_page_preview": "true"})
        except Exception as e:
            print("telegram send hata:", e)
            return False
    return True
