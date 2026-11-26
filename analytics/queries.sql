-- ============================================================
-- SQL Analytics Engine — 15 Business Questions
-- AI-Powered Business Decision Intelligence System
-- Database: quickcommerce_db (MySQL 8.0+)
-- Requires: MySQL 8.0+ for CTEs and Window Functions
-- ============================================================

USE quickcommerce_db;


-- ============================================================
-- Q1: Monthly Revenue, Order Volume, AOV
-- Executive trend — is the business growing or declining?
-- ============================================================
SELECT 
    DATE_FORMAT(order_datetime, '%Y-%m')   AS month,
    COUNT(order_id)                        AS total_orders,
    ROUND(SUM(total_amount), 2)            AS total_revenue,
    ROUND(SUM(total_amount) / COUNT(order_id), 2) AS aov,
    COUNT(CASE WHEN order_status = 'Delivered'  THEN 1 END) AS delivered,
    COUNT(CASE WHEN order_status = 'Cancelled'  THEN 1 END) AS cancelled,
    ROUND(COUNT(CASE WHEN order_status = 'Cancelled' THEN 1 END) * 100.0 / COUNT(order_id), 2) AS cancellation_rate_pct
FROM orders
GROUP BY DATE_FORMAT(order_datetime, '%Y-%m')
ORDER BY month;


-- ============================================================
-- Q2: Top and Bottom Store Performers
-- Which stores drive revenue — and which are dragging it down?
-- ============================================================
SELECT 
    s.store_id,
    s.store_name,
    s.city,
    s.rider_capacity,
    COUNT(o.order_id)                            AS total_orders,
    ROUND(SUM(o.total_amount), 2)                AS total_revenue,
    ROUND(SUM(o.total_amount) / COUNT(o.order_id), 2) AS aov,
    ROUND(COUNT(CASE WHEN o.order_status = 'Cancelled' THEN 1 END) * 100.0 / COUNT(o.order_id), 2) AS cancellation_rate_pct,
    ROUND(COUNT(CASE WHEN o.order_status = 'Delivered' THEN 1 END) * 100.0 / COUNT(o.order_id), 2) AS fulfillment_rate_pct,
    RANK() OVER (ORDER BY SUM(o.total_amount) DESC) AS revenue_rank
FROM stores s
LEFT JOIN orders o ON s.store_id = o.store_id
GROUP BY s.store_id, s.store_name, s.city, s.rider_capacity
ORDER BY total_revenue DESC;


-- ============================================================
-- Q3: Month-over-Month Revenue Change by City
-- Which cities are growing vs declining?
-- Uses: CTEs + LAG() window function
-- ============================================================
WITH monthly_city AS (
    SELECT 
        s.city,
        DATE_FORMAT(o.order_datetime, '%Y-%m') AS month,
        ROUND(SUM(o.total_amount), 2)          AS revenue
    FROM orders o
    JOIN stores s ON o.store_id = s.store_id
    GROUP BY s.city, DATE_FORMAT(o.order_datetime, '%Y-%m')
),
city_mom AS (
    SELECT 
        city, month, revenue,
        LAG(revenue) OVER (PARTITION BY city ORDER BY month) AS prev_revenue
    FROM monthly_city
)
SELECT 
    city, month, revenue, prev_revenue,
    ROUND((revenue - prev_revenue) / prev_revenue * 100, 2) AS mom_change_pct,
    CASE 
        WHEN (revenue - prev_revenue) / prev_revenue * 100 < -5 THEN '🔴 Declining'
        WHEN (revenue - prev_revenue) / prev_revenue * 100 > 5  THEN '🟢 Growing'
        ELSE '🟡 Stable'
    END AS trend
FROM city_mom
WHERE prev_revenue IS NOT NULL
ORDER BY mom_change_pct ASC;


-- ============================================================
-- Q4: Stores with Highest Stock-out Rate
-- Which stores are losing sales due to inventory failures?
-- ============================================================
SELECT 
    s.store_id,
    s.store_name,
    s.city,
    COUNT(i.inventory_id)                                              AS total_records,
    SUM(i.stockout_flag)                                               AS stockout_events,
    ROUND(SUM(i.stockout_flag) * 100.0 / COUNT(i.inventory_id), 2)   AS stockout_rate_pct,
    RANK() OVER (ORDER BY SUM(i.stockout_flag) * 100.0 / COUNT(i.inventory_id) DESC) AS stockout_rank
FROM stores s
JOIN inventory i ON s.store_id = i.store_id
GROUP BY s.store_id, s.store_name, s.city
ORDER BY stockout_rate_pct DESC;


-- ============================================================
-- Q5: Products Causing the Most Stock-outs
-- Which SKUs are the biggest inventory problem?
-- ============================================================
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    p.brand,
    COUNT(i.inventory_id)                                            AS total_records,
    SUM(i.stockout_flag)                                             AS stockout_events,
    ROUND(SUM(i.stockout_flag) * 100.0 / COUNT(i.inventory_id), 2) AS stockout_rate_pct
FROM products p
JOIN inventory i ON p.product_id = i.product_id
GROUP BY p.product_id, p.product_name, p.category, p.brand
HAVING stockout_events > 0
ORDER BY stockout_events DESC
LIMIT 20;


-- ============================================================
-- Q6: High-Demand BUT Low-Availability Products (Lost Sales)
-- High demand + high stockout = potential lost revenue
-- Uses: CTEs + PERCENT_RANK()
-- ============================================================
WITH product_demand AS (
    SELECT 
        p.product_id, p.product_name, p.category,
        SUM(oi.quantity)       AS total_units_sold,
        ROUND(SUM(oi.item_revenue), 2) AS total_revenue,
        RANK() OVER (ORDER BY SUM(oi.quantity) DESC) AS demand_rank
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    JOIN orders o   ON oi.order_id   = o.order_id
    WHERE o.order_status = 'Delivered'
    GROUP BY p.product_id, p.product_name, p.category
),
product_stockout AS (
    SELECT 
        product_id,
        ROUND(SUM(stockout_flag) * 100.0 / COUNT(*), 2) AS stockout_rate_pct
    FROM inventory
    GROUP BY product_id
)
SELECT 
    d.product_id, d.product_name, d.category,
    d.total_units_sold, d.total_revenue, d.demand_rank,
    s.stockout_rate_pct,
    '⚠ HIGH DEMAND — LOW AVAILABILITY' AS flag
FROM product_demand d
JOIN product_stockout s ON d.product_id = s.product_id
WHERE d.demand_rank <= 20 AND s.stockout_rate_pct > 15
ORDER BY d.demand_rank ASC;


-- ============================================================
-- Q7: Stores with Highest Average Delivery Time
-- Slow delivery → bad UX → cancellations
-- ============================================================
SELECT 
    s.store_id, s.store_name, s.city, s.rider_capacity,
    COUNT(d.delivery_id)                                               AS total_deliveries,
    ROUND(AVG(d.delivery_time_min), 2)                                 AS avg_delivery_time_min,
    ROUND(SUM(d.delay_flag) * 100.0 / COUNT(d.delivery_id), 2)       AS delay_rate_pct,
    RANK() OVER (ORDER BY AVG(d.delivery_time_min) DESC) AS delay_rank
FROM stores s
JOIN orders o    ON s.store_id  = o.store_id
JOIN deliveries d ON o.order_id = d.order_id
GROUP BY s.store_id, s.store_name, s.city, s.rider_capacity
ORDER BY avg_delivery_time_min DESC;


-- ============================================================
-- Q8: Delivery Delay vs. Cancellation Rate Correlation
-- Answers: does slower delivery cause more cancellations?
-- Uses: CASE classification for risk assessment
-- ============================================================
WITH store_metrics AS (
    SELECT 
        o.store_id,
        s.store_name,
        ROUND(AVG(d.delivery_time_min), 2)                           AS avg_delivery_time,
        ROUND(SUM(d.delay_flag) * 100.0 / COUNT(d.delivery_id), 2)  AS delay_rate_pct,
        ROUND(COUNT(CASE WHEN o.order_status = 'Cancelled' THEN 1 END) * 100.0 / COUNT(o.order_id), 2) AS cancellation_rate_pct
    FROM orders o
    JOIN stores s     ON o.store_id  = s.store_id
    LEFT JOIN deliveries d ON o.order_id = d.order_id
    GROUP BY o.store_id, s.store_name
)
SELECT 
    store_id, store_name, avg_delivery_time, delay_rate_pct, cancellation_rate_pct,
    CASE 
        WHEN delay_rate_pct > 35 AND cancellation_rate_pct > 10 THEN '🔴 HIGH RISK — Delay driving cancellations'
        WHEN delay_rate_pct > 20 AND cancellation_rate_pct > 7  THEN '🟡 MEDIUM RISK — Monitor closely'
        ELSE '🟢 Normal'
    END AS risk_assessment
FROM store_metrics
ORDER BY delay_rate_pct DESC;


-- ============================================================
-- Q9: Peak Ordering Hours by Store
-- Informs rider scheduling and inventory pre-stocking
-- Uses: HOUR() + RANK()
-- ============================================================
SELECT 
    s.store_name,
    HOUR(o.order_datetime)     AS order_hour,
    COUNT(o.order_id)          AS order_count,
    ROUND(SUM(o.total_amount), 2) AS revenue,
    RANK() OVER (PARTITION BY s.store_id ORDER BY COUNT(o.order_id) DESC) AS hour_rank
FROM orders o
JOIN stores s ON o.store_id = s.store_id
GROUP BY s.store_id, s.store_name, HOUR(o.order_datetime)
ORDER BY s.store_name, order_count DESC;


-- ============================================================
-- Q10: Customer Segment Revenue Breakdown
-- Which customer type generates the most value?
-- Uses: SUM() OVER() for percentage share
-- ============================================================
SELECT 
    c.customer_segment,
    COUNT(DISTINCT c.customer_id)         AS unique_customers,
    COUNT(o.order_id)                     AS total_orders,
    ROUND(SUM(o.total_amount), 2)         AS total_revenue,
    ROUND(AVG(o.total_amount), 2)         AS avg_order_value,
    ROUND(SUM(o.total_amount) * 100.0 / SUM(SUM(o.total_amount)) OVER (), 2) AS revenue_share_pct
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_status = 'Delivered'
GROUP BY c.customer_segment
ORDER BY total_revenue DESC;


-- ============================================================
-- Q11: Customers with Declining Purchase Frequency
-- Identifies at-risk customers before they churn
-- Uses: LAG() + CTEs
-- ============================================================
WITH customer_monthly AS (
    SELECT 
        customer_id,
        DATE_FORMAT(order_datetime, '%Y-%m') AS month,
        COUNT(order_id) AS monthly_orders
    FROM orders
    WHERE order_status = 'Delivered'
    GROUP BY customer_id, DATE_FORMAT(order_datetime, '%Y-%m')
),
customer_trend AS (
    SELECT 
        customer_id, month, monthly_orders,
        LAG(monthly_orders) OVER (PARTITION BY customer_id ORDER BY month) AS prev_month_orders
    FROM customer_monthly
)
SELECT 
    c.customer_id, c.customer_segment, c.city,
    ct.month, ct.monthly_orders, ct.prev_month_orders,
    (ct.monthly_orders - ct.prev_month_orders) AS order_change
FROM customer_trend ct
JOIN customers c ON ct.customer_id = c.customer_id
WHERE ct.prev_month_orders IS NOT NULL
  AND ct.monthly_orders < ct.prev_month_orders
ORDER BY order_change ASC
LIMIT 30;


-- ============================================================
-- Q12: Repeat Customer Revenue Percentage
-- What share of revenue comes from loyal customers?
-- ============================================================
WITH customer_order_counts AS (
    SELECT customer_id, COUNT(order_id) AS order_count
    FROM orders
    WHERE order_status = 'Delivered'
    GROUP BY customer_id
)
SELECT 
    COUNT(CASE WHEN order_count = 1  THEN 1 END)  AS one_time_customers,
    COUNT(CASE WHEN order_count > 1  THEN 1 END)  AS repeat_customers,
    COUNT(*)                                        AS total_active_customers,
    ROUND(COUNT(CASE WHEN order_count > 1 THEN 1 END) * 100.0 / COUNT(*), 2) AS repeat_customer_rate_pct,
    (
        SELECT ROUND(
            SUM(o.total_amount) * 100.0 /
            (SELECT SUM(total_amount) FROM orders WHERE order_status = 'Delivered'), 2)
        FROM orders o
        JOIN customer_order_counts coc ON o.customer_id = coc.customer_id
        WHERE coc.order_count > 1 AND o.order_status = 'Delivered'
    ) AS repeat_customer_revenue_pct
FROM customer_order_counts;


-- ============================================================
-- Q13: Products Ranked by Revenue AND Gross Margin
-- Revenue ≠ profit — this reveals the real performers
-- ============================================================
SELECT 
    p.product_id, p.product_name, p.category, p.brand,
    SUM(oi.quantity)                                                              AS units_sold,
    ROUND(SUM(oi.item_revenue), 2)                                                AS total_revenue,
    ROUND(SUM(oi.quantity * p.unit_cost), 2)                                      AS total_cost,
    ROUND(SUM(oi.item_revenue) - SUM(oi.quantity * p.unit_cost), 2)              AS gross_margin,
    ROUND((SUM(oi.item_revenue) - SUM(oi.quantity * p.unit_cost)) * 100.0 / SUM(oi.item_revenue), 2) AS margin_pct,
    RANK() OVER (ORDER BY SUM(oi.item_revenue) DESC)                              AS revenue_rank,
    RANK() OVER (ORDER BY (SUM(oi.item_revenue) - SUM(oi.quantity * p.unit_cost)) * 100.0 / SUM(oi.item_revenue) DESC) AS margin_rank
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN orders   o ON oi.order_id   = o.order_id
WHERE o.order_status = 'Delivered'
GROUP BY p.product_id, p.product_name, p.category, p.brand
ORDER BY total_revenue DESC;


-- ============================================================
-- Q14: High-Sales, Low-Margin Products ("Hidden Loss" Products)
-- These look good on dashboards but erode profitability
-- ============================================================
WITH product_performance AS (
    SELECT 
        p.product_id, p.product_name, p.category,
        SUM(oi.quantity)                      AS units_sold,
        ROUND(SUM(oi.item_revenue), 2)        AS total_revenue,
        ROUND(
            (SUM(oi.item_revenue) - SUM(oi.quantity * p.unit_cost)) * 100.0 / SUM(oi.item_revenue)
        , 2) AS margin_pct,
        PERCENT_RANK() OVER (ORDER BY SUM(oi.item_revenue) DESC) AS revenue_pct_rank,
        PERCENT_RANK() OVER (ORDER BY 
            (SUM(oi.item_revenue) - SUM(oi.quantity * p.unit_cost)) * 100.0 / SUM(oi.item_revenue) 
        ASC) AS low_margin_pct_rank
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    JOIN orders   o ON oi.order_id   = o.order_id
    WHERE o.order_status = 'Delivered'
    GROUP BY p.product_id, p.product_name, p.category
)
SELECT 
    product_id, product_name, category,
    units_sold, total_revenue, margin_pct,
    '⚠ HIGH SALES — LOW MARGIN' AS alert
FROM product_performance
WHERE revenue_pct_rank  <= 0.30   -- Top 30% by revenue
  AND low_margin_pct_rank <= 0.30  -- Bottom 30% by margin
ORDER BY total_revenue DESC;


-- ============================================================
-- Q15: Root-Cause Diagnosis for a Specific Store (FLAGSHIP)
-- Complete monthly KPI profile — feeds the AI engine
-- Change @target to any store_id you want to investigate
-- ============================================================
SET @target = 3;   -- Store 3: QuickMart Koramangala (underperformer)

WITH store_monthly AS (
    SELECT 
        DATE_FORMAT(order_datetime, '%Y-%m')   AS month,
        COUNT(order_id)                          AS orders,
        ROUND(SUM(total_amount), 2)              AS revenue,
        ROUND(SUM(discount_amount), 2)           AS total_discounts,
        COUNT(CASE WHEN order_status = 'Cancelled' THEN 1 END) AS cancellations
    FROM orders
    WHERE store_id = @target
    GROUP BY DATE_FORMAT(order_datetime, '%Y-%m')
),
store_stockout AS (
    SELECT 
        DATE_FORMAT(record_date, '%Y-%m')                             AS month,
        ROUND(SUM(stockout_flag) * 100.0 / COUNT(*), 2)              AS stockout_rate_pct
    FROM inventory
    WHERE store_id = @target
    GROUP BY DATE_FORMAT(record_date, '%Y-%m')
),
store_delivery AS (
    SELECT 
        DATE_FORMAT(o.order_datetime, '%Y-%m')                        AS month,
        ROUND(AVG(d.delivery_time_min), 2)                            AS avg_delivery_min,
        ROUND(SUM(d.delay_flag) * 100.0 / COUNT(d.delivery_id), 2)  AS delay_rate_pct
    FROM deliveries d
    JOIN orders o ON d.order_id = o.order_id
    WHERE o.store_id = @target
    GROUP BY DATE_FORMAT(o.order_datetime, '%Y-%m')
),
store_feedback AS (
    SELECT 
        DATE_FORMAT(cf.feedback_date, '%Y-%m')                        AS month,
        ROUND(AVG(cf.rating), 2)                                      AS avg_rating,
        COUNT(CASE WHEN cf.sentiment = 'Negative' THEN 1 END)        AS negative_count
    FROM customer_feedback cf
    JOIN orders o ON cf.order_id = o.order_id
    WHERE o.store_id = @target
    GROUP BY DATE_FORMAT(cf.feedback_date, '%Y-%m')
)
SELECT 
    sm.month,
    sm.orders,
    sm.revenue,
    ROUND(sm.total_discounts * 100.0 / sm.revenue, 2)                    AS discount_rate_pct,
    ROUND(sm.cancellations * 100.0 / sm.orders, 2)                       AS cancellation_rate_pct,
    ss.stockout_rate_pct,
    sd.avg_delivery_min,
    sd.delay_rate_pct,
    sf.avg_rating,
    sf.negative_count,
    LAG(sm.revenue) OVER (ORDER BY sm.month)                              AS prev_month_revenue,
    ROUND(
        (sm.revenue - LAG(sm.revenue) OVER (ORDER BY sm.month)) * 100.0 /
        LAG(sm.revenue) OVER (ORDER BY sm.month), 2
    )                                                                      AS revenue_change_pct
FROM store_monthly sm
LEFT JOIN store_stockout ss  ON sm.month = ss.month
LEFT JOIN store_delivery sd  ON sm.month = sd.month
LEFT JOIN store_feedback sf  ON sm.month = sf.month
ORDER BY sm.month;
