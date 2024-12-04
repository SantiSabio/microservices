from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime
db = SQLAlchemy()

class Purchase(db.Model):
    id_purchase = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    purchase_date = db.Column(db.DateTime, nullable=True)
    purchase_direction = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Purchase {self.id_purchase}>'