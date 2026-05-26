# Commandes utiles

## Docker

```bash
docker compose up -d          # démarrer
docker compose ps             # état des conteneurs
docker compose logs -f odoo   # logs Odoo
docker compose restart odoo   # redémarrer Odoo
docker compose down           # arrêter
docker compose down -v        # arrêter et supprimer les volumes locaux
```

## Makefile

```bash
make up
make down
make restart
make logs
make shell
make psql
make clean
```

## Installation modules

```bash
./scripts/install-sav-magasin.sh NOM_BASE
./scripts/install-demo-data.sh NOM_BASE
./scripts/install-v050.sh NOM_BASE
```

## Mise à jour d’un module

```bash
docker compose run --rm odoo odoo -c /etc/odoo/odoo.conf -d NOM_BASE -u sav_magasin_core --stop-after-init
docker compose restart odoo
```

Mise à jour de plusieurs modules :

```bash
docker compose run --rm odoo odoo -c /etc/odoo/odoo.conf -d NOM_BASE -u sav_magasin_app,sav_magasin_core,sav_magasin_stock,sav_magasin_repair,sav_magasin_knowledge --stop-after-init
docker compose restart odoo
```

## Vérification addons

```bash
./scripts/check-addons.sh
```

## Git — push de la version actuelle

```bash
git status
git add -A
git commit -m "Documentation propre v0.5.1"
git push origin BRANCHE
```

Remplacer le contenu de `master` par la branche courante :

```bash
git push origin HEAD:master --force
```

Remplacer le contenu de `main` par la branche courante :

```bash
git push origin HEAD:main --force
```
