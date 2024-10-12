#ms-cart/app/routes.py
from datetime import datetime
from flask import Blueprint, request,jsonify
from models import db, Purchase

cart = Blueprint('cart', __name__)

# Ruta para manejar la creación de compras
@cart.route('/purchase/add', methods=['POST'])
def add_purchase():
    data = request.get_json()

    # Validar que los datos necesarios estén presentes
    required_fields = ['product_id', 'purchase_date', 'purchase_direction']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing fields'}), 400
    
    try:
        # Crear una nueva compra
        new_purchase = Purchase(
            product_id=data['product_id'],
            purchase_date=datetime.strptime(data['purchase_date'], '%Y-%m-%d'),
            purchase_direction=data['purchase_direction']
        )

        # Agregar la nueva compra a la base de datos
        db.session.add(new_purchase)
        db.session.commit()

        return jsonify({
            'message': 'Purchase added successfully',
            'purchase_id': new_purchase.id_purchase}), 201
    except Exception as e:
        db.session.rollback()  # Rollback en caso de error
        return jsonify({'error': str(e)}), 500
