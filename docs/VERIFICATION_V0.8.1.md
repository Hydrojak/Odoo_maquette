# Vérification v0.8.1

Contrôles effectués :

- Compilation Python des modules.
- Parsing XML des vues et rapports.
- Vérification des fichiers référencés dans les manifests.
- Recherche des XPath interdits basés sur `@string`.
- Correction de la catégorie FAQ `diagnostic` utilisée par le hook Knowledge.

Limite : test runtime complet à effectuer dans le conteneur Odoo local.
