{
    "name": "Dashboard Recruteur",
    "summary": "Starter custom module for Odoo 19 - simple Academy app",
    "version": "19.0.1.0.0",
    "category": "Education",
    "author": "Odooistic",
    "website": "https://www.odooistic.co.uk",
    "license": "LGPL-3",
    "depends": ["base", "hr", "hr_recruitment", "mail", "calendar"],
    "data": [
        "security/ir.model.access.csv",
        "views/dashboard_recruteur_view.xml",
        "data/static_dashboard_data.xml",
    ],
    "assets": {
    'web.assets_backend': [
        'dashboard_recruteur/static/src/css/dashboard_recruteur.css',
    ],
},

    "installable": True,
    "application": True,

}