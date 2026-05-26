# Re-Watt ERP v1.0.0 — Diagnostics batterie et non-conformités

## Objectif

Créer un suivi exploitable des anomalies qualité batterie, lié aux checklists et aux dossiers atelier.

## Ajouts

- Nouveau modèle `sav.battery.diagnostic`.
- Diagnostics liés à :
  - dossier batterie ;
  - checklist ;
  - ligne de contrôle non conforme.
- Gravité : mineur, majeur, critique.
- États : ouvert, en traitement, résolu, rejeté, clôturé.
- Causes : mesure hors seuil, défaut visuel, assemblage, isolement, BMS, charge/décharge, documentation, autre.
- Preuves / photos sur le diagnostic.
- Action corrective et note de résolution.
- Création ou mise à jour automatique d’un diagnostic quand une ligne de checklist est `Non conforme`.
- Blocage de la validation batterie si un diagnostic critique reste ouvert.
- Smart button `Diagnostics ouverts` sur le dossier batterie.
- Menus :
  - `Diagnostics batterie` ;
  - `Diagnostics critiques ouverts`.
- Rapport technicien enrichi avec les diagnostics et non-conformités.
- Données de démonstration enrichies avec un diagnostic critique ouvert.

## Règles métier

- Un contrôle `Fail / Non conforme` crée ou lie un diagnostic.
- Un diagnostic critique ouvert empêche la validation finale de la batterie.
- Un diagnostic ne peut être marqué résolu sans action corrective.
- Un diagnostic ne peut être clôturé que s’il est résolu ou rejeté.
- L’historique reste tracé via le chatter Odoo.

## Limites

- Les droits fins responsable qualité restent à renforcer dans une version ultérieure.
- La révision verrouillée de checklist après modification post-validation reste prévue pour v1.2.
- Les tests charge/décharge structurés restent prévus pour v1.1.
