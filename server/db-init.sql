CREATE TABLE testers (
    ID INT8 PRIMARY KEY NOT NULL,
    username STRING,
    age INT8,
    industry STRING,
);

CREATE TABLE companies (
    ID INT8 PRIMARY KEY NOT NULL,
    name STRING,
    email STRING
);

CREATE TABLE products (
    ID INT8 PRIMARY KEY NOT NULL,
    company_id INT8,
    name STRING,
    description STRING,
    hourly NUMERIC,
    target_age INT8,
    target_industry STRING,
    issues STRING DEFAULT "{}"
);

CREATE TABLE reviews (
    ID INT8 PRIMARY KEY NOT NULL,
    tester_id INT8,
    product_id INT8,
    rating NUMERIC,
    feedback STRING
);