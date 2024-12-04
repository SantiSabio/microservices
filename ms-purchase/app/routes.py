#ms-purchase/app/routes.py
from datetime import datetime
from flask import Blueprint, request, jsonify
from app.models import db, Purchase
from app import Config
import json
from tenacity import retry
from tenacity.wait import wait_fixed
from tenacity.stop import stop_after_attempt
from pybreaker import CircuitBreaker, CircuitBreakerError

breaker = CircuitBreaker(fail_max=10, reset_timeout=10)

# Definicion del Blueprint
purchase = Blueprint('purchase', __name__)

# Ruta para manejar la creación de compras
@purchase.route('/purchase/add', methods=['POST'])
@breaker
@retry(stop=stop_after_attempt(3), wait=wait_fixed(0.5))
def add_purchase():
    data = request.get_json()

    # Validar que los datos necesarios estén presentes
    required_fields = ['product_id', 'purchase_direction']
    if data is None or not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing fields'}), 400
    
    try:
        # Crear una nueva compra
        new_purchase = Purchase(
            product_id=data['product_id'],
            purchase_date=datetime.utcnow(),  # Fecha de compra automática
            purchase_direction=data['purchase_direction']
        )

        purchase_data = {
            'id_purchase': new_purchase.id_purchase,
            'product_id': new_purchase.product_id,
            'purchase_direction': new_purchase.purchase_direction
        }
        
        Config.r.set(f"purchase:{new_purchase.id_purchase}", json.dumps(purchase_data), ex=3600)

        # Agregar la nueva compra a la base de datos
        db.session.add(new_purchase)
        db.session.commit()

        return jsonify({
            'message': 'Purchase added successfully',
            'id_purchase': new_purchase.id_purchase}), 201
    
    except CircuitBreakerError as e:
        return jsonify({'error': 'Circuito Abierto'}), 500
    except Exception as e:
        db.session.rollback()  # Rollback en caso de error
        return jsonify({'error': str(e)}), 500
    

@purchase.route('/purchase/remove', methods=['POST'])
@breaker
@retry(stop=stop_after_attempt(3), wait=wait_fixed(0.5))
#Ruta para manejar la eliminacion de una compra
def remove_purchase():
    data = request.get_json()

    if not 'id_purchase' in data:
        return jsonify({'error': 'Missing fields'}, 400)
    
    try:
        # Buscar la compra
        purchase = Purchase.query.get(data['id_purchase'])
        
        if not purchase:
            return jsonify({'error': 'Purchase not found'}), 404
        
        # Eliminar el pago encontrado
        db.session.delete(purchase)
        db.session.commit()
        return jsonify({'message': 'Purchase removed succesfully'}), 200
    
    except CircuitBreakerError as e:
        return jsonify({'error': 'Circuito Abierto'}), 500
    except Exception as e:
        db.session.rollback()  # Hacer rollback en caso de error
        return jsonify({'error': str(e)}), 500
