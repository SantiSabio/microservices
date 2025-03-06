from .models import db, Stock

def update_stock(product_id, amount, in_out):
    try:
        stock = Stock(
            product_id=product_id,
            amount=amount,
            in_out=in_out
        )
        db.session.add(stock)
        db.session.commit()  # Garantiza la atomicidad y durabilidad
        return stock
    except Exception as e:
        db.session.rollback()  # Si hay error, revierte la transacción
        raise e