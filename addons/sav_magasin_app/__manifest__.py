{
    "name": "SAV Magasin - Application principale",
    "version": "19.0.2.2.0",
    "category": "Services/Repair",
    "summary": "Application centrale SAV Magasin : SAV magasin, clients, articles, stock, achats et pilotage.",
    "description": """
SAV Magasin regroupe les modules métier nécessaires à l'exploitation d'un SAV magasin sur Odoo Community.
Installez ce module pour charger l'ensemble du socle SAV Magasin.
    """,
    "author": "Projet SAV Magasin",
    "license": "LGPL-3",
    "depends": [
        "sav_magasin_product",
        "sav_magasin_partner",
        "sav_magasin_core",
        "sav_magasin_stock",
        "sav_magasin_purchase",
        "sav_magasin_dashboard",
    ],
    "data": [
        "views/sav_magasin_app_views.xml",
    ],
    "installable": True,
    "application": True,
    "sequence": 1,
}
