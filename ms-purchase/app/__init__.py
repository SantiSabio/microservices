from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@mysql_db:3306/catalogodb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = True
    app.config.from_object(Config)
    db.init_app(app)

    from .routes import purchase
    app.register_blueprint(purchase)
    
    return app
