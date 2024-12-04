#ms-payment/app/models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Payment(db.Model):
    __tablename__ = 'payment'

    payment_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    amount= db.Column(db.Integer, nullable=True)
    price=db.Column(db.Float, nullable=True)
    id_purchase = db.Column(db.Integer, nullable=False)
    payment_method = db.Column(db.String(80), nullable = False)
    def __repr__(self):
        return f'<Payment number: {self.payment_id}>'