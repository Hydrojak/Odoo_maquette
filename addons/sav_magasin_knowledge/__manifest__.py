{
    'name': 'Re-Watt ERP - Knowledge métier',
    'version': '19.0.7.0.0',
    'category': 'Services/Repair',
    'summary': 'Base de procédures, FAQ et guides métier intégrés au Re-Watt ERP.',
    'description': "\nModule Knowledge interne au projet Re-Watt ERP. Il ne dépend pas de l'application Knowledge Enterprise.\nIl permet de documenter les procédures de comptoir, diagnostic, stock, achat, substitution et restitution.\n    ",
    'author': 'Projet Re-Watt ERP',
    'license': 'LGPL-3',
    'depends': ['mail', 'sav_magasin_core'],
    'data': ['security/ir.model.access.csv', 'views/procedure_views.xml', 'views/sav_order_knowledge_views.xml', 'views/menu.xml'],
    'installable': True,
    'application': False,
    'post_init_hook': 'post_init_hook',
}
