#cart/app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@mysql_db:3306/catalogodb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = True

    db.init_app(app)

    with app.app_context():
        # Importa tus modelos aquí
        from .models import Purchase  # Asegúrate de que el nombre del modelo sea correcto
        
        # Crea las tablas
        db.create_all()

    from .routes import cart
    app.register_blueprint(cart)
    
    return app
