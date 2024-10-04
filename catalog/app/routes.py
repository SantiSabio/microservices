#catalog/app/routes.py
from flask import Blueprint, jsonify
from .models import Product

catalog = Blueprint('catalog', __name__)

@catalog.route('/catalog', methods=['GET'])
def get_catalogo():
    products = Product.query.all()
    product_list = [{"id": p.id, "name": p.name, "price": p.price, "stock": p.stock} for p in products]
    return jsonify(product_list)
