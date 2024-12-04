from flask import jsonify
from app.utils import response_from_url

# Paso 1: Enviar los datos de compra a ms-purchase
def add_purchase(product_id, purchase_direction):
    purchase_data = {
        'product_id': product_id,
        'purchase_direction': purchase_direction
    }
    add_purchase_url = 'http://ms-purchase:5002/purchase/add'

    response = response_from_url(add_purchase_url, purchase_data)
    
    if response['status_code'] == 201:
        id_purchase = response.get('id_purchase')
        return {'purchase_id': id_purchase}
    else:
        raise Exception(f"Error al realizar el pago: {response['status_code']} {response.get('text', '')}")

# Compensacion
def remove_purchase(id_purchase):
    purchase_data = {
        'id_purchase': id_purchase
    }
    remove_purchase_url = 'http://ms-purchase:5002/purchase/remove'

    response = response_from_url(remove_purchase_url, purchase_data)
    
    if response['status_code'] == 200:
        return response
    else:
        raise Exception(f"Error al remover la compra: {response['status_code']} {response.get('text', '')}")

# Paso 2: Enviar los datos de pago a ms-payment
def add_payment(product_id, price, payment_method):
    payment_data = {
        'product_id': product_id,
        'price': price,
        'payment_method': payment_method
    }
    add_payment_url = 'http://ms-payment:5004/payment/add'
    
    response = response_from_url(add_payment_url, payment_data)
    
    return response

def remove_payment(payment_id):
    payment_data = {
        'payment_id': payment_id
    }
    remove_payment_url = 'http://ms-payment:5004/payment/remove'

    response = response_from_url(remove_payment_url, payment_data)
    
    return response

# Paso 3: Registrar stock
def update_stock(product_id, ammount, in_out):
    stock_data = {
        'product_id': product_id,
        'ammount': ammount,
        'in_out': in_out
    }
    add_stock_url = 'http://ms-inventory:5003/inventory/update'

    response = response_from_url(add_stock_url, stock_data)
    
    return response

def remove_stock(stock_id):
    stock_data = {
        'stock_id': stock_id
    }
    remove_stock_url = 'http://ms-inventory:5003/inventory/remove'

    response = response_from_url(remove_stock_url, stock_data)
    
    return response

# Paso 4: Saga completada
def success():
    return jsonify({'message': "Compra realizada con éxito."}), 201
