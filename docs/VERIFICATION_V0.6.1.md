# Vérification v0.6.1 — Correction XML Odoo 19

## Correction appliquée

Certains fichiers XML de données utilisaient la forme :

```xml
<odoo>
  <data noupdate="1">
    ...
  </data>
</odoo>
```

La version Odoo utilisée rejette ce wrapper `data` et retourne :

```text
AssertionError: Element odoo has extra content: data, line 2
```

La v0.6.1 remplace ces wrappers par :

```xml
<odoo noupdate="1">
  ...
</odoo>
```

## Fichiers corrigés

- `addons/sav_magasin_demo/data/demo_data.xml`
- `addons/sav_magasin_knowledge/data/default_procedures.xml`

## Contrôles statiques réalisés

- Parsing XML : OK
- Compilation Python : OK
- Recherche des wrappers `<data>` restants : OK
- Recherche des anciens attributs `category_id` sur `res.groups` : OK
- Recherche des anciens groupes `expand` en vue search : OK
