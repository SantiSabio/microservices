from flask import Flask
from app.routes import api_gateway
import os
import redis

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = os.getenv('API_GATEWAY_SECRET')
    app.config['DEBUG'] = True

    app.register_blueprint(api_gateway)

    r = redis.StrictRedis(host='redis_cache', port=6379, db=0, decode_responses=True)

    return app
