from flask import Blueprint, request, jsonify
from .models import db, Payment
from app import Config
import json

redis_client = Config.redis_client
payment = Blueprint('payment', __name__)

# Ruta para manejar la creación de compras
@payment.route('/payment/add', methods=['POST'])
def add_payment():
    data = request.get_json()
    required_fields = ['product_id', 'price', 'payment_method','amount','id_purchase']

    missing_fields = [field for field in required_fields if field not in data]
    present_fields = {field: data[field] for field in required_fields if field in data}

    if missing_fields:
        return jsonify({'error': 'Missing fields', 'present_fields': present_fields}), 400

    try:
        new_payment = Payment(
            product_id=data['product_id'],
            amount=data['amount'],
            price=data['price'],
            id_purchase=data['id_purchase'],
            payment_method=data['payment_method']
        )

        # Add to database first to get the ID
        db.session.add(new_payment)
        db.session.flush()  # This assigns the ID without committing

        # Now we have the payment_id
        payment_data = {
            'payment_id': new_payment.payment_id,
            'product_id': new_payment.product_id,
            'amount': new_payment.amount,
            'price': new_payment.price,
            'id_purchase': new_payment.id_purchase,
            'payment_method': new_payment.payment_method
        }

        # Save to Redis cache
        if redis_client:
            try:
                redis_client.set(f"payment:{payment_data['payment_id']}", 
                           json.dumps(payment_data), ex=3600)
            except Exception as redis_err:
                print(f"Redis error (non-critical): {redis_err}")

        # Complete the transaction
        db.session.commit()

        # Return the payment ID for use in subsequent operations
        return jsonify({
            'message': 'Payment added successfully',
            'payment_id': new_payment.payment_id
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@payment.route('/payment/remove', methods=['POST'])
def remove_payment():
    data = request.get_json()

    # Validate payment_id exists and is not None
    if 'payment_id' not in data or data['payment_id'] is None:
        return jsonify({'error': 'Missing or invalid payment_id'}), 400

    try:
        # Use filter_by instead of get to avoid SQLAlchemy warning
        old_payment = Payment.query.filter_by(payment_id=data['payment_id']).first()

        if not old_payment:
            return jsonify({'error': 'Payment not found'}), 404

        # Remove from cache if it exists
        if redis_client:
            try:
                redis_client.delete(f"payment:{data['payment_id']}")
            except Exception as redis_err:
                print(f"Redis error (non-critical): {redis_err}")

        db.session.delete(old_payment)
        db.session.commit()

        return jsonify({'message': 'Payment removed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500