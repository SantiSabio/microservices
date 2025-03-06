from flask import Blueprint, request, jsonify
from .models import db, Payment
from app import Config
import json
from tenacity import retry
from tenacity.wait import wait_fixed
from tenacity.stop import stop_after_attempt
from pybreaker import CircuitBreaker, CircuitBreakerError

breaker = CircuitBreaker(fail_max=10, reset_timeout=10)

payment = Blueprint('payment', __name__)

# Ruta para manejar la creación de compras
@payment.route('/payment/add', methods=['POST'])
@breaker
@retry(stop=stop_after_attempt(3), wait=wait_fixed(0.5))
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

        payment_data = {
            'payment_id': new_payment.payment_id,
            'product_id': new_payment.product_id,
            'amount': new_payment.amount,
            'price': new_payment.price,
            'id_purchase': new_payment.id_purchase,
            'payment_method': new_payment.payment_method
        }

        Config.r.set(f"payment:{payment_data['payment_id']}", json.dumps(payment_data), ex=3600)

        db.session.add(new_payment)
        db.session.commit()

        return jsonify({'message': 'Payment added successfully'}), 201
    except CircuitBreakerError as e:
        return jsonify({'error': 'Circuito Abierto'}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@payment.route('/payment/remove', methods=['POST'])
@breaker
@retry(stop=stop_after_attempt(3), wait=wait_fixed(0.5))
def remove_payment():
    data = request.get_json()

    if not 'payment_id' in data:
        return jsonify({'error': 'Missing fields'}), 400

    try:
        old_payment = Payment.query.get(data['payment_id'])

        if not old_payment:
            return jsonify({'error': 'Payment not found'}), 404

        db.session.delete(old_payment)
        db.session.commit()

        return jsonify({'message': 'Payment removed successfully'}), 200
    except CircuitBreakerError as e:
        return jsonify({'error': 'Circuito Abierto'}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
