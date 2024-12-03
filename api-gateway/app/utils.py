import requests
from flask import jsonify


# Obtiene la respuesta (o excepción) al enviar una solicitud a una url (microservicio)
def response_from_url(url, data):

    if not data:
        return jsonify({'error': 'Datos inválidos'}), 400
    
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Lanza una excepción si el código de estado es 4xx o 5xx
        return response.json()
    except requests.exceptions.RequestException as e:
        # Lanza una excepción para que saga-py inicie la compensación
        raise Exception(f"Error al realizar la compra: {str(e)}")
