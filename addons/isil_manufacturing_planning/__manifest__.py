{
    "name": "ISIL Manufacturing Planning",
    "version": "2.0",
    "category": "Manufacturing",
    "summary": "Advanced manufacturing planning with quality control and stock traceability",
    "depends": ["mrp", "isil_stock_traceability", "isil_hr_advanced"],
    "data": [
        "security/ir.model.access.csv",
        "data/manufacturing_data.xml",
        "views/mrp_production_views.xml",
        "views/mrp_bom_views.xml",
        "views/quality_check_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "isil_manufacturing_planning/static/src/scss/mfg_variables.scss",
            "isil_manufacturing_planning/static/src/scss/mfg_quality.scss",
            "isil_manufacturing_planning/static/src/scss/mfg_production.scss",
            "isil_manufacturing_planning/static/src/js/quality_score_gauge.js",
            "isil_manufacturing_planning/static/src/js/qc_status_badge.js",
            "isil_manufacturing_planning/static/src/js/bom_type_badge.js",
            "isil_manufacturing_planning/static/src/xml/quality_score_gauge.xml",
            "isil_manufacturing_planning/static/src/xml/qc_status_badge.xml",
            "isil_manufacturing_planning/static/src/xml/bom_type_badge.xml",
        ],
    },
    "installable": True,
    "application": True,
}
