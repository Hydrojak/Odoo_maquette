{
    'name': 'Re-Watt ERP - Flux stock réels',
    'version': '19.0.7.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'Création de transferts, réservations et réceptions stock Odoo depuis les composants batterie.',
    'description': """
Ce module relie les décisions métier des lignes composants batterie aux objets stock Odoo :
stock.picking et stock.move. Il reste volontairement prudent : il crée les flux stock,
les confirme si possible, puis laisse l'utilisateur valider l'opération physique dans Odoo Inventory.
    """,
    'author': 'Projet Re-Watt ERP',
    'license': 'LGPL-3',
    'depends': ['sav_magasin_purchase', 'sav_magasin_stock', 'stock'],
    'data': ['views/stock_flow_views.xml'],
    'installable': True,
    'application': False,
}
