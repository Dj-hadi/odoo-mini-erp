from odoo import models, fields, api


class FinanceGeneralLedgerLine(models.Model):
    _name = "isil.finance.analytics.general.ledger.line"
    _description = "Analytical General Ledger Line"
    _order = "date, id"

    date = fields.Datetime(string="Date", required=True)
    partner_name = fields.Char(string="Partner")
    description = fields.Char(string="Description")

    analytic_account_id = fields.Many2one(
        "isil_finance_analytics.analytic_account",
        string="Department (Analytic Account)",
    )

    source_model = fields.Char(
        string="Source Model",
        help="Technical name of the source model.",
    )
    source_ref = fields.Char(
        string="Source Reference",
        help="ID or name of the source record.",
    )

    account_type = fields.Selection(
        [
            ("asset", "Asset"),
            ("liability", "Liability"),
            ("receivable", "Receivable"),
            ("payable", "Payable"),
            ("wage", "Wage / Payroll"),
        ],
        string="Account Type",
        required=True,
    )

    debit = fields.Float(string="Debit", digits="Account")
    credit = fields.Float(string="Credit", digits="Account")

    balance = fields.Float(
        string="Balance",
        compute="_compute_balance",
        store=True,
    )

    @api.depends("debit", "credit")
    def _compute_balance(self):
        for line in self:
            line.balance = (line.debit or 0.0) - (line.credit or 0.0)
    @api.model
    def create_from_receivable(self, receivable):
        return self.create({
            "date": receivable.Dept_Date,
            "partner_name": receivable.Comp_Name,
            "description": receivable.Product_Name,
            "source_model": receivable._name,
            "source_ref": str(receivable.id),
            "account_type": "receivable",
            "debit": receivable.Debit_Score or 0.0,
            "credit": receivable.Credit_Score or 0.0,
        })

    @api.model
    def create_from_liability(self, liability):
        return self.create({
            "date": liability.Dept_Date,
            "partner_name": liability.Comp_Name,
            "description": liability.Product_Name,
            "source_model": liability._name,
            "source_ref": str(liability.id),
            "account_type": "liability",
            "debit": liability.Debit_Score or 0.0,
            "credit": liability.Credit_Score or 0.0,
        })

    @api.model
    def create_from_asset(self, asset):
        return self.create({
            "date": asset.Expiry_Date or fields.Datetime.now(),
            "partner_name": False,
            "description": asset.Asset_Name,
            "source_model": asset._name,
            "source_ref": str(asset.id),
            "account_type": "asset",
            "debit": asset.Debit_Score or 0.0,
            "credit": asset.Credit_Score or 0.0,
        })

    @api.model
    def create_from_wage(self, wage):
        return self.create({
            "date": wage.wage_date,
            "partner_name": wage.employee_name,
            "description": "Wage payment",
            "source_model": wage._name,
            "source_ref": str(wage.id),
            "account_type": "wage",
            "debit": 0.0,
            "credit": wage.credit_score or 0.0,
        })

    @api.model
    def rebuild_from_sources(self):
        self.search([]).unlink()

        receivables = self.env["isil.finance.analytics.account.receivable"].search([])
        for rec in receivables:
            self.create_from_receivable(rec)

        liabilities = self.env["isil.finance.analytics.account.liability"].search([])
        for liability in liabilities:
            self.create_from_liability(liability)

        assets = self.env["isil.finance.analytics.asset.management"].search([])
        for asset in assets:
            self.create_from_asset(asset)

        wages = self.env["isil.finance.analytics.account.wages"].search([])
        for wage in wages:
            self.create_from_wage(wage)

        return True
