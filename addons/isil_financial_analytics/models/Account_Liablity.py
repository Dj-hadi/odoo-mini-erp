from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountLiability(models.Model):
    """
    Accounts Payable / Liabilities (Analytics Only)

    This model is meant to:
      - Represent vendor liabilities linked to analytic accounts
      - Only REFER to the related asset in Asset Management
      - Avoid any recursive dependencies with other analytic models
    """
    _name = "isil.finance.analytics.account.liability"
    _description = "Accounts Payable (Analytics Only)"
    _order = "date desc, id desc"

    name = fields.Char(
        string="Reference",
        required=True,
        default=lambda self: _("Accounts Payable Entry"),
    )

    date = fields.Date(
        string="Date",
        required=True,
        default=fields.Date.context_today,
    )

    description = fields.Text(
        string="Description",
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
        required=True,
        default=lambda self: self.env.company.currency_id,
    )

    partner_id = fields.Many2one(
        "res.partner",
        string="Vendor",
        help="Vendor or creditor associated with this liability.",
    )

    move_id = fields.Many2one(
        "account.move",
        string="Journal Entry",
        help="Optional link to the accounting entry representing this payable.",
    )

    analytic_account_id = fields.Many2one(
        "isil_finance_analytics.analytic_account",
        string="Analytic Account / Project / Department",
        help="Analytic dimension used for profitability analysis (department/project).",
    )

    asset_id = fields.Many2one(
        "isil.finance.analytics.asset.management",
        string="Related Asset",
        help=(
            "The asset for which this liability exists. "
            "This is ONLY a reference; amounts can be queried from the asset model "
            "without duplicating values here."
        ),
    )


    debit = fields.Monetary(
        string="Debit",
        currency_field="currency_id",
        default=0.0,
        help="Debit amount for this liability (from accounting perspective).",
    )

    credit = fields.Monetary(
        string="Credit",
        currency_field="currency_id",
        default=0.0,
        help="Credit amount for this liability (usually the payable amount).",
    )

    balance = fields.Monetary(
        string="Balance (Debit - Credit)",
        currency_field="currency_id",
        compute="_compute_balance",
        store=True,
        help="Signed balance of this liability line.",
    )

    @api.depends("debit", "credit")
    def _compute_balance(self):
        """
        Simple, local computation: no cross-model dependencies and no recursion.
        """
        for rec in self:
            rec.balance = (rec.debit or 0.0) - (rec.credit or 0.0)

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("posted", "Posted"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        default="draft",
        required=True,
    )

    @api.constrains("debit", "credit")
    def _check_amounts_non_negative(self):
        for rec in self:
            if rec.debit and rec.debit < 0:
                raise ValidationError(_("Debit amount cannot be negative."))
            if rec.credit and rec.credit < 0:
                raise ValidationError(_("Credit amount cannot be negative."))

    def action_confirm(self):
        for rec in self:
            rec.state = "confirmed"

    def action_post(self):
        for rec in self:
            rec.state = "posted"

    def action_cancel(self):
        for rec in self:
            rec.state = "cancelled"

    def action_reset_to_draft(self):
        for rec in self:
            rec.state = "draft"
