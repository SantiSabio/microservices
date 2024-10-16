#ms-payment/app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@mysql_db:3306/catalogodb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = True
    r=redis.REDIS(host='localhost',port=6379, db=0)
    db.init_app(app)

    from .routes import payment
    app.register_blueprint(payment)
    
    return app
