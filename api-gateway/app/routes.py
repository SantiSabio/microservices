import os, requests
from flask import Blueprint, jsonify, request

from app.services import build_saga, execute_saga
from app.utils import activate_product 
api_gateway = Blueprint('api_gateway', __name__)

# Comenzar orden
@api_gateway.route('/order', methods=['POST','GET'])
def create_order():
    # Obtener datos de la orden
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Datos de compra inválidos'}), 400

    # Validar que contiene los campos requeridos
    required_fields = ['product_id', 'amount', 'payment_method', 'purchase_direction', 'in_out']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'El campo {field} es requerido'}), 400
    
    # Obtener el precio del producto desde el servicio de catálogo
    try:
        # Hard-code the URL format to ensure correctness
        base_url = os.getenv('CATALOG_SERVICE_URL', 'http://ms-catalog:5001')
        # Remove any trailing /catalog if present
        if base_url.endswith('/catalog'):
            base_url = base_url[:-8]  # Remove trailing /catalog
        elif base_url.endswith('/'):
            base_url = base_url[:-1]  # Remove trailing slash
            
        # Now construct the correct URL
        catalog_url = f"{base_url}/{data['product_id']}"
        
        print(f"Calling catalog service at: {catalog_url}")
        
        catalog_response = requests.get(catalog_url)
        print(f"Catalog response: {catalog_response.text}")
        
        catalog_response.raise_for_status()
        product_info = catalog_response.json()
        print(f"Product info: {product_info}")
        
        # Get the is_active value
        is_active = product_info.get('is_active')
        print(f"Raw is_active value: {is_active}, Type: {type(is_active).__name__}")

        # Convert various forms of boolean-like values to actual boolean
        if isinstance(is_active, str):
            is_active = is_active.lower() in ('true', 'yes', '1')
        elif isinstance(is_active, int):
            is_active = bool(is_active)
        # Otherwise assume it's already a boolean

        print(f"Processed is_active value: {is_active}")

        # Check if product is active
        if not is_active:
            return jsonify({'error': 'El producto no está activo o no existe'}), 400
        
        # Obtener el precio del producto
        price = product_info.get('price')
        if not price:
            return jsonify({'error': 'No se pudo obtener el precio del producto'}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error al comunicarse con el servicio de catálogo: {str(e)}'}), 500

    # Crear el contexto de la saga con el precio obtenido del catálogo
    saga_context = {
        'product_id': data['product_id'],
        'amount': data['amount'],
        'payment_method': data['payment_method'],
        'purchase_direction': data['purchase_direction'],
        'in_out': data['in_out'],
        'price': price  # Precio obtenido del catálogo
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
    

 # Importar la función que ya tienes

# Endpoint para activar/desactivar productos
@api_gateway.route('/activate/<int:product_id>', methods=['PATCH'])
def update_product_status(product_id):
    data = request.get_json()
    
    if 'is_active' not in data:
        return jsonify({'error': 'El parámetro is_active es requerido'}), 400
        
    # Usar la función del archivo saga_order.py para activar el producto
    result = activate_product(product_id,is_active=data['is_active'])
    
    if result is None:
        return jsonify({'error': 'No se pudo actualizar el estado del producto'}), 500
        
    return jsonify({'message': 'Estado del producto actualizado correctamente', 'data': result}), 200

