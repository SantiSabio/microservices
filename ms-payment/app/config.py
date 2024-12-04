import os, redis

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'mysql+mysqlconnector://root:password@mysql_db:3306/catalogodb')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')
    r = redis.StrictRedis.from_url(REDIS_URL)
