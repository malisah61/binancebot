#!/usr/bin/env bash
# Binance API anahtarını yalnız bu sunucuya (/etc/kripto.env, başkaları okuyamaz) kaydeder; GitHub'a gitmez.
set -euo pipefail
read -r -p "Binance API Key: " K
read -r -s -p "Binance Secret Key (ekranda görünmez): " S; echo
grep -v '^BINANCE_REAL_' /etc/kripto.env > /etc/kripto.env.tmp || true
printf 'BINANCE_REAL_KEY=%s\nBINANCE_REAL_SECRET=%s\n' "$K" "$S" >> /etc/kripto.env.tmp
mv /etc/kripto.env.tmp /etc/kripto.env; chown root:kripto /etc/kripto.env; chmod 640 /etc/kripto.env
unset K S
echo "Kaydedildi. Kontrol ediliyor..."
sudo -u kripto bash -c 'set -a; . /etc/kripto.env; set +a; /home/kripto/venv/bin/python /home/kripto/binancebot/server/kontrol.py'
