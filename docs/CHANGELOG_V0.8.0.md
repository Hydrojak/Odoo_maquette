# Changelog v0.8.0 — Battery Foundation

## Ajouté

- Nouveau module `sav_battery_quality`.
- Extension du dossier existant vers dossier batterie.
- Modèle batterie : tension nominale, tension maximale, capacité Ah, chimie, architecture S/P, BMS, connectique, chargeur.
- Contrainte serveur `< 60 V`.
- Statut calculé `Compatible < 60 V`.
- Étapes batterie.
- Modèles de checklists qualité batterie.
- Première checklist standard atelier.
- Rapport technicien batterie en squelette QWeb.
- Données de démonstration batteries.

## Conservé

- Modèle principal `sav.magasin.order`.
- Clients.
- Stock Odoo.
- Achats.
- Repair.
- Dashboard.
- Knowledge métier.
- Substitutions composants.

## Non fait volontairement

- Pas encore de diagnostic batterie complet.
- Pas encore de sessions charge/décharge structurées.
- Pas encore de PDF final verrouillé.
- Pas encore de traçabilité lots cellules/BMS complète.
