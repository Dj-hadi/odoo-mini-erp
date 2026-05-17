# ISIL DZ — Odoo 17 Enterprise Management System

A custom Odoo 17 Community setup built for Algerian enterprises, featuring 7 purpose-built modules with a unified design system.

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

## Quick Start

```bash
git clone <your-repo-url>
cd odoo-project
bash setup.sh
```

Then open **http://localhost:8069** and log in with `admin` / `admin`.

> The setup script starts the containers, waits for Postgres, creates the `GRH` database, and installs all 7 modules automatically. Takes about 2 minutes.

## Manual Setup (alternative)

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

> `data/` is excluded from git (PostgreSQL data and Odoo filestore are machine-specific).

## Stopping / Restarting

```bash
docker compose down        # stop containers, keep data
docker compose up -d       # start again (data preserved)
docker compose down -v     # stop and DELETE all data (full reset)
```

## Upgrading a Module After Code Changes

```bash
docker compose exec odoo odoo -u <module_name> -d GRH --stop-after-init
docker compose restart odoo
```

## Configuration

Edit `config/odoo.conf` to change:
- `admin_passwd` — master password for the Odoo settings page
- `log_level` — `debug` for development, `info` for production

## Tech Stack

- **Odoo 17.0 Community** (`odoo:17.0` Docker image)
- **PostgreSQL 15** (`postgres:15` Docker image)
- **OWL 2** (Odoo Web Library) for frontend components
- **SCSS** with CSS custom properties for the design system
