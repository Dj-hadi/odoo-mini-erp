{
    "name": "ISIL Welcome",
    "version": "1.0",
    "summary": "Animated welcome slideshow for ISIL DZ",
    "category": "Extra Tools",
    "depends": ["web"],
    "data": ["views/welcome_views.xml"],
    "assets": {
        "web.assets_backend": [
            "isil_welcome/static/src/scss/welcome.scss",
            "isil_welcome/static/src/js/welcome.js",
            "isil_welcome/static/src/xml/welcome.xml",
        ],
    },
    "installable": True,
    "application": True,
}
