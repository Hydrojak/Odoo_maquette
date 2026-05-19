{
    "name": "SAV Magasin - SAV magasin",
    "version": "19.0.2.2.0",
    "category": "Services/Repair",
    "summary": "Dossier SAV magasin ergonomique : dépôt, diagnostic, attente pièce, réparation, facturation, restitution.",
    "author": "Projet SAV Magasin",
    "license": "LGPL-3",
    "depends": [
        "mail",
        "product",
        "stock",
        "sale_management",
        "account",
        "sav_magasin_product",
        "sav_magasin_partner"
    ],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "data/sequence.xml",
        "views/sav_order_views.xml",
        "views/sav_create_wizard_views.xml",
        "views/menu.xml",
        "reports/sav_deposit_report.xml"
    ],
    "installable": True,
    "application": False,
}
