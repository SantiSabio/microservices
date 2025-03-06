# app/utils.py
import requests

class MockResponse:
    def __init__(self, json_data, status_code, text=""):
        self._json_data = json_data
        self.status_code = status_code
        self.text = text

    def json(self):
        return self._json_data

def response_from_url(url, data=None, method='POST'):
    """Envía una solicitud HTTP a una URL específica"""
    
    headers = {'Content-Type': 'application/json'}
    
    print(f"Enviando {method} a {url}")
    print(f"Datos: {data}")
    
    try:
        if method.upper() == 'POST':
            return requests.post(url, json=data, headers=headers)
        elif method.upper() == 'PATCH':
            return requests.patch(url, json=data, headers=headers)
        elif method.upper() == 'PUT':
            return requests.put(url, json=data, headers=headers)
        elif method.upper() == 'GET':
            return requests.get(url, headers=headers)
        else:
            raise ValueError(f"Método HTTP no soportado: {method}")
    except Exception as e:
        print(f"Error en la solicitud HTTP: {e}")
        raise