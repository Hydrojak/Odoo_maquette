# Architecture fonctionnelle

## Modules Odoo standards utilisés

- `contacts` : clients particuliers et professionnels
- `product` : articles, pièces, services
- `stock` : stock local, stock distant, mouvements, emplacements
- `purchase` : commandes fournisseurs
- `sale_management` : devis / commandes client
- `account` : facturation
- `mail` : chatter, notes, suivi

## Modules custom

```text
sav_magasin_product
sav_magasin_partner
sav_magasin_core
sav_magasin_stock
sav_magasin_purchase
sav_magasin_dashboard
```

## Flux cible

```text
Client arrive
  ↓
Recherche ou création client
  ↓
Création dossier SAV
  ↓
Dépôt produit + symptôme + état visuel
  ↓
Diagnostic
  ↓
Besoin pièce ?
  ├─ Non → réparation → facturation → restitution
  └─ Oui → stock local ?
         ├─ Oui → réservation / sortie pièce
         ├─ Non, stock distant → transfert
         └─ Non disponible → commande fournisseur
```

## Règles UX

- Pas plus de 12 champs visibles sur l'écran de dépôt.
- Bouton principal clair à chaque étape.
- Statut visible en permanence.
- Recherche rapide : client, téléphone, email, numéro dossier, numéro de série, référence article.
- Les actions stock/achat doivent être guidées, pas laissées à l'utilisateur dans les menus standards.
