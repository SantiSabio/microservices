#ms-catalogo/app/routes.py
from flask import Blueprint, jsonify, request
import requests
from .models import Product
from app.config import Config
import json
catalogo = Blueprint('catalogo', __name__)



@catalogo.route('/catalogo', methods=['GET'])
def get_catalogo():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    products = Product.query.paginate(page=page, per_page=per_page)
    product_list = [{"id": p.id, "name": p.name, "price": p.price, "is_active": p.is_active} for p in products.items]

    for product in product_list:
        product_key = f"product:{product['id']}"
        Config.r.set(product_key, json.dumps(product), ex=3600)  


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