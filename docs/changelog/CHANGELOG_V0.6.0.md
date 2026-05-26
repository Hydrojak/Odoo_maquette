# Changelog v0.6.0 — Achats fournisseurs SAV

## Objectif

Connecter les lignes composants batterie SAV au module standard Odoo Purchase afin de pouvoir créer une commande fournisseur depuis une composant batterie à commander.

## Ajouts

- Extension de `purchase.order` avec un lien vers le dossier SAV.
- Extension de `purchase.order.line` avec un lien vers la ligne composant batterie SAV.
- Champs achat sur les lignes composants batterie SAV : fournisseur, commande, ligne commande, date attendue, statut achat.
- Bouton `Créer commande fournisseur` depuis une ligne composant batterie.
- Bouton `Ouvrir commande` depuis une ligne composant batterie.
- Smart button `Achats` sur le dossier SAV.
- Menu `Achats / Réceptions → Commandes fournisseur SAV`.
- Menus `Composants batterie commandées` et `Composants batterie reçues`.
- Réception sans commande enrichie avec rattachement possible à une ligne composant batterie SAV.
- Validation d'une réception sans commande : les lignes SAV liées passent en état `Reçue`.
- Données de démonstration enrichies pour montrer un scénario composant batterie à commander puis réception.

## Limites

- Les commandes fournisseurs sont créées en brouillon / demande de prix.
- La validation logistique complète des réceptions Odoo (`stock.picking`) reste à développer.
- La génération automatique de mouvements stock réels depuis les lignes SAV n'est pas encore activée.

## Scénario de démonstration

1. Ouvrir `SAV-DEMO-003`.
2. Aller dans l'onglet `Composants / stock`.
3. Ouvrir la ligne `Composant batterie critique en attente pour scénario B2B`.
4. Cliquer sur `Créer commande fournisseur`.
5. Ouvrir le smart button `Achats` sur le dossier.
6. Ouvrir `Achats / Réceptions → Réceptions sans commande`.
7. Ouvrir la réception de démonstration et la valider pour marquer la composant batterie comme reçue.
