from datetime import date
from odoo import models, fields, api

class AnalyticReport(models.Model):
    _name = "isil_finance_analytics.analytic_report"
    _description = "Analytic Accounting Report"
    _order = "id desc"

    name = fields.Char(
        string="Report Name",
        required=True,
        default="Analytic Report",
    )

    created_on = fields.Datetime(
        string="Created On",
        default=fields.Datetime.now,
        readonly=True,
    )

    generated_for = fields.Char(
        string="Generated For",
        readonly=True,
    )

    start_date = fields.Date(
        string="Start Date",
        required=True,
        default=date.today(),
    )

    end_date = fields.Date(
        string="End Date",
        required=True,
        default=date.today(),
    )

    analytic_account_id = fields.Many2one(
        "isil_finance_analytics.analytic_account",
        string="Analytic Account / Department",
    )

    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
    )

    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        default=lambda self: self.env.company.currency_id,
    )

    selling_price = fields.Float(
        string="Selling Price",
        help="Final selling price, filled manually.",
    )

    total_raw_materials = fields.Float(
        string="Total Raw Materials",
        help="Sum of raw materials spent, entered manually from the lines.",
    )

    total_debit = fields.Monetary(
        string="Total Debit",
        currency_field="currency_id",
        compute="_compute_totals",
        store=True,
        readonly=True,
    )

    total_credit = fields.Monetary(
        string="Total Credit",
        currency_field="currency_id",
        compute="_compute_totals",
        store=True,
        readonly=True,
    )

    total_balance = fields.Monetary(
        string="Total Balance",
        currency_field="currency_id",
        compute="_compute_totals",
        store=True,
        readonly=True,
    )

    line_ids = fields.One2many(
        "isil_finance_analytics.analytic_report_line",
        "report_id",
        string="Report Lines",
    )
    def action_generate_report(self):
        """Called when clicking 'Generate Report' button."""
        # Implement your logic or keep it empty for now
        return True
    @api.depends("line_ids.debit", "line_ids.credit")
    def _compute_totals(self):
        for rec in self:
            debit = sum(line.debit for line in rec.line_ids)
            credit = sum(line.credit for line in rec.line_ids)
            rec.total_debit = debit
            rec.total_credit = credit
            rec.total_balance = debit - credit
        
            if rec.analytic_account_id:
                rec.generated_for = rec.analytic_account_id.name
            else:
                rec.generated_for = "All Accounts"

# AnalyticReportLine is defined in analytic_report_line.py