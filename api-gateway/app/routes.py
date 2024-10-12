from flask import Blueprint, jsonify, request
from services import build_saga, execute_saga

api_gateway = Blueprint('api_gateway', __name__)

CATALOG_SERVICE_URL = 'http://ms-catalog:5001/catalog'
PURCHASE_SERVICE_URL = 'http://ms-purchase:5002/purchase'
PAYMENT_SERVICE_URL = 'http://ms-payment:5004/payment'
STOCK_SERVICE_URL = 'http://ms-inventory:5004/stock'

# Comenzar orden
@api_gateway.route('/order', methods=['POST'])
def create_order(data):
    # Obtener datos de la orden
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Datos de compra inválidos'}), 400

    # Crear el contexto de la saga
    saga_context = {
        'product_id': data['product_id'],
        'ammount': data['ammount'],
        'pay_method': data['pay_method'],
        'address': data['address']
    }
    saga = build_saga(saga_context)
    order_result = execute_saga(saga)

    return order_result
    
# Consultar catálogo
# @app.route('/catalog', methods=['GET'])
# El usuario busca por 'product_id' y obtiene los atributos del producto
# def search_product(id):
# get_product_url = CATALOG_SERVICE_URL

    # try:
    #     response = requests.post(get_product_url, json=product)
    #     response.raise_for_status()
    # except requests.exceptions.RequestException as e:
    #     return jsonify({'error': str(e)}), 500
    
    # return jsonify(response.json()), response.status_code