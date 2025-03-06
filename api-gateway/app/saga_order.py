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
activate_product_url = 'http://ms-catalog:5001/set-active/'



def activate_product(product_id):
    """Actualiza el estado is_active de un producto a True"""
    product_data = {
        'is_active': True
    }
    
    # Corregir la URL - importante añadir la barra antes del ID
    
    
    print(f"Llamando a: {activate_product_url}/{product_id}")
    response = response_from_url(f"{activate_product_url}/{product_id}", product_data, method='PATCH')
    
    # Imprimir la respuesta para depuración
    print(f"Respuesta status: {response.status_code}")
    print(f"Respuesta headers: {response.headers}")
    print(f"Respuesta contenido: {response.text[:100]}...")  # Mostrar primeros 100 caracteres
    
    # Si la respuesta contiene HTML (error probable) en lugar de JSON
    if 'text/html' in response.headers.get('Content-Type', ''):
        print("¡Error! Se recibió HTML en lugar de JSON")
        return None
        
    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            print(f"Error al parsear JSON: {response.text}")
            return None
    else:
        print(f"Error al activar el producto {product_id}: {response.status_code}, {response.text}")
        return None


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
    
    if in_out == 'in' and response.status_code == 200:
        activate_product(product_id)


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