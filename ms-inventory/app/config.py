import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'mysql://user:password@localhost/inventory_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
