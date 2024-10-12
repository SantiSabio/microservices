from flask import Blueprint, request, jsonify
from services import update_stock

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/update', methods=['POST'])
def update_stock_route():
    data = request.json
    
    producto_id = data[('producto_id')]
    cantidad = data[('cantidad')]
    entrada_salida = data[('entrada_salida')]

    if not producto_id or not cantidad or not entrada_salida:
        return jsonify({"error": "Datos incompletos"}), 400

    try:
        stock = update_stock(producto_id, cantidad, entrada_salida)
        return jsonify({"success": True, "stock_id": stock.id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500