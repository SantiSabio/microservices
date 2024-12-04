from flask import jsonify
from app.utils import response_from_url

# Paso 1: Enviar los datos de compra a ms-purchase
def add_purchase(product_id, purchase_direction):
    # Recibir datos de compra en json, y colocarlos en el contexto
    purchase_data = {
        'product_id': product_id,
        'purchase_direction': purchase_direction
    }
    # Enviar al microservicio
    add_purchase_url = 'http://ms-purchase:5002/purchase/add'

    response = response_from_url(add_purchase_url, purchase_data)
    
    if response.status_code == 201:
        id_purchase = response.json().get('id_purchase')
        return {'id_purchase': id_purchase}
    else:
        raise Exception(f"Error al realizar el pago: {response.status_code} {response.json()}")

# Compensación
def remove_purchase(id_purchase):
    purchase_data = {
        'id_purchase': id_purchase
    }
    
    # Enviar 'data' al microservicio 'ms-purchase' (solicitud POST)
    remove_purchase_url = 'http://ms-purchase:5002/purchase/remove'

    response = response_from_url(remove_purchase_url, purchase_data)
    
    if response.status_code == 201:
        return response.json()
    else:
        raise Exception(f"Error al remover la compra: {response.status_code} {response.json()}")

# Paso 2: Enviar los datos de pago a ms-payment
def add_payment(product_id, price, payment_method, purchase_id):
    # Recibir los datos de pago
    payment_data = {
        'product_id': product_id,
        'price': price,
        'payment_method': payment_method,
        'purchase_id': purchase_id
    }
    
    add_payment_url = 'http://ms-payment:5004/payment/add'
    
    response = response_from_url(add_payment_url, payment_data)
    
    if response.status_code == 201:
        payment_id = response.json().get('payment_id')
        return {'payment_id': payment_id}
    else:
        raise Exception(f"Error al realizar el pago: {response.status_code} {response.json()}")

def remove_payment(payment_id):
    # Recibir los datos de pago
    payment_data = {
        'payment_id': payment_id
    }
    
    # Enviar al microservicio
    remove_payment_url = 'http://ms-payment:5004/payment/remove'

    response = response_from_url(remove_payment_url, payment_data)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error al remover el pago: {response.status_code} {response.json()}")

# Paso 3: Registrar stock
def update_stock(product_id, quantity, direction):
    stock_data = {
        'product_id': product_id,
        'quantity': quantity,
        'direction': direction
    }
    
    update_stock_url = 'http://ms-inventory:5003/inventory/update'
    
    response = response_from_url(update_stock_url, stock_data)
    
    if response.status_code == 200:
        stock_id = response.json().get('stock_id')
        return {'stock_id': stock_id}
    else:
        raise Exception(f"Error al actualizar el stock: {response.status_code} {response.json()}")

def remove_stock(stock_id):
    stock_data = {
        'stock_id': stock_id
    }
    
    remove_stock_url = 'http://ms-inventory:5003/inventory/remove'
    
    response = response_from_url(remove_stock_url, stock_data)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error al remover el stock: {response.status_code} {response.json()}")
    
def success():
    return jsonify({"message": "Pedido procesado con éxito"}), 201