from flask import Blueprint, jsonify, request
from .models import Product, db
from app.config import Config
import json

catalogo = Blueprint('catalogo', __name__)

@catalogo.route('/catalogo', methods=['GET'])
def get_catalog():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    products = Product.query.paginate(page=page, per_page=per_page)
    product_list = [{"id": p.id, "name": p.name, "price": p.price, "is_active": p.is_active} for p in products.items]

    for product in product_list:
        product_key = f"product:{product['id']}"
        Config.r.client.set(product_key, json.dumps(product), ex=3600)  

    return jsonify({
        "products": product_list,
        "total": products.total,
        "pages": products.pages,
        "current_page": products.page
    })


@catalogo.route('/catalogo/<int:product_id>', methods=['GET'])
#primer paso validar producto existente
def validate_product(product_id):
    product = Product.query.get(product_id)
    
    if product and product.is_active == True:
        return jsonify({"exists": True}), 200
    else:
        return jsonify({"exists": False}), 404
    

@catalogo.route('/set-active/<int:product_id>', methods=['PATCH'])
def set_is_active(product_id):
    # Obtener los datos del request
    data = request.json
    
    # Validar que se incluya el parámetro is_active
    if not data or 'is_active' not in data:
        return jsonify({"error": "El parámetro 'is_active' es requerido"}), 400
    
    # Convertir explícitamente a booleano para asegurar el tipo correcto
    is_active = bool(data['is_active'])
    
    # Buscar el producto por ID
    product = Product.query.get(product_id)
    
    # Verificar si el producto existe
    if not product:
        return jsonify({"error": f"Producto con ID {product_id} no encontrado"}), 404
    
    # Actualizar el estado del producto
    try:
        product.is_active = is_active
        db.session().commit()
        
        # Actualizar la caché si existe
        product_key = f"product:{product_id}"
        if Config.r.exists(product_key):
            product_data = json.loads(Config.r.get(product_key))
            product_data["is_active"] = is_active
            Config.r.set(product_key, json.dumps(product_data), ex=3600)
        
        # Responder con el producto actualizado
        return jsonify({
            "message": f"Estado del producto actualizado correctamente a {'activo' if is_active else 'inactivo'}",
            "product": {
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "is_active": product.is_active
            }
        }), 200
    except Exception as e:
        # Revertir cambios en caso de error
        db.session().rollback()
        return jsonify({"error": f"Error al actualizar el estado del producto: {str(e)}"}), 500