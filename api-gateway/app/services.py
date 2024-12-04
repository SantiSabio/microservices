import requests
from saga import SagaBuilder, SagaError
from app.saga_order import add_purchase, remove_purchase, add_payment, remove_payment, update_stock, remove_stock, success
from flask import jsonify

# Crear la saga ('context' será el conjunto de datos obtenidos al solicitar la creación de la orden)
def build_saga(saga_context):
    # Pasos de la saga a construir
    return SagaBuilder.create() \
        .action(
            lambda: saga_context.update(add_purchase(
                saga_context['product_id'],
                saga_context['purchase_direction']
            )),
            lambda: remove_purchase(saga_context.get('id_purchase'))
        ) \
        .action(
            lambda: saga_context.update(add_payment(
                saga_context['product_id'],
                saga_context['price'],
                saga_context['payment_method'],
                saga_context['amount'],
                saga_context.get('id_purchase')
            )),
            lambda: remove_payment(saga_context.get('payment_id'))
        ) \
        .action(
            lambda: saga_context.update(update_stock(
                saga_context['product_id'],
                saga_context['amount'],
                'out'
            )),
            lambda: remove_stock(saga_context.get('stock_id'))
        ) \
        .action(
            lambda: success(),
            lambda: None  # No hay acción de compensación para el éxito
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
        return jsonify({"error": str(e)}), 500