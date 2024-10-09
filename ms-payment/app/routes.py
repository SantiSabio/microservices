#ms-payment/app/routes.py
from flask import Blueprint, request,jsonify
from .models import db, Payment

payment = Blueprint('payment', __name__)

# Ruta para manejar la creación de compras
@payment.route('/finish', methods=['POST'])
def add_payment():
    data = request.get_json()

    # Validar que los datos necesarios estén presentes
    required_fields = ['product_id', 'quantity', 'price','purchase_id','payment_method']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing fields'}), 400
    
    try:
        # Crear una nueva compra
        new_payment = Payment(
            product_id=data['product_id'],
            quantity=data['quantity'],
            price=data['price'],
            purchase_id=data['purchase_id'],
            payment_method=data['payment_method']
        )

        # Agregar la nueva compra a la base de datos
        db.session.add(new_payment)
        db.session.commit()

        return jsonify({'message': 'Purchase added successfully'}), 201
    except Exception as e:
        db.session.rollback()  # Hacer rollback en caso de error
        return jsonify({'error': str(e)}), 500
