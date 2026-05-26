# Changelog v1.1.0 — Tests charge/décharge batterie

## Ajouté

- Modèle `sav.battery.test.session`.
- Modèle `sav.battery.test.measurement`.
- Types de tests : charge, décharge, BMS, capacité, équilibrage.
- Mesures : tension départ, tension fin, courant, capacité Ah, température BMS, delta cellules.
- Seuils par mesure : tension max, température max, delta max, capacité minimale.
- Calcul automatique conforme / non conforme.
- Création de diagnostics batterie depuis les mesures non conformes.
- Smart button Tests batterie sur le dossier batterie.
- Menu Tests charge/décharge et Tests non conformes.
- Section Tests charge/décharge dans le rapport technicien.
- Données de démonstration avec une session de décharge non conforme.

## Limites

- Pas encore d’import CSV.
- Pas encore de courbe charge/décharge.
- Pas encore de verrouillage PDF final.
