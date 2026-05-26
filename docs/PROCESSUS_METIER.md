# Processus métier couverts

## 1. Création d’un dossier SAV

```text
Re-Watt ERP → Atelier batteries → Nouveau dossier
```

Étapes :

1. rechercher ou créer un client ;
2. renseigner le batterie ;
3. préciser marque, gamme, modèle si disponibles ;
4. saisir le symptôme client ;
5. saisir les accessoires déposés ;
6. saisir l’état visuel ;
7. valider et ouvrir le dossier ou valider et imprimer le bon de dépôt.

Contrôles principaux :

- client obligatoire ;
- téléphone ou email obligatoire ;
- batterie obligatoire ;
- symptôme obligatoire ;
- état visuel obligatoire ;
- magasin obligatoire.

## 2. Suivi du dossier SAV

Statuts principaux :

```text
Brouillon → Dépôt validé → Diagnostic → Attente client / Attente composant batterie → Réparation → Prêt à restituer → Restitué → Clôturé
```

Le dossier affiche :

- prochaine action ;
- point bloquant ;
- dates de progression ;
- technicien ;
- composants batterie ;
- documents.

## 3. Gestion des composants batterie

Une ligne composant batterie contient :

- article ;
- quantité ;
- stock local ;
- stock distant ;
- stock total ;
- action recommandée ;
- statut ligne.

Actions disponibles :

```text
Vérifier stock
Réserver
Demander transfert
Prévoir commande
Consommer
Annuler réservation
```

Dans la version actuelle, ces actions tracent la décision métier. La génération de mouvements Odoo réels est prévue en v0.6.0.

## 4. Substitution article

Si la composant batterie d’origine est indisponible, le module de substitution peut proposer un article alternatif.

Critères gérés :

- type de substitution ;
- état de validation ;
- priorité ;
- impact prix ;
- impact garantie ;
- note technique.

Décision possible :

```text
Utiliser substitut
```

## 5. Réparation batterie Odoo

Depuis le dossier SAV, un ordre de réparation batterie Odoo peut être créé.

But : séparer :

- le dossier magasin : accueil, dépôt, suivi client, restitution ;
- l’ordre de réparation : traitement technique.

## 6. Knowledge métier

Les procédures permettent de guider les utilisateurs selon les cas :

- création dossier ;
- diagnostic ;
- attente composant batterie ;
- substitution ;
- réception sans commande ;
- restitution client.

## 7. Réception sans commande

Le module achat prépare une réception rapide avec :

- fournisseur ;
- numéro BL ;
- numéro facture ;
- magasin ;
- lignes articles ;
- rattachement éventuel à un dossier SAV.

Cette partie reste à renforcer pour générer les flux stock complets.
