import os
import redis
from app import database_url,redis_url

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', database_url)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_URL = os.getenv('REDIS_URL', redis_url)
    r = redis.StrictRedis.from_url(REDIS_URL)