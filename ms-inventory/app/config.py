import os, redis
from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    API_GATEWAY_URL = os.getenv('API_GATEWAY_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=1)