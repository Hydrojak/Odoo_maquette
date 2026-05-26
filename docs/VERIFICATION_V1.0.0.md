# Vérification v1.0.0

Contrôles réalisés avant génération du ZIP :

- Lecture des manifests Python.
- Vérification des fichiers déclarés dans les manifests.
- Parsing XML avec `lxml`.
- Compilation Python des addons.
- Recherche de XPath Odoo 19 interdits basés sur `@string`.
- Suppression des fichiers `__pycache__`.

Points non couverts :

- Test runtime complet dans un conteneur Odoo local.
- Test fonctionnel réel de validation de checklist dans l’interface.
- Validation des droits fins qualité par profil utilisateur.
