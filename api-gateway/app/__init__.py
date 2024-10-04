from flask import Flask
from .routes import api_gateway

def create_app():
    app = Flask(__name__)
    
    # Configuración de la aplicación
    app.config['SECRET_KEY'] = 'supersecretkey'

    # Registro de las rutas
    app.register_blueprint(api_gateway)

    return app
