from odoo import models, fields, api

class StockAlert(models.Model):
    _name = 'stock.alert'
    _description = 'Stock Alert'
    _order = 'alert_date desc'

    product_id = fields.Many2one('product.product', string='Product', required=True)
    product_tmpl_id = fields.Many2one('product.template', related='product_id.product_tmpl_id', store=True)
    current_qty = fields.Float(string='Current Quantity')
    reorder_threshold = fields.Float(string='Reorder Threshold')
    qty_gap = fields.Float(string='Qty Gap', compute='_compute_qty_gap', store=False)
    alert_date = fields.Datetime(string='Alert Date', default=fields.Datetime.now)
    is_active = fields.Boolean(string='Active', default=True)
    resolved_by = fields.Many2one('res.users', string='Resolved By')
    note = fields.Text(string='Note')

    @api.depends('current_qty', 'reorder_threshold')
    def _compute_qty_gap(self):
        for rec in self:
            rec.qty_gap = max(0.0, rec.reorder_threshold - rec.current_qty)

    @api.model
    def check_and_create_alerts(self):
        Product = self.env['product.product'].sudo()
        Alert = self.env['stock.alert'].sudo()
        products = Product.search([('reorder_threshold', '>', 0)])
        for product in products:
            qty_available = product.qty_available
            threshold = product.reorder_threshold or 0.0
            existing = Alert.search([('product_id', '=', product.id), ('is_active', '=', True)], limit=1)

            if qty_available <= threshold:
                if not existing:
                    Alert.create({
                        'product_id': product.id,
                        'current_qty': qty_available,
                        'reorder_threshold': threshold,
                    })
                else:
                    existing.write({'current_qty': qty_available})
            else:
                if existing:
                    existing.write({'is_active': False, 'note': 'Auto-resolved by scheduler', 'resolved_by': self.env.uid})

    def action_go_back(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Stock Alerts',
            'res_model': 'stock.alert',
            'view_mode': 'tree,form',
            'target': 'current',
        }

    def action_mark_resolved(self):
        for rec in self:
            rec.is_active = False
            rec.resolved_by = self.env.uid
            rec.note = (rec.note or '') + '\nResolved by user.'
