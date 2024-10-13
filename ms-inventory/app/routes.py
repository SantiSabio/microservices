from flask import Blueprint, request, jsonify
from models import Stock, db

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/update', methods=['POST'])
def update_stock():
    data = request.json
    # Validar que los datos necesarios estén presentes
    required_fields = ['product_id', 'ammount', 'in_out']
    
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing fields'}), 400
    
    try:
        new_stock = Stock(
            producto_id=data['product_id'],
            cantidad=data['ammount'],
            entrada_salida=data['in_out']
        )
        db.session.add(new_stock)
        db.session.commit()
        return jsonify({'message': 'Stock updated successfully'}), 201
    except Exception as e:
        db.session.rollback()
        raise e
    
@inventory_bp.route('/remove', methods=['POST'])
def remove_stock():
    data = request.get_json()
    
    if not 'stock_id' in data:
        return jsonify({'error': 'Missing fields'}), 400
    
    try:
        # Buscar el stock
        old_stock = Stock.query.get(data['stock_id'])
        
        if not old_stock:
            return jsonify({'error': 'Stock not found'}), 404
        
        # Eliminar el pago encontrado
        db.session.delete(old_stock)
        db.session.commit()

        return jsonify({'message': 'Stock removed successfully'}), 200
    except Exception as e:
        db.session.rollback()  # Hacer rollback en caso de error
        return jsonify({'error': str(e)}), 500
