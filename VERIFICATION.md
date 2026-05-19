# Vérification statique

Version : 0.2.1
Nom projet : Odoo SAV Magasin

Contrôles effectués :

- Parsing XML des vues, menus, sécurité, rapports et données.
- Compilation Python de tous les modules custom.
- Lecture des manifests `__manifest__.py`.
- Contrôle des dépendances internes `sav_magasin_*`.
- Contrôle des références `model_*` dans les fichiers `ir.model.access.csv`.
- Mise en mode `application=False` pour les sous-modules ; seul `sav_magasin_app` est visible comme application principale.

Limite : cette vérification est statique. Elle ne remplace pas un test d'installation réel dans ton conteneur Odoo/PostgreSQL.
