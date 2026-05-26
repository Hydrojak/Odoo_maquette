# Vérification v0.6.0

Contrôles réalisés avant livraison :

- compilation Python des modules custom ;
- parsing XML des vues et données ;
- lecture des manifests ;
- suppression des fichiers `__pycache__` ;
- ajout des dépendances nécessaires au module `sav_magasin_purchase` ;
- vérification des nouveaux fichiers de documentation.

Test runtime complet à faire dans Odoo :

```bash
docker compose run --rm odoo odoo -c /etc/odoo/odoo.conf -d NOM_BASE -u sav_magasin_app,sav_magasin_purchase,sav_magasin_demo --stop-after-init
```
