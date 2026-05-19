#!/usr/bin/env bash
set -euo pipefail

DB_NAME="${1:-}"

if [ -z "$DB_NAME" ]; then
  echo "Usage: ./scripts/install-sav-magasin.sh <nom_de_la_base_odoo>"
  echo "Exemple: ./scripts/install-sav-magasin.sh savmagasin"
  exit 1
fi

echo "Arrêt temporaire du serveur Odoo..."
docker compose stop odoo

echo "Installation du module principal sav_magasin_app sur la base: $DB_NAME"
docker compose run --rm odoo odoo -c /etc/odoo/odoo.conf -d "$DB_NAME" -i sav_magasin_app --stop-after-init

echo "Redémarrage Odoo..."
docker compose up -d odoo

echo "Terminé. Ouvre http://localhost:8069 puis cherche le menu SAV Magasin."
