{'name': 'Re-Watt ERP - Application principale',
 'version': '1.1.0',
 'category': 'Services/Repair',
 'summary': 'Application atelier batterie < 60 V basée sur Odoo.',
 'description': '\n'
                "Re-Watt ERP regroupe les modules métier nécessaires à l'exploitation d'un atelier batterie sur Odoo "
                'Community.\n'
                "Installez ce module pour charger l'ensemble du socle Re-Watt ERP, incluant la liaison Repair, la base "
                'de procédures métier et les achats fournisseurs liés aux dossiers batterie.\n'
                '    ',
 'author': 'Projet Re-Watt ERP',
 'license': 'LGPL-3',
 'depends': ['sav_magasin_product',
             'sav_magasin_partner',
             'sav_magasin_core',
             'sav_battery_quality',
             'sav_magasin_stock',
             'sav_magasin_substitution',
             'sav_magasin_repair',
             'sav_magasin_knowledge',
             'sav_magasin_purchase',
             'sav_magasin_stock_flow',
             'sav_magasin_dashboard'],
 'data': ['views/sav_magasin_app_views.xml'],
 'installable': True,
 'application': True,
 'sequence': 1}
