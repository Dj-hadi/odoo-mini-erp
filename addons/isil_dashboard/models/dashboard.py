from odoo import models, fields, api
from datetime import datetime


class DashboardKPI(models.Model):
    _name = "isil_dashboard.kpi"
    _description = "Dashboard KPI"

    name = fields.Char("KPI Name", required=True)
    value = fields.Float("Current Value")
    target = fields.Float("Target Value")
    unit = fields.Char("Unit")
    is_active = fields.Boolean("Active", default=True)
    color = fields.Char("Color", default="#3498db")
    kpi_type = fields.Selection([
        ("sales", "Sales"),
        ("stock", "Stock"),
        ("manufacturing", "Manufacturing"),
        ("financial", "Financial"),
        ("general", "General"),
    ], string="KPI Type", default="general")


class StrategicObjective(models.Model):
    _name = "isil_dashboard.objective"
    _description = "Strategic Objective"

    name = fields.Char("Objective Name", required=True)
    description = fields.Text("Description")
    progress = fields.Float("Progress %")
    status = fields.Selection([
        ("on_track", "On Track"),
        ("at_risk", "At Risk"),
        ("behind", "Behind Schedule"),
        ("completed", "Completed"),
    ], string="Status")
    start_date = fields.Date("Start Date", default=fields.Date.today)
    end_date = fields.Date("End Date")
    target_value = fields.Float("Target Value")
    current_value = fields.Float("Current Value")
    kpi_ids = fields.Many2many("isil_dashboard.kpi", string="Related KPIs")


class Dashboard(models.Model):
    _name = "isil_dashboard.dashboard"
    _description = "Dashboard"

    name = fields.Char("Dashboard", default="Main Dashboard")

    def open_kpi_action(self):
        return {
            'name': 'KPIs',
            'type': 'ir.actions.act_window',
            'res_model': 'isil_dashboard.kpi',
            'view_mode': 'tree,form',
        }

    def open_objective_action(self):
        return {
            'name': 'Strategic Objectives',
            'type': 'ir.actions.act_window',
            'res_model': 'isil_dashboard.objective',
            'view_mode': 'tree,form',
        }

    def _get_sale_data(self):
        SaleOrder = self.env['sale.order']
        confirmed = SaleOrder.search([('state', 'in', ['sale', 'done'])])
        total_revenue = sum(confirmed.mapped('amount_total'))
        return {
            'total_orders': len(confirmed),
            'total_revenue': total_revenue,
        }

    def _get_stock_data(self):
        Alert = self.env['stock.alert']
        Product = self.env['product.product']
        active_alerts = Alert.search([('is_active', '=', True)])
        all_products = Product.search([('type', 'in', ['product', 'consu'])])
        total_value = sum(p.qty_available * p.standard_price for p in all_products)
        return {
            'total_products': len(all_products),
            'low_stock_count': len(active_alerts),
            'total_value': total_value,
        }

    def _get_manufacturing_data(self):
        MrpProduction = self.env['mrp.production']
        in_progress = MrpProduction.search([('state', 'in', ['confirmed', 'progress'])])
        pending_qc = MrpProduction.search([
            ('quality_check_required', '=', True),
            ('quality_check_done', '=', False),
            ('state', 'not in', ['done', 'cancel']),
        ])
        return {
            'orders_in_progress': len(in_progress),
            'pending_quality_checks': len(pending_qc),
        }

    def _get_hr_data(self):
        Employee = self.env['hr.custom.employee']
        Request = self.env['hr.employee.request']
        total_employees = Employee.search_count([])
        pending_requests = Request.search_count([('state', 'not in', ['approved', 'rejected'])])
        return {
            'total_employees': total_employees,
            'pending_requests': pending_requests,
        }

    def generate_sales_report(self):
        sale_data = self._get_sale_data()
        return {
            'kpis': self.env['isil_dashboard.kpi'].search([('kpi_type', '=', 'sales')]).read(),
            'objectives': self.env['isil_dashboard.objective'].search([]).read(),
            'report_date': datetime.now().strftime("%Y-%m-%d"),
            'total_revenue': sale_data['total_revenue'],
            'total_orders': sale_data['total_orders'],
        }

    def generate_stock_report(self):
        stock_data = self._get_stock_data()
        return {
            'total_products': stock_data['total_products'],
            'low_stock_count': stock_data['low_stock_count'],
            'total_value': stock_data['total_value'],
            'report_date': datetime.now().strftime("%Y-%m-%d"),
        }

    def generate_full_report(self):
        return {
            'report_date': datetime.now().strftime("%Y-%m-%d"),
            'sales': self._get_sale_data(),
            'stock': self._get_stock_data(),
            'manufacturing': self._get_manufacturing_data(),
            'hr': self._get_hr_data(),
        }
