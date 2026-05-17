from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class StockLotIsil(models.Model):
    _name = 'stock.lot.isil'
    _description = 'Stock Lot ISIL'
    _order = 'expiry_date asc, id desc'

    name = fields.Char(string='Lot Name', required=True)
    product_id = fields.Many2one('product.product', string='Product', required=True, ondelete='cascade')
    quantity = fields.Float(string='Quantity', default=0.0)
    location_id = fields.Many2one('stock.location', string='Location')
    production_date = fields.Date(string='Production Date')
    expiry_date = fields.Date(string='Expiry Date')
    active = fields.Boolean(string='Active', default=True)

    lot_type = fields.Selection([
        ('raw_material', 'Raw Material'),
        ('finished_product', 'Finished Product')
    ], string="Lot Type", required=True, default='raw_material')

    expiry_status = fields.Selection([
        ('no_date',       'No Date'),
        ('fresh',         'Fresh'),
        ('expiring_soon', 'Expiring Soon'),
        ('expired',       'Expired'),
    ], string='Expiry Status', compute='_compute_expiry_status', store=False)

    @api.depends('expiry_date')
    def _compute_expiry_status(self):
        today = fields.Date.today()
        soon = today + timedelta(days=30)
        for rec in self:
            if not rec.expiry_date:
                rec.expiry_status = 'no_date'
            elif rec.expiry_date < today:
                rec.expiry_status = 'expired'
            elif rec.expiry_date <= soon:
                rec.expiry_status = 'expiring_soon'
            else:
                rec.expiry_status = 'fresh'

    _sql_constraints = [
        ('lot_product_uniq', 'unique(name, product_id)', 'Lot name must be unique per product.'),
    ]

    @api.constrains('expiry_date')
    def _check_dates(self):
        for rec in self:
            if rec.expiry_date and rec.production_date and rec.expiry_date < rec.production_date:
                raise ValidationError('Expiry date cannot be before production date.')

    def action_go_back(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Stock Lots',
            'res_model': 'stock.lot.isil',
            'view_mode': 'tree,form',
            'target': 'current',
        }

    def consume(self, qty):
        if qty > self.quantity:
            raise ValidationError(f"Cannot consume {qty} from lot {self.name}, only {self.quantity} available")
        self.quantity -= qty
        if self.quantity <= 0:
            self.active = False
        # Only check alert for raw material consumption
        if self.lot_type == 'raw_material':
            self.product_id._check_alert(self.product_id)
