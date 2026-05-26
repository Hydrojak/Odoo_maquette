{
    'name': 'Re-Watt ERP - Achats et réception sans commande',
    'version': '19.0.7.0.0',
    'category': 'Inventory/Purchase',
    'summary': 'Achats fournisseurs liés aux dossiers batterie, commandes depuis composants batterie et réception sans commande.',
    'author': 'Projet Re-Watt ERP',
    'license': 'LGPL-3',
    'depends': ['purchase', 'stock', 'sav_magasin_stock'],
    'data': ['security/ir.model.access.csv', 'views/quick_receipt_views.xml', 'views/purchase_link_views.xml', 'views/menu.xml'],
    'installable': True,
    'application': False,
    'post_init_hook': 'post_init_hook',
}
