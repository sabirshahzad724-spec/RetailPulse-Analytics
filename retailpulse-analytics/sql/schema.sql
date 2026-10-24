-- MySQL 8+ schema for RetailPulse.
CREATE DATABASE IF NOT EXISTS retailpulse;
USE retailpulse;

CREATE TABLE IF NOT EXISTS retail_orders (
    order_id VARCHAR(12) PRIMARY KEY,
    order_date DATE NOT NULL,
    customer_id VARCHAR(12) NOT NULL,
    city VARCHAR(80),
    customer_segment VARCHAR(50),
    sales_channel VARCHAR(50),
    product_id VARCHAR(12),
    product_name VARCHAR(150),
    category VARCHAR(80),
    quantity INT,
    unit_price DECIMAL(12,2),
    discount_pct DECIMAL(5,2),
    order_status VARCHAR(20),
    gross_sales DECIMAL(14,2),
    net_sales DECIMAL(14,2),
    recognized_revenue DECIMAL(14,2),
    INDEX idx_order_date (order_date),
    INDEX idx_city_category (city, category),
    INDEX idx_customer (customer_id)
);

-- Import data/retail_orders.csv using MySQL Workbench Table Data Import Wizard.
-- Match the CSV columns to the table fields in the same order.
