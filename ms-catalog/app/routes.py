#ms-catalog/app/routes.py
from flask import Blueprint, jsonify, request
import requests
from .models import Product, db
from app.config import Config
import json


catalog = Blueprint('catalog', __name__)


@catalog.route('/catalog', methods=['GET'])
def get_catalog():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    products = Product.query.paginate(page=page, per_page=per_page)
    product_list = [{"id": p.id, "name": p.name, "price": p.price, "is_active": p.is_active} for p in products.items]
    #obtenemos la lista de productos y la guardamos en redis
    for product in product_list:
        if Config.redis_client is not None:
            try:
                product_key = f"product:{product['id']}"
                Config.redis_client.set(product_key, json.dumps(product), ex=3600)
            except Exception as e:
                print(f"Redis caching error: {str(e)}")

    #Devolvemos un json con todos los productos
    return jsonify({
        "products": product_list,
        "total": products.total,
        "pages": products.pages,
        "current_page": products.page
    })


@catalog.route('/catalog/<int:product_id>', methods=['GET'])
#primer paso validar producto existente
def validate_product(product_id):
    product = Product.query.get(product_id)
    
    if product and product.is_active == True:
        return jsonify({"exists": True}), 200
    else:
        return jsonify({"exists": False}), 404
    

@catalog.route('/set-active/<int:product_id>', methods=['PATCH'])
def set_is_active(product_id):
    # Obtener los datos del request
    data = request.json
    
    # Validar que se incluya el parámetro is_active
    if 'is_active' not in data:
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
        db.session.commit()
        
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
        db.session.rollback()
        return jsonify({"error": f"Error al actualizar el estado del producto: {str(e)}"}), 500


@catalog.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    try:
        product = Product.query.get(product_id)
        
        if not product:
            return jsonify({"error": "Product not found"}), 404
        
        product_data = {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "is_active": product.is_active
        }
        #lo almacenamos al producto existente en redis
        Config.r.set(f"product:{product_id}", json.dumps(product_data), ex=3600)
        return jsonify(product_data)
        
    except Exception as e:
        print(f"Error in get_product: {str(e)}")
        return jsonify({"error": str(e)}), 500