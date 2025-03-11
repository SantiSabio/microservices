from flask import Blueprint, request, jsonify
from app.models import Stock
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.config import Config

import requests

redis_client = Config.r

inventory_bp = Blueprint('inventory', __name__)

# Configuración de la base de datos
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)

# Helper functions
def update_product_status(product_id, is_active):
    #cambiar el estado de un producto mediante api gateway
    response_message = {}
    try:
        #mandamos solicitud PATCH a la API Gateway
        api_gateway_response = requests.patch(
            f"{Config.API_GATEWAY_URL}/activate/{product_id}",
            json={"is_active": is_active},
            headers={"Content-Type": "application/json"}
        )
        #definimos por defecto desactivar el producto
        status_text = "activar" if is_active else "desactivar"
        if api_gateway_response.status_code >= 400:
            print(f"Error al {status_text} el producto: {api_gateway_response.text}")
            response_message['api_gateway_error'] = api_gateway_response.text
    except requests.RequestException as e:
        print(f"Error de conexión con API Gateway: {str(e)}")
        response_message['api_gateway_error'] = str(e)
    
    return response_message #devolvemos todas las respuestas

def process_stock_update(session, stock_item, amount, in_out):
    #Activamos o desactivamos un producto dependiendo si sube o baja stock
    response_message = {}
    
    if in_out == 'out':
        if stock_item.amount < amount:
            return {'error': 'Insufficient stock'}, 400
            
        stock_item.amount -= amount
        
        # Check si nos quedamos sin stock por la compra
        if stock_item.amount <= 0:
            print(f"¡Producto {stock_item.product_id} sin stock! Intentando desactivar...")
            response_message.update(update_product_status(stock_item.product_id, False)) #desactivamos el producto
            
    elif in_out == 'in':
        stock_item.amount += amount
        response_message.update(update_product_status(stock_item.product_id, True)) #activamos el producto
        
    else:
        return {'error': 'Invalid in_out value'}, 400
        
    return response_message, 200

@inventory_bp.route('/update', methods=['POST'])

def update_stock():
    data = request.json
    required_fields = ['product_id', 'amount', 'in_out']
    
    missing_fields = [field for field in required_fields if field not in data]
    present_fields = {field: data[field] for field in required_fields if field in data}
    
    if missing_fields:
        return jsonify({'error': 'Missing fields', 'present_fields': present_fields}), 400

    # Bloqueamos el hilo
    lock = redis_client.lock('stock_lock', timeout=10)
    session = None
    
    try:
        # Damos un bloqueo de 5 segundos
        if not lock.acquire(blocking=True, blocking_timeout=5):
            return jsonify({'error': 'Recurso solicitado en uso'}), 409
            
        redis_client.set('estado', 'abierto') #abrimos el circuito , no dejamos hacer solicitudes al stock
        session = Session()
        
        with session.begin():
            # Obtenemos el profucto mientras el circuito esta abierto
            stock_item = session.query(Stock).with_for_update().filter_by(
                product_id=data['product_id']).first()
                
            if not stock_item:
                return jsonify({'error': 'Stock not found'}), 404
                
            #Cambiamos el stock del producto
            response_message, status_code = process_stock_update(
                session, 
                stock_item, 
                data['amount'], 
                data['in_out']
            )
            
            if status_code != 200:
                return jsonify(response_message), status_code
            
            session.commit()
            
        return jsonify(response_message), 200

    except SQLAlchemyError as e:
        if session:
            session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        # Cerramos el circuito y liberamos el bloqueo
        with redis_client.pipeline() as pipe:
            pipe.set('estado', 'cerrado')
            pipe.execute()

        if lock and lock.locked():

            lock.release()
        if session:
            session.close()