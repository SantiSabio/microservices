#catalogo/app/routes.py
from flask import Blueprint

catalogo = Blueprint('catalogo', __name__)

@catalogo.route('/catalogo')
def get_catalogo():
    return "Este es el catálogo"
