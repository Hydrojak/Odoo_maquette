#!/usr/bin/env bash
set -euo pipefail
DB_NAME="${1:-}"
if [ -z "$DB_NAME" ]; then
  echo "Usage: ./scripts/install-v060.sh NOM_DE_TA_BASE"
  exit 1
fi
docker compose run --rm odoo odoo -c /etc/odoo/odoo.conf -d "$DB_NAME" -u sav_magasin_app,sav_magasin_purchase,sav_magasin_demo --stop-after-init
docker compose restart odoo
