import unittest
from app import create_app, db
from app.models import Purchase


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
        # Datos de prueba
        product_id = 1
        purchase_direction = '123 Calle Falsa'

        purchase_data = {
            'product_id': product_id,
            'purchase_direction': purchase_direction
        }
        # Se realiza la solicitud
        response = self.client.post('/purchase/add', json=purchase_data)
        print(response.data)
        self.assertEqual(response.status_code, 201)

        # Se imprime la respuesta
        response_json = response.get_json()
        print(response_json)

        # Se obtiene el ID de la compra
        purchase_id = response_json.get('purchase_id')

        # Se verifica que se haya creado correctamente
        try:
            with self.app.app_context():
                purchase = Purchase.query.filter_by(id_purchase=purchase_id).first()
                self.assertIsNotNone(purchase)
                self.assertEqual(purchase.purchase_direction, purchase_data["purchase_direction"])
        
        # Se elimina la compra
        finally:
            with self.app.app_context():
                if purchase_id:
                    purchase = Purchase.query.filter_by(id_purchase=purchase_id).first()  # Use the correct primary key attribute
                    if purchase:
                        db.session.delete(purchase)
                        db.session.commit()

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
