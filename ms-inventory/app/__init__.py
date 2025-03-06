from flask import Flask
from .config import Config
from .routes import inventory_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['DEBUG'] = True
    app.register_blueprint(inventory_bp, url_prefix='/inventory')

    return app