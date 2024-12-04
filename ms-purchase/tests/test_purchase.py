# ms-purchase/tests/test_purchase.py
import unittest
from datetime import datetime
from app import create_app, db
from app.models import Purchase
from unittest.mock import MagicMock

class PurchaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_purchase_success(self):
        # Simula la verificación de la existencia del producto
        def mock_get_product_by_id(product_id):
            if product_id == 1:
                return {'id_producto': 1, 'name': 'Producto de prueba', 'description': 'Descripción de prueba'}
            return None

        # Mockear manualmente la función dentro del test
        self.app.config['get_product_by_id'] = mock_get_product_by_id

        purchase_data = {
            'product_id': 1,
            'purchase_date': '2024-10-06',  # Asegúrate de que este formato sea aceptado por tu aplicación
            'purchase_direction': '123 Calle Falsa'
        }
        response = self.client.post('/purchase/add', json=purchase_data)
        print(response.data)  # Imprime el contenido de la respuesta
        self.assertEqual(response.status_code, 201)

        with self.app.app_context():
            purchase = Purchase.query.filter_by(product_id=1).first()
            self.assertIsNotNone(purchase)
            self.assertEqual(purchase.purchase_direction, '123 Calle Falsa')

    def test_missing_fields(self):
        purchase_data = {
            'product_id': 1
        }
        response = self.client.post('/purchase/add', json=purchase_data)
        response_data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], 'Missing fields')

if __name__ == '__main__':
    unittest.main()
