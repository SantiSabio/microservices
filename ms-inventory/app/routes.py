from flask import Blueprint, request, jsonify
from .models import db, Product, InventoryTransaction
from .services import process_inventory_update

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/')
def index():
    return "<h1>Éste es el inventario</h1>"

@inventory_bp.route('/update_inventory', methods=['POST'])
def update_inventory():
    data = request.get_json()
    try:
        product_id = data['product_id']
        user_id = data['user_id']
        quantity = data['quantity']
        transaction_type = data['transaction_type']  # 'purchase', 'refund', etc.
        
        process_inventory_update(product_id, user_id, quantity, transaction_type)
        return jsonify({"message": "Inventory updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
