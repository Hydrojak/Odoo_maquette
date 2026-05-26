# Architecture

## Objectif architectural

Le projet sépare le moteur ERP standard Odoo de la couche métier Re-Watt ERP.

```text
Odoo standard
├── Contacts
├── Produits
├── Stock
├── Achats
├── Repair
├── Vente / Facturation future
└── Mail / Chatter

Modules Re-Watt ERP
├── Dossier batterie
├── Assistant comptoir
├── Référentiel métier
├── Composants batterie et stock visible depuis le dossier
├── Substitutions articles
├── Liaison Repair
├── Knowledge métier
└── Pilotage opérationnel
```

## Flux fonctionnel cible

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
Besoin composant batterie ?
  ├─ Non → réparation → restitution
  └─ Oui → stock local ?
         ├─ Oui → réservation métier / consommation
         ├─ Non, stock distant → demande de transfert
         ├─ Non disponible → commande fournisseur à prévoir
         └─ Substitut disponible → proposition de substitution
```

## Rôle du dossier SAV

Le modèle `sav.magasin.order` est le centre fonctionnel. Il regroupe :

- client ;
- batterie ;
- symptôme ;
- état visuel ;
- statut ;
- composants batterie ;
- décision stock ;
- ordre de réparation lié ;
- procédures métier ;
- documents.

## Rôle de Repair

Le module `repair` Odoo est utilisé comme moteur technique optionnel. Il ne remplace pas le dossier atelier batterie.

```text
Dossier atelier batterie
  ↓ bouton Créer ordre réparation
repair.order Odoo
```

## Rôle du Knowledge métier

Le module `sav_magasin_knowledge` documente les procédures directement dans Odoo Community :

- procédures ;
- étapes ;
- FAQ ;
- aide par statut ;
- aide par profil utilisateur.

## Limites de la version actuelle

Les actions suivantes sont encore métier / démonstration et ne créent pas encore tous les objets techniques Odoo :

- transfert stock réel ;
- sortie physique de stock ;
- commande fournisseur réelle depuis une ligne composant batterie ;
- synchronisation complète des composants batterie avec `repair.order` ;
- facturation automatique depuis dossier SAV.
