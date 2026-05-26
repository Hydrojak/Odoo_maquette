# Vérification v0.7.0

Contrôles réalisés hors runtime Odoo :

- parsing XML des vues ;
- compilation Python ;
- lecture des manifests ;
- absence de fichiers `__pycache__` ;
- absence de sélecteurs XPath `@string` dans les vues héritées ajoutées ;
- contrôle de présence du module `sav_magasin_stock_flow` dans l'application principale.

Un test runtime complet reste à faire dans le conteneur Odoo cible.
