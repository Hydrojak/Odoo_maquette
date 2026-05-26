# Guide développeur

## Structure des addons

```text
addons/
├── sav_magasin_app
├── sav_magasin_core
├── sav_magasin_product
├── sav_magasin_partner
├── sav_magasin_stock
├── sav_magasin_substitution
├── sav_magasin_repair
├── sav_magasin_purchase
├── sav_magasin_knowledge
├── sav_magasin_dashboard
└── sav_magasin_demo
```

## Convention de nommage

- Préfixe technique : `sav_magasin_`.
- Modèles métier : `sav.magasin.*`.
- Nom affiché : `Re-Watt ERP`.
- Ne pas réintroduire l’ancien nom `destock`.

## Ajouter un module

Un module doit contenir au minimum :

```text
__init__.py
__manifest__.py
models/
views/
security/ir.model.access.csv si nouveaux modèles
```

## Mise à jour après modification

```bash
docker compose run --rm odoo odoo -c /etc/odoo/odoo.conf -d NOM_BASE -u NOM_MODULE --stop-after-init
docker compose restart odoo
```

## Contrôles avant commit

```bash
python -m compileall addons
find addons -name '*.xml' -print
./scripts/check-addons.sh
```

## Points de vigilance Odoo

- chaque modèle custom doit avoir une ligne dans `ir.model.access.csv` ;
- les références XML doivent exister au moment du chargement ;
- l’ordre des fichiers dans `__manifest__.py` est important ;
- les menus doivent pointer vers des actions valides ;
- éviter de masquer tous les menus derrière des groupes pendant le MVP ;
- ne pas dépendre d’un champ Odoo sans vérifier sa présence si la version peut varier.

## Stratégie custom / standard

À recoder en custom :

- assistant comptoir ;
- workflow atelier batterie ;
- procédures métier ;
- décision stock dans le dossier ;
- règles de substitution métier.

À utiliser via Odoo standard :

- clients ;
- produits ;
- stocks ;
- achats ;
- ordres Repair ;
- facturation future.
