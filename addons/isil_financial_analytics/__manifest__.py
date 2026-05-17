{
    "name": "ISIL Financial Analytics",
    "version": "2.0",
    "summary": "Financial analytics — GL, AR, AP, Assets, Payroll, Analytic Reports",
    "category": "Accounting",
    "depends": ["base", "account"],
    "data": [
        "security/ir.model.access.csv",
        "views/analytic_account_views.xml",
        "views/finance_submodules_views.xml",
        "views/analytic_report_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "isil_financial_analytics/static/src/scss/finance_variables.scss",
            "isil_financial_analytics/static/src/scss/finance_tables.scss",
            "isil_financial_analytics/static/src/js/account_type_badge.js",
            "isil_financial_analytics/static/src/xml/account_type_badge.xml",
        ],
    },
    "installable": True,
    "application": True,
}
