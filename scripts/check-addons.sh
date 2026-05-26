#!/usr/bin/env bash
set -euo pipefail

echo "== Conteneurs =="
docker compose ps

echo ""
echo "== Addons montés dans Odoo =="
docker compose exec odoo bash -lc 'ls -la /mnt/extra-addons && echo && find /mnt/extra-addons -maxdepth 2 -name __manifest__.py -print | sort'

echo ""
echo "== addons_path dans la configuration =="
docker compose exec odoo bash -lc "grep -n '^addons_path' /etc/odoo/odoo.conf || true"
