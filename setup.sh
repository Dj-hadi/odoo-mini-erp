#!/usr/bin/env bash
# ISIL DZ — first-time setup script
# Usage: bash setup.sh
set -e

DB_NAME="GRH"
MODULES="isil_hr_advanced,isil_stock_traceability,isil_manufacturing_planning,isil_sales_crm,isil_financial_analytics,isil_dashboard,isil_welcome"

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║        ISIL DZ — Project Setup           ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# 1. Start containers
echo "▸ Starting containers..."
docker compose up -d

# 2. Wait for Postgres to be ready
echo "▸ Waiting for PostgreSQL to be ready..."
until docker compose exec -T db pg_isready -U odoo -q 2>/dev/null; do
  sleep 2
done
echo "  PostgreSQL is ready."

# 3. Wait a bit more for Odoo to fully start
echo "▸ Waiting for Odoo to initialise (20 s)..."
sleep 20

# 4. Install all custom modules + create the database
echo "▸ Installing modules into database '$DB_NAME'..."
docker compose exec -T odoo odoo \
  -i "$MODULES" \
  -d "$DB_NAME" \
  --db_host=db \
  --db_user=odoo \
  --db_password=odoo \
  --stop-after-init \
  --without-demo=all

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║  Done!  Open http://localhost:8069       ║"
echo "║  Database : $DB_NAME                        ║"
echo "║  Login    : admin / admin                ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# 5. Restart so Odoo picks up all installed modules
docker compose restart odoo
