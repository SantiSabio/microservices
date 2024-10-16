import os,redis

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'mysql+mysqlconnector://root:password@mysql_db:3306/catalogodb')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    r=redis.REDIS(host='localhost',port=6379, db=0)