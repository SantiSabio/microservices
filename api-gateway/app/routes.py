import os
from flask import Blueprint, jsonify, request
from app.services import build_saga, execute_saga
import requests

api_gateway = Blueprint('api_gateway', __name__)

CATALOG_SERVICE_URL = os.getenv('CATALOG_SERVICE_URL')
PURCHASE_SERVICE_URL = os.getenv('PURCHASE_SERVICE_URL')
STOCK_SERVICE_URL = os.getenv('STOCK_SERVICE_URL')
PAYMENT_SERVICE_URL = os.getenv('PAYMENT_SERVICE_URL')

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
    
# Consultar catálogo
@api_gateway.route('/catalog/<int:id>', methods=['GET'])
def search_product(id):
    get_product_url = f"{CATALOG_SERVICE_URL}/catalog/{id}"
    try:
        response = requests.get(get_product_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500
    
    return jsonify(response.json()), response.status_code
