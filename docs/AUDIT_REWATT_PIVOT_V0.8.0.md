# Audit technique avant pivot Re-Watt ERP v0.8.0

## Source inspectée

Base inspectée : `odoo-sav-magasin-v0.7.0-stock-flux-reels`.

## Modules détectés

| Module | Origine | Rôle actuel | Décision pivot |
|---|---|---|---|
| `sav_magasin_app` | Custom | Application principale | Conservé, libellés interface orientés Re-Watt ERP |
| `sav_magasin_core` | Custom | Dossier principal `sav.magasin.order` | Conservé comme modèle principal de dossier batterie |
| `sav_magasin_stock` | Custom | Lignes composants et disponibilité | Conservé pour composants batterie |
| `sav_magasin_stock_flow` | Custom | Liens vers `stock.picking` / `stock.move` | Conservé pour flux stock réels |
| `sav_magasin_purchase` | Custom | Achats et réception sans commande | Conservé pour composants batterie |
| `sav_magasin_repair` | Custom | Liaison vers `repair.order` | Conservé comme moteur réparation Odoo |
| `sav_magasin_product` | Custom | Référentiel marques/gammes/modèles/types | Conservé, utilisable pour modèles batteries/composants |
| `sav_magasin_partner` | Custom | Clients B2C/B2B | Conservé |
| `sav_magasin_substitution` | Custom | Substitutions articles | Conservé pour composants batterie substituables |
| `sav_magasin_knowledge` | Custom | Procédures métier | Conservé et réorienté atelier batterie |
| `sav_magasin_dashboard` | Custom | Pilotage opérationnel | Conservé |
| `sav_magasin_demo` | Custom | Données de démonstration | Réécrit en démo batterie |

## Modèle principal identifié

Le modèle central reste :

```text
sav.magasin.order
```

Il porte déjà le dossier opérationnel, les statuts, le client, le magasin, les composants, les dates, les notes, les rapports et les liens avec vente/facturation/réparation.  
Le pivot v0.8.0 l’étend au lieu de créer un modèle parallèle, afin de ne pas casser les modules stock, achat, repair et dashboard.

## Dépendances Odoo conservées

- `contacts`
- `product`
- `stock`
- `purchase`
- `sale_management`
- `account`
- `repair`
- `mail`

## Vues et rapports existants identifiés

- Formulaire, liste, kanban et recherche du dossier `sav.magasin.order`
- Assistant de création rapide
- Rapports dépôt/restitution
- Vues composants/stock
- Vues achats/réception
- Vues repair
- Vues knowledge
- Vues dashboard

## Changement effectué en v0.8.0

Nouveau module ajouté :

```text
sav_battery_quality
```

Objectif : ajouter la couche métier batterie sans renommer techniquement tous les modules.

## Points volontairement non réécrits

- Les noms techniques `sav_magasin_*` sont conservés.
- Le modèle principal `sav.magasin.order` est conservé.
- Les flux stock et achat existants sont conservés.
- Le lien vers `repair.order` est conservé.

Cette approche correspond à une migration incrémentale, moins risquée qu’une réécriture complète.
