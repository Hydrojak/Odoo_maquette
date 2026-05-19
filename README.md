# SAV Magasin Odoo — socle SAV / magasin / stock

Projet Odoo Community prêt à lancer avec Docker Compose.

L'objectif du repo est de fournir une base propre pour reconstruire un logiciel métier de type SAV magasin : dossiers d'intervention, clients, produits déposés, pièces, stock local/distant, achats et réception sans commande.

## Stack

- Odoo Community, via l'image Docker officielle `odoo:${ODOO_VERSION}`
- PostgreSQL
- Addons custom montés dans `/mnt/extra-addons`
- Configuration Odoo dans `config/odoo.conf`

## Lancement rapide

```bash
cp .env.example .env
docker compose up -d
```

Puis ouvrir :

```text
http://localhost:8069
```

Créer une base Odoo depuis l'interface, puis installer les applications `SAV Magasin` depuis Apps.

## Modules custom inclus

| Module | Rôle |
|---|---|
| `sav_magasin_product` | Référentiel articles : marque, gamme, modèle, type article, statut de complétude |
| `sav_magasin_partner` | Adaptation client magasin : particulier, professionnel, client livré/facturé, contrôle anti-doublon |
| `sav_magasin_core` | Dossier SAV magasin : dépôt, diagnostic, attente pièce, réparation, facturation, restitution |
| `sav_magasin_stock` | Lecture ergonomique du stock local/distant depuis les lignes de pièces SAV |
| `sav_magasin_purchase` | Réception sans commande et rattachement éventuel à un dossier SAV |
| `sav_magasin_dashboard` | Menus opérationnels : dossiers du jour, attente pièce, à restituer, à facturer |

## Ordre conseillé d'installation

1. `sav_magasin_product`
2. `sav_magasin_partner`
3. `sav_magasin_core`
4. `sav_magasin_stock`
5. `sav_magasin_purchase`
6. `sav_magasin_dashboard`

Odoo installe normalement les dépendances automatiquement.

## Comptes et accès

Depuis Odoo, créer les utilisateurs puis leur affecter les groupes :

- SAV Magasin / Accueil magasin
- SAV Magasin / Technicien SAV
- SAV Magasin / Stock & Achat
- SAV Magasin / Responsable magasin
- SAV Magasin / Administrateur métier

## Commandes utiles

```bash
make up          # démarre Odoo + PostgreSQL
make down        # arrête les conteneurs
make logs        # logs Odoo
make restart     # redémarre Odoo
make shell       # shell dans le conteneur Odoo
make psql        # shell PostgreSQL
```

## Mise à jour d'un module après modification

Dans l'interface Odoo :

1. Activer le mode développeur.
2. Aller dans Apps.
3. Mettre à jour la liste des apps.
4. Mettre à niveau le module modifié.

Ou en ligne de commande, après avoir remplacé `savmagasin` par le nom de la base :

```bash
docker compose exec odoo odoo -d savmagasin -u sav_magasin_core --stop-after-init
```

Puis :

```bash
docker compose restart odoo
```

## Intention UX

Le principe n'est pas de reproduire un ERP dense écran par écran, mais de créer une interface métier guidée :

```text
Client → Dossier SAV → Produit déposé → Diagnostic → Pièces → Stock → Achat → Réparation → Facture → Restitution
```

Le module central est `sav_magasin_core`.

## Dépannage : aucune app SAV Magasin visible

Si les modules SAV Magasin ne sont pas visibles dans Odoo :

1. Vérifier que le dossier `addons` est bien monté dans le conteneur :

```bash
./scripts/check-addons.sh
```

Tu dois voir notamment :

```text
/mnt/extra-addons/sav_magasin_app/__manifest__.py
/mnt/extra-addons/sav_magasin_core/__manifest__.py
/mnt/extra-addons/sav_magasin_product/__manifest__.py
```

2. Dans Odoo, activer le mode développeur puis aller dans Apps et cliquer sur **Mettre à jour la liste des apps**.

3. Dans Apps, chercher :

```text
SAV Magasin
```

4. Installer l'app centrale :

```text
SAV Magasin - Application principale
```

5. Installation CLI si l'app n'apparaît toujours pas :

```bash
./scripts/install-sav-magasin.sh <nom_de_ta_base_odoo>
```

Exemple :

```bash
./scripts/install-sav-magasin.sh sav_magasin
```



## Correction v0.1.2

Cette version corrige la compatibilité Odoo Community lorsque le champ `res.partner.mobile` n'existe pas dans le registre.
Le module `sav_magasin_partner` ne déclare plus `mobile` dans les dépendances `@api.depends` et vérifie son existence avant toute recherche.

## Version 0.1.3 — correctifs d’installation

Cette version corrige les erreurs rencontrées à l’installation sur l’image Odoo utilisée localement :

- retrait de `category_id` sur `res.groups`, champ absent sur certaines versions récentes d’Odoo ;
- conservation des groupes SAV Magasin sans catégorie applicative pour garantir l’installation ;
- sécurisation de la logique produit si le champ `type` varie selon la version d’Odoo ;
- conservation du correctif précédent sur `res.partner.mobile`.

Pour repartir proprement en développement :

```bash
docker compose down -v
docker compose up -d
```

Puis recréer la base, mettre à jour la liste des apps et installer **SAV Magasin - Application principale**.


## Changelog v0.2.2

- Ajout du menu **Comptoir SAV > Nouveau dossier**.
- Ajout d'un assistant guidé pour créer un dossier SAV en situation d'accueil magasin.
- Renforcement des contrôles avant validation du dépôt : client, contact, produit, symptôme, état visuel, magasin.
- Amélioration du workflow SAV et des boutons d'action.
- Vue formulaire et Kanban SAV retravaillées pour un usage plus opérationnel.
