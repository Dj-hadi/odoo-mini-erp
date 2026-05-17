from odoo import models, fields


class AnalyticReportLine(models.Model):
    _name = "isil_finance_analytics.analytic_report_line"
    _description = "Analytic Report Line"
    _order = "date asc"

    report_id = fields.Many2one(
        "isil_finance_analytics.analytic_report",
        string="Report",
        ondelete="cascade",
    )

    date = fields.Date(string="Date")
    ref = fields.Char(string="Reference")

    analytic_account_id = fields.Many2one(
        "isil_finance_analytics.analytic_account",
        string="Analytic Account",
    )

    debit = fields.Float(string="Debit")
    credit = fields.Float(string="Credit")

    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        default=lambda self: self.env.company.currency_id,
    )
