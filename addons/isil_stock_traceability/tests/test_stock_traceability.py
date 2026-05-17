from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestStockLotIsil(TransactionCase):

    def setUp(self):
        super().setUp()
        self.product = self.env['product.product'].create({
            'name': 'ISIL Test Product',
            'type': 'product',
        })

    def _make_lot(self, name='LOT001', qty=100.0, lot_type='raw_material'):
        return self.env['stock.lot.isil'].create({
            'name': name,
            'product_id': self.product.id,
            'quantity': qty,
            'lot_type': lot_type,
        })

    def test_consume_partial(self):
        lot = self._make_lot(qty=100.0)
        lot.consume(30)
        self.assertEqual(lot.quantity, 70.0)
        self.assertTrue(lot.active)

    def test_consume_all_deactivates_lot(self):
        lot = self._make_lot(qty=50.0)
        lot.consume(50)
        self.assertEqual(lot.quantity, 0.0)
        self.assertFalse(lot.active)

    def test_consume_more_than_available_raises(self):
        lot = self._make_lot(qty=10.0)
        with self.assertRaises(ValidationError):
            lot.consume(20)

    def test_expiry_before_production_raises(self):
        with self.assertRaises(ValidationError):
            self.env['stock.lot.isil'].create({
                'name': 'BAD_LOT',
                'product_id': self.product.id,
                'quantity': 10.0,
                'lot_type': 'raw_material',
                'production_date': '2026-06-01',
                'expiry_date': '2026-01-01',
            })

    def test_lot_name_unique_per_product(self):
        self._make_lot('DUPE_LOT')
        with self.assertRaises(Exception):
            self._make_lot('DUPE_LOT')

    def test_lots_count_on_product(self):
        self._make_lot('RM001', lot_type='raw_material')
        self._make_lot('RM002', lot_type='raw_material')
        self._make_lot('FP001', lot_type='finished_product')
        self.assertEqual(self.product.lots_count, 2)


class TestStockAlert(TransactionCase):

    def setUp(self):
        super().setUp()
        self.product = self.env['product.product'].create({
            'name': 'Alert Test Product',
            'type': 'product',
            'reorder_threshold': 5.0,
        })

    def test_alert_created_when_stock_low(self):
        self.env['stock.lot.isil'].create({
            'name': 'LOW001',
            'product_id': self.product.id,
            'quantity': 3.0,
            'lot_type': 'raw_material',
        })
        alert = self.env['stock.alert'].search([
            ('product_id', '=', self.product.id),
            ('is_active', '=', True),
        ], limit=1)
        self.assertTrue(alert)
        self.assertEqual(alert.current_qty, 3.0)

    def test_alert_resolved_when_stock_sufficient(self):
        lot = self.env['stock.lot.isil'].create({
            'name': 'ENOUGH001',
            'product_id': self.product.id,
            'quantity': 3.0,
            'lot_type': 'raw_material',
        })
        lot.quantity = 20.0
        self.product._check_alert(self.product)
        alert = self.env['stock.alert'].search([
            ('product_id', '=', self.product.id),
            ('is_active', '=', True),
        ], limit=1)
        self.assertFalse(alert)

    def test_action_mark_resolved(self):
        alert = self.env['stock.alert'].create({
            'product_id': self.product.id,
            'current_qty': 1.0,
            'reorder_threshold': 5.0,
        })
        alert.action_mark_resolved()
        self.assertFalse(alert.is_active)
        self.assertEqual(alert.resolved_by.id, self.env.uid)
