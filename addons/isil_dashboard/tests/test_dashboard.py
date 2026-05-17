from odoo.tests.common import TransactionCase


class TestDashboardKPI(TransactionCase):

    def test_create_kpi(self):
        kpi = self.env['isil_dashboard.kpi'].create({
            'name': 'Revenue',
            'value': 50000.0,
            'target': 100000.0,
            'kpi_type': 'sales',
            'unit': 'DZD',
        })
        self.assertEqual(kpi.kpi_type, 'sales')
        self.assertTrue(kpi.is_active)

    def test_kpi_default_active(self):
        kpi = self.env['isil_dashboard.kpi'].create({'name': 'KPI Test'})
        self.assertTrue(kpi.is_active)


class TestStrategicObjective(TransactionCase):

    def test_create_objective(self):
        obj = self.env['isil_dashboard.objective'].create({
            'name': 'Increase Sales by 20%',
            'status': 'on_track',
            'target_value': 1000000.0,
            'current_value': 400000.0,
            'progress': 40.0,
        })
        self.assertEqual(obj.status, 'on_track')
        self.assertEqual(obj.progress, 40.0)

    def test_objective_with_kpis(self):
        kpi = self.env['isil_dashboard.kpi'].create({'name': 'Revenue KPI', 'kpi_type': 'sales'})
        obj = self.env['isil_dashboard.objective'].create({
            'name': 'Revenue Goal',
            'kpi_ids': [(4, kpi.id)],
        })
        self.assertIn(kpi, obj.kpi_ids)


class TestDashboardReports(TransactionCase):

    def test_generate_sales_report_returns_dict(self):
        dashboard = self.env['isil_dashboard.dashboard'].create({})
        result = dashboard.generate_sales_report()
        self.assertIn('total_revenue', result)
        self.assertIn('total_orders', result)
        self.assertIn('report_date', result)
        self.assertIsInstance(result['total_revenue'], float)

    def test_generate_stock_report_returns_dict(self):
        dashboard = self.env['isil_dashboard.dashboard'].create({})
        result = dashboard.generate_stock_report()
        self.assertIn('total_products', result)
        self.assertIn('low_stock_count', result)
        self.assertIn('total_value', result)

    def test_generate_full_report_has_all_sections(self):
        dashboard = self.env['isil_dashboard.dashboard'].create({})
        result = dashboard.generate_full_report()
        for section in ('sales', 'stock', 'manufacturing', 'hr'):
            self.assertIn(section, result)

    def test_open_kpi_action_returns_act_window(self):
        dashboard = self.env['isil_dashboard.dashboard'].create({})
        action = dashboard.open_kpi_action()
        self.assertEqual(action['type'], 'ir.actions.act_window')
        self.assertEqual(action['res_model'], 'isil_dashboard.kpi')
