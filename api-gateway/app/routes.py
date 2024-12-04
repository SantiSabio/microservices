from flask import Blueprint, jsonify, request
from app.services import build_saga, execute_saga

api_gateway = Blueprint('api_gateway', __name__)

CATALOG_SERVICE_URL = 'http://ms-catalog:5001/catalog'
PURCHASE_SERVICE_URL = 'http://ms-purchase:5002/purchase'
STOCK_SERVICE_URL = 'http://ms-inventory:5003/stock'
PAYMENT_SERVICE_URL = 'http://ms-payment:5004/payment'

# Comenzar orden
@api_gateway.route('/order', methods=['POST','GET'])
def create_order():
    # Obtener datos de la orden
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Datos de compra inválidos'}), 400

    # Crear el contexto de la saga
    saga_context = {
        'product_id': data['product_id'],
        'amount': data['amount'],
        'payment_method': data['payment_method'],
        'purchase_direction': data['purchase_direction'],
        'in_out': data['in_out'],
        'price': data['price']
    }
    # Construir saga
    saga = build_saga(saga_context)
    order_result = execute_saga(saga)

    return order_result
    
