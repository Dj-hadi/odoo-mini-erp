from odoo import models, fields

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    analytic_account_id = fields.Many2one(
        comodel_name="isil_finance_analytics.analytic_account",
        string="Analytic Account",
        help="Custom analytic account from ISIL Finance Analytics."
    )
