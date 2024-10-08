#ms-catalogo/app/routes.py
from flask import Blueprint, jsonify, request
from .models import Product

catalogo = Blueprint('catalogo', __name__)


@catalogo.route('/catalogo', methods=['GET'])
def get_catalogo():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    products = Product.query.paginate(page=page, per_page=per_page)
    product_list = [{"id": p.id, "name": p.name, "price": p.price, "stock": p.stock} for p in products.items]
    
    return jsonify({
        "products": product_list,
        "total": products.total,
        "pages": products.pages,
        "current_page": products.page
    })
