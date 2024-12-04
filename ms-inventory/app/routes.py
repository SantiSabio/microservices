from flask import Blueprint, request, jsonify
from app.models import Stock
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.config import Config
from tenacity import retry
from tenacity.wait import wait_fixed
from tenacity.stop import stop_after_attempt
from pybreaker import CircuitBreaker, CircuitBreakerError

redis_client = Config.r


inventory_bp = Blueprint('inventory', __name__)

# Configuración de la base de datos
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

breaker = CircuitBreaker(fail_max=10, reset_timeout=10)

@inventory_bp.route('/update', methods=['POST'])
@breaker
#@retry(stop=stop_after_attempt(3), wait=wait_fixed(0.5))
def update_stock():
    data = request.json
    
    required_fields = ['product_id', 'amount', 'in_out']

    missing_fields = [field for field in required_fields if field not in data]
    present_fields = {field: data[field] for field in required_fields if field in data}

    if missing_fields:
        return jsonify({'error': 'Missing fields', 'present_fields': present_fields}), 400

    lock = redis_client.lock('stock_lock', timeout=10)
    try:
        if lock.acquire(blocking=False):
            if redis_client.get('estado') == b'abierto':
                return jsonify({'error': 'Circuito Abierto'}), 500
            else:
                with session.begin():
                    redis_client.set('estado', 'abierto')
                    stock_item = session.query(Stock).with_for_update().filter_by(product_id=data['product_id']).first()
                    
                    if not stock_item:
                        return jsonify({'error': 'Stock not found'}), 404
                    
                    if data['in_out'] == 'out':
                        if stock_item.amount < data['amount']:
                            return jsonify({'error': 'Insufficient stock'}), 400
                        stock_item.amount -= data['amount']
                    elif data['in_out'] == 'in':
                        stock_item.amount += data['amount']
                    else:
                        return jsonify({'error': 'Invalid in_out value'}), 400
                    redis_client.set('estado', 'cerrado')
                    session.commit()
                    
                return jsonify({'message': 'Stock updated successfully'}), 200
        else:
            return jsonify({'error': 'Recurso solicitado en uso'}), 409
        
    except CircuitBreakerError:
        return jsonify({'error': 'Circuito Abierto'}), 500
    except SQLAlchemyError as e:
        session.rollback()  # Hacer rollback en caso de error
        return jsonify({'error': str(e)}), 500
    finally:
        redis_client.set('estado', 'cerrado')

        if lock.locked():
            lock.release()
