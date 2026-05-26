# Vérification v0.5.0

Contrôles effectués avant génération du ZIP :

- parsing XML de tous les fichiers `addons/**/*.xml` ;
- compilation Python de tous les modules `addons/**/*.py` ;
- suppression des dossiers `__pycache__` ;
- lecture statique des manifests ;
- ajout contrôlé des modules `sav_magasin_repair` et `sav_magasin_knowledge` ;
- mise à jour de `sav_magasin_app` pour charger les nouveaux modules ;
- mise à jour de `sav_magasin_demo` pour enrichir le scénario de démonstration.

Limite : validation runtime complète à effectuer dans ton conteneur Odoo local après installation ou mise à jour des modules.
