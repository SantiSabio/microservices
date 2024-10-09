import unittest
from app import create_app,db
from app.models import Payment
class PaymentTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@microservices-mysql_db-1:3306/catalogodb'
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        

    def test_payment_success(self):
        purchase_data = {
            'product_id' : 1,
            'quantity' : 3,
            'price' : 320.5,
            'purchase_id' :  7,
            'payment_method' : 'mercado_pago'

        }
        response = self.client.post('/finish', json=purchase_data)
        print(response.data)  # Imprime el contenido de la respuesta
        self.assertEqual(response.status_code, 201)
        
        with self.app.app_context():
            payment = Payment.query.filter_by(product_id=1).first()
            self.assertIsNotNone(payment)
            self.assertEqual(payment.payment_method,'mercado_pago')     

    def test_missing_fields(self):
        purchase_data = {
            'product_id': 1
        }
        with self.app.app_context():
            response = self.client.post('/finish', json=purchase_data)
            response_data = response.get_json()
            self.assertEqual(response.status_code, 400)
            self.assertIn('error', response_data)
            self.assertEqual(response_data['error'], 'Missing fields')

if __name__ == '__main__':
    unittest.main()