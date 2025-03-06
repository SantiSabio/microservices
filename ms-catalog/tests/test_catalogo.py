import unittest
from unittest.mock import patch
from flask_testing import TestCase
from app import create_app, db
from app.models import Product

class TestCatalog(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        return app

    def setUp(self):
        self.client = self.app.test_client()
        self.mock_product = {
            "id": 1,
            "is_active": True,
            "name": "Laptop",
            "price": 1500.5
        }
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    @patch('app.models.Product.query.get')
    def test_get_product_success(self, mock_get):
        mock_get.return_value = Product(**self.mock_product)
        response = self.client.get('/catalog/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, self.mock_product)

    @patch('app.models.Product.query.get')
    def test_get_product_not_found(self, mock_get):
        mock_get.return_value = None
        response = self.client.get('/catalog/500')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {'error': 'Product not found'})

    @patch('app.models.Product.query.get')
    def test_get_product_invalid_id(self):
        response = self.client.get('/catalog/0')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {'error': 'Invalid ID'})


if __name__ == '__main__':
    unittest.main()