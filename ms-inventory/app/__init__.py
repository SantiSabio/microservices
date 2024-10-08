from flask import Flask
from .models import db
from .routes import inventory_bp
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.register_blueprint(inventory_bp, url_prefix='/inventory')

    return app
