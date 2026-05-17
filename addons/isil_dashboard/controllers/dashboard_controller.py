from odoo import http
from odoo.http import request


class DashboardController(http.Controller):

    @http.route('/isil_dashboard/get_live_data', type='json', auth='user')
    def get_live_data(self):
        env = request.env

        # ── Sales ─────────────────────────────────────────────────────
        sale_orders = env['sale.order'].search([('state', 'in', ['sale', 'done'])])
        total_revenue  = sum(sale_orders.mapped('amount_total'))
        pending_invoice = len([o for o in sale_orders if o.invoice_status == 'to invoice'])

        # ── Stock ─────────────────────────────────────────────────────
        active_alerts = env['stock.alert'].search_count([('is_active', '=', True)])
        all_products  = env['product.product'].search([('type', 'in', ['product', 'consu'])])
        total_value   = sum(p.qty_available * p.standard_price for p in all_products)

        # ── Manufacturing ─────────────────────────────────────────────
        orders_in_progress = env['mrp.production'].search_count(
            [('state', 'in', ['confirmed', 'progress'])]
        )
        pending_qc = env['mrp.production'].search_count([
            ('quality_check_required', '=', True),
            ('quality_check_done', '=', False),
            ('state', 'not in', ['done', 'cancel']),
        ])

        # ── HR ────────────────────────────────────────────────────────
        total_employees  = env['hr.custom.employee'].search_count([])
        pending_requests = env['hr.employee.request'].search_count(
            [('state', 'not in', ['approved', 'rejected'])]
        )

        # ── Objectives ────────────────────────────────────────────────
        objectives = env['isil_dashboard.objective'].search([])

        return {
            'sales': {
                'total_orders':   len(sale_orders),
                'total_revenue':  total_revenue,
                'pending_invoice': pending_invoice,
            },
            'stock': {
                'total_products': len(all_products),
                'active_alerts':  active_alerts,
                'total_value':    total_value,
            },
            'mfg': {
                'orders_in_progress': orders_in_progress,
                'pending_qc':         pending_qc,
            },
            'hr': {
                'total_employees':  total_employees,
                'pending_requests': pending_requests,
            },
            'objectives': objectives.read(['name', 'progress', 'status']),
        }
