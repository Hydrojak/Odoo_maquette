# Correction v0.2.2 - Menus SAV visibles

Cause du symptôme : le référentiel produit était visible via `base.group_user`, mais les menus SAV pointaient vers des modèles protégés par les groupes spécifiques SAV.
Un utilisateur interne sans groupe `Accueil magasin` ne voyait donc que : Marques, Gammes, Modèles, Types articles.

Correctif MVP : les modèles opérationnels SAV et réception rapide donnent maintenant accès aux utilisateurs internes (`base.group_user`).
Les groupes métier spécifiques restent présents pour une future sécurisation plus fine.

Après remplacement du projet :

```bash
docker compose run --rm odoo odoo -c /etc/odoo/odoo.conf -d NOM_DE_TA_BASE -u sav_magasin_core,sav_magasin_purchase,sav_magasin_app --stop-after-init
docker compose restart odoo
```

Puis recharger Odoo avec Ctrl+F5.
