# Vérification v0.8.2

Correction du jeu de données de démonstration Re-Watt ERP.

## Correctif

Le hook `sav_magasin_demo` utilisait la valeur `different` pour le champ `warranty_impact` du modèle `sav.magasin.product.substitution`.
Cette valeur n'existe pas dans la sélection autorisée.

Correction : `different` remplacé par `confirm`.

## Contrôles statiques

- Python compilé.
- XML parsé.
- Recherche de la valeur invalide dans le code : absente.
- Recherche des XPath interdits `@string` : absente dans les vues héritées critiques.
