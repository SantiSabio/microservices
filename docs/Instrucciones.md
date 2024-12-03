http://127.0.0.1:5000/productos debería devolver los productos que estén en el catalogo.

http://127.0.0.1:5001/catalogo debería devolver los productos que estén en el catalogo.

```shell
docker exec -it microservices-api-gateway-1 python -m unittest discover -s tests
```

```shell
docker exec -it microservices-ms-catalogo-1 python -m unittest discover -s tests
```

```shell
curl http://localhost:5000/productos
curl http://localhost:5001/catalogo   
```

```shell
docker-compose up -d --build
docker-compose down
docker ps
```

```shell
docker logs microservices-mysql_db-1 
docker logs microservices-api-gateway-1
docker logs microservices-ms-catalogo-1
docker logs microservices-ms-cart-1
```

### Levantamos los contenedores

```shell
docker-compose up -d
```

### Nos conectamos al contenedor MySQL

```shell
docker exec -it microservices-mysql_db-1 mysql -u root -p
```

```sql
USE catalogodb;
SHOW TABLES;
```

```sql
-- Insertar datos de prueba en 'products'
INSERT INTO products (name_product, price, is_active) VALUES
('Laptop', 1500.50, TRUE),
('Smartphone', 700.99, TRUE),
('Tablet', 350.75, TRUE);

-- Insertar datos de prueba en 'purchase'
INSERT INTO purchase (product_id, purchase_date, purchase_direction) VALUES
(1, NOW(), '123 Main St, Cityville'),
(2, NOW(), '456 Oak Ave, Townsville');

-- Insertar datos de prueba en 'payment'
INSERT INTO payment (product_id, quantity, price, purchase_id, payment_method) VALUES
(1, 1, 1500.50, 1, 'Credit Card'),
(2, 1, 700.99, 2, 'PayPal');

-- Insertar datos de prueba en 'stocks'
INSERT INTO stocks (product_id, stock_quantity) VALUES
(1, 50),
(2, 30),
(3, 20);
```

## Pruebas de stock no negativo

Al ejecutar en el terminal usando el product_id y la cantidad a comprar (out) y si se agrega (in) podemos hacer pruebas sobre la base de datos para que no permita llegar a un stock negativo

### PowerShell

```powershell
for ($i=1; $i -le 10; $i++) {
    Invoke-RestMethod -Uri http://localhost:5003/inventory/update -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"product_id": 1, "ammount": 9, "in_out": "out"}'
    }
```

### Bash

```shell
for i in {1..10}; do
  curl -X POST http://localhost:5003/inventory/update \
    -H "Content-Type: application/json" \
    -d '{"product_id": 1, "ammount": 9, "in_out": "out"}'
done
```
