from odoo import models, fields, api


class Invoicing(models.Model):
    _name = "isil.finance.analytics.invoicing"
    _description = "Invoicing & bills helpers for finance analytics"

    name = fields.Char(string="Name", default="Finance Invoicing Helper")

    @api.model
    def create_customer_invoice(self, client_name, date, amount, product_name=False):        
        receivable_model = self.env["isil.finance.analytics.account.receivable"]
        asset_model = self.env["isil.finance.analytics.asset.management"]
        receivable = receivable_model.create({
            "Comp_Name": client_name,                       
            "Product_Name": product_name or "Customer Invoice",
            "Dept_Date": date,
            "Debit_Score": amount,
        })
        asset_model.create({
            "Asset_Name": product_name or ("Product sold to %s" % client_name),
            "Asset_quantity": 1,
            "Debit_Score": -amount,
            "Is_Tangible": False,
        })

        return receivable
    
    @api.model
    def create_vendor_bill(self, vendor_name, date, amount, product_name=False):
        liability_model = self.env["isil.finance.analytics.account.liability"]
        liability = liability_model.create({
            "name": product_name or "Vendor Bill",
            "date": date,
            "credit": amount,
        })
        return liability

    @api.model
    def CreateCustomerInvoice(self, name, date, number):
        return self.create_customer_invoice(name, date, number)

    @api.model
    def CreateVendorBill(self, name, date, number):
        return self.create_vendor_bill(name, date, number)