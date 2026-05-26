# Vérification v0.8.0 — Re-Watt ERP Battery Foundation

## Contrôles statiques effectués

- Lecture des manifests `__manifest__.py`.
- Vérification des fichiers déclarés dans `data`.
- Vérification des dépendances custom `sav_*`.
- Compilation Python par `py_compile`.
- Parsing XML avec `lxml.etree`.
- Recherche des XPath interdits basés sur `@string`.
- Suppression des dossiers `__pycache__`.
- Recherche de termes téléphone/mobile dans les addons.

## Résultat

Aucune erreur statique détectée.

## Limite

Aucun test runtime complet n’a été exécuté dans le conteneur Odoo local de l’utilisateur.  
La validation finale reste à faire par installation sur base vierge Odoo.
