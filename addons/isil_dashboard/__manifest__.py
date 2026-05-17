{
    "name": "ISIL Dashboard & Reports",
    "version": "2.0",
    "summary": "Business Intelligence Dashboard with live KPIs from all modules",
    "category": "Business Intelligence",
    "depends": [
        "base", "web",
        "isil_hr_advanced",
        "isil_stock_traceability",
        "isil_manufacturing_planning",
        "isil_sales_crm",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/dashboard_views.xml",
        "report/reports.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "isil_dashboard/static/src/scss/dashboard.scss",
            "isil_dashboard/static/src/js/dashboard.js",
            "isil_dashboard/static/src/xml/dashboard.xml",
        ],
    },
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}
