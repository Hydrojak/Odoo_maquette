# Changelog v0.5.0 — Repair & Knowledge métier

## Objectif

Cette version renforce la maquette Re-Watt ERP avec deux briques structurantes :

- une première liaison entre le dossier atelier batterie et le module standard Odoo `repair` ;
- une base de procédures métier intégrée, indépendante de l'application Knowledge Enterprise.

## Nouveaux modules

### `sav_magasin_repair`

Rôle : relier le dossier atelier batterie à un ordre de réparation batterie Odoo standard.

Fonctions ajoutées :

- champ `Produit Odoo à réparer` sur le dossier SAV ;
- champ `Ordre de réparation batterie` lié ;
- bouton `Créer ordre réparation` ;
- smart button `Réparation` ;
- ouverture directe du `repair.order` lié ;
- création prudente de l'ordre Repair via introspection des champs disponibles.

Le dossier SAV reste l'écran principal de comptoir. `repair.order` sert de moteur technique.

### `sav_magasin_knowledge`

Rôle : intégrer une base de procédures et FAQ métier directement dans Odoo Community.

Fonctions ajoutées :

- procédures métier ;
- étapes de procédure ;
- FAQ métier ;
- menus `Re-Watt ERP > Knowledge métier` ;
- smart button `Procédures` sur le dossier SAV ;
- procédures par statut SAV et profil utilisateur.

## Données de démonstration

Le module `sav_magasin_demo` ajoute maintenant un scénario de présentation direction et renseigne certains dossiers avec un produit Odoo à réparer.

## Limites volontaires

- Le module ne synchronise pas encore automatiquement les lignes composants batterie avec les lignes techniques de `repair.order`.
- La consommation de stock reste encore une décision métier tracée, pas un vrai `stock.move` automatique.
- Les commandes fournisseurs réelles depuis ligne composant batterie restent prévues pour la suite.

## Suite recommandée

v0.6.0 : relier les décisions de stock aux vrais objets Odoo : `stock.picking`, `stock.move`, `purchase.order`.
