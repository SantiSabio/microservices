from flask import Blueprint, jsonify, request  # Importa request
import requests
api_gateway = Blueprint('api_gateway', __name__)

CART_SERVICE_URL='http://ms-cart:5002/purchase'

CATALOGO_SERVICE_URL = 'http://ms-catalog:5001/catalogo'

PAYMENT_SERVICE_URL= 'http://ms-payment:5004/finish'

@api_gateway.route('/productos', methods=['GET'])
def obtener_productos():
    try:
        # solicitud GET al microservicio de catálogo
        response = requests.get(CATALOGO_SERVICE_URL)
        
        # verificamos si la solicitud fue exitosa
        if response.status_code == 200:
            productos = response.json()
            return jsonify(productos), 200
        else:
            # si hay un error, retornara el código de estado del microservicio
            return jsonify({"error": "Error al obtener productos del catálogo"}), response.status_code
    except requests.exceptions.RequestException as e:
        # en caso de error en la solicitud, devuelve un error 500
        return jsonify({"error": str(e)}), 500

@api_gateway.route('/purchase', methods=['POST'])
def add_purchase():
    # Validar que los datos necesarios estén presentes en la solicitud
    required_fields = ['product_id', 'purchase_date', 'purchase_direction']
    if not all(field in request.json for field in required_fields):
        return jsonify({'error': 'Missing fields'}), 400
    
    # Reenviar la solicitud al microservicio ms-cart
    url = 'http://ms-cart:5002/purchase'
    try:
        response = requests.post(url, json=request.json)
        response.raise_for_status()  # Lanza una excepción si hay un error HTTP
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500



    return jsonify(response.json()), response.status_code


@api_gateway.route('/payment', methods=['POST'])
def add_payment():
    # Validar que los datos necesarios estén presentes en la solicitud
    required_fields = ['product_id', 'quantity', 'price','purchase_id','payment_method']

    if not all(field in request.json for field in required_fields):
        return jsonify({'error': 'Missing fields'}), 400
    
    # Reenviar la solicitud al microservicio ms-cart
    url = 'http://ms-payment:5004/finish'
    try:
        response = requests.post(url, json=request.json)
        response.raise_for_status()  # Lanza una excepción si hay un error HTTP
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500



    return jsonify(response.json()), response.status_code
