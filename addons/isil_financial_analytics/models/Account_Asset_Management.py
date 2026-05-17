from datetime import timedelta
from odoo import models, fields, api


class AccountAssetManagement(models.Model):
    _name = "isil.finance.analytics.asset.management"
    _description = "Tracks and records company assets"

    Asset_Name = fields.Char(string="Asset", required=True)
    Asset_quantity = fields.Integer(string="Quantity", default=1)

    material_type = fields.Selection(
        [
            ("concrete", "Concrete"),
            ("steel", "Steel"),
            ("brick", "Brick"),
            ("wood", "Wood"),
            ("glass", "Glass"),
            ("other", "Other"),
        ],
        string="Material Type",
    )

    Debit_Score = fields.Float(string="Debit")
    Credit_Score = fields.Float(string="Credit")

    Is_Tangible = fields.Boolean(string="Is Tangible", required=True, default=True)

    Expiry_Date = fields.Datetime(string="Expiry Date")

    Tax_Amount = fields.Float(string="Tax Amount")
    Total_With_Tax = fields.Float(string="Total With Tax")

    @api.model
    def create(self, vals):
        rec = super().create(vals)

        taxation = self.env["isil.finance.taxation"].search([], limit=1)
        if taxation and rec.Debit_Score:
            tax = taxation.asset_tax(rec.Debit_Score)
            rec.write({
                "Tax_Amount": tax,
                "Total_With_Tax": rec.Debit_Score + tax,
            })

        self.env["isil.finance.analytics.general.ledger.line"].create_from_asset(rec)

        if rec.Credit_Score and rec.Credit_Score > 0:
            self._sync_to_receivable(rec)

        return rec

    def write(self, vals):
        res = super().write(vals)

        for asset in self:
            if asset.Credit_Score and asset.Credit_Score > 0:
                self._sync_to_receivable(asset)

        return res

    def _sync_to_receivable(self, asset):
        Receivable = self.env["isil.finance.analytics.account.receivable"]

        existing = Receivable.search([("asset_id", "=", asset.id)])

        vals = {
            "asset_id": asset.id,
            "Product_Name": asset.Asset_Name,
            "Debit_Score": asset.Debit_Score,
            "Credit_Score": asset.Credit_Score,
            "project_sale_price": asset.Credit_Score,
        }

        if existing:
            existing.with_context(skip_sync=True).write(vals)
        else:
            vals.setdefault("Comp_Name", "Unknown Customer")
            vals.setdefault("Dept_Date", fields.Datetime.now())
            vals.setdefault("Dept_Length", 30)
            Receivable.with_context(skip_sync=True).create(vals)

    def get_expiring_assets(self):
        today = fields.Datetime.now()
        horizon = today + timedelta(days=7)
        return self.search([
            ("Expiry_Date", ">=", today),
            ("Expiry_Date", "<=", horizon),
        ])
