from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

db = SQLAlchemy()

class Product(db.Model):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    brand = db.Column(db.String(100), db.ForeignKey('brands.id'), nullable=False)
    stock_quantity = Column(Integer, nullable=False)

class InventoryTransaction(db.Model):
    __tablename__ = 'inventory_transactions'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    transaction_type = Column(String(50), nullable=False)  # 'purchase', 'refund', etc.
    timestamp = Column(DateTime, default=datetime.utcnow)

class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

class Brand(db.Model):
    __tablename__ = 'brands'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    amount_art = db.Column(db.Integer, nullable=False, default=0)
    products = db.relationship('Products', backref='brand_ref', lazy=True)