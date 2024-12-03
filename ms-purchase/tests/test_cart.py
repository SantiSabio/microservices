import unittest
from app import create_app, db
from app.models import Purchase
class PurchaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@microservices-mysql_db-1:3306/catalogodb'
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    

    def test_purchase_success(self):
        purchase_data = {
            'product_id': 1,
            'purchase_date': '2024-10-06',
            'purchase_direction': '123 Calle Falsa'
        }
        response = self.client.post('/purchase', json=purchase_data)
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
        with self.app.app_context():
            response = self.client.post('/purchase', json=purchase_data)
            response_data = response.get_json()
            self.assertEqual(response.status_code, 400)
            self.assertIn('error', response_data)
            self.assertEqual(response_data['error'], 'Missing fields')

if __name__ == '__main__':
    unittest.main()