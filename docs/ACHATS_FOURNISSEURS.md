# Achats fournisseurs SAV

La v0.6.0 introduit une première liaison entre les besoins de composants batterie du SAV et le module standard Odoo Purchase.

## Principe

Une ligne composant batterie SAV peut être dans l'état `Commande à prévoir`. L'utilisateur peut alors créer une commande fournisseur depuis cette ligne.

```text
Dossier batterie
→ Ligne composant batterie
→ Fournisseur
→ Créer commande fournisseur
→ Purchase Order Odoo
```

## Champs ajoutés aux lignes composants batterie

| Champ | Rôle |
|---|---|
| Fournisseur | Fournisseur utilisé pour commander la composant batterie |
| Réception prévue | Date attendue de réception |
| Commande fournisseur | Commande Odoo créée depuis la ligne |
| Ligne commande | Ligne de commande Odoo liée |
| Statut achat | Statut de la commande fournisseur |
| Note achat | Commentaire opérationnel |

## Boutons utilisateur

| Bouton | Effet |
|---|---|
| Créer commande fournisseur | Crée une demande de prix Odoo liée au dossier SAV |
| Ouvrir commande | Ouvre la commande fournisseur liée |
| Marquer reçue | Marque la ligne composant batterie comme reçue côté SAV |

## Réception sans commande

La réception sans commande permet de rattacher une ligne de réception à une ligne composant batterie SAV. Lors de la validation, la ligne composant batterie est marquée comme reçue.

Cette fonction reste volontairement métier : elle trace la réception dans le SAV, mais ne remplace pas encore entièrement les flux logistiques Odoo.

## Limites actuelles

- Les commandes créées sont en brouillon.
- Les réceptions ne créent pas encore automatiquement les mouvements de stock Odoo.
- Les écarts quantité/prix seront traités dans une version ultérieure.
