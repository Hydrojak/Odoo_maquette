# Sécurité et limites de la maquette

## Statut

Cette base est une maquette de développement. Elle n’est pas prête pour production sans durcissement.

## Points à durcir avant production

- changer `admin_passwd` dans `config/odoo.conf` ;
- changer les mots de passe PostgreSQL ;
- désactiver ou restreindre `list_db` ;
- définir des droits utilisateurs par profil ;
- contrôler les accès aux menus stock, achat et configuration ;
- mettre en place des sauvegardes ;
- journaliser les actions sensibles ;
- séparer environnement démo, test et production ;
- supprimer les données de démonstration.

## Profils métier cibles

| Profil | Rôle |
|---|---|
| Accueil magasin | créer client, créer dossier, imprimer bon dépôt |
| Technicien SAV | diagnostic, réparation, composants batterie |
| Stock / achat | réception, transfert, commande |
| Responsable magasin | pilotage, validation, arbitrage |
| Administration métier | référentiel, procédures, configuration fonctionnelle |
| Administrateur technique | maintenance Odoo / Docker |
