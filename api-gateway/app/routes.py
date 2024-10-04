from flask import Blueprint, jsonify
import requests

api_gateway = Blueprint('api_gateway', __name__)

@api_gateway.route('/productos', methods=['GET'])
def obtener_productos():
    response = requests.get('http://catalogo:5001/productos')
    return jsonify(response.json())
