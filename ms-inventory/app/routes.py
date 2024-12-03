from flask import Blueprint, request, jsonify
from app.models import Stock
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.config import Config
import threading
from tenacity import retry, stop_after_attempt, wait_fixed
from pybreaker import CircuitBreaker, CircuitBreakerError


redis = Config.r

redis.set('estado', 'cerrado')

inventory_bp = Blueprint('inventory', __name__)

# Configuración de la base de datos
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

breaker = CircuitBreaker(fail_max=10, reset_timeout=10)



@inventory_bp.route('/update', methods=['POST'])
@breaker
@retry(stop=stop_after_attempt(3), wait=wait_fixed(0.5))
def update_stock():
    data = request.json
    # Validar que los datos necesarios estén presentes
    required_fields = ['product_id', 'ammount', 'in_out']
    
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing fields'}), 400
    
    lock = redis.lock('stock_lock', timeout=10)

    try:
        
        if lock.acquire(blocking=False):
            if redis.get('estado') == 'abierto':
                return jsonify({'error': 'Circuito Abierto'}), 500
            else:
                # Iniciar una transacción

                with session.begin():
                    redis.set('estado', 'abierto')
                    # Bloquear la fila del stock para evitar modificaciones concurrentes
                    stock_item = session.query(Stock).with_for_update().filter_by(product_id=data['product_id']).first()
                    
                    if not stock_item:
                        return jsonify({'error': 'Stock not found'}), 404
                    
                    # Actualizar la cantidad de stock
                    if data['in_out'] == 'out':
                        if stock_item.stock_quantity < data['ammount']:
                            return jsonify({'error': 'Insufficient stock'}), 400
                        stock_item.stock_quantity -= data['ammount']
                    elif data['in_out'] == 'in':
                        stock_item.stock_quantity += data['ammount']
                    else:
                        return jsonify({'error': 'Invalid in_out value'}), 400
                    
                    session.commit()
                    redis.set('estado', 'cerrado')
                return jsonify({'message': 'Stock updated successfully'}), 200
        else:
            return jsonify({'error': 'Recurso solicitado en uso'}), 409
        
    except CircuitBreakerError as e:
        return jsonify({'error': 'Circuito Abierto'}), 500
    except SQLAlchemyError as e:
        session.rollback()  # Hacer rollback en caso de error
        return jsonify({'error': str(e)}), 500





  
    