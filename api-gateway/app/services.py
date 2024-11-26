import requests
from saga import SagaBuilder, SagaError
from app.saga_order import add_purchase, remove_purchase, add_payment, remove_payment, update_stock, remove_stock, success
from flask import jsonify

# Crear la saga ('context' será el conjunto de datos obtenidos al solicitar la creación de la orden)
def build_saga(saga_context):
    # Pasos de la saga a construir
    return SagaBuilder.create() \
        .action(
            # Guardar 'purchase_id' devuelto por 'add_purchase' en 'saga_context'
            lambda: saga_context.update({
                'purchase_id': add_purchase(
                    saga_context['product_id'],
                    saga_context['address']
                    )}),
            # Usar 'purchase_id' para remover la compra
            lambda: remove_purchase(saga_context['purchase_id'])
        ) \
        .action(
            lambda: saga_context.update({
                'payment_id': add_payment(
                    saga_context['product_id'],
                    saga_context['pay_method']
                    )}),
            lambda: remove_payment(saga_context['payment_id'])
        ) \
        .action(
            lambda: saga_context.update({
                'stock_id': update_stock(
                    saga_context['product_id'],
                    saga_context['ammount'], saga_context['in_out'])}),
            lambda: remove_stock(saga_context['product_id'])
        ) \
        .action(lambda: success()) \
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
