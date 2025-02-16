#ms-catalogo/app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
import os
from dotenv import load_dotenv
db = SQLAlchemy()

database_url = os.getenv('DATABASE_URL')
redis_url = os.getenv('REDIS_URL')


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    app.config.from_object(Config)
    from .routes import catalogo
    app.register_blueprint(catalogo)
    
    return app
