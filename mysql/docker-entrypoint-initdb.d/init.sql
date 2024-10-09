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
    quantity INT NOT NULL,
    price FLOAT NOT NULL,
    purchase_id INT NOT NULL,
    payment_method VARCHAR(80) NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(id_producto),
    FOREIGN KEY (purchase_id) REFERENCES purchase(id_purchase)
);

CREATE TABLE stocks (
    id_stock INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    stock_quantity INT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(id_producto)
);
