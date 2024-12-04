CREATE DATABASE IF NOT EXISTS catalogodb;
USE catalogodb;

CREATE TABLE products (
    id_producto INT NOT NULL AUTO_INCREMENT,
    name_product VARCHAR(80) NOT NULL UNIQUE,
    price FLOAT,
    is_active BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (id_producto)
);

CREATE TABLE purchase (
    id_purchase INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    purchase_date DATETIME NOT NULL,
    purchase_direction VARCHAR(255) NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(id_producto)
);

CREATE TABLE payment (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    amount INT NOT NULL,
    price FLOAT NOT NULL,
    id_purchase INT NOT NULL,
    payment_method VARCHAR(80) NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(id_producto),
    FOREIGN KEY (id_purchase) REFERENCES purchase(id_purchase)
);

CREATE TABLE stocks (
    id_stock INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    amount INT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(id_producto)
);


INSERT INTO products (name_product, price, is_active) VALUES
('Laptop', 1500.50, TRUE),
('Smartphone', 700.99, TRUE),
('Tablet', 350.75, TRUE);



-- Insertar datos de prueba en 'stocks'
INSERT INTO stocks (product_id, amount) VALUES
(1, 50),
(2, 30),
(3, 20);


-- Insertar datos de prueba en 'purchase'
INSERT INTO purchase (product_id, purchase_date, purchase_direction) VALUES
(1, NOW(), '123 Main St, Cityville'),
(2, NOW(), '456 Oak Ave, Townsville');

-- Insertar datos de prueba en 'payment'
INSERT INTO payment (product_id, amount, price, id_purchase, payment_method) VALUES
(1, 1, 1500.50, 1, 'Credit Card'),
(2, 1, 700.99, 2, 'PayPal');