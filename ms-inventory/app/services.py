from .models import db, Stock

def update_stock(producto_id, cantidad, entrada_salida):
    try:
        stock = Stock(
            producto_id=producto_id,
            cantidad=cantidad,
            entrada_salida=entrada_salida
        )
        db.session.add(stock)
        db.session.commit()  # Garantiza la atomicidad y durabilidad
        return stock
    except Exception as e:
        db.session.rollback()  # Si hay error, revierte la transacción
        raise e
