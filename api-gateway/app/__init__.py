#api-gateway/app/__init__.py
import redis
from flask import Flask
from app.routes import api_gateway



def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'supersecretkey'
    app.config['DEBUG'] = True

    app.register_blueprint(api_gateway)

    r=redis.REDIS(host='redis_cache',port=6379, db=0,decode_responses=True)

    return app