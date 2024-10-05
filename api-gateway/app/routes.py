#api-gateway/app/routes.py
from flask import Blueprint, jsonify, request
import requests

api_gateway = Blueprint('api_gateway', __name__)

# URL con la que nos comunicamos al microservicio de catálogo
CATALOGO_SERVICE_URL = 'http://ms-catalogo:5001/catalogo'

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
