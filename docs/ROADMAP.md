# Roadmap

## Version actuelle — v0.5.1-docs

Base fonctionnelle : v0.5.0 Repair & Knowledge métier.

Fonctionnalités disponibles :

- dossier SAV ;
- assistant nouveau dossier ;
- bons PDF dépôt/restitution ;
- lignes composants batterie ;
- lecture stock métier ;
- substitutions articles ;
- liaison Repair Odoo ;
- knowledge métier ;
- données de démonstration.

## v0.6.0 — Stock réel et achats réels

Objectif : connecter les décisions métier aux objets Odoo.

À développer :

1. créer un `stock.move` ou `stock.picking` lors de la consommation composant batterie ;
2. créer un transfert interne Odoo depuis une ligne en demande transfert ;
3. créer une commande fournisseur depuis une ligne à commander ;
4. lier `stock.picking` et `purchase.order` au dossier SAV ;
5. ajouter smart buttons : transferts, commandes, mouvements ;
6. relancer automatiquement un dossier quand une composant batterie arrive.

## v0.7.0 — Repair approfondi et kits

Objectif : renforcer le lien technique réparation.

À développer :

- synchroniser les composants batterie du dossier avec Repair ;
- récupérer les composants batterie consommées depuis Repair ;
- ajouter modèles de réparation ;
- évaluer BoM / kits de réparation.

## v0.8.0 — Devis, vente, facturation

Objectif : couvrir le cycle commercial.

À développer :

- créer devis depuis dossier ;
- convertir devis en commande ;
- créer facture ;
- gérer réparation gratuite / garantie ;
- gérer B2B facturation différée ;
- bloquer ou alerter avant restitution si facture non traitée.

## v0.9.0 — Sécurité, pilotage, qualité

Objectif : préparer un usage plus réaliste.

À développer :

- droits par profil ;
- règles par magasin ;
- KPI SAV ;
- registre des dossiers bloqués ;
- articles incomplets ;
- stock critique ;
- journalisation métier renforcée.

## v1.0.0 — Démonstrateur métier stable

Critères :

- installation propre ;
- données de démo fiables ;
- parcours complet de bout en bout ;
- documentation utilisateur ;
- flux stock/achat/facturation suffisamment représentatifs ;
- validation par utilisateurs métier.
