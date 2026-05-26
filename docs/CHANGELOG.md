## v1.1.0 — Tests charge/décharge batterie

- Ajout des sessions de tests batterie.
- Ajout des mesures techniques : tension, courant, capacité, température BMS, delta cellules.
- Calcul automatique conforme / non conforme.
- Création de diagnostics depuis les mesures non conformes.
- Intégration des tests dans le rapport technicien.


## v1.0.0 — Diagnostics batterie et non-conformités

- Ajout du modèle `sav.battery.diagnostic`.
- Création / liaison automatique d’un diagnostic quand un contrôle checklist est non conforme.
- Blocage de la validation batterie en présence d’un diagnostic critique ouvert.
- Menus Diagnostics batterie et Diagnostics critiques ouverts.
- Rapport technicien enrichi avec les diagnostics.

# Changelog

## v0.5.1-docs

Version de nettoyage documentaire.

Ajouts :

- README réécrit ;
- index documentaire ;
- documentation installation ;
- documentation configuration ;
- documentation commandes ;
- rapport modules ;
- rapport origine standard/custom ;
- documentation processus métier ;
- documentation démo direction ;
- documentation développeur ;
- FAQ dépannage ;
- roadmap remise à jour ;
- anciens fichiers de correction déplacés dans `docs/archive/` ;
- anciens changelogs déplacés dans `docs/changelog/`.

Aucun changement métier majeur n’est introduit dans le code.

## v0.5.0 — Repair & Knowledge métier

- ajout du module `sav_magasin_repair` ;
- lien dossier SAV ↔ ordre de réparation batterie Odoo ;
- ajout du module `sav_magasin_knowledge` ;
- procédures et FAQ métier ;
- données de démonstration enrichies.

## v0.4.0 — Stock & substitutions

- lignes composants batterie enrichies ;
- décisions stock ;
- substitutions articles ;
- suggestion de substitut ;
- menus Stock / Composants batterie.

## v0.3.0 — SAV Core exploitable

- workflow enrichi ;
- bons PDF ;
- prochain action / point bloquant ;
- assistant nouveau dossier amélioré.

## v0.2.x — Base Re-Watt ERP

- renommage du projet ;
- corrections menus/droits ;
- données de démonstration initiales.

## v0.6.2 — Correction XML data Odoo

Correction du format des fichiers XML de données rejetés par le validateur Odoo.

## v0.6.4 - Correction XPath Odoo 19

- Correction des vues héritées qui utilisaient `@string` comme sélecteur XPath.
- Ajout d'attributs `name` stables sur les pages principales du formulaire dossier SAV.
- Fichiers concernés : `sav_magasin_purchase/views/purchase_link_views.xml`, `sav_magasin_repair/views/sav_order_repair_views.xml`, `sav_magasin_core/views/sav_order_views.xml`.

## v0.7.0 — Flux stock réels

- Ajout du module `sav_magasin_stock_flow`.
- Création de `stock.picking` et `stock.move` depuis les lignes composants batterie SAV.
- Réservation métier maintenant liée à un flux stock Odoo.
- Demande de transfert distante transformée en transfert interne Odoo.
- Réception sans commande enrichie avec une réception stock Odoo.
- Ajout d'un menu `Re-Watt ERP → Stock / Composants batterie → Flux stock SAV`.
- Ajout d'un bouton de synchronisation statut stock sur les lignes composants batterie.

## v0.9.0 — Checklist qualité batterie

- Renforcement de la checklist qualité batterie.
- Ajout de champs de mesure, seuils actifs, unités et verdicts.
- Calcul automatique Pass/Fail pour les mesures chiffrées.
- Blocage de validation si contrôles obligatoires incomplets.
- Commentaire obligatoire pour tout Fail.
- Preuve/photo obligatoire pour Fail critique.
- Rapport technicien marqué brouillon si aucune checklist validée.
