# Roadmap Re-Watt ERP

## v0.8.0 — Battery Foundation

Objectif : pivoter le projet vers un ERP atelier batterie < 60 V.

Livré : champs batterie, tension nominale, tension maximale, capacité, chimie, architecture S/P, BMS, connectique, chargeur, contrainte serveur < 60 V, menu Réparation batteries, première checklist et squelette de rapport.

## v0.9.0 — Checklist qualité batterie

Objectif : rendre la checklist qualité réellement exploitable en atelier.

Livré : phases qualité, contrôles obligatoires, mesures chiffrées, unités, seuils, calcul automatique Pass/Fail, preuves photo, validation bloquante, progression fiable et verrouillage.

## v1.0.0 — Diagnostic batterie et non-conformités

Objectif : créer un vrai suivi des anomalies.

À faire : modèle `sav.battery.diagnostic`, création automatique depuis Fail, sévérité, cause, action corrective, responsable, état, photos et blocage validation si diagnostic critique ouvert.

## v1.1.0 — Tests charge/décharge

Objectif : stocker les mesures techniques batterie.

À faire : sessions de test, mesures charge/décharge/BMS/capacité/équilibrage, pièces jointes et préparation import CSV.

## v1.2.0 — Rapport PDF technicien batterie

Objectif : rapport complet, auditable et verrouillé.

À faire : PDF final interdit avant validation, brouillon filigrané, verrouillage checklist, révisions et version notice.

## v1.3.0 — Stock composants batterie

Objectif : adapter le stock aux composants batterie.

À faire : cellules, BMS, nickel, Kapton, papier isolant, connecteurs, câbles, fusibles, chargeurs, lots et traçabilité.

## v1.4.0 — Dashboard atelier batterie

Objectif : supervision atelier.

À faire : KPI batteries reçues, en diagnostic, en réparation, en test, validées, bloquées, durée moyenne, taux Fail, diagnostics ouverts, PDF générés, stock critique.
