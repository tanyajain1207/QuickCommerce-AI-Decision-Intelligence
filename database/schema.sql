-- ============================================================
-- AI-Powered Business Decision Intelligence System
-- Quick-Commerce Operations | MySQL 8.0+
-- Project: Major Project - 4th Year IT
-- Run: mysql -u root -p < schema.sql
-- ============================================================

CREATE DATABASE IF NOT EXISTS quickcommerce_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE quickcommerce_db;

-- Drop in reverse dependency order for clean re-runs
DROP TABLE IF EXISTS customer_feedback;
DROP TABLE IF EXISTS deliveries;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS inventory;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS stores;
DROP TABLE IF EXISTS customers;

-- ============================================================
-- TABLE 1: customers
-- ============================================================
CREATE TABLE customers (
    customer_id         INT            AUTO_INCREMENT PRIMARY KEY,
    signup_date         DATE           NOT NULL,
    city                VARCHAR(50)    NOT NULL,
    zone                VARCHAR(50),
    age_group           VARCHAR(20),
    customer_segment    VARCHAR(30),
    acquisition_channel VARCHAR(30),
    INDEX idx_city      (city),
    INDEX idx_segment   (customer_segment)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- TABLE 2: stores
-- ============================================================
CREATE TABLE stores (
    store_id            INT            AUTO_INCREMENT PRIMARY KEY,
    store_name          VARCHAR(100)   NOT NULL,
    city                VARCHAR(50)    NOT NULL,
    zone                VARCHAR(50),
    opening_date        DATE,
    store_type          VARCHAR(30)    DEFAULT 'Dark Store',
    delivery_radius_km  DECIMAL(4,2),
    storage_capacity    INT,
    rider_capacity      INT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- TABLE 3: products
-- ============================================================
CREATE TABLE products (
    product_id      INT            AUTO_INCREMENT PRIMARY KEY,
    product_name    VARCHAR(150)   NOT NULL,
    category        VARCHAR(50),
    subcategory     VARCHAR(50),
    brand           VARCHAR(100),
    unit_price      DECIMAL(10,2)  NOT NULL,
    unit_cost       DECIMAL(10,2)  NOT NULL,
    shelf_life_days INT,
    is_perishable   TINYINT(1)     DEFAULT 0,
    INDEX idx_category (category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- TABLE 4: orders
-- ============================================================
CREATE TABLE orders (
    order_id                BIGINT         AUTO_INCREMENT PRIMARY KEY,
    customer_id             INT            NOT NULL,
    store_id                INT            NOT NULL,
    order_datetime          DATETIME       NOT NULL,
    order_status            VARCHAR(30)    NOT NULL,
    payment_method          VARCHAR(30),
    subtotal                DECIMAL(10,2),
    discount_amount         DECIMAL(10,2)  DEFAULT 0.00,
    delivery_fee            DECIMAL(10,2)  DEFAULT 0.00,
    total_amount            DECIMAL(10,2),
    estimated_delivery_min  INT,
    actual_delivery_min     INT,
    cancellation_reason     VARCHAR(100),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE RESTRICT,
    FOREIGN KEY (store_id)    REFERENCES stores(store_id)       ON DELETE RESTRICT,
    INDEX idx_store     (store_id),
    INDEX idx_customer  (customer_id),
    INDEX idx_datetime  (order_datetime),
    INDEX idx_status    (order_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- TABLE 5: order_items
-- ============================================================
CREATE TABLE order_items (
    order_item_id   BIGINT         AUTO_INCREMENT PRIMARY KEY,
    order_id        BIGINT         NOT NULL,
    product_id      INT            NOT NULL,
    quantity        INT            NOT NULL DEFAULT 1,
    unit_price      DECIMAL(10,2),
    discount_amount DECIMAL(10,2)  DEFAULT 0.00,
    item_revenue    DECIMAL(10,2),
    FOREIGN KEY (order_id)   REFERENCES orders(order_id)     ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE RESTRICT,
    INDEX idx_order   (order_id),
    INDEX idx_product (product_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- TABLE 6: inventory
-- ============================================================
CREATE TABLE inventory (
    inventory_id    BIGINT         AUTO_INCREMENT PRIMARY KEY,
    store_id        INT            NOT NULL,
    product_id      INT            NOT NULL,
    record_date     DATE           NOT NULL,
    opening_stock   INT            DEFAULT 0,
    received_stock  INT            DEFAULT 0,
    units_sold      INT            DEFAULT 0,
    damaged_units   INT            DEFAULT 0,
    closing_stock   INT            DEFAULT 0,
    reorder_level   INT            DEFAULT 20,
    stockout_flag   TINYINT(1)     DEFAULT 0,
    FOREIGN KEY (store_id)   REFERENCES stores(store_id)     ON DELETE RESTRICT,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE RESTRICT,
    INDEX idx_store_product (store_id, product_id),
    INDEX idx_date          (record_date),
    INDEX idx_stockout      (stockout_flag)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- TABLE 7: deliveries
-- ============================================================
CREATE TABLE deliveries (
    delivery_id          BIGINT         AUTO_INCREMENT PRIMARY KEY,
    order_id             BIGINT         NOT NULL,
    rider_id             INT,
    assigned_datetime    DATETIME,
    pickup_datetime      DATETIME,
    delivered_datetime   DATETIME,
    delivery_distance_km DECIMAL(5,2),
    delivery_time_min    INT,
    delivery_status      VARCHAR(30),
    delay_flag           TINYINT(1)     DEFAULT 0,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    INDEX idx_order (order_id),
    INDEX idx_delay (delay_flag),
    INDEX idx_rider (rider_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- TABLE 8: customer_feedback
-- ============================================================
CREATE TABLE customer_feedback (
    feedback_id       BIGINT         AUTO_INCREMENT PRIMARY KEY,
    order_id          BIGINT         NOT NULL,
    customer_id       INT            NOT NULL,
    rating            INT,
    feedback_text     TEXT,
    feedback_date     DATE,
    feedback_category VARCHAR(50),
    sentiment         VARCHAR(20),
    FOREIGN KEY (order_id)    REFERENCES orders(order_id)       ON DELETE CASCADE,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE RESTRICT,
    INDEX idx_order     (order_id),
    INDEX idx_customer  (customer_id),
    INDEX idx_rating    (rating),
    INDEX idx_sentiment (sentiment)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

SHOW TABLES;
