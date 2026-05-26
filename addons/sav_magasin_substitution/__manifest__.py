{
    'name': 'Re-Watt ERP - Substitutions articles',
    'version': '19.0.7.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'Gestion des composants batterie équivalentes et composants de substitution pour les dossiers batterie.',
    'author': 'Projet Re-Watt ERP',
    'license': 'LGPL-3',
    'depends': ['sav_magasin_core', 'sav_magasin_stock', 'product', 'stock'],
    'data': ['security/ir.model.access.csv', 'views/product_substitution_views.xml', 'views/sav_part_line_substitution_views.xml', 'views/menu.xml'],
    'installable': True,
    'application': False,
}
