from flask import jsonify
import request
from app.utils import response_from_url

def create_order():
    data = request.get_json()
    
    # Paso 1: Crear compra
    purchase_response, status_code = create_purchase(data)
    if status_code != 201:
        return jsonify({'error': 'Error al crear la compra'}), status_code
    
    purchase_id = purchase_response['id_purchase']
    
    # Paso 2: Agregar pago
    payment_response, status_code = add_payment(purchase_id, data)
    if status_code != 201:
        # Compensar la compra
        remove_purchase(purchase_id)
        return jsonify({'error': 'Error al agregar el pago'}), status_code
    
    # Paso 3: Actualizar inventario
    stock_response, status_code = update_stock(data)
    if status_code != 200:
        # Compensar el pago y la compra
        remove_payment(payment_response['payment_id'])
        remove_purchase(purchase_id)
        return jsonify({'error': 'Error al actualizar el inventario'}), status_code
    
    # Paso 4: Saga completada
    return success()

def create_purchase(data):
    purchase_url = 'http://ms-purchase:5002/purchase/add'
    return response_from_url(purchase_url, data)

def add_payment(purchase_id, data):
    payment_data = {
        'purchase_id': purchase_id,
        'product_id': data['product_id'],
        'quantity': data['quantity'],
        'price': data['price'],
        'payment_method': data['payment_method']
    }
    payment_url = 'http://ms-payment:5004/payment/add'
    return response_from_url(payment_url, payment_data)

def update_stock(data):
    stock_data = {
        'product_id': data['product_id'],
        'quantity': data['quantity']
    }
    add_stock_url = 'http://ms-inventory:5003/inventory/update'
    return response_from_url(add_stock_url, stock_data)

def remove_purchase(purchase_id):
    purchase_data = {'id_purchase': purchase_id}
    remove_purchase_url = 'http://ms-purchase:5002/purchase/remove'
    return response_from_url(remove_purchase_url, purchase_data)

def remove_payment(payment_id):
    payment_data = {'payment_id': payment_id}
    remove_payment_url = 'http://ms-payment:5004/payment/remove'
    return response_from_url(remove_payment_url, payment_data)

def success():
    return jsonify({'message': "Compra realizada con éxito."}), 201

