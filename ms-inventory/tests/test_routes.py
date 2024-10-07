import unittest
from app import create_app

class TestInventoryRoutes(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_update_stock(self):
        response = self.client.post('/inventory/update', json={
            "producto_id": 1,
            "cantidad": 10.5,
            "entrada_salida": 1
        })
        self.assertEqual(response.status_code, 200)

# Test Docker:
# docker exec -it microservices-api-gateway-1 python -m unittest discover -s tests
