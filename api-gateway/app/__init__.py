#api-gateway/app/__init__.py
from flask import Flask
from routes import api_gateway

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'supersecretkey'
    app.config['DEBUG'] = True

    app.register_blueprint(api_gateway)

    return app