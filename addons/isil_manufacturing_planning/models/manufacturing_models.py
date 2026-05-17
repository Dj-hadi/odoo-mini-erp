from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import date

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    quality_check_required = fields.Boolean(string='Quality Check Required', default=True)
    quality_check_done = fields.Boolean(string='Quality Check Done', default=False)
    quality_check_id = fields.Many2one('quality.check', string='Quality Check')

    # FIXED: Use Selection field instead of Char for gantt_color
    gantt_color = fields.Selection([
        ('#FF0000', 'Red - High Priority'),
        ('#FFA500', 'Orange - Medium Priority'),
        ('#008000', 'Green - Low Priority'),
        ('#0000FF', 'Blue - Normal')
    ], string='Gantt Color', default='#0000FF')

    consumed_lot_ids = fields.Many2many(
        'stock.lot.isil', string='Consumed Raw Material Lots', readonly=True
    )
    finished_lot_id = fields.Many2one(
        'stock.lot.isil', string='Finished Product Lot', readonly=True
    )

    purchase_order_count = fields.Integer(
        string='Purchase Orders', compute='_compute_purchase_order_count'
    )
    # added new field to override Mrp model for custom employees (author:Djouini)
    responsible_id = fields.Many2one(
        "hr.custom.employee",
        string="Production Lead",
        domain="[('department','=','production'), ('position','=','employee')]"
    )
    def _compute_purchase_order_count(self):
        for production in self:
            production.purchase_order_count = 0  # Placeholder, can be extended

    def button_mark_done(self):
        for production in self:
            if production.quality_check_required and not production.quality_check_done:
                raise UserError(
                    "Quality check is required before marking this manufacturing order as done!"
                )

            consumed_lots = []
            for line in production.move_raw_ids:
                product = line.product_id
                qty_needed = line.product_uom_qty
                # Only consume raw material lots
                lots = self.env['stock.lot.isil'].search(
                    [
                        ('product_id', '=', product.id),
                        ('active', '=', True),
                        ('lot_type', 'in', ['raw_material', 'finished_product']),
                    ],
                    order='expiry_date asc'
                )
                qty_to_consume = qty_needed
                for lot in lots:
                    if qty_to_consume <= 0:
                        break
                    take_qty = min(lot.quantity, qty_to_consume)
                    lot.consume(take_qty)
                    consumed_lots.append(lot)
                    qty_to_consume -= take_qty
                if qty_to_consume > 0:
                    raise UserError(f"Not enough raw material stock in ISIL lots for {product.name}")

            production.consumed_lot_ids = [(6, 0, [lot.id for lot in consumed_lots])]

            # Create finished product lot
            lot_vals = {
                'name': f"{production.product_id.name}_{production.id}",
                'product_id': production.product_id.id,
                'quantity': production.product_qty,
                'production_date': date.today(),
                'active': True,
                'lot_type': 'finished_product'
            }
            finished_lot = self.env['stock.lot.isil'].create(lot_vals)
            production.finished_lot_id = finished_lot

        return super().button_mark_done()

    def action_create_quality_check(self):
        """Create a quality check for this manufacturing order"""
        if not self:
            return
        for production in self:
            if not production.quality_check_id:
                quality_check = self.env['quality.check'].create({
                    'production_id': production.id,
                })
                production.quality_check_id = quality_check.id
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'quality.check',
            'res_id': self[0].quality_check_id.id,
            'view_mode': 'form',
            'target': 'current',
        }

class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    technical_validation_required = fields.Boolean(string='Technical Validation Required', default=False)
    is_complex_product = fields.Boolean(string='Complex Product', default=False)
    expert_email = fields.Char(string='Expert Email', help='Email address of technical expert for validation')

    @api.model
    def create(self, vals):
        # Automatically set complex product when technical validation is required
        if vals.get('technical_validation_required'):
            vals['is_complex_product'] = True
        return super().create(vals)

    @api.onchange('technical_validation_required')
    def _onchange_technical_validation_required(self):
        """Automatically set complex product when technical validation is required"""
        if self.technical_validation_required:
            self.is_complex_product = True
