# Origine des modules

## Synthèse

| Origine | Présence | Détail |
|---|---:|---|
| Odoo standard / Community | Oui | `contacts`, `product`, `stock`, `purchase`, `sale_management`, `account`, `repair`, `mail` |
| Modules communautaires tiers / OCA | Non | Aucun module OCA embarqué dans cette version |
| Modules custom projet | Oui | Tous les modules `sav_magasin_*` |
| Images Docker externes | Oui | `odoo:${ODOO_VERSION}`, `postgres:${POSTGRES_VERSION}` |

## Odoo standard

Ces modules ne sont pas développés dans le projet. Ils sont fournis par Odoo et utilisés comme socle ERP.

| Module | Rôle |
|---|---|
| `contacts` | Fiches clients, sociétés, adresses |
| `product` | Articles, composants batterie, prestations |
| `stock` | Entrepôts, emplacements, quantités |
| `purchase` | Fournisseurs, achats, réceptions standards |
| `sale_management` | Devis et ventes futures |
| `account` | Facturation future |
| `repair` | Ordres de réparation techniques |
| `mail` | Historique, chatter, activités |

## Modules custom développés pour la maquette

| Module | Justification |
|---|---|
| `sav_magasin_core` | Besoin métier spécifique : dépôt, diagnostic, attente composant batterie, restitution |
| `sav_magasin_stock` | Lecture stock directement dans le dossier SAV |
| `sav_magasin_substitution` | Substituts validés métier et impact garantie/prix |
| `sav_magasin_repair` | Liaison contrôlée avec Repair sans remplacer le dossier SAV |
| `sav_magasin_knowledge` | Base de procédures interne compatible Community |
| `sav_magasin_purchase` | Réception sans commande orientée SAV |
| `sav_magasin_dashboard` | Vues opérationnelles adaptées magasin |
| `sav_magasin_demo` | Données pour démonstration direction |

## Positionnement

La stratégie projet est :

```text
Odoo standard pour le moteur ERP
+ modules custom pour l’expérience métier atelier batterie
+ modules communautaires éventuels uniquement après évaluation
```

Aucun module communautaire n’est intégré pour l’instant afin de garder la maquette maîtrisée et facile à déployer.
