#ms-cart/app/routes.py
import requests
from flask import Blueprint

cart = Blueprint('cart', __name__)

@cart.route('/cart')
def get_cart():
    return "Este es el carrito"

def get_product(product_id):
    url = f'http://ms-catalogo:5001/products/{product_id}'
    response= requests.get(url)
    if response.status_code==200:
        return response.json()
    return None

