'''
Saga 'product_order'
Los datos se recibirán de un formulario
1. purchase: se envían los datos de la compra a ms-cart.
2. payment: se envían los datos de pago a ms-payment.
3. stock: se envían los datos de actualización de stock a ms-inventory.
4. Se devuelve el mensaje de finalización al usuario.
'''

from flask import jsonify, request
from services import response_from_url

# Paso 1: Enviar los datos de compra a ms-purchase
# TODO: Refactoizar
def add_purchase(product_id, address):
    # Recibir datos de compra en json, y colocarlos en el contexto
    purchase_data = {
        'product_id': product_id,
        'address': address
    }
    # Enviar al microservicio
    add_purchase_url = 'http://ms-purchase:5002/purchase/add'

    return response_from_url(add_purchase_url, purchase_data) # Será 'purchase_id' o una excepción

# Compensación
def remove_purchase(purchase_id):
    
    purchase_data = {
        'purchase_id': purchase_id
    }
    
    # Enviar 'data' al microservicio 'ms-purchase' (solicitud POST)
    remove_purchase_url = 'http://ms-purchase:5002/purchase/remove'

    return response_from_url(remove_purchase_url, purchase_data) # Será 200 o una excepción

# Paso 2: Enviar los datos de pago a ms-payment
# ---
def add_payment(product_id, pay_method):
    # Recibir los datos de pago
    payment_data = {
        'product_id': product_id,
        'pay_method': pay_method
    }
    
    add_payment_url = 'http://ms-payment:5004/payment/add'
    
    response_from_url(add_payment_url, payment_data)

def remove_payment(payment_id):
    # Recibir los datos de pago
    payment_data = {
        'payment_id': payment_id
    }
    
    # Enviar al microservicio
    remove_payment_url = 'http://ms-payment:5004/payment/remove'

    return response_from_url(remove_payment_url, payment_data)

# Paso 3: Registrar strock
def update_stock(product_id, ammount, in_out):
    # Recibir los datos de actualización de stock
    stock_data = {
        'product_id': product_id,
        'ammount': ammount,
        'in_out' : in_out
    }
    
    # Enviar al microservicio
    add_stock_url = 'http://ms-inventory:5003/inventory/update'

    return response_from_url(add_stock_url, stock_data)

def remove_stock(stock_id):
    
    stock_data = {
        'stock_id': stock_id
    }
    
    # Enviar al microservicio
    remove_stock_url = 'http://ms-inventory:5003/inventory/remove'

    return response_from_url(remove_stock_url, stock_data)

# Paso 4: Saga completada
def success():
    return jsonify({'message': "Compra realizada con éxito."}), 201