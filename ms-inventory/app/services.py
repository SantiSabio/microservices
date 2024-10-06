from .models import db, Product, InventoryTransaction

def process_inventory_update(product_id, user_id, quantity, transaction_type):
    try:
        # Inicia una transacción
        product = Product.query.get(product_id)
        if not product:
            raise Exception("Product not found")

        # Operaciones ACID
        if transaction_type == 'purchase':
            if product.stock_quantity < quantity:
                raise Exception("Insufficient stock")
            product.stock_quantity -= quantity
        elif transaction_type == 'refund':
            product.stock_quantity += quantity
        
        # Registrar la transacción
        transaction = InventoryTransaction(
            product_id=product_id,
            user_id=user_id,
            quantity=quantity,
            transaction_type=transaction_type
        )
        db.session.add(transaction)
        db.session.commit()  # Commit garantiza ACID
    except Exception as e:
        db.session.rollback()  # Revertir si hay error, garantiza atomicidad
        raise e
