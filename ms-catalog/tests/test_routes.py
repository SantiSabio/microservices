import unittest, json
from flask_testing import TestCase
from app import create_app, db
from app.models import Product
from unittest.mock import patch, MagicMock

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

    @patch('app.models.Product.query.paginate')
    @patch('app.config.Config.r.client.set')
    def test_get_catalog(self, mock_set, mock_paginate):
        mock_paginate.return_value = MagicMock(items=[Product(**self.mock_product)], total=1, pages=1, page=1)
        response = self.client.get('/catalogo?page=1&per_page=10')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['products'][0]['id'], self.mock_product['id'])
        self.assertEqual(response.json['total'], 1)
        self.assertEqual(response.json['pages'], 1)
        self.assertEqual(response.json['current_page'], 1)

    @patch('app.models.Product.query.get')
    @patch('app.config.Config.r.exists')
    @patch('app.config.Config.r.get')
    @patch('app.config.Config.r.set')
    def test_set_is_active(self, mock_set, mock_get, mock_exists, mock_query_get):
        mock_query_get.return_value = Product(**self.mock_product)
        mock_exists.return_value = True
        mock_get.return_value = json.dumps(self.mock_product)
        response = self.client.patch('/set-active/1', json={"is_active": False})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['product']['is_active'], False)

    @patch('app.models.Product.query.get')
    def test_set_is_active_product_not_found(self, mock_query_get):
        mock_query_get.return_value = None
        response = self.client.patch('/set-active/500', json={"is_active": False})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"error": "Producto con ID 500 no encontrado"})

    def test_set_is_active_missing_param(self):
        response = self.client.patch('/set-active/1', json={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "El parámetro 'is_active' es requerido"})


if __name__ == '__main__':
    unittest.main()