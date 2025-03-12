#ms-purchase/app/routes.py
from datetime import datetime
from flask import Blueprint, request, jsonify
from app.models import db, Purchase
from app import Config
import json

redis_client = Config.redis_client

# Definicion del Blueprint
purchase = Blueprint('purchase', __name__)

@purchase.route('/purchase/add', methods=['POST'])
def add_purchase():
    data = request.get_json()
    print(f"Datos recibidos: {data}")

    # Validar que los datos necesarios estén presentes
    required_fields = ['product_id', 'purchase_direction']
    if data is None or not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing fields'}), 400
    
    try:
        # Crear una nueva compra
        new_purchase = Purchase(
            product_id=data['product_id'],
            purchase_date=datetime.utcnow(),
            purchase_direction=data['purchase_direction']
        )

        # Agregar la nueva compra a la base de datos
        db.session.add(new_purchase)
        db.session.commit()
        
        # Guardar en cache después de confirmar la transacción
        purchase_data = {
            'id_purchase': new_purchase.id_purchase,
            'product_id': new_purchase.product_id,
            'purchase_direction': new_purchase.purchase_direction
        }
        

        try:
            redis_client.set(f"purchase:{new_purchase.id_purchase}", 
                        json.dumps(purchase_data), ex=3600)
        except Exception as cache_error:
            print(f"Cache error (non-critical): {cache_error}")

        return jsonify({
            'message': 'Purchase added successfully',
            'id_purchase': new_purchase.id_purchase}), 201
    
    except Exception as e:
        print(f"Error in add_purchase: {e}")
        db.session.rollback()  # Rollback en caso de error
        return jsonify({'error': str(e)}), 500
    

#Ruta para manejar la eliminacion de una compra
@purchase.route('/purchase/remove', methods=['POST'])
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
    
    except Exception as e:
        db.session.rollback()  # Hacer rollback en caso de error
        return jsonify({'error': str(e)}), 500
