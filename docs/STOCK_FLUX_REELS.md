# Flux stock réels SAV

## Principe

Les lignes composants batterie SAV peuvent maintenant créer des flux stock Odoo :

- réservation / sortie composant batterie depuis le magasin du dossier ;
- transfert interne depuis un autre magasin ;
- réception stock depuis une réception sans commande.

## Parcours recommandé

1. Ouvrir un dossier SAV.
2. Ajouter une composant batterie.
3. Vérifier le stock.
4. Cliquer sur `Réserver`, `Transfert` ou `Consommer`.
5. Ouvrir le flux stock créé.
6. Valider l'opération physique dans Odoo Stock.
7. Revenir sur la ligne composant batterie et cliquer sur `Synchroniser stock`.

## Limite volontaire

La validation physique n'est pas automatisée. Cela évite de contourner les contrôles Odoo : lots, numéros de série, quantités disponibles, règles d'entrepôt, droits utilisateurs.
