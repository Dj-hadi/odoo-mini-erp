from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestTaxation(TransactionCase):

    def setUp(self):
        super().setUp()
        self.tax = self.env['isil.finance.taxation'].create({
            'vat_rate': 19.0,
            'cit_rate': 26.0,
            'irg_rate': 23.0,
        })

    def test_asset_tax(self):
        self.assertAlmostEqual(self.tax.asset_tax(1000), 260.0)

    def test_liability_tax(self):
        self.assertAlmostEqual(self.tax.liability_tax(500), 130.0)

    def test_wager_tax(self):
        self.assertAlmostEqual(self.tax.wager_tax(2000), 460.0)

    def test_zero_amount(self):
        self.assertEqual(self.tax.asset_tax(0), 0.0)


class TestAccountLiability(TransactionCase):

    def test_balance_computed(self):
        liability = self.env['isil.finance.analytics.account.liability'].create({
            'name': 'Test Liability',
            'date': '2026-01-01',
            'debit': 700.0,
            'credit': 300.0,
        })
        self.assertEqual(liability.balance, 400.0)

    def test_negative_debit_raises(self):
        with self.assertRaises(ValidationError):
            self.env['isil.finance.analytics.account.liability'].create({
                'name': 'Bad Liability',
                'date': '2026-01-01',
                'debit': -100.0,
                'credit': 0.0,
            })

    def test_state_transitions(self):
        liability = self.env['isil.finance.analytics.account.liability'].create({
            'name': 'Transition Test',
            'date': '2026-01-01',
        })
        self.assertEqual(liability.state, 'draft')
        liability.action_confirm()
        self.assertEqual(liability.state, 'confirmed')
        liability.action_post()
        self.assertEqual(liability.state, 'posted')
        liability.action_reset_to_draft()
        self.assertEqual(liability.state, 'draft')


class TestAnalyticReport(TransactionCase):

    def setUp(self):
        super().setUp()
        self.account = self.env['isil_finance_analytics.analytic_account'].create({
            'name': 'Test Department',
            'code': 'TD01',
        })

    def test_report_totals_computed(self):
        report = self.env['isil_finance_analytics.analytic_report'].create({
            'name': 'Test Report',
            'start_date': '2026-01-01',
            'end_date': '2026-12-31',
            'analytic_account_id': self.account.id,
        })
        self.env['isil_finance_analytics.analytic_report_line'].create([
            {'report_id': report.id, 'debit': 1000.0, 'credit': 300.0},
            {'report_id': report.id, 'debit': 500.0, 'credit': 200.0},
        ])
        self.assertEqual(report.total_debit, 1500.0)
        self.assertEqual(report.total_credit, 500.0)
        self.assertEqual(report.total_balance, 1000.0)

    def test_generated_for_set_from_account(self):
        report = self.env['isil_finance_analytics.analytic_report'].create({
            'name': 'Dept Report',
            'start_date': '2026-01-01',
            'end_date': '2026-12-31',
            'analytic_account_id': self.account.id,
        })
        self.assertEqual(report.generated_for, 'Test Department')


class TestGeneralLedger(TransactionCase):

    def test_create_from_asset(self):
        asset = self.env['isil.finance.analytics.asset.management'].create({
            'Asset_Name': 'Office Equipment',
            'Is_Tangible': True,
            'Debit_Score': 5000.0,
        })
        lines = self.env['isil.finance.analytics.general.ledger.line'].search([
            ('source_model', '=', 'isil.finance.analytics.asset.management'),
            ('source_ref', '=', str(asset.id)),
        ])
        self.assertTrue(lines)
        self.assertEqual(lines[0].debit, 5000.0)
        self.assertEqual(lines[0].account_type, 'asset')


class TestAccountWages(TransactionCase):

    def setUp(self):
        super().setUp()
        self.dept = self.env['isil_finance_analytics.analytic_account'].create({
            'name': 'HR Department',
        })

    def test_net_salary_computed(self):
        wage = self.env['isil.finance.analytics.account.wages'].create({
            'name': 'March Salary',
            'date': '2026-03-31',
            'department_id': self.dept.id,
            'amount_gross': 100000.0,
            'tax_amount': 23000.0,
        })
        self.assertEqual(wage.amount_net, 77000.0)

    def test_state_workflow(self):
        wage = self.env['isil.finance.analytics.account.wages'].create({
            'name': 'April Salary',
            'date': '2026-04-30',
            'department_id': self.dept.id,
            'amount_gross': 50000.0,
        })
        self.assertEqual(wage.state, 'draft')
        wage.action_confirm()
        self.assertEqual(wage.state, 'confirmed')
        wage.action_mark_paid()
        self.assertEqual(wage.state, 'paid')
