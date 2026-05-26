# Installation locale

## Prérequis

- Docker installé ;
- Docker Compose disponible ;
- Git recommandé ;
- port `8069` libre sur la machine.

## Lancer la maquette

Depuis la racine du projet :

```bash
cp .env.example .env
docker compose up -d
```

Vérifier les conteneurs :

```bash
docker compose ps
```

Ouvrir :

```text
http://localhost:8069
```

## Créer la base Odoo

Dans l’interface Odoo :

1. créer une nouvelle base ;
2. choisir une langue ;
3. créer l’utilisateur administrateur ;
4. se connecter.

## Installer l’application Re-Watt ERP

Dans Odoo :

```text
Apps → Mettre à jour la liste des apps → chercher "Re-Watt ERP"
```

Installer :

```text
Re-Watt ERP - Application principale
```

Le module principal installe automatiquement les modules métier nécessaires.

## Installer les données de démonstration

Dans Odoo :

```text
Apps → Re-Watt ERP - Données de démonstration → Installer
```

Ou en ligne de commande :

```bash
./scripts/install-demo-data.sh NOM_BASE
```

## Installation complète en ligne de commande

```bash
./scripts/install-sav-magasin.sh NOM_BASE
./scripts/install-demo-data.sh NOM_BASE
```

## Remise à zéro locale

Attention : cette commande supprime les données locales Docker.

```bash
docker compose down -v
docker compose up -d
```

## Contrôle des addons

```bash
./scripts/check-addons.sh
```

Tu dois voir des manifests comme :

```text
/mnt/extra-addons/sav_magasin_app/__manifest__.py
/mnt/extra-addons/sav_magasin_core/__manifest__.py
/mnt/extra-addons/sav_magasin_demo/__manifest__.py
```
