#api-gateway/app/routes.py
from flask import Blueprint, jsonify
import requests

api_gateway = Blueprint('api_gateway', __name__)

@api_gateway.route('/productos', methods=['GET'])
def obtener_productos():
    # Lógica para obtener productos
    return  "Estos son los productos"
