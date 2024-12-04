from flask import jsonify
from app.utils import response_from_url

# Paso 1: Enviar los datos de compra a ms-purchase
def agregar_compra(product_id, direccion_compra):
    datos_compra = {
        'product_id': product_id,
        'purchase_direction': direccion_compra
    }
    url_agregar_compra = 'http://ms-purchase:5002/purchase/add'

    response = response_from_url(url_agregar_compra, datos_compra)
    
    if response['status_code'] == 201:
        id_compra = response.get('id_purchase')
        return {'purchase_id': id_compra}
    else:
        raise Exception(f"Error al realizar el pago: {response['status_code']} {response.get('text', '')}")

# Compensación
def remover_compra(id_compra):
    datos_compra = {
        'id_purchase': id_compra
    }
    url_remover_compra = 'http://ms-purchase:5002/purchase/remove'

    response = response_from_url(url_remover_compra, datos_compra)
    
    if response['status_code'] == 200:
        return response
    else:
        raise Exception(f"Error al remover la compra: {response['status_code']} {response.get('text', '')}")

# Paso 2: Enviar los datos de pago a ms-payment
def agregar_pago(product_id, precio, metodo_pago):
    datos_pago = {
        'product_id': product_id,
        'price': precio,
        'payment_method': metodo_pago
    }
    url_agregar_pago = 'http://ms-payment:5004/payment/add'
    
    response = response_from_url(url_agregar_pago, datos_pago)
    
    return response

def remover_pago(payment_id):
    datos_pago = {
        'payment_id': payment_id
    }
    url_remover_pago = 'http://ms-payment:5004/payment/remove'

    response = response_from_url(url_remover_pago, datos_pago)
    
    return response

# Paso 3: Registrar stock
def actualizar_stock(product_id, cantidad, entrada_salida):
    datos_stock = {
        'product_id': product_id,
        'ammount': cantidad,
        'in_out': entrada_salida
    }
    url_actualizar_stock = 'http://ms-inventory:5003/inventory/update'

    response = response_from_url(url_actualizar_stock, datos_stock)
    
    return response

def remover_stock(stock_id):
    datos_stock = {
        'stock_id': stock_id
    }
    url_remover_stock = 'http://ms-inventory:5003/inventory/remove'

    response = response_from_url(url_remover_stock, datos_stock)
    
    return response

# Paso 4: Saga completada
def exito():
    return jsonify({'message': "Compra realizada con éxito."}), 201