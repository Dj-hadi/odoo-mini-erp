from odoo import models, fields


class AnalyticAccount(models.Model):
    _name = "isil_finance_analytics.analytic_account"
    _description = "ISIL Analytic Account (Departments)"
    _rec_name = "name"

    name = fields.Char(string="Department Name", required=True)
    code = fields.Char(string="Code")
    active = fields.Boolean(string="Active", default=True)

    description = fields.Text(string="Description")
