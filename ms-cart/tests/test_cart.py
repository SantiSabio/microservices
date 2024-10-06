import unittest
from app import create_app
from app.models import Purchase

class TestCart(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
    
    def test_get_cart(self):
        # Test para la ruta GET /cart
        response = self.client.get('/cart')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Este es el carrito', response.data)

    def test_agregar_compra(self):
        # Datos de prueba para la compra
        purchase_data = {
            'product_id': 1,
            'purchase_direction': '123 Main St, Springfield',  # Asegúrate de que este campo coincida con el que espera el microservicio
            'purchase_date': '2024-10-10'  # Ajusta según lo que necesites
        }

        # Realiza la solicitud POST al API Gateway para agregar la compra
        response = self.client.post('/purchase', json=purchase_data)  # Cambia '/cart' a '/purchase'
        print(response.json)  # Cambia el print para que imprima la respuesta en formato JSON

        # Verifica que la respuesta sea correcta
        self.assertEqual(response.status_code, 201)
        self.assertIn('id_purchase', response.json)  # Asegúrate de que la respuesta contiene el ID de la compra

        # Verifica que la compra se haya añadido a la base de datos
        with self.app.app_context():
            purchase = Purchase.query.filter_by(product_id=1).first()  # Asegúrate de que estás buscando correctamente
            self.assertIsNotNone(purchase)
            self.assertEqual(purchase.purchase_direction, '123 Main St, Springfield')  # Corrige 'purchase_address' a 'purchase_direction'

    def test_compra_missing_data(self):
        # Test cuando falta algún dato en la solicitud de compra
        data = {
            'product_id': 1
            # Falta la dirección de envío
        }
        response = self.client.post('/purchase', json=data)
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
