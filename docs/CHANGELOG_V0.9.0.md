# Changelog v0.9.0 — Checklist qualité batterie

## Objectif

Renforcer le workflow qualité batterie Re-Watt autour d'une checklist exploitable en atelier : phases, mesures, seuils, verdicts, preuves et validation.

## Ajouts fonctionnels

- Modèle de checklist batterie enrichi.
- Lignes de checklist avec :
  - phase ;
  - critère attendu ;
  - instruction atelier ;
  - type de mesure ;
  - valeur mesurée ;
  - unité ;
  - seuil minimum actif ;
  - seuil maximum actif ;
  - verdict ;
  - commentaire ;
  - preuve/photo ;
  - caractère obligatoire ;
  - caractère bloquant.
- Progression calculée sur les contrôles obligatoires complétés.
- Calcul automatique Pass/Fail pour les mesures chiffrées.
- Blocage de validation si :
  - un contrôle obligatoire est incomplet ;
  - un Fail n'a pas de commentaire ;
  - un Fail critique n'a pas de preuve/photo.
- Indicateurs : conformes, non conformes, N/A, en attente, non-conformités bloquantes, preuves critiques manquantes.
- Statut de checklist : brouillon, en cours, à corriger, validée, verrouillée, annulée.
- Réouverture possible avant verrouillage.
- Verrouillage de la checklist validée.
- Blocage de la validation batterie si aucune checklist validée/verrouillée n'est disponible.
- Rapport technicien marqué comme brouillon si aucune checklist validée n'est rattachée.

## Contrôles atelier standard

La checklist par défaut contient les phases :

1. Identification batterie
2. Diagnostic initial
3. Préparation cellules
4. Assemblage pack
5. Contrôle soudures / isolants
6. Contrôle BMS
7. Test charge
8. Test décharge
9. Validation finale

Contrôles principaux : tension maximale < 60 V, aspect visuel cellules, delta cellules ≤ 0,05 V, isolants, sens cellules, nickel, points de soudure, isolement Kapton/papier isolant, BMS, tensions connectique, équilibrage, température BMS.

## Limites

- Les diagnostics de non-conformité ne sont pas encore un modèle dédié complet. Ils sont prévus pour v1.0.0.
- Les tests charge/décharge structurés en sessions et mesures sont prévus pour v1.1.0.
- Le PDF final auditable avec révisions est prévu pour v1.2.0.
