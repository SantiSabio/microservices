#catalogo/app/routes.py
from flask import Blueprint

catalogo = Blueprint('catalog', __name__)

@catalogo.route('/catalog')
def get_catalogo():
    return "Este es el catálogo"
