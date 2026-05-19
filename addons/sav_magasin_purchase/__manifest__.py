{
    "name": "SAV Magasin - Achats et réception sans commande",
    "version": "19.0.2.2.0",
    "category": "Inventory/Purchase",
    "summary": "Réception sans commande fournisseur et rattachement à un dossier SAV.",
    "author": "Projet SAV Magasin",
    "license": "LGPL-3",
    "depends": ["purchase", "stock", "sav_magasin_core"],
    "data": [
        "security/ir.model.access.csv",
        "data/sequence.xml",
        "views/quick_receipt_views.xml",
        "views/menu.xml"
    ],
    "installable": True,
    "application": False,
}
