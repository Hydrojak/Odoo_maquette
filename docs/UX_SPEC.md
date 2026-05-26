# Spécification UX — Re-Watt ERP

## Principes

1. Le dossier SAV est l’écran central.
2. Le comptoir doit pouvoir créer un dossier rapidement.
3. Les écrans techniques Odoo doivent rester en arrière-plan.
4. Chaque statut doit suggérer l’action suivante.
5. Les décisions stock doivent être visibles dans le dossier, sans obliger l’utilisateur à naviguer dans Inventory.
6. Les procédures métier doivent être accessibles depuis l’écran de travail.

## Écran — Nouveau dossier batterie

Objectif : créer un dossier en moins d’une minute.

Champs essentiels :

- client existant ou client à créer ;
- type client ;
- téléphone ou email ;
- batterie ;
- marque / gamme / modèle ;
- numéro de série ;
- garantie ;
- symptôme ;
- accessoires ;
- état visuel ;
- magasin ;
- technicien.

Actions :

```text
Valider et ouvrir
Valider et imprimer
Annuler
```

## Écran — Dossier batterie

Sections recommandées :

- en-tête avec statut et boutons ;
- résumé client ;
- batterie ;
- symptôme et état visuel ;
- diagnostic ;
- composants batterie / stock ;
- documents ;
- historique.

Indicateurs importants :

- prochaine action ;
- point bloquant ;
- nombre de jours depuis dépôt ;
- montant estimé ;
- statut de la réparation liée.

## Écran — Ligne composant batterie

Informations critiques :

- article ;
- quantité ;
- stock local ;
- stock distant ;
- source distante ;
- action recommandée ;
- substitut proposé ;
- note de décision.

Actions :

```text
Vérifier stock
Réserver
Transfert
Commander
Consommer
Utiliser substitut
```

## Écran — Knowledge métier

But : guider les utilisateurs sans sortir d’Odoo.

Contenu :

- procédures ;
- étapes ;
- FAQ ;
- profils concernés ;
- statut SAV associé.

## Écran — Démo direction

La démonstration doit montrer peu d’écrans, mais bien choisis :

1. Accueil atelier ;
2. Nouveau dossier ;
3. dossier en attente composant batterie ;
4. ligne composant batterie avec stock/substitution ;
5. ordre Repair lié ;
6. procédure métier.
