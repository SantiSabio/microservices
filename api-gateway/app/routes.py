
from flask import Blueprint, jsonify, request  # Importa request
import requests
api_gateway = Blueprint('api_gateway', __name__)

CART_SERVICE_URL='http://ms-cart:5004/purchase'

@api_gateway.route('/purchase', methods=['POST'])
def add_purchase():
    # Validar que los datos necesarios estén presentes en la solicitud
    required_fields = ['product_id', 'purchase_date', 'purchase_direction']
    if not all(field in request.json for field in required_fields):
        return jsonify({'error': 'Missing fields'}), 400
    
    # Reenviar la solicitud al microservicio ms-cart
    url = 'http://ms-cart:5004/purchase'
    try:
        response = requests.post(url, json=request.json)
        response.raise_for_status()  # Lanza una excepción si hay un error HTTP
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

    return jsonify(response.json()), response.status_code


