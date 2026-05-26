# Données de démonstration

Le module optionnel `sav_magasin_demo` ajoute une base de présentation pour démontrer la maquette.

## Installation

```bash
./scripts/install-demo-data.sh NOM_BASE
```

Ou depuis Odoo :

```text
Apps → Re-Watt ERP - Données de démonstration → Installer
```

## Contenu attendu

Le module ajoute des données simples pour illustrer :

- clients particuliers ;
- client professionnel ;
- fournisseur ;
- marques ;
- gammes ;
- modèles ;
- types articles ;
- articles / composants batterie ;
- dossiers SAV ;
- lignes composants batterie ;
- substitutions ;
- procédures métier ;
- FAQ.

## Cas démontrables

| Cas | Ce qu’il montre |
|---|---|
| Dossier dépôt validé | Création et suivi initial |
| Dossier diagnostic | Passage en traitement technique |
| Dossier attente composant batterie | Cas critique stock |
| Dossier prêt à restituer | Fin de parcours magasin |
| Substitution article | Proposition de composant batterie alternative |
| Knowledge métier | Procédures intégrées au logiciel |
| Repair lié | Connexion au module Repair Odoo |

## Recommandation

Ces données sont prévues pour une démonstration. Ne pas les utiliser comme données de production.
