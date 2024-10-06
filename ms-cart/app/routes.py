#ms-cart/app/routes.py
import datetime,requests
from flask import Blueprint, request,jsonify
from .models import db, Purchase
cart = Blueprint('cart', __name__)

def get_product(product_id):
    url = f'http://ms-catalogo:5001/products/{product_id}'
    response= requests.get(url)
    if response.status_code==200:
        return response.json()
    return None


@cart.route('/purchase', methods=['POST'])
def create_purchase():
    data = request.json
    new_purchase = Purchase(
        product_id=data['product_id'],
        purchase_date=data['purchase_date'],
        purchase_direction=data['purchase_direction']
    )
    db.session.add(new_purchase)
    db.session.commit()
    return jsonify({'id_purchase': new_purchase.id_purchase}), 201

