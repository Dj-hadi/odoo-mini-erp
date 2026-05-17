{
    'name': 'ISIL Stock Traceability',
    'version': '2.0',
    'category': 'Inventory',
    'summary': 'Traceability with expiry, production date & stock alerts',
    'depends': [
        'base',
        'stock',
        'product',
        'sale',
        'purchase',
    ],
    'data': [
        # Security
        'security/stock_security.xml',
        'security/ir.model.access.csv',

        # Cron
        'data/cron.xml',

        # Actions & Menus
        'views/actions.xml',
        'views/menu.xml',
        'views/product_views.xml',
        'views/stock_lot_views.xml',
        'views/stock_alert_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'isil_stock_traceability/static/src/scss/stock_variables.scss',
            'isil_stock_traceability/static/src/scss/stock_tables.scss',
            'isil_stock_traceability/static/src/js/expiry_badge_widget.js',
            'isil_stock_traceability/static/src/js/lot_type_badge_widget.js',
            'isil_stock_traceability/static/src/xml/expiry_badge_widget.xml',
            'isil_stock_traceability/static/src/xml/lot_type_badge_widget.xml',
        ],
    },
    'installable': True,
    'application': True,
}
