# Vérification v0.4.0

Contrôles effectués hors runtime Odoo :

- parsing XML des vues et données ;
- compilation Python des modules custom ;
- lecture des manifests ;
- vérification des dépendances internes ;
- contrôle d'absence d'anciens préfixes `destock` ;
- création du ZIP final.

Limite : ce contrôle ne remplace pas une installation réelle dans Odoo. Tester sur base vierge avec :

```bash
docker compose down -v
docker compose up -d
```

Puis installer :

- `Re-Watt ERP - Application principale` ;
- `Re-Watt ERP - Données de démonstration`.
