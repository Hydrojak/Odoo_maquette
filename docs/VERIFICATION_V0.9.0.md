# Vérification v0.9.0

Contrôles statiques effectués :

- parsing XML ;
- compilation Python ;
- lecture des manifests ;
- vérification des fichiers déclarés dans les manifests ;
- recherche de XPath interdits `@string` ;
- suppression des dossiers `__pycache__`.

Limite : aucun test runtime complet n'a été effectué dans une instance Odoo locale depuis cet environnement.
