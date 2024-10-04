#catalog/app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@mysql_db:3306/catalogodb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .routes import catalog
    app.register_blueprint(catalog)
    
    return app
