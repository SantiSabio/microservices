import unittest
import json
from app import create_app, db
from app.models import Payment

class PaymentTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@microservices-mysql_db-1:3306/catalogodb'
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            # Insertar datos necesarios en la tabla `purchase`
            db.session.execute("INSERT INTO purchase (product_id, purchase_date, purchase_direction) VALUES (1, NOW(), '123 Main St, Cityville')")
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_payment_success(self):
        # Limpia la tabla payment antes de la prueba
        with self.app.app_context():
            db.session.execute("DELETE FROM payment")
            db.session.commit()

        payment_data = {
            'product_id': 1,
            'quantity': 3,
            'price': 320.5,
            'purchase_id': 1,
            'payment_method': 'mercado_pago'
        }
        response = self.client.post('/payment/add', json=payment_data)
        print(response.data)
        self.assertEqual(response.status_code, 201)

        with self.app.app_context():
            payment = Payment.query.filter_by(product_id=1).order_by(Payment.payment_id.desc()).first()
            self.assertIsNotNone(payment)
            self.assertEqual(payment.payment_method, 'mercado_pago')

    def test_missing_fields(self):
        payment_data = {
            'product_id': 1
        }
        response = self.client.post('/payment/add', json=payment_data)
        response_data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], 'Missing fields')

if __name__ == '__main__':
    unittest.main()
