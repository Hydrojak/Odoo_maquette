# FAQ dépannage

## Je ne vois pas l’application Re-Watt ERP

Vérifier que les addons sont bien montés :

```bash
./scripts/check-addons.sh
```

Puis dans Odoo :

```text
Apps → Mettre à jour la liste des apps
```

Chercher :

```text
Re-Watt ERP
```

## Je ne vois que Référentiel

Ca indique souvent que seul `sav_magasin_product` est installé ou que les autres modules n’ont pas été mis à jour.

Installer ou mettre à jour :

```bash
./scripts/install-sav-magasin.sh NOM_BASE
```

## Une erreur apparaît à l’installation

Lire les logs :

```bash
docker compose logs -f odoo
```

Puis identifier :

- le fichier XML concerné ;
- le modèle concerné ;
- le champ absent ;
- la référence XML introuvable.

## Les modules n’apparaissent pas dans Apps

Vérifier `addons_path` :

```bash
docker compose exec odoo bash -lc "grep -n '^addons_path' /etc/odoo/odoo.conf"
```

Vérifier les manifests :

```bash
docker compose exec odoo bash -lc "find /mnt/extra-addons -maxdepth 2 -name __manifest__.py -print"
```

## Odoo garde une ancienne version

Mettre à jour le module :

```bash
docker compose run --rm odoo odoo -c /etc/odoo/odoo.conf -d NOM_BASE -u sav_magasin_app --stop-after-init
docker compose restart odoo
```

Puis faire un rafraîchissement navigateur forcé.

## Je veux repartir de zéro

Attention : supprime la base locale et le filestore local.

```bash
docker compose down -v
docker compose up -d
```

## Le port 8069 est déjà utilisé

Modifier `.env` :

```text
ODOO_PORT=8070
```

Puis relancer :

```bash
docker compose up -d
```

## Les données de démo ne sont pas visibles

Installer explicitement :

```bash
./scripts/install-demo-data.sh NOM_BASE
```
