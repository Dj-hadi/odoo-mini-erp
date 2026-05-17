# ISIL Stock Traceability

Install:
1. Place this module in your addons path.
2. Restart Odoo server.
3. Update apps list and install `ISIL Stock Traceability`.

Run tests:
- From Odoo CLI:
  ./odoo-bin -d <your_db> -i isil_stock_traceability --test-enable --stop-after-init

Notes:
- Cron job `ISIL: Stock Reorder Check` runs daily to create alerts.
- Ensure `product.product.qty_available` values are populated by stock moves / inventory.
