# Re-Watt ERP

Gestion atelier de réparation de batteries strictement inférieures à 60 V, basée sur Odoo Community.

## Objectif

Ce projet pivote l’ancien socle SAV Magasin vers un ERP vertical atelier batterie :

- dossiers batteries ;
- clients ;
- composants batterie ;
- stock Odoo ;
- achats fournisseurs ;
- réparation Odoo ;
- checklists qualité ;
- contraintes < 60 V ;
- rapport technicien batterie.

## Version

```text
v1.1.0-tests-batterie
```

## Lancement Docker

```bash
docker compose up -d
```

Puis ouvrir :

```text
http://localhost:8069
```

## Installation dans Odoo

1. Créer une base Odoo.
2. Aller dans Apps.
3. Mettre à jour la liste des apps.
4. Installer `Re-Watt ERP - Application principale`.
5. Installer `Re-Watt ERP - Données de démonstration`, si besoin.

En ligne de commande :

```bash
./scripts/install-v110.sh NOM_DE_TA_BASE
```

## Module principal du pivot batterie

```text
sav_battery_quality
```

Ce module ajoute :

- `sav.battery.model`
- `sav.battery.checklist.template`
- `sav.battery.checklist.template.line`
- `sav.battery.checklist`
- `sav.battery.checklist.line`

Il étend aussi le modèle existant :

```text
sav.magasin.order
```

## Règle métier centrale

Une batterie du workflow standard doit avoir :

```text
tension maximale < 60 V
```

Cette règle est contrôlée côté serveur Odoo par contrainte Python.  
Une batterie avec tension maximale `>= 60 V` est refusée dans le workflow standard.

## Menus principaux

```text
Re-Watt ERP
→ Réparation batteries
   → Dossiers batteries
   → Checklists qualité
   → Diagnostics batterie
   → Diagnostics critiques ouverts
   → Batteries bloquées
→ Stock / Composants
→ Achats / Réceptions
→ Knowledge métier
→ Référentiel
   → Référentiel batterie
      → Modèles batteries
      → Modèles checklists
```

## Documentation

- `docs/AUDIT_REWATT_PIVOT_V0.8.0.md`
- `docs/ROADMAP_REWATT.md`
- `docs/CHANGELOG_V0.8.0.md`
- `docs/VERIFICATION_V0.8.0.md`
- `docs/CHANGELOG_V1.1.0.md`
- `docs/VERIFICATION_V1.1.0.md`
- `docs/ROADMAP_REWATT_RESTANTE.md`


## Correctif v0.9.0

Correction du jeu de données de démonstration : la valeur d'impact garantie `different` a été remplacée par `confirm`, valeur acceptée par le champ `warranty_impact`.

## Version v1.1.0

La v1.1.0 ajoute les sessions de tests charge/décharge, les mesures techniques batterie, les seuils de conformité, la création de diagnostics depuis les mesures non conformes et l’intégration des tests dans le rapport technicien.
