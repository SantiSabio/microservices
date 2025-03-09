import os, requests
from flask import Blueprint, jsonify, request
from app.services import build_saga, execute_saga
from app.utils import activate_product

api_gateway = Blueprint('api_gateway', __name__)

# Comenzar orden
@api_gateway.route('/order', methods=['POST', 'GET'])
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
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

# Endpoint para activar/desactivar productos
@api_gateway.route('/activate/<int:product_id>', methods=['PATCH'])
def update_product_status(product_id):
    data = request.get_json()

    if 'is_active' not in data:
        return jsonify({'error': 'El parámetro is_active es requerido'}), 400

    # Usar la función del archivo saga_order.py para activar el producto
    result = activate_product(product_id, is_active=data['is_active'])

    if result is None:
        return jsonify({'error': 'No se pudo actualizar el estado del producto'}), 500
        
    return jsonify({'message': 'Estado del producto actualizado correctamente', 'data': result}), 200
