from odoo import models, fields, api

class QualityCheck(models.Model):
    _name = 'quality.check'
    _description = 'Quality Control Check'

    name = fields.Char(string='Reference', required=True, default='New')
    production_id = fields.Many2one('mrp.production', string='Manufacturing Order', required=True)
    product_id = fields.Many2one('product.product', string='Product', related='production_id.product_id', store=True)
    check_date = fields.Datetime(string='Check Date', default=fields.Datetime.now)
    responsible_id = fields.Many2one(
    'hr.custom.employee',
    string="Responsible",
    domain="[('department', '=', 'production'), ('position', '=', 'supervisor')]"
)


    passed = fields.Boolean(string='Passed', compute='_compute_passed', store=True)
    notes = fields.Text(string='Notes')
    defects_found = fields.Integer(string='Defects Found')
    quality_score = fields.Float(string='Quality Score', required=True, default=0.0)

    @api.depends('quality_score')
    def _compute_passed(self):
        for record in self:
            # Auto-pass if score >= 50, auto-fail if score < 50
            record.passed = record.quality_score >= 50.0
            # Update manufacturing order status automatically
            if record.production_id:
                record.production_id.write({
                    'quality_check_done': record.passed
                })

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('quality.check') or 'New'
        return super().create(vals)
