import os
import requests
from flask import Blueprint, jsonify, request
from .services import build_saga, execute_saga

api_gateway = Blueprint('api_gateway', __name__)

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
    return execute_saga(saga)
    
# Consultar catálogo
@api_gateway.route('/catalog/<int:id>', methods=['GET'])
def search_product(id):
    get_product_url = f"{os.getenv('CATALOG_SERVICE_URL')}/{id}"
    try:
        response = requests.get(get_product_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500
    
    return jsonify(response.json()), response.status_code
