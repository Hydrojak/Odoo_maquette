{
    'name': 'Re-Watt ERP - Référentiel produits',
    'version': '19.0.7.0.0',
    'category': 'Inventory/Products',
    'summary': 'Référentiel métier articles : marques, gammes, modèles, types et contrôle de complétude.',
    'author': 'Projet Re-Watt ERP',
    'license': 'LGPL-3',
    'depends': ['product', 'stock'],
    'data': ['security/ir.model.access.csv', 'views/product_referential_views.xml', 'views/product_template_views.xml', 'views/menu.xml'],
    'installable': True,
    'application': False,
}
