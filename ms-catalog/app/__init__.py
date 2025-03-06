from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    app.config.from_object(Config)
    from .routes import catalogo
    app.register_blueprint(catalogo)
    
    return app
