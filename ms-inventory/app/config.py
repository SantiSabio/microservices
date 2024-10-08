import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'mysql+mysqlconnector://root:password@mysql_db:3306/catalogodb')
    SQLALCHEMY_TRACK_MODIFICATIONS = False