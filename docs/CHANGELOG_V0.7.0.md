# Changelog v0.7.0 — Flux stock réels

## Objectif

Connecter progressivement le métier SAV aux objets natifs Stock d'Odoo sans automatiser brutalement la validation physique.

## Ajouts

- Module `sav_magasin_stock_flow`.
- Champs de liaison sur `stock.picking` et `stock.move` : dossier SAV, ligne composant batterie SAV, réception SAV.
- Création de flux de réservation / sortie depuis une ligne composant batterie.
- Création de transfert interne depuis un stock distant identifié.
- Création de réception stock depuis une réception sans commande.
- Menu `Flux stock SAV`.
- Bouton `Synchroniser stock` sur les lignes composants batterie.

## Choix de conception

La v0.7.0 crée les flux stock, les confirme et tente une assignation si possible. Elle ne force pas la validation automatique (`button_validate`) afin de conserver les contrôles natifs Odoo Inventory.
