"""GitHub Actions'tan Hetzner sunucusu kurar (HCLOUD_TOKEN gizli değişkeni ile). Adımlar:
  ip   : Almanya'da sabit bir IPv4 ayırır ve Telegram'a yazar (Binance API anahtarının IP kısıtlamasına girilecek).
  kur  : Bu IP ile Ubuntu 24.04 sunucu açar; kur.sh'yi çalıştırır; BINANCE_REAL_KEY/SECRET varsa yalnız sunucudaki
         /etc/kripto.env dosyasına yazar; salt-okur kontrol sonucunu Telegram'a gönderir.
  sil  : Sunucuyu siler (IP kalır)."""
import json, os, sys, time
import requests
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "bot"))
import telegram  # noqa: E402

API = "https://api.hetzner.cloud/v1"
H = {"Authorization": f"Bearer {os.environ['HCLOUD_TOKEN']}", "Content-Type": "application/json"}
NAME, IPNAME, LOC = "kripto-bot", "kripto-ip", "nbg1"
TYPES = ["cx23", "cx22", "cpx22", "cpx11", "cax11"]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHAT = os.environ.get("TELEGRAM_CHAT_ID") or str(json.load(open(os.path.join(ROOT, "state", "futures.json"))).get("chat_id") or "")


def call(m, path, **kw):
    r = requests.request(m, API + path, headers=H, timeout=30, **kw)
    if r.status_code >= 300:
        raise RuntimeError(f"{m} {path}: {r.status_code} {r.text[:300]}")
    return r.json() if r.text else {}


def say(t):
    print(t)
    telegram.send(CHAT, t)


def get_ip():
    for p in call("GET", "/primary_ips", params={"name": IPNAME})["primary_ips"]:
        return p
    return None


def step_ip():
    p = get_ip() or call("POST", "/primary_ips", json={"name": IPNAME, "type": "ipv4", "assignee_type": "server",
                                                         "location": LOC, "auto_delete": False})["primary_ip"]
    say(f"🖥️ Sunucu IP adresi ayrıldı: {p['ip']}\nBinance API anahtarını oluştururken 'Restrict access to trusted IPs only' kısmına bunu yazın.")


def user_data():
    k, s = os.environ.get("BINANCE_REAL_KEY", ""), os.environ.get("BINANCE_REAL_SECRET", "")
    tok = os.environ.get("TELEGRAM_TOKEN", "")
    env = f"TELEGRAM_TOKEN={tok}\nTELEGRAM_CHAT_ID={CHAT}\n" + (f"BINANCE_REAL_KEY={k}\nBINANCE_REAL_SECRET={s}\n" if k and s else "")
    ind = "\n".join("      " + x for x in env.strip().splitlines())
    return f"""#cloud-config
write_files:
  - path: /etc/kripto.env
    permissions: '0640'
    content: |
{ind}
runcmd:
  - [bash, -c, "curl -fsSL https://raw.githubusercontent.com/malisah61/binancebot/main/server/kur.sh | bash > /var/log/kripto-kur.log 2>&1"]
  - [bash, -c, "set -a; . /etc/kripto.env; set +a; OUT=$(sudo -u kripto --preserve-env=BINANCE_REAL_KEY,BINANCE_REAL_SECRET /home/kripto/venv/bin/python /home/kripto/binancebot/server/kontrol.py 2>&1); curl -s -X POST https://api.telegram.org/bot$TELEGRAM_TOKEN/sendMessage --data-urlencode chat_id=$TELEGRAM_CHAT_ID --data-urlencode \\"text=🖥️ Sunucu kuruldu. Kontrol:\\n$OUT\\" > /dev/null"]
"""


def step_kur():
    for s in call("GET", "/servers", params={"name": NAME})["servers"]:
        say(f"Sunucu zaten var ({s['public_net']['ipv4']['ip']}). Yeniden kurmak için önce 'sil' adımını çalıştırın.")
        return
    p = get_ip()
    if not p:
        step_ip()
        p = get_ip()
    last = None
    for t in TYPES:
        try:
            r = call("POST", "/servers", json={"name": NAME, "server_type": t, "image": "ubuntu-24.04", "location": LOC,
                                                "public_net": {"enable_ipv4": True, "enable_ipv6": True, "ipv4": p["id"]},
                                                "user_data": user_data()})
            break
        except RuntimeError as e:
            last = e
            print("tip denenemedi:", t, e)
    else:
        raise last
    has_key = bool(os.environ.get("BINANCE_REAL_KEY"))
    say(f"🖥️ Sunucu açılıyor: {r['server']['server_type']['name']} · Almanya · IP {p['ip']}\n"
        f"Root şifresi Hetzner'in e-postasına gelir. Kurulum ~3-5 dk sürer; bitince kontrol sonucu buraya gelecek.\n"
        f"Binance anahtarı: {'sunucuya yazıldı (yalnız sunucuda)' if has_key else 'henüz yok — GitHub secrets ekleyip sil + kur yapın'}.")


def step_sil():
    for s in call("GET", "/servers", params={"name": NAME})["servers"]:
        call("DELETE", f"/servers/{s['id']}")
        say("🗑️ Sunucu silindi (IP adresi korunuyor).")
        return
    say("Silinecek sunucu yok.")


def step_durum():
    S = call("GET", "/servers", params={"name": NAME})["servers"]
    if not S:
        say("Sunucu yok.")
        return
    s = S[0]
    say(f"🖥️ Sunucu durumu: {s['status']} · {s['server_type']['name']} · IP {s['public_net']['ipv4']['ip']} · açılış {s['created'][:16].replace('T', ' ')} UTC")


if __name__ == "__main__":
    {"ip": step_ip, "kur": step_kur, "sil": step_sil, "durum": step_durum}[sys.argv[1]]()
