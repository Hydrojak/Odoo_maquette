# Changelog v0.8.1 — Correction Knowledge FAQ

## Correction

- Ajout des catégories `diagnostic`, `substitution` et `return` dans le modèle `sav.magasin.faq`.
- Correction de l’erreur d’installation : `Wrong value for sav.magasin.faq.category: 'diagnostic'`.
- Conservation du pivot Re-Watt ERP v0.8.0 : atelier batterie < 60 V, module `sav_battery_quality`, checklist qualité et rapport technicien.

## Impact

La correction évite le crash du `post_init_hook` de `sav_magasin_knowledge` lors de l’installation de l’application principale.
