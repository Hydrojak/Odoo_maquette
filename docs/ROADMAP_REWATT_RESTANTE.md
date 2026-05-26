# Roadmap Re-Watt ERP restante après v1.1.0

## État atteint

- v0.8.x : pivot batterie < 60 V, modèles batterie, contrainte serveur tension maximale < 60 V.
- v0.9.0 : checklist qualité batterie, Pass/Fail/N.A., seuils, progression et verrouillage.
- v1.0.0 : diagnostics batterie et non-conformités, blocage si diagnostic critique ouvert.
- v1.1.0 : sessions de tests charge/décharge, mesures techniques, seuils et lien PDF.

## v1.2.0 — Rapport PDF technicien batterie auditable

Objectif : rendre le PDF complet, contrôlé et utilisable comme preuve qualité.

À faire :

- distinguer PDF brouillon et PDF final ;
- interdire le PDF final sans checklist verrouillée ;
- ajouter filigrane brouillon ;
- intégrer les sessions de tests validées ;
- intégrer diagnostics, actions correctives et preuves ;
- ajouter horodatage, technicien, responsable qualité ;
- préparer une logique de révision si modification après validation.

## v1.3.0 — Stock composants batterie

Objectif : adapter le stock aux composants réels de l’atelier batterie.

À faire :

- catégories composants : cellules lithium, BMS, nickel, Kapton, papier isolant, connecteurs, câbles, fusibles, gaine thermo, chargeurs, supports cellules ;
- réservation de composants sur dossier batterie ;
- consommation réelle via Odoo Stock ;
- suivi lots cellules / BMS ;
- seuils minimum ;
- kits par modèle batterie ;
- réception stock et traçabilité lot.

## v1.4.0 — Dashboard atelier batterie

Objectif : pilotage opérationnel direction / manager.

KPI :

- batteries reçues ;
- batteries en diagnostic ;
- batteries en réparation ;
- batteries en test ;
- batteries validées ;
- batteries bloquées ;
- durée moyenne de réparation ;
- taux de non-conformité ;
- taux de Fail par contrôle ;
- diagnostics ouverts ;
- PDF générés ;
- stock critique.

## v1.5.0 — Révision qualité et verrouillage documentaire

Objectif : rendre les validations auditables.

À faire :

- verrouillage des checklists validées ;
- procédure de révision avec motif ;
- conservation ancienne version ;
- journal qualité ;
- gestion version notice / checklist / PDF.

## v1.6.0 — Imports et mesures instrumentées

Objectif : préparer l’import de fichiers de mesure.

À faire :

- import CSV sessions de tests ;
- mapping colonnes ;
- pièces jointes fichier brut ;
- premières courbes charge/décharge ;
- contrôle cohérence des unités.

## v1.7.0 — Code-barres / QR code atelier

Objectif : réduire les erreurs de saisie.

À faire :

- QR code dossier batterie ;
- étiquette batterie ;
- scan commande ;
- scan composant / lot ;
- lien direct vers checklist ou session de test.

## v2.0.0 — Version atelier bêta

Critères :

- workflow batterie complet ;
- checklists et diagnostics robustes ;
- tests charge/décharge intégrés ;
- PDF final auditable ;
- stock composants exploitable ;
- dashboard direction ;
- données de démo propres ;
- documentation utilisateur et technique à jour.
