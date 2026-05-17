from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError


class TestManufacturingPlanning(TransactionCase):

    def setUp(self):
        super().setUp()
        self.product = self.env['product.product'].create({
            'name': 'Test Product',
            'type': 'product',
        })
        self.bom = self.env['mrp.bom'].create({
            'product_tmpl_id': self.product.product_tmpl_id.id,
            'product_qty': 1,
        })
        self.production = self.env['mrp.production'].create({
            'product_id': self.product.id,
            'product_qty': 10,
            'bom_id': self.bom.id,
        })

    def test_quality_check_creation(self):
        self.production.action_create_quality_check()
        self.assertTrue(self.production.quality_check_id)
        self.assertEqual(self.production.quality_check_id.production_id, self.production)

    def test_quality_check_required_before_mark_done(self):
        with self.assertRaises(UserError):
            self.production.button_mark_done()

    def test_quality_check_pass_on_high_score(self):
        self.production.action_create_quality_check()
        self.production.quality_check_id.quality_score = 80.0
        self.assertTrue(self.production.quality_check_id.passed)
        self.assertTrue(self.production.quality_check_done)

    def test_quality_check_fail_on_low_score(self):
        self.production.action_create_quality_check()
        self.production.quality_check_id.quality_score = 30.0
        self.assertFalse(self.production.quality_check_id.passed)
        self.assertFalse(self.production.quality_check_done)

    def test_technical_validation_sets_complex_product(self):
        bom = self.env['mrp.bom'].create({
            'product_tmpl_id': self.product.product_tmpl_id.id,
            'product_qty': 1,
            'technical_validation_required': True,
        })
        self.assertTrue(bom.is_complex_product)

    def test_quality_check_sequence(self):
        qc1 = self.env['quality.check'].create({'production_id': self.production.id})
        qc2 = self.env['quality.check'].create({'production_id': self.production.id})
        self.assertNotEqual(qc1.name, qc2.name)
        self.assertTrue(qc1.name.startswith('QC/'))

    def test_bom_cost_share_on_line(self):
        line = self.env['mrp.bom.line'].create({
            'bom_id': self.bom.id,
            'product_id': self.product.id,
            'product_qty': 2,
            'cost_share': 0.4,
        })
        self.assertEqual(line.cost_share, 0.4)


class TestQualityCheck(TransactionCase):

    def setUp(self):
        super().setUp()
        product = self.env['product.product'].create({'name': 'QC Product'})
        bom = self.env['mrp.bom'].create({
            'product_tmpl_id': product.product_tmpl_id.id,
            'product_qty': 1,
        })
        self.production = self.env['mrp.production'].create({
            'product_id': product.id,
            'product_qty': 5,
            'bom_id': bom.id,
        })

    def test_passed_threshold_is_50(self):
        qc = self.env['quality.check'].create({
            'production_id': self.production.id,
            'quality_score': 50.0,
        })
        self.assertTrue(qc.passed)

    def test_score_49_fails(self):
        qc = self.env['quality.check'].create({
            'production_id': self.production.id,
            'quality_score': 49.9,
        })
        self.assertFalse(qc.passed)

    def test_defects_field(self):
        qc = self.env['quality.check'].create({
            'production_id': self.production.id,
            'quality_score': 60.0,
            'defects_found': 3,
            'notes': 'Minor surface defects',
        })
        self.assertEqual(qc.defects_found, 3)
