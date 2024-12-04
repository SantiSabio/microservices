# tests/test_saga_order.py
import unittest
from unittest.mock import patch, Mock
from app.saga_order import add_purchase, remove_purchase, add_payment, remove_payment, update_stock, remove_stock

class TestSagaOrder(unittest.TestCase):

    @patch('app.saga_order.response_from_url')
    def test_add_purchase(self, mock_response):
        mock_response.return_value = Mock(status_code=201, json=lambda: {'id_purchase': 1})
        response = add_purchase(1, '123 Main St')
        self.assertEqual(response, 1)

    @patch('app.saga_order.response_from_url')
    def test_remove_purchase(self, mock_response):
        mock_response.return_value = Mock(status_code=200)
        response = remove_purchase(1)
        self.assertEqual(response.status_code, 200)

    @patch('app.saga_order.response_from_url')
    def test_add_payment(self, mock_response):
        mock_response.return_value = Mock(status_code=201, json=lambda: {'payment_id': 1})
        response = add_payment(1, 100.0, 'Credit Card')
        self.assertEqual(response, {'payment_id': 1})

    @patch('app.saga_order.response_from_url')
    def test_remove_payment(self, mock_response):
        mock_response.return_value = Mock(status_code=200)
        response = remove_payment(1)
        self.assertEqual(response.status_code, 200)
    
    @patch('app.saga_order.response_from_url')
    def test_update_stock(self, mock_response):
        mock_response.return_value = Mock(status_code=200, json=lambda: {'stock_id': 1})
        response = update_stock(1, 10, 'in')
        self.assertEqual(response, {'stock_id': 1})

    @patch('app.saga_order.response_from_url')
    def test_remove_stock(self, mock_response):
        mock_response.return_value = Mock(status_code=200)
        response = remove_stock(1)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()