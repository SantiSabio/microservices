from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Stock(db.Model):
    __tablename__ = 'stocks'
    
    id_stock = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    #fecha_transaccion = db.Column(db.DateTime, default=datetime.utcnow)
    amount = db.Column(db.Float, nullable=False)
    #entrada_salida = db.Column(db.Integer, nullable=False)  # 1: entrada, 2: salida