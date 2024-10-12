from flask import Flask
from routes import inventory_bp
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(inventory_bp, url_prefix='/inventory')

    return app