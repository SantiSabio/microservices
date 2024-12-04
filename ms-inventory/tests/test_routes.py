import unittest
from app import create_app
from app.config import Config
import redis
from unittest.mock import patch, MagicMock

class TestInventoryRoutes(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config.from_object(Config)
        self.redis_client = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=1)
        self.redis_client.flushdb()  # Limpiar la base de datos de pruebas antes de cada prueba

    def tearDown(self):
        self.redis_client.flushdb()  # Limpiar la base de datos de pruebas después de cada prueba

    def test_update_stock(self):
        response = self.client.post('/inventory/update', json={
            "product_id": 1,
            "ammount": 10,
            "in_out": "in"
        })
        self.assertEqual(response.status_code, 200)

    def test_update_stock_missing_fields(self):
        response = self.client.post('/inventory/update', json={
            "product_id": 1,
            "ammount": 10
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], 'Missing fields')

    @patch('app.routes.redis_client.lock')
    def test_update_stock_lock_in_use(self, mock_lock):
        # Mock del comportamiento del lock
        mock_lock_obj = mock_lock.return_value
        mock_lock_obj.acquire.return_value = False  # Simula que el lock no se puede adquirir porque está en uso

        # Mock de los datos de entrada
        data = {
            'product_id': 1,
            'ammount': 10,
            'in_out': 'in'
        }

        response = self.client.post('/inventory/update', json=data)
        
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json['error'], 'Recurso solicitado en uso')

    @patch('app.routes.redis_client.get')
    def test_update_stock_circuit_open(self, mock_redis_get):
        mock_redis_get.return_value = b'abierto'

        response = self.client.post('/inventory/update', json={
            "product_id": 1,
            "ammount": 10,
            "in_out": "in"
        })
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json['error'], 'Circuito Abierto')

    @patch('app.routes.session.query')
    def test_update_stock_not_found(self, mock_query):
        mock_query.return_value.filter_by.return_value.first.return_value = None

        response = self.client.post('/inventory/update', json={
            "product_id": 1,
            "ammount": 10,
            "in_out": "in"
        })
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], 'Stock not found')

    @patch('app.routes.session.query')
    def test_update_stock_insufficient_stock(self, mock_query):
        stock_item = MagicMock()
        stock_item.stock_quantity = 5
        mock_query.return_value.filter_by.return_value.first.return_value = stock_item

        response = self.client.post('/inventory/update', json={
            "product_id": 1,
            "ammount": 10,
            "in_out": "out"
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], 'Insufficient stock')

    @patch('app.routes.session.query')
    def test_update_stock_invalid_in_out(self, mock_query):
        stock_item = MagicMock()
        stock_item.stock_quantity = 5
        mock_query.return_value.filter_by.return_value.first.return_value = stock_item

        response = self.client.post('/inventory/update', json={
            "product_id": 1,
            "ammount": 10,
            "in_out": "invalid"
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], 'Invalid in_out value')

if __name__ == '__main__':
    unittest.main()
