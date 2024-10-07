# api-gateway/tests/test_productos.py
import unittest
from app import create_app

class TestProductos(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_obtener_productos(self):
        response = self.client.get('/productos')
        self.assertEqual(response.status_code, 200)
        self.assertIn('products', response.get_json())

if __name__ == '__main__':
    unittest.main()
