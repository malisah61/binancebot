#!/usr/bin/env bash
# Root olarak çalışır: kodu çeker, server/units altındaki servisleri kurar/günceller, gerekirse paketleri yükler.
set -uo pipefail
R=/home/kripto/binancebot
OLD=$(sudo -u kripto git -C $R rev-parse HEAD 2>/dev/null)
sudo -u kripto git -C $R pull -q --ff-only || sudo -u kripto git -C $R reset -q --hard origin/main
NEW=$(sudo -u kripto git -C $R rev-parse HEAD)
if [ "$OLD" != "$NEW" ] && ! sudo -u kripto git -C $R diff --quiet "$OLD" "$NEW" -- bot/requirements.txt 2>/dev/null; then
  sudo -u kripto /home/kripto/venv/bin/pip install -q -r $R/bot/requirements.txt
fi
CH=0
for f in $R/server/units/*; do
  b=$(basename "$f")
  if ! cmp -s "$f" "/etc/systemd/system/$b"; then cp "$f" "/etc/systemd/system/$b"; CH=1; fi
done
if [ $CH = 1 ]; then
  systemctl daemon-reload
  for t in $R/server/units/*.timer; do systemctl enable --now "$(basename "$t")" >/dev/null 2>&1; done
fi
