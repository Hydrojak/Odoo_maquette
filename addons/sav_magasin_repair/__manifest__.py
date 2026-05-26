{
    'name': 'Re-Watt ERP - Liaison réparation batterie Odoo',
    'version': '19.0.7.0.0',
    'category': 'Services/Repair',
    'summary': 'Relie le dossier atelier batterie aux ordres de réparation batterie Odoo standard.',
    'description': '\nCe module garde le dossier atelier batterie comme écran principal et utilise le module Repair Odoo\ncomme moteur technique optionnel de réparation.\n    ',
    'author': 'Projet Re-Watt ERP',
    'license': 'LGPL-3',
    'depends': ['repair', 'sav_magasin_core', 'sav_magasin_stock'],
    'data': ['views/sav_order_repair_views.xml', 'views/menu.xml'],
    'installable': True,
    'application': False,
}
