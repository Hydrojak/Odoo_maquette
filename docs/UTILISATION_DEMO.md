# Utilisation démonstration direction

## Objectif

Montrer que la maquette couvre un parcours atelier batterie cohérent :

```text
client → dossier SAV → diagnostic → composant batterie → stock/substitution → réparation → restitution
```

## Préparer la démo

1. Lancer Odoo.
2. Installer `Re-Watt ERP - Application principale`.
3. Installer `Re-Watt ERP - Données de démonstration`.
4. Ouvrir le menu `Re-Watt ERP`.

## Parcours conseillé — 10 minutes

### 1. Montrer l’accueil SAV

Menu :

```text
Re-Watt ERP → Accueil atelier
```

Montrer :

- dossiers en cours ;
- statuts ;
- vue Kanban / liste ;
- prochaine action.

### 2. Créer un dossier en direct

Menu :

```text
Re-Watt ERP → Atelier batteries → Nouveau dossier
```

Saisir rapidement :

- client ;
- batterie ;
- symptôme ;
- état visuel ;
- magasin.

Puis cliquer :

```text
Valider et imprimer
```

Montrer le bon de dépôt.

### 3. Montrer un dossier en attente composant batterie

Ouvrir un dossier de démo en statut attente composant batterie.

Montrer :

- point bloquant ;
- prochaine action ;
- lignes composants batterie ;
- stock local/distant ;
- action recommandée.

### 4. Montrer une substitution

Dans une ligne composant batterie :

- afficher le substitut proposé ;
- montrer le niveau de validation ;
- expliquer l’impact métier : délai réduit, stock mieux utilisé, validation responsable si nécessaire.

### 5. Montrer la liaison Repair

Depuis un dossier :

```text
Créer ordre réparation
```

Puis ouvrir le smart button ou menu :

```text
Atelier batteries → Réparations batterie Odoo
```

Message à faire passer : le dossier SAV reste l’écran magasin, Repair sert de moteur technique.

### 6. Montrer Knowledge métier

Menu :

```text
Re-Watt ERP → Knowledge métier → Procédures
```

Montrer :

- procédure création dossier ;
- procédure attente composant batterie ;
- FAQ.

## Messages clés pour la direction

- L’outil est organisé autour du parcours réel du magasin.
- Odoo standard est utilisé pour le socle ERP.
- Les modules custom portent uniquement l’expérience métier spécifique.
- Les données de démo permettent de visualiser rapidement les cas critiques.
- La prochaine étape est de connecter les décisions stock aux objets Odoo réels.

## Limites à annoncer clairement

- La maquette n’est pas encore une production.
- Les mouvements stock réels et commandes fournisseurs automatiques sont prévus en v0.6.0.
- La facturation complète est prévue après stabilisation du flux composants batterie/stock.


## Démo v0.6.0 — Achat fournisseur

1. Ouvrir `SAV-DEMO-003`.
2. Ouvrir la ligne composant batterie en attente.
3. Cliquer sur `Créer commande fournisseur`.
4. Ouvrir le smart button `Achats`.
5. Montrer la réception sans commande liée à la ligne composant batterie.
