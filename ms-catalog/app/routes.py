from flask import Blueprint, json, jsonify, request
from .config import Config
from .models import Product


catalogo = Blueprint('catalogo', __name__)


@catalogo.route('/catalogo', methods=['GET'])
def get_catalogo():
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
