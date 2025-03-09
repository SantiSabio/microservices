import unittest
from unittest.mock import patch
from app import create_app
from app.saga_order import add_purchase, remove_purchase, add_payment, remove_payment, update_stock

class TestSagaOrder(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()

    # Se "mockea" response_from_url para inyectarla
    @patch('app.saga_order.response_from_url')
    def test_add_purchase(self, mock_response):
        # Valor que devuelve el mock
        mock_response.return_value = {'status_code': 201, 'id_purchase': 1}
        response = add_purchase(1, '123 Main St')
        self.assertEqual(response, {'id_purchase': 1})

    @patch('app.saga_order.response_from_url')
    def test_add_purchase_failure(self, mock_response):
        mock_response.return_value = {'status_code': 400, 'error': 'Bad Request'}
        with self.assertRaises(Exception):
            add_purchase(1, '123 Main St')

    @patch('app.saga_order.response_from_url')
    def test_remove_purchase(self, mock_response):
        mock_response.return_value = {'status_code': 200}
        response = remove_purchase(1)
        self.assertEqual(response['status_code'], 200)

    @patch('app.saga_order.response_from_url')
    def test_remove_purchase_failure(self, mock_response):
        mock_response.return_value = {'status_code': 404, 'error': 'Not Found'}
        with self.assertRaises(Exception):
            remove_purchase(1)

    @patch('app.saga_order.response_from_url')
    def test_add_payment(self, mock_response):
        mock_response.return_value = {'status_code': 201, 'payment_id': 1}
        response = add_payment(1, 1, 100.0, 1, 'Credit Card')
        self.assertEqual(response['status_code'], 201)
        self.assertEqual(response['payment_id'], 1)

    @patch('app.saga_order.response_from_url')
    def test_add_payment_failure(self, mock_response):
        mock_response.return_value = {'status_code': 400, 'error': 'Bad Request'}
        with self.assertRaises(Exception):
            add_payment(1, 1, 100.0, 1, 'Credit Card')

    @patch('app.saga_order.response_from_url')
    def test_remove_payment(self, mock_response):
        mock_response.return_value = {'status_code': 200}
        response = remove_payment(1)
        self.assertEqual(response['status_code'], 200)

    @patch('app.saga_order.response_from_url')
    def test_remove_payment_failure(self, mock_response):
        mock_response.return_value = {'status_code': 404, 'error': 'Not Found'}
        with self.assertRaises(Exception):
            remove_payment(1)

    @patch('app.saga_order.response_from_url')
    def test_update_stock(self, mock_response):
        mock_response.return_value = {'status_code': 200, 'stock_id': 1}
        response = update_stock(1, 10, 'in')
        self.assertEqual(response['status_code'], 200)
        self.assertEqual(response['stock_id'], 1)

    @patch('app.saga_order.response_from_url')
    def test_update_stock_failure(self, mock_response):
        mock_response.return_value = {'status_code': 400, 'error': 'Bad Request'}
        with self.assertRaises(Exception):
            update_stock(1, 10, 'in')

if __name__ == '__main__':
    unittest.main()
