#catalog/app/routes.py
from flask import Blueprint

catalog = Blueprint('catalog', __name__)

@catalog.route('/catalog')
def get_catalogo():
    return "Este es el catálogo"
