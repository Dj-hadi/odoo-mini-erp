from odoo import models

class ReportSalesMonthly(models.AbstractModel):
    _name = "report.isil_dashboard.report_sales_monthly_template"
    _description = "Monthly Sales Report"

    def _get_report_values(self, docids, data=None):
        docs = self.env["isil_dashboard.kpi"].browse(docids)
        return {
            "doc_ids": docids,
            "doc_model": "isil_dashboard.kpi",
            "docs": docs,
            "data": data,
        }

class ReportStockValued(models.AbstractModel):
    _name = "report.isil_dashboard.report_stock_valued_template"
    _description = "Valued Stock Report"

    def _get_report_values(self, docids, data=None):
        docs = self.env["isil_dashboard.kpi"].browse(docids)
        return {
            "doc_ids": docids,
            "doc_model": "isil_dashboard.kpi",
            "docs": docs,
            "data": data,
        }