from datetime import timedelta
from odoo import models, fields, api


class AccountReceivable(models.Model):
    _name = "isil.finance.analytics.account.receivable"
    _description = "External receivables such as customer debts"

    Comp_Name = fields.Char(string="Counterparty", required=True)
    Product_Name = fields.Char(string="Product / Service", required=True)

    Dept_Date = fields.Datetime(string="Date", required=True)
    Dept_Length = fields.Integer(string="Debt Length", required=True)

    Maturity_Date = fields.Datetime(
        string="Maturity Date",
        compute="_compute_maturity_date",
        store=True,
    )

    @api.depends("Dept_Date", "Dept_Length")
    def _compute_maturity_date(self):
        for record in self:
            if record.Dept_Date and record.Dept_Length:
                record.Maturity_Date = record.Dept_Date + timedelta(days=record.Dept_Length)
            else:
                record.Maturity_Date = False

    asset_id = fields.Many2one(
        "isil.finance.analytics.asset.management",
        string="Related Asset / Project",
        help="If set and the asset has a positive Credit, "
             "this receivable will automatically pull its values.",
    )

    Debit_Score = fields.Float(string="Debit")
    Credit_Score = fields.Float(string="Credit")

    project_sale_price = fields.Float(
        string="Sold Project Price",
        help="Value of the project when sold (from asset credit).",
    )

    Tax_Amount = fields.Float(string="Tax Amount")
    Total_With_Tax = fields.Float(string="Total With Tax")


    def _prepare_vals_from_asset(self, vals):
        """
        Pull values from asset only if NOT coming from skip_sync.
        Prevents endless recursion.
        """
        if self.env.context.get("skip_sync"):
            return vals

        asset_id = vals.get("asset_id")
        if not asset_id:
            return vals

        asset_model = self.env["isil.finance.analytics.asset.management"]

        if isinstance(asset_id, int):
            asset = asset_model.browse(asset_id)
        elif isinstance(asset_id, (list, tuple)) and len(asset_id) >= 2:
            asset = asset_model.browse(asset_id[1])
        else:
            return vals

        if asset and asset.Credit_Score > 0:
            vals.setdefault("Product_Name", asset.Asset_Name)
            vals.setdefault("Debit_Score", asset.Debit_Score)
            vals.setdefault("Credit_Score", asset.Credit_Score)
            vals.setdefault("project_sale_price", asset.Credit_Score)

        return vals

    @api.model
    def create(self, vals):
        if not self.env.context.get("skip_sync"):
            vals = self._prepare_vals_from_asset(vals)

        rec = super().create(vals)


        taxation = self.env["isil.finance.taxation"].search([], limit=1)
        base = rec.Credit_Score or rec.Debit_Score
        if taxation and base:
            tax = taxation.liability_tax(base)
            rec.write({
                "Tax_Amount": tax,
                "Total_With_Tax": base + tax,
            })

        return rec

    def write(self, vals):
        if not self.env.context.get("skip_sync"):
            vals = self._prepare_vals_from_asset(vals)

        res = super().write(vals)

        taxation = self.env["isil.finance.taxation"].search([], limit=1)
        for rec in self:
            base = rec.Credit_Score or rec.Debit_Score
            if taxation and base:
                tax = taxation.liability_tax(base)
                rec.Tax_Amount = tax
                rec.Total_With_Tax = base + tax

        return res

    def get_payable_liabilities(self):
        today = fields.Datetime.now()
        horizon = today + timedelta(days=7)
        return self.search([
            ("Maturity_Date", ">=", today),
            ("Maturity_Date", "<=", horizon),
        ])
