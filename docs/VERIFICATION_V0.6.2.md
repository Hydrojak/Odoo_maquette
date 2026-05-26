# Vérification v0.6.2 — Correction XML data Odoo

## Correction appliquée

La v0.6.1 utilisait des racines XML de type :

```xml
<odoo noupdate="1">
```

L'image Odoo utilisée dans l'environnement de test a rejeté ce format avec :

```text
AssertionError: Element odoo has extra content: record, line 2
```

La v0.6.2 revient au format le plus compatible pour les fichiers de données chargés par le manifest :

```xml
<odoo>
    <record ...>
        ...
    </record>
</odoo>
```

## Fichiers corrigés

- `addons/sav_magasin_core/data/sequence.xml`
- `addons/sav_magasin_purchase/data/sequence.xml`
- `addons/sav_magasin_demo/data/demo_data.xml`
- `addons/sav_magasin_knowledge/data/default_procedures.xml`

## Contrôles statiques

- Suppression des attributs `noupdate` placés directement sur `<odoo>`.
- Vérification qu'il ne reste plus de `<odoo noupdate="1">`.
- Parsing XML avec `xmllint`.
- Compilation Python.
- Suppression des fichiers `__pycache__`.
