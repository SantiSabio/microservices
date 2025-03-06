from flask import Flask
from app.config import Config
from app.routes import inventory_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(inventory_bp, url_prefix='/inventory')
    app.config['DEBUG'] = True
    return app