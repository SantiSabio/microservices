-- Crear base de datos catalogdb y sus tablas
CREATE DATABASE IF NOT EXISTS catalogdb;
USE catalogdb;

CREATE TABLE products (
    id_producto INT NOT NULL AUTO_INCREMENT,
    name_product VARCHAR(80) NOT NULL UNIQUE,
    price FLOAT,
    is_active BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (id_producto)
);

INSERT INTO products (name_product, price, is_active) VALUES
('Laptop', 1500.50, TRUE),
('Smartphone', 700.99, TRUE),
('Tablet', 350.75, TRUE);

-- Crear base de datos purchasedb y sus tablas
CREATE DATABASE IF NOT EXISTS purchasedb;
USE purchasedb;

CREATE TABLE purchase (
    id_purchase INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    purchase_date DATETIME NOT NULL,
    purchase_direction VARCHAR(255) NOT NULL
);

INSERT INTO purchase (product_id, purchase_date, purchase_direction) VALUES
(1, NOW(), '123 Main St, Cityville'),
(2, NOW(), '456 Oak Ave, Townsville');

-- Crear base de datos paymentdb y sus tablas
CREATE DATABASE IF NOT EXISTS paymentdb;
USE paymentdb;

CREATE TABLE payment (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    amount INT NOT NULL,
    price FLOAT NOT NULL,
    id_purchase INT NOT NULL,
    payment_method VARCHAR(80) NOT NULL
);

INSERT INTO payment (product_id, amount, price, id_purchase, payment_method) VALUES
(1, 1, 1500.50, 1, 'Credit Card'),
(2, 1, 700.99, 2, 'PayPal');

-- Crear base de datos inventorydb y sus tablas
CREATE DATABASE IF NOT EXISTS inventorydb;
USE inventorydb;

CREATE TABLE stocks (
    id_stock INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    amount INT NOT NULL
);

INSERT INTO stocks (product_id, amount) VALUES
(1, 50),
(2, 30),
(3, 20);