from odoo import models, fields, api

class ProductProduct(models.Model):
    _inherit = 'product.product'

    reorder_threshold = fields.Float(
        string='Reorder Threshold',
        help='Minimum quantity before triggering a stock alert',
        default=5.0
    )

    stock_lot_isil_ids = fields.One2many(
        'stock.lot.isil', 'product_id', string='Stock Lots'
    )

    lots_count = fields.Integer(
        string='Lots Count',
        compute='_compute_lots_count'
    )

    @api.depends('stock_lot_isil_ids')
    def _compute_lots_count(self):
        for product in self:
            # Count only raw material lots
            product.lots_count = len(product.stock_lot_isil_ids.filtered(lambda l: l.lot_type == 'raw_material'))

    @api.model
    def create(self, vals):
        if 'reorder_threshold' not in vals or vals.get('reorder_threshold') is None:
            vals['reorder_threshold'] = 5.0
        product = super().create(vals)
        self._check_alert(product)
        return product

    def write(self, vals):
        res = super().write(vals)
        for product in self:
            self._check_alert(product)
        return res

    def _check_alert(self, product):
        Alert = self.env['stock.alert'].sudo()

        # ❗ NEW RULE: ignore products that don't use our ISIL lots
        lots = product.stock_lot_isil_ids.filtered(
            lambda l: l.active and l.lot_type == 'raw_material'
        )
        if not lots:
            # no custom ISIL lots → no alert for this product
            return

        qty_available = sum(lot.quantity for lot in lots)
        threshold = product.reorder_threshold or 5.0
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
                existing.write({'is_active': False, 'note': 'Auto-resolved', 'resolved_by': self.env.uid})
