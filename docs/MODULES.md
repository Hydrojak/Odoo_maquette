# Modules du projet

## Vue d’ensemble

Le projet s’appuie sur des modules Odoo standards et des modules custom `sav_magasin_*`.

## Module applicatif principal

### `sav_magasin_app`

Rôle : point d’entrée installable depuis Apps.

Il dépend des modules métier :

```text
sav_magasin_product
sav_magasin_partner
sav_magasin_core
sav_magasin_stock
sav_magasin_substitution
sav_magasin_repair
sav_magasin_knowledge
sav_magasin_purchase
sav_magasin_dashboard
```

## Modules métier custom

| Module | Responsabilité |
|---|---|
| `sav_magasin_core` | Dossier batterie, workflow, assistant nouveau dossier, documents PDF |
| `sav_magasin_product` | Référentiel articles : marques, gammes, modèles, types |
| `sav_magasin_partner` | Adaptation client magasin, type client, anti-doublon |
| `sav_magasin_stock` | Lignes composants batterie, stock local/distant, décisions stock |
| `sav_magasin_substitution` | Substitutions articles, compatibilités, proposition de substitut |
| `sav_magasin_repair` | Liaison dossier SAV avec `repair.order` standard Odoo |
| `sav_magasin_purchase` | Réception rapide / sans commande fournisseur |
| `sav_magasin_knowledge` | Procédures, étapes, FAQ métier |
| `sav_magasin_dashboard` | Vues de pilotage opérationnel |
| `sav_magasin_demo` | Données de démonstration |

## Modèles principaux

| Modèle | Module | Rôle |
|---|---|---|
| `sav.magasin.order` | `sav_magasin_core` | Dossier atelier batterie |
| `sav.magasin.part.line` | `sav_magasin_core` / `stock` / `substitution` | Composants batterie liées au dossier |
| `sav.magasin.create.wizard` | `sav_magasin_core` | Assistant nouveau dossier |
| `sav.magasin.product.brand` | `sav_magasin_product` | Marques |
| `sav.magasin.product.range` | `sav_magasin_product` | Gammes |
| `sav.magasin.device.model` | `sav_magasin_product` | Modèles appareils |
| `sav.magasin.article.type` | `sav_magasin_product` | Types articles |
| `sav.magasin.product.substitution` | `sav_magasin_substitution` | Substitutions articles |
| `sav.magasin.quick.receipt` | `sav_magasin_purchase` | Réception rapide fournisseur |
| `sav.magasin.procedure` | `sav_magasin_knowledge` | Procédure métier |
| `sav.magasin.faq` | `sav_magasin_knowledge` | FAQ métier |

## Modules Odoo standards utilisés

| Module Odoo | Usage dans le projet |
|---|---|
| `contacts` | Clients particuliers et professionnels |
| `product` | Articles, composants batterie, prestations |
| `stock` | Entrepôts, stocks, quantités |
| `purchase` | Fournisseurs et achats |
| `sale_management` | Base future devis / commandes client |
| `account` | Base future facturation |
| `repair` | Ordres de réparation techniques |
| `mail` | Chatter, notes, activités |

## Modules non inclus

Aucun module OCA / communautaire tiers n’est embarqué dans cette version. Le projet reste basé sur Odoo standard + modules custom.
