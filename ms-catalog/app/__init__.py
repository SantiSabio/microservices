from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config


from app.models import db

def create_app():
    app = Flask(__name__)
    db.init_app(app)
    app.config.from_object(Config)
    from .routes import catalog
    app.register_blueprint(catalog)
    
    return app
