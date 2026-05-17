from odoo import models, fields

class FinanceTaxation(models.Model):
    _name = "isil.finance.taxation"
    _description = "Simplified Algerian taxation for analytics"

    vat_rate = fields.Float(string="VAT Rate (%)", default=19.0)
    cit_rate = fields.Float(string="Liability Tax CIT Rate (%)", default=26.0)
    irg_rate = fields.Float(string="Wagers Tax IRG Rate (%)", default=23.0)

    def asset_tax(self, amount):
        self.ensure_one()
        if not amount:
            return 0.0
        return amount * (self.cit_rate / 100.0)

    def liability_tax(self, amount):
        self.ensure_one()
        if not amount:
            return 0.0
        return amount * (self.cit_rate / 100.0)

    def wager_tax(self, annual_salary):
        self.ensure_one()
        if not annual_salary:
            return 0.0
        return annual_salary * (self.irg_rate / 100.0)