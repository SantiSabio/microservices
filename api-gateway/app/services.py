import requests
from saga import SagaBuilder, SagaError
from saga_order import *
from flask import jsonify

# Crear la saga ('context' será el conjunto de datos obtenidos al solicitar la creación de la orden)
def build_saga(saga_context):
    # Pasos de la saga a construir
    return SagaBuilder.create() \
        .action(
            lambda: add_purchase(saga_context['product_id'], saga_context['purchase_address']),
            # ---
            lambda: remove_purchase(saga_context['product_id'], saga_context['purchase_address'])
        ) \
        .action(
            lambda: register_payment(saga_context['user_id'], saga_context['total']),
            lambda: remove_payment(saga_context['user_id'], saga_context['total'])
        ) \
        .action(
            lambda: add_stock(saga_context['product_id']),
            lambda: remove_stock(saga_context['product_id'])
        .action(
            lambda: success()
        )
        ) \
        .build()

def execute_saga(saga):
    # Ejecutar la Saga
    try:
        saga.execute()
        return jsonify({"message": "Pedido procesado con éxito"}), 200
    # Caso de error de saga
    except SagaError as e:
        # Se manejan las compensaciones
        return jsonify({
            "error": str(e.action),
            "compensation_errors": [str(comp_error) for comp_error in e.compensations]
        }), 400
    # Caso de otra excepción
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Obtiene la respuesta (o excepción) al enviar una solicitud a una url (microservicio)
def response_from_url(url, data):

    if not data:
        return jsonify({'error': 'Datos inválidos'}), 400
    
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Lanza una excepción si el código de estado es 4xx o 5xx
        return response
    except requests.exceptions.RequestException as e:
        # Lanza una excepción para que saga-py inicie la compensación
        raise Exception(f"Error al realizar la compra: {str(e)}")
