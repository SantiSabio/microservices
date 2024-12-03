# tests/test_saga_order.py
import unittest
from unittest.mock import patch
from app.saga_order import add_purchase, remove_purchase, add_payment

class TestSagaOrder(unittest.TestCase):

    @patch('app.saga_order.response_from_url')
    def test_add_purchase(self, mock_response):
        mock_response.return_value = {'purchase_id': 1}
        response = add_purchase(1, '123 Main St')
        self.assertEqual(response, {'purchase_id': 1})

    @patch('app.saga_order.response_from_url')
    def test_remove_purchase(self, mock_response):
        mock_response.return_value = 200
        response = remove_purchase(1)
        self.assertEqual(response, 200)

    @patch('app.saga_order.response_from_url')
    def test_add_payment(self, mock_response):
        mock_response.return_value = {'payment_id': 1}
        response = add_payment(1, 100.0, 'Credit Card')
        self.assertEqual(response, {'payment_id': 1})

if __name__ == '__main__':
    unittest.main()