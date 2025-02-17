from flask import jsonify
from app.utils import response_from_url
import os

add_purchase_url = os.getenv('ADD_PURCHASE_URL')
remove_purchase_url = os.getenv('REMOVE_PURCHASE_URL')
add_payment_url = os.getenv('ADD_PAYMENT_URL')
remove_payment_url = os.getenv('REMOVE_PAYMENT_URL')
update_stock_url = os.getenv('UPDATE_STOCK_URL')
remove_stock_url = os.getenv('REMOVE_STOCK_URL')
product_url = os.getenv('CATALOG_SERVICE_URL')


def add_purchase(product_id, purchase_direction):
    purchase_data = {
        'product_id': product_id,
        'purchase_direction': purchase_direction
    }
    
    response = response_from_url(add_purchase_url, purchase_data)
    
    if response.status_code == 201:
        id_purchase = response.json().get('id_purchase')
        return {'id_purchase': id_purchase}
    else:
        raise Exception(f"Error al realizar el pago: {response.status_code}, {response.json()}")

# Compensación
def remove_purchase(id_purchase):
    purchase_data = {
        'id_purchase': id_purchase
    }
    response = response_from_url(remove_purchase_url, purchase_data)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error al remover la compra: {response.status_code}, {response.json()}")

# Paso 2: Enviar los datos de pago a ms-payment
def add_payment(product_id, amount,price,id_purchase,payment_method):
    payment_data = {
        'product_id': product_id,
        'amount': amount,
        'price': price,
        'id_purchase': id_purchase,
        'payment_method': payment_method
        
       
    }
    
    response = response_from_url(add_payment_url, payment_data)
    
    if response.status_code == 201:
        payment_id = response.json().get('payment_id')
        return {'payment_id': payment_id}
    else:
        raise Exception(f"Error al realizar el pago: {response.status_code}, {response.json()}")

def remove_payment(payment_id):
    payment_data = {
        'payment_id': payment_id
    }
    
    response = response_from_url(remove_payment_url, payment_data)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error al remover el pago: {response.status_code}, {response.json()}")

# Paso 3: Registrar stock
def update_stock(product_id, amount, in_out):
    stock_data = {
        'product_id': product_id,
        'amount': amount,
        'in_out': in_out
    }
    response = response_from_url(update_stock_url, stock_data)
    
    if response.status_code == 200:
        stock_id = response.json().get('stock_id')
        return {'stock_id': stock_id}
    else:
        raise Exception(f"Error al actualizar el stock: {response.status_code}, {response.json()}")

def remove_stock(stock_id):
    stock_data = {
        'stock_id': stock_id
    }
    
    response = response_from_url(remove_stock_url, stock_data)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error al remover el stock: {response.status_code}, {response.json()}")

def success():
    return {"message": "Pedido procesado con éxito"}