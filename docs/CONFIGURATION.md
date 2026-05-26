# Configuration

## Fichier `.env`

Le fichier `.env.example` fournit les valeurs par défaut à copier :

```bash
cp .env.example .env
```

Variables utilisées par `docker-compose.yml` :

| Variable | Rôle | Exemple |
|---|---|---|
| `ODOO_VERSION` | Version de l’image Odoo | `19.0` |
| `POSTGRES_VERSION` | Version PostgreSQL | `16` |
| `POSTGRES_DB` | Base système PostgreSQL | `postgres` |
| `POSTGRES_USER` | Utilisateur PostgreSQL | `odoo` |
| `POSTGRES_PASSWORD` | Mot de passe PostgreSQL | `odoo` |
| `ODOO_PORT` | Port local Odoo | `8069` |

## Fichier `config/odoo.conf`

Points importants :

```ini
addons_path = /usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons
```

Le chemin `/mnt/extra-addons` correspond au dossier local :

```text
./addons
```

## Volumes Docker

Deux volumes sont créés :

| Volume | Contenu |
|---|---|
| `db-data` | Données PostgreSQL |
| `odoo-data` | Filestore Odoo |

## Environnement local uniquement

La configuration fournie est pensée pour une maquette locale. Avant un usage serveur ou production, il faudra au minimum :

- changer `admin_passwd` ;
- changer les mots de passe PostgreSQL ;
- désactiver ou encadrer `list_db` ;
- activer `proxy_mode` si Odoo est derrière un reverse proxy ;
- mettre en place des sauvegardes ;
- contrôler les droits utilisateurs.
