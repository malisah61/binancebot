#!/usr/bin/env bash
# Kripto bot sunucu kurulumu (Ubuntu 24.04). Kullanım:
#   curl -fsSL https://raw.githubusercontent.com/malisah61/binancebot/main/server/kur.sh | sudo bash
set -euo pipefail
echo "== Paketler kuruluyor =="
apt-get update -qq
DEBIAN_FRONTEND=noninteractive apt-get install -y -qq git python3 python3-venv python3-pip ufw unattended-upgrades >/dev/null
echo "== Güvenlik duvarı (yalnız SSH açık) =="
ufw allow OpenSSH >/dev/null; ufw --force enable >/dev/null
dpkg-reconfigure -f noninteractive unattended-upgrades >/dev/null || true
id kripto >/dev/null 2>&1 || useradd -m -s /bin/bash kripto
echo "== Kod indiriliyor =="
if [ -d /home/kripto/binancebot ]; then sudo -u kripto git -C /home/kripto/binancebot pull -q; else sudo -u kripto git clone -q https://github.com/malisah61/binancebot /home/kripto/binancebot; fi
sudo -u kripto python3 -m venv /home/kripto/venv
sudo -u kripto /home/kripto/venv/bin/pip install -q -r /home/kripto/binancebot/bot/requirements.txt
echo "== Otomatik güncelleme (her 15 dk) =="
cat > /etc/systemd/system/kripto-guncelle.service <<'U'
[Unit]
Description=Kripto bot kodunu guncelle
[Service]
Type=oneshot
User=kripto
ExecStart=/usr/bin/git -C /home/kripto/binancebot pull -q --ff-only
U
cat > /etc/systemd/system/kripto-guncelle.timer <<'U'
[Unit]
Description=Kripto bot 15 dakikada bir guncelle
[Timer]
OnBootSec=2min
OnUnitActiveSec=15min
[Install]
WantedBy=timers.target
U
systemctl daemon-reload; systemctl enable --now kripto-guncelle.timer >/dev/null
touch /etc/kripto.env; chown root:kripto /etc/kripto.env; chmod 640 /etc/kripto.env
echo
echo "== Kurulum tamam. Şimdi bağlantı kontrolü: =="
sudo -u kripto /home/kripto/venv/bin/python /home/kripto/binancebot/server/kontrol.py
echo
echo "API anahtarını girmek için (anahtar ekranda görünmez):  sudo bash /home/kripto/binancebot/server/anahtar.sh"
