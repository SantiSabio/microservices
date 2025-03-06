from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Stock(db.Model):
    __tablename__ = 'stocks'
    
    id_stock = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)