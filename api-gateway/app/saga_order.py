'''
Saga 'product_order'
Los datos se recibirán de un formulario
1. purchase: se envían los datos de la compra a ms-purchase.
2. payment: se envían los datos de pago a ms-payment.
3. stock: se envían los datos de actualización de stock a ms-inventory.
4. Se devuelve el mensaje de finalización al usuario.
'''

from flask import jsonify, request
from services import handle_response

# Paso 1: Enviar los datos de compra a ms-purchase
# TODO: Refactoizar
def add_purchase(product_id, address):
    # Recibir datos de compra en json, y colocarlos en el contexto
    # purchase_data = request.get_json()
    purchase_data = {
        'product_id': product_id,
        'address': address
    }

    if not purchase_data:
        return jsonify({'error': 'Datos de compra inválidos'}), 400
    
    # Enviar 'data' al microservicio 'ms-purchase' (solicitud POST)
    # TODO: Recibir 'purchase_id'
    add_purchase_url = 'http://ms-purchase:5002/purchase/add'

    return handle_response(add_purchase_url, purchase_data)

# Compensación
def remove_purchase(purchase_id):
    
    purchase_data = {
        'purchase_id': purchase_id
    }

    if not purchase_data:
        return jsonify({'error': 'Datos de cancelación de compra inválidos'}), 400
    
    # Enviar 'data' al microservicio 'ms-purchase' (solicitud POST)
    remove_purchase_url = 'http://ms-purchase:5002/purchase/remove'

    return handle_response(remove_purchase_url, purchase_data)


# Paso 2: Enviar los datos de pago a ms-payment
# ---
def register_payment():
    # Recibir los datos de pago
    payment_data = request.get_json()

    if not payment_data:
        return jsonify({'error': 'Datos inválidos'}), 400
    
    # Enviar al microservicio
    add_payment_url = 'http://ms-payment:5004/payment/add'
    
    handle_response(add_payment_url, payment_data)

def remove_payment():
    # Recibir los datos de pago
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Datos inválidos'}), 400
    
    # Enviar al microservicio
    remove_payment_url = 'http://ms-payment:5004/payment/remove'

    return handle_response(remove_payment_url, data)

# Paso 3: Registrar strock
def add_stock():
    # Recibir los datos de pago
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Datos inválidos'}), 400
    
    # Enviar al microservicio
    add_stock_url = 'http://ms-inventory:5004/stock/add'

    return handle_response(add_stock_url, data)

def remove_stock():
    # Recibir los datos de pago
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Datos inválidos'}), 400
    
    # Enviar al microservicio
    remove_stock_url = 'http://ms-inventory:5004/stock/remove'

    return handle_response(remove_stock_url, data)

# Paso 4: Saga completada
def success():
    return "Compra realizada con éxito."
