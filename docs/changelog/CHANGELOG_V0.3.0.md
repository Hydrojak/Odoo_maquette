# Re-Watt ERP v0.3.0 — Dossier batterie exploitable

## Objectif

Cette version transforme la maquette en une base métier plus démontrable : le dossier SAV affiche une prochaine action, un point bloquant, des dates de progression et deux documents PDF opérationnels.

## Nouveautés

- Fiche dossier SAV enrichie : contact client, indicateurs, prochaine action, point bloquant.
- Workflow renforcé avec contrôles de statut côté serveur.
- Dates automatiques : validation dépôt, diagnostic, début réparation, prêt à restituer, restitution, clôture.
- Bon de dépôt PDF plus complet et présentable.
- Bon de restitution PDF basique.
- Assistant de création rapide avec deux sorties : ouvrir le dossier ou imprimer le bon de dépôt.
- Lignes composants batterie enrichies avec statut : à vérifier, réservée, consommée, annulée.
- Stock ergonomique enrichi : stock local, distant, total, décision stock et note de décision.
- Données de démonstration compatibles avec la fiche enrichie.

## Parcours de démonstration conseillé

1. Aller dans `Re-Watt ERP → Atelier batteries → Dossiers batteries`.
2. Ouvrir `SAV-DEMO-001` et cliquer sur `Lancer diagnostic`.
3. Ouvrir `SAV-DEMO-003` pour montrer le point bloquant `Attente composant batterie`.
4. Ouvrir `SAV-DEMO-004`, imprimer le bon de restitution ou passer en `Restitué`.
5. Utiliser `Re-Watt ERP → Atelier batteries → Nouveau dossier` pour créer un dossier en direct.
6. Cliquer sur `Valider et imprimer` pour générer le bon de dépôt.

## Limites connues

- La réservation de composant batterie reste métier : elle ne crée pas encore un mouvement stock réel.
- La commande fournisseur depuis le dossier SAV n’est pas encore automatisée.
- La facturation n’est pas encore générée automatiquement depuis le dossier.
- Les transferts inter-stock réels seront traités dans une version suivante.
