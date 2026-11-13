"""Bir markdown dosyasını Telegram'a gönderir (gece analiz raporu için).
Kullanım: python bot/notify.py docs/gunluk/2026-11-13.md"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import telegram  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def md_to_tg(md):
    out = []
    for line in md.splitlines():
        line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        line = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", line)
        if line.startswith("#"):
            line = "<b>" + line.lstrip("# ").strip() + "</b>"
        if re.match(r"^\|[-| :]+\|$", line):
            continue
        out.append(line)
    return "\n".join(out)


def main():
    path = os.path.join(ROOT, sys.argv[1])
    chat = os.environ.get("TELEGRAM_CHAT_ID")
    for f in ("futures.json", "portfolio.json"):
        p = os.path.join(ROOT, "state", f)
        if not chat and os.path.exists(p):
            chat = json.load(open(p, encoding="utf-8")).get("chat_id")
    text = open(path, encoding="utf-8").read()
    ok = telegram.send(chat, md_to_tg(text))
    print("gönderildi" if ok else "gönderilemedi")


if __name__ == "__main__":
    main()
