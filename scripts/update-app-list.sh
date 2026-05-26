#!/usr/bin/env bash
set -euo pipefail

DB_NAME="${1:-}"

if [ -z "$DB_NAME" ]; then
  echo "Usage: ./scripts/update-app-list.sh <nom_de_la_base_odoo>"
  echo "Exemple: ./scripts/update-app-list.sh savmagasin"
  exit 1
fi

echo "Arrêt temporaire du serveur Odoo..."
docker compose stop odoo

echo "Mise à jour de la liste des modules sur la base: $DB_NAME"
docker compose run --rm odoo odoo -c /etc/odoo/odoo.conf -d "$DB_NAME" -u base --stop-after-init

echo "Redémarrage Odoo..."
docker compose up -d odoo
