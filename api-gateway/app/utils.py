import requests

activate_product_url = 'http://ms-catalog:5001/set-active/'

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

def activate_product(product_id,is_active):
    """Actualiza el estado is_active de un producto a True"""
    product_data = {
        'is_active': is_active
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