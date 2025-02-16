#ms-payment/app/__init__.py
from flask import Flask
from app.config import Config
from app.models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    from .routes import payment
    app.register_blueprint(payment)
    
    return app
