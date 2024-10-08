from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Stock(db.Model):
    __tablename__ = 'stock'
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, nullable=False)
    fecha_transaccion = db.Column(db.DateTime, default=datetime.utcnow)
    cantidad = db.Column(db.Float, nullable=False)
    entrada_salida = db.Column(db.Integer, nullable=False)  # 1: entrada, 2: salida