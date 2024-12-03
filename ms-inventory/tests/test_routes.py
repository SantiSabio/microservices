import unittest
from app import create_app
from app.config import Config
import redis
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



    def test_update_stock_lock_in_use(self):
        # Mock de los datos de entrada
        data = {
            'product_id': 1,
            'ammount': 10,
            'in_out': 'in'
        }
        
        # Adquirir el lock manualmente para simular que está en uso
        lock = self.redis_client.lock('stock_lock', timeout=10)
        lock.acquire(blocking=False)
        
        response = self.client.post('/inventory/update', json=data)
        
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json['error'], 'Recurso solicitado en uso')
        
        lock.release()