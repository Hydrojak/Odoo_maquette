# Changelog v0.4.0 — Stock SAV et substitutions

## Objectif

La v0.4.0 ajoute une première couche métier autour des composants batterie SAV : décision stock, réservation métier, demande de transfert, demande de commande fournisseur et composants de substitution.

## Nouveautés principales

### Stock / composants batterie SAV

- Ajout d'un menu `Re-Watt ERP → Stock / Composants batterie`.
- Ajout d'une vue globale des lignes composants batterie SAV.
- Ajout des vues `Composants batterie à transférer` et `Composants batterie à commander`.
- Ajout d'une action recommandée sur chaque ligne composant batterie : réserver localement, demander transfert, commander fournisseur.
- Ajout des champs : stock local, stock distant, stock total, source distante, note de décision stock.
- Ajout de boutons métier : vérifier, réserver, transfert, commander, consommer, annuler réservation.

### Substitutions articles

- Nouveau module `sav_magasin_substitution`.
- Nouveau menu `Re-Watt ERP → Référentiel → Substitutions articles`.
- Possibilité de définir des substituts entre articles.
- Qualification du substitut : équivalent, compatible, supérieur, dégradé, dépannage temporaire.
- Validation métier : validé, à tester, validation responsable, interdit.
- Impact garantie et politique prix.
- Suggestion de substitut directement sur les lignes composants batterie SAV.
- Bouton `Utiliser substitut` depuis la ligne composant batterie.

### Données de démonstration

- Ajout d'articles de démonstration spécifiques à la v0.4.0.
- Ajout de substitutions batterie iPhone 13 et écran Galaxy S22.
- Ajout de lignes composants batterie sur des dossiers SAV de démonstration.
- Ajout de cas de démonstration : composant batterie à vérifier, composant batterie à commander, substitution validée, substitution avec validation responsable.

## Limites assumées

- La réservation est une réservation métier SAV, pas encore une réservation stock Odoo `stock.move`.
- Le transfert est une intention métier, pas encore un picking interne généré automatiquement.
- La commande fournisseur est une intention métier, pas encore une commande `purchase.order` générée.
- La consommation de composant batterie est tracée dans le dossier, mais ne décrémente pas encore physiquement le stock Odoo.

Ces points sont volontairement gardés pour la v0.5.0 afin de ne pas complexifier le MVP avant validation du parcours métier.
