{
    'name': 'Re-Watt ERP - atelier batterie',
    'version': '19.0.7.0.0',
    'category': 'Services/Repair',
    'summary': 'Dossier atelier batterie ergonomique : dépôt, diagnostic, attente composant batterie, réparation, facturation, restitution.',
    'author': 'Projet Re-Watt ERP',
    'license': 'LGPL-3',
    'depends': ['mail', 'product', 'stock', 'sale_management', 'account', 'sav_magasin_product', 'sav_magasin_partner'],
    'data': ['security/security.xml', 'security/ir.model.access.csv', 'views/sav_order_views.xml', 'views/sav_create_wizard_views.xml', 'views/menu.xml', 'reports/sav_deposit_report.xml'],
    'installable': True,
    'application': False,
    'post_init_hook': 'post_init_hook',
}
