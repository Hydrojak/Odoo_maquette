# Vérification v0.6.4

Correction ciblée pour Odoo 19.

## Problème corrigé

Odoo 19 refuse les vues héritées utilisant `@string` comme sélecteur XPath :

```xml
<xpath expr="//page[@string='Commercial']/group" ...>
```

## Correction

Les pages du formulaire SAV ont maintenant des attributs `name` stables :

- `page_resume_depot`
- `page_diagnosis_repair`
- `page_parts_stock`
- `page_commercial`

Les vues héritées ciblent désormais ces attributs :

```xml
<xpath expr="//page[@name='page_commercial']/group" ...>
```

## Contrôles statiques effectués

- XML parsé avec `lxml`.
- Python compilé avec `compileall`.
- Recherche des XPath interdits `@string`.
- Suppression des `__pycache__`.
