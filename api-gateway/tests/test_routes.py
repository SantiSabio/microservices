from flask import jsonify
import unittest, requests
from unittest.mock import patch, MagicMock
from app import create_app

class TestApiGatewayRoutes(unittest.TestCase):
     
    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()

    @patch('app.services.build_saga')
    @patch('app.services.execute_saga')
    # Se verifica que los datos se envíen
    def test_create_order_success(self, mock_execute_saga):
        mock_execute_saga.return_value = {"message": "Datos enviados con éxito"}, 200

        response = self.client.post('/order', json={})
        response, status_code = mock_execute_saga()

        self.assertEqual(status_code, 200)
        self.assertEqual(response['message'], "Order processed successfully")

    def test_create_order_invalid_data(self, mock_execute_saga):
        mock_execute_saga.return_value = {'error': 'Datos de compra inválidos'}, 400

        response = self.client.post('/order', json={})
        response, status_code = mock_execute_saga()

        self.assertEqual(status_code, 400)
        self.assertEqual(response.json['error'], 'Datos de compra inválidos')

    @patch('requests.get')
    def test_search_product_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {'id': 1, 'name': 'Product'}
        mock_get.return_value = mock_response

        response = self.client.get('/catalog/1')
        self.assertEqual(response.status_code, 200)

    @patch('requests.get')
    def test_search_product_failure(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException('error'), 500

        response = self.client.get('/catalog/1')
        
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json['error'], 'Producto no encontrado')

    @patch('app.routes.activate_product')
    def test_update_product_status_success(self, mock_activate_product):
        mock_activate_product.return_value = {'product_id': 1, 'is_active': True}
        response = self.client.patch('/activate/1', json={'is_active': True})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Estado del producto actualizado correctamente')

    def test_update_product_status_missing(self):
        response = self.client.patch('/activate/1', json={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], 'El parámetro "is_active" es requerido')

    @patch('app.routes.activate_product')
    def test_update_product_status_failure(self, mock_activate_product):
        mock_activate_product.return_value = None
        response = self.client.patch('/activate/1', json={'is_active': True})
        self.assertEqual(response.status_code, 500)
        self.assertIsNotNone(response.json)
        self.assertEqual(response.json['error'], 'Fallo al actualizar el estado')

if __name__ == '__main__':
    unittest.main()

import unittest
from unittest.mock import patch, MagicMock
from your_module import send_order

class TestMicroservice(unittest.TestCase):

    @patch('your_module.send_order')
    def test_send_order_success(self, mock_send_order):
        # Configurar el mock para que devuelva una respuesta exitosa
        mock_send_order.return_value = {"message": "Order processed successfully"}, 200

        # Datos de prueba
        data = {
            'product_id': 1,
            'amount': 10,
            'payment_method': 'credit_card',
            'purchase_direction': 'north',
            'in_out': 'in',
            'price': 100.0
        }

        # Llamar a la función que se está probando
        response, status_code = send_order(data)

        # Verificar que la respuesta es la esperada
        self.assertEqual(status_code, 200)
        self.assertEqual(response['message'], "Order processed successfully")

if __name__ == '__main__':
    unittest.main()