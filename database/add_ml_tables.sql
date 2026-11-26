-- ============================================================
-- AI-Powered Business Decision Intelligence System
-- Machine Learning Integration Schema Extensions
-- Tables: demand_forecasts, churn_scores, delivery_predictions
-- Database: quickcommerce_db (MySQL 8.0+)
-- ============================================================

USE quickcommerce_db;

-- ------------------------------------------------------------
-- TABLE 1: demand_forecasts (Meta/XGBoost Demand Forecasting)
-- ------------------------------------------------------------
DROP TABLE IF EXISTS demand_forecasts;

CREATE TABLE demand_forecasts (
    forecast_id      BIGINT         AUTO_INCREMENT PRIMARY KEY,
    store_id         INT            NOT NULL,
    product_id       INT            NOT NULL,
    forecast_date    DATE           NOT NULL,
    predicted_units  INT            NOT NULL,
    confidence_low   INT            DEFAULT 0,
    confidence_high  INT            DEFAULT 0,
    current_stock    INT            DEFAULT 0,
    reorder_level    INT            DEFAULT 20,
    restock_alert    TINYINT(1)     DEFAULT 0,
    model_version    VARCHAR(50)    DEFAULT 'XGBoost_v1.0',
    generated_at     DATETIME       DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (store_id)   REFERENCES stores(store_id)   ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE,
    INDEX idx_store_product  (store_id, product_id),
    INDEX idx_forecast_date  (forecast_date),
    INDEX idx_restock_alert  (restock_alert)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ------------------------------------------------------------
-- TABLE 2: churn_scores (Customer Retention & Churn Prediction)
-- ------------------------------------------------------------
DROP TABLE IF EXISTS churn_scores;

CREATE TABLE churn_scores (
    score_id               BIGINT         AUTO_INCREMENT PRIMARY KEY,
    customer_id            INT            NOT NULL,
    churn_probability      DECIMAL(5,4)   NOT NULL,
    risk_label             VARCHAR(20)    NOT NULL, -- 'HIGH', 'MEDIUM', 'LOW'
    primary_risk_driver    VARCHAR(150),            -- e.g. 'High Delivery Delays', 'No Order in 45 Days'
    days_since_last_order  INT            DEFAULT 0,
    total_orders           INT            DEFAULT 0,
    avg_order_value        DECIMAL(10,2)  DEFAULT 0.00,
    cancellation_rate_pct  DECIMAL(5,2)   DEFAULT 0.00,
    model_version          VARCHAR(50)    DEFAULT 'RandomForest_XGB_v1.0',
    scored_at              DATETIME       DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE,
    INDEX idx_customer    (customer_id),
    INDEX idx_risk_label  (risk_label),
    INDEX idx_churn_prob  (churn_probability)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ------------------------------------------------------------
-- TABLE 3: delivery_predictions (Dynamic Delivery ETA Engine)
-- ------------------------------------------------------------
DROP TABLE IF EXISTS delivery_predictions;

CREATE TABLE delivery_predictions (
    pred_id                BIGINT         AUTO_INCREMENT PRIMARY KEY,
    store_id               INT            NOT NULL,
    order_hour             INT            NOT NULL,
    day_of_week            VARCHAR(20)    NOT NULL,
    delivery_distance_km   DECIMAL(5,2)   NOT NULL,
    predicted_delivery_min DECIMAL(5,2)   NOT NULL,
    sla_target_min         INT            DEFAULT 15,
    delay_risk_flag        TINYINT(1)     DEFAULT 0,
    model_version          VARCHAR(50)    DEFAULT 'GradientBoosting_v1.0',
    scored_at              DATETIME       DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (store_id) REFERENCES stores(store_id) ON DELETE CASCADE,
    INDEX idx_store        (store_id),
    INDEX idx_delay_risk   (delay_risk_flag)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

SHOW TABLES;
