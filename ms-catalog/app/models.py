#ms-catalogo/app/models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column('id_producto', db.Integer, primary_key=True)
    name = db.Column('name_product', db.String(80), nullable=False, unique=True)
    price = db.Column(db.Float, nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Product {self.name}>'