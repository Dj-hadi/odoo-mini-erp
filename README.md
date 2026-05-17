# ISIL DZ — Preview Section
| | |
|---|---|
| <img width="260" height="220" alt="Screenshot 1" src="https://github.com/user-attachments/assets/6cb0f49a-71e6-4f50-9fdb-439f3e6d480c" /> | <img width="260" height="220" alt="Screenshot 2" src="https://github.com/user-attachments/assets/a1c4aa62-d04e-4c8d-ba65-286898b18fd0" /> |
| <img width="260" height="220" alt="Screenshot 3" src="https://github.com/user-attachments/assets/08fabd63-a976-4cba-81e2-34a88916b109" /> | <img width="260" height="220" alt="Screenshot 4" src="https://github.com/user-attachments/assets/cedb129f-be11-4275-8900-b54819b0253e" /> |
| <img width="260" height="220" alt="Screenshot 5" src="https://github.com/user-attachments/assets/5de23b4d-aaa9-4b62-a1c1-2be5761d3c50" /> | <img width="260" height="220" alt="Screenshot 6" src="https://github.com/user-attachments/assets/731112fd-9c49-42ad-9d06-51d01258b9a2" /> |
# ISIL DZ — Odoo 17 Enterprise Management System

A custom Odoo 17 Community setup built for online enterprises, featuring 6 purpose-built modules with a unified design system. 

## Modules

| Module | Description |
|--------|-------------|
| **isil_hr_advanced** | Employee management, payroll, skills, workflows |
| **isil_stock_traceability** | Lot tracking, expiry management, stock alerts |
| **isil_manufacturing_planning** | BOM management, quality control, production planning |
| **isil_sales_crm** | Sales orders with technical validation workflow |
| **isil_financial_analytics** | General ledger, AR, AP, assets, payroll analytics |
| **isil_dashboard** | Live KPI dashboard across all modules |
| **isil_welcome** | Animated company welcome screen |

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/) (v2+)

## Quick Start <- (not recommended)

```bash
git clone https://github.com/Dj-hadi/odoo-mini-erp
cd odoo-mini-erp
bash setup.sh
```

Then open **http://localhost:8069** and log in with `admin` / `admin`.

The setup script inistially starts the containers, waits for Postgres, creates the `GRH` database, and installs all 7 modules automatically. Shouldn't take a long time (2 minutes) unless you have terrible internet like me.

## Manual Setup (alternative) <- (recommended)

```bash
# 1. Start containers
docker compose up -d

# 2. Wait ~20 seconds for Odoo to boot, then install modules
docker compose exec odoo odoo \
  -i isil_hr_advanced,isil_stock_traceability,isil_manufacturing_planning,isil_sales_crm,isil_financial_analytics,isil_dashboard,isil_welcome \
  -d GRH --stop-after-init --without-demo=all

# 3. Restart
docker compose restart odoo
```

## Project Structure

```
odoo-project/
├── addons/                  # All custom modules
│   ├── isil_hr_advanced/
│   ├── isil_stock_traceability/
│   ├── isil_manufacturing_planning/
│   ├── isil_sales_crm/
│   ├── isil_financial_analytics/
│   ├── isil_dashboard/
│   └── isil_welcome/
├── config/
│   └── odoo.conf            # Odoo configuration
├── docker-compose.yml
└── setup.sh                 # One-command setup
```
there should also be a ./data sub folder for postgreSQL data handling which is not included here

## Stopping / Restarting (if needed after tweaking source code)

```bash
docker compose down        # stop containers, keep data
docker compose up -d       # start again (data preserved)
docker compose down -v     # stop and DELETE all data (full reset)
```

## Upgrading a Module After Code Changes (after restarting)

```bash
docker compose exec odoo odoo -u <module_name> -d GRH --stop-after-init
docker compose restart odoo
```

## Configuration (needed to log into GRH)

Edit `config/odoo.conf` to change:
- `admin_passwd` — master password for the Odoo settings page
- `log_level` — `debug` for development, `info` for production

## Tech Stack (specs)

- **Odoo 17.0 Community** (`odoo:17.0` Docker image)
- **PostgreSQL 15** (`postgres:15` Docker image)
- **OWL 2** (Odoo Web Library) for frontend components
- **SCSS** with CSS custom properties for the design system
