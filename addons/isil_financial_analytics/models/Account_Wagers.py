from odoo import api, fields, models, _


class AccountWages(models.Model):
    _name = "isil.finance.analytics.account.wages"
    _description = "Wage and Salary Payments (Analytics Only)"
    _order = "date desc, id desc"
    employee_name = fields.Char(string="Employee Name")
    wage_date = fields.Date(string="Wage Date")
    credit_score = fields.Float(string="Credit Score")
    name = fields.Char(
        string="Reference",
        required=True,
        default=lambda self: _("Wage Payment"),
    )
    date = fields.Date(
        string="Payment Date",
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
    analytic_account_id = fields.Many2one(
        "isil_finance_analytics.analytic_account",
        string="Analytic Account / Project",
        help=(
            "Analytic account associated with this wage payment. "
            "Usually refers to the project or cost center."
        ),
    )
    department_id = fields.Many2one(
        "isil_finance_analytics.analytic_account",
        string="Department (Analytic Account)",
        required=True,
        help=(
            "Department analytic account. This is required for analytic reports. "
            "It is automatically filled from analytic_account_id when possible."
        ),
    )

    amount_gross = fields.Monetary(
        string="Gross Salary",
        currency_field="currency_id",
        required=True,
        default=0.0,
    )

    tax_amount = fields.Monetary(
        string="Taxes",
        currency_field="currency_id",
        default=0.0,
    )

    amount_net = fields.Monetary(
        string="Net Salary",
        currency_field="currency_id",
        compute="_compute_amount_net",
        store=True,
        help="Computed as Gross Salary - Taxes.",
    )

    @api.depends("amount_gross", "tax_amount")
    def _compute_amount_net(self):
        """
        Local computation only. No dependency on other models.
        """
        for rec in self:
            gross = rec.amount_gross or 0.0
            tax = rec.tax_amount or 0.0
            rec.amount_net = gross - tax

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("paid", "Paid"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        default="draft",
        required=True,
    )

    @api.model
    def _get_default_department_from_vals(self, vals):
        department_id = vals.get("department_id")
        if department_id:
            return department_id

        analytic_id = vals.get("analytic_account_id")
        if analytic_id:
            return analytic_id

        return False

    @api.model
    def create(self, vals):
        if not vals.get("department_id"):
            dept_id = self._get_default_department_from_vals(vals)
            if dept_id:
                vals["department_id"] = dept_id

        return super(AccountWages, self).create(vals)

    def write(self, vals):
        for rec in self:
            if "department_id" in vals and vals["department_id"]:
                continue

            if "analytic_account_id" in vals and vals["analytic_account_id"]:
                dept_id = vals.get("analytic_account_id")
                if dept_id:
                    vals.setdefault("department_id", dept_id)

        return super(AccountWages, self).write(vals)

    def action_confirm(self):
        for rec in self:
            rec.state = "confirmed"

    def action_mark_paid(self):
        for rec in self:
            rec.state = "paid"

    def action_cancel(self):
        for rec in self:
            rec.state = "cancelled"

    def action_reset_to_draft(self):
        for rec in self:
            rec.state = "draft"