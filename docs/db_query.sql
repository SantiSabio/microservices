-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS catalogodb;

-- Usar la base de datos
USE catalogodb;

-- Tabla 'products'
CREATE TABLE products (
    id_producto INT NOT NULL AUTO_INCREMENT,
    name_product VARCHAR(80) NOT NULL UNIQUE,
    price FLOAT,
    activate BOOLEAN,
    PRIMARY KEY (id_producto)
);

-- Tabla 'purchase'
CREATE TABLE purchase (
    id_purchase INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    purchase_date DATETIME,
    purchase_direction VARCHAR(255) NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(id_producto)
);

-- Tabla 'payments'
CREATE TABLE payments (
    id_payments INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    price FLOAT,
    payment_method VARCHAR(80),
    FOREIGN KEY (product_id) REFERENCES products(id_producto)
);

-- Tabla 'stocks'
CREATE TABLE stocks (
    id_stock INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    stock_quantity INT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(id_producto)
);

