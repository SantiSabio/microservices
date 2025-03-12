# app/config.py
import os,redis
from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.getenv('DEBUG', 'False').lower() in ['true', '1', 't']
    REDIS_URL = os.getenv('REDIS_URL')
    # Iniciamos redis
    try:
        redis_client = redis.StrictRedis.from_url(REDIS_URL, decode_responses=True)
        # Testeamos conexion
        redis_client.ping()
        print("Redis connection successful")
    except Exception as e:
        print(f"Redis connection failed: {str(e)}")
        redis_client = None