CREATE TABLE customer (
    customer_id INT PRIMARY KEY,
    username VARCHAR(20),
    passwrd VARCHAR(20),
    first_name VARCHAR(20),
    last_name VARCHAR(20),
    date_created DATE
);

CREATE TABLE product (
    id INT PRIMARY KEY,
    name VARCHAR(20),
    description VARCHAR(20),
    inventory INT,
    price DECIMAL(10,2),
    date_created DATE
);

CREATE TABLE shopping_cart (
    id int PRIMARY KEY,
    customer_id int,
    product_id int,
    price DECIMAL(10,2),
    FOREIGN KEY(customer_id) REFERENCES customer(customer_id) ON DELETE SET NULL,
    FOREIGN KEY(product_id) REFERENCES product(id) ON DELETE SET NULL
    
);



DESCRIBE shopping_cart;


//fsff
