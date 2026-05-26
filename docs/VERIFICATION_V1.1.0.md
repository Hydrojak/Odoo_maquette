# Vérification v1.1.0

Contrôles effectués hors runtime Odoo local :

- manifests lisibles ;
- fichiers XML parsés ;
- fichiers Python compilés ;
- absence de `__pycache__` ;
- recherche XPath interdit `@string` ;
- nouveaux modèles ajoutés aux droits d’accès ;
- nouveau fichier de vues déclaré dans le manifest.

Un test d’installation runtime reste nécessaire dans le conteneur Odoo cible.
