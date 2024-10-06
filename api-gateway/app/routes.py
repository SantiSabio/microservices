
from flask import Blueprint, jsonify, request  # Importa request
import requests
api_gateway = Blueprint('api_gateway', __name__)

@api_gateway.route('/productos', methods=['GET'])
def obtener_productos():
    # Lógica para obtener productos
    return  "Estos son los productos"


@api_gateway.route('/cart', methods=['GET', 'POST'])
def manage_cart():
    if request.method == 'GET':  # Cambia requests.method a request.method
        url = 'http://ms-cart:5002/cart'
        response = requests.get(url)
        return jsonify(response.json()), response.status_code
    elif request.method == 'POST':
        url = 'http://ms-cart:5002/compra'
        response = requests.post(url, json=request.get_json())  # Usa request.get_json()
        return jsonify(response.json()), response.status_code



@api_gateway.route('/purchase', methods=['POST'])
def add_purchase():
    # Validar que los datos necesarios estén presentes
    if not request.json or 'product_id' not in request.json or 'purchase_date' not in request.json or 'purchase_direction' not in request.json:
        return jsonify({'error': 'Missing fields'}), 400
    
    # Construir la URL del microservicio de compras
    url = 'http://ms-cart:5000/purchase'
    response = requests.post(url, json=request.json)  # Reenviar los datos al microservicio

    return jsonify(response.json()), response.status_code

