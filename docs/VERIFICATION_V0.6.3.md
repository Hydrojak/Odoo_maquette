# Vérification v0.6.3

## Objet

Correction de l'erreur d'installation Odoo liée aux fichiers XML de données.

## Changements

- Retrait des fichiers XML de données des manifests pour les modules concernés :
  - `sav_magasin_core/data/sequence.xml`
  - `sav_magasin_purchase/data/sequence.xml`
  - `sav_magasin_knowledge/data/default_procedures.xml`
  - `sav_magasin_demo/data/demo_data.xml`
- Création des séquences via `post_init_hook` Python.
- Création des procédures Knowledge via `post_init_hook` Python.
- Création des données de démonstration via `post_init_hook` Python.
- Ajout d'un fallback Python si une séquence manque lors de la création d'un dossier SAV ou d'une réception.

## Contrôles statiques

- Parsing XML effectué.
- Compilation Python effectuée.
- Lecture des manifests effectuée.
- Vérification de l'existence des fichiers référencés dans les manifests effectuée.
- Suppression des dossiers `__pycache__` effectuée.

## Limite

La validation runtime complète doit être faite dans un conteneur Odoo réel.
