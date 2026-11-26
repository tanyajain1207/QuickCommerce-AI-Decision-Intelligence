# 📖 QUICKCOMMERCE AI — COMPLETE STUDY NOTES
### Everything explained from scratch · Read top to bottom in 3–4 hours
> **Team:** Tanya Jain (23104034) · Tanmay Tiwari (23104032) · Tanishq Jain (23104060)
> **Supervisor:** Dr. Diksha Chawla | **Project Code:** 15B29CI692 | **JIIT Noida, B.Tech CSE/IT, Sem 8**

---

# PART 1 — WHAT IS THIS PROJECT AND WHY DOES IT EXIST?

---

## 1.1 Quick-Commerce — The Domain

**Quick-commerce (Q-commerce)** is ultra-fast grocery and essentials delivery — typically within **10–15 minutes** of placing an order. Think **Blinkit** (owned by Zomato), **Zepto**, and **Swiggy Instamart** in India.

This is fundamentally different from normal e-commerce:

| | E-Commerce (Amazon/Flipkart) | Quick-Commerce (Blinkit/Zepto) |
|---|---|---|
| Delivery time | 1–2 days | 10–15 minutes |
| Warehouse size | Large central hubs | Tiny hyper-local dark stores |
| Products | Everything | Groceries, medicines, essentials |
| Customer need | Planned purchases | Impulse / urgent needs |
| Order distance | City-wide | 2–3 km radius only |

---

## 1.2 What Is a Dark Store?

A **dark store** is a small, hyper-local warehouse — typically **1,000 to 3,000 sq ft** — located inside a residential or commercial area. It is called "dark" because there is **no customer-facing floor**. Customers cannot walk in. The entire space is for storage, picking, and packing.

Orders are fulfilled by **delivery riders** who travel to customers within a 2–3 km radius. A city like Bengaluru may have **50+ dark stores** to cover all zones. Each store serves a specific neighbourhood — Koramangala, Indiranagar, Whitefield, etc.

**The key operational challenge:** A company running 100+ dark stores cannot manually monitor each one. They need automated intelligence.

---

## 1.3 The Business Problem We Solve

A quick-commerce company operating many dark stores faces this critical question every morning:

> *"Which stores are failing — and WHY — and what should we do about it?"*

**Without our system (the old way):**
- Managers manually pull data from ERP, POS systems, delivery apps, and CRM tools
- Takes **4–6 hours** of analyst work to identify problems
- By the time the problem is spotted, it has already cost the company lakhs of rupees
- They see WHAT happened, not WHY — and cannot predict WHAT WILL happen tomorrow

**A concrete example of the problem:**
> Store 3 (Koramangala, Bengaluru) has only **5 delivery riders** but receives high order volume. Delivery times spike to **30 minutes** (SLA is 15 minutes). Customers get frustrated, give 2.15/5.0 ratings, and switch to Blinkit. Orders drop 30% month-over-month. Revenue falls 23.57%. The store starts running out of stock because it can't restock fast enough. Stockout rate hits 33.48%. The manager does not know the **root cause is rider shortage** — they just know revenue is falling.

Our system would have caught this 2 weeks ago and dispatched an alert automatically.

---

## 1.4 What We Built — One-Paragraph Summary

**QuickCommerce AI** is a **5-layer Decision Intelligence System** that:
1. Stores all operational data in a MySQL relational database (11 tables, 54,900+ records)
2. Runs 15 SQL analytics queries to compute exact KPIs (revenue, stockout rate, delivery time, margins)
3. Runs 3 machine learning models to **PREDICT** the future (demand, churn, delivery ETA)
4. Uses Google Gemini 2.5 Flash AI to **INTERPRET** the numbers and generate a natural language executive diagnosis
5. Displays everything on a Streamlit dashboard and sends 12 automated operational alerts

**Result:** Complete store health diagnosis with root causes and recommended actions in **65 seconds** — instead of 4–6 hours.

---

## 1.5 The Doctor Analogy (use this in viva)

> "Think of our system like a **doctor's diagnostic report** for a sick store. When you go to a doctor, they run blood tests (SQL analytics), interpret results using medical expertise (ML models), consult a specialist (Gemini AI), and write a prescription (automated alerts). Our system does exactly this — but for dark stores."

---

## 1.6 Two-Sentence Pitch (memorize this exactly)

> *"We built an AI-powered decision intelligence system for quick-commerce dark store operations. It combines a MySQL database, 15 SQL analytics queries, three XGBoost machine learning models, and the Google Gemini 2.5 Flash API to automatically diagnose store health, predict demand stockouts and customer churn, estimate delivery ETA, and dispatch 12 automated operational alerts — reducing diagnostic time from 4–6 hours to 65 seconds."*

---

# PART 2 — SYSTEM ARCHITECTURE (THE 5 LAYERS)

---

## 2.1 Why a Layered Architecture?

A layered architecture means each layer has ONE job. Layer 1 stores data. Layer 2 computes metrics. Layer 3 predicts. Layer 4 interprets. Layer 5 presents. This follows the **Single Responsibility Principle** — a core software engineering principle. If Layer 3 (ML) needs to be updated, Layers 1, 2, 4, and 5 don't change. This makes the system maintainable and extensible.

---

## 2.2 The 5 Layers — Detailed

```
╔══════════════════════════════════════════════════════════╗
║           QUICKCOMMERCE AI — 5 LAYER ARCHITECTURE        ║
╠══════════════════════════════════════════════════════════╣
║  LAYER 5: PRESENTATION & ALERTS                          ║
║  Streamlit Dashboard (5 tabs) + Alert Dispatcher (12)    ║
║                        ↑                                 ║
║  LAYER 4: GENERATIVE AI INTERPRETATION                   ║
║  Google Gemini 2.5 Flash — interprets SQL+ML numbers     ║
║                        ↑                                 ║
║  LAYER 3: PREDICTIVE MACHINE LEARNING                    ║
║  XGBoost: Demand Forecast + Churn + Delivery ETA         ║
║                        ↑                                 ║
║  LAYER 2: DETERMINISTIC SQL ANALYTICS                    ║
║  15 BI Queries — CTEs, Window Functions, KPIs            ║
║                        ↑                                 ║
║  LAYER 1: MYSQL RELATIONAL DATABASE                      ║
║  11 tables · 54,900 records · Single source of truth     ║
╚══════════════════════════════════════════════════════════╝
```

| Layer | File(s) | Technology | Purpose |
|-------|---------|------------|---------|
| 1 | `database/schema.sql` | MySQL 8.0 | 11 tables, all raw data |
| 2 | `analytics/queries.sql` | SQL, CTEs, Window Functions | 15 KPI queries — deterministic |
| 3 | `ml/*.py` | XGBoost, pandas, scikit-learn | 3 ML models — predict future |
| 4 | `ai/insights.py` | Google Gemini 2.5 Flash API | AI synthesis — interpret verified numbers |
| 5 | `app/streamlit_app.py` + `ml/alert_notifier.py` | Streamlit, Python | Dashboard + 12 auto-notifications |

---

## 2.3 Data Flow (How Information Moves)

```
MySQL DB
   ↓ (SQL queries via Python mysql-connector)
15 KPI DataFrames (revenue MoM, stockout rate, delivery time…)
   ↓
3 XGBoost Models run → write predictions to MySQL + JSON files
   ↓
JSON payload assembled (KPIs + ML predictions merged)
   ↓
Gemini 2.5 Flash gets JSON → returns natural language diagnosis
   ↓
Streamlit renders 5-tab dashboard
   ↓
Alert Dispatcher reads all outputs → sends 12 notifications
```

**Total time: ~65 seconds** from `python ml\run_all_ml.py` to full dashboard ready.

---

## 2.4 The Golden Rule of the Architecture

> **SQL computes ALL numbers. Gemini only INTERPRETS. Never the other way.**

This is the anti-hallucination principle — the most important architectural decision in the project. Never let an AI model invent numbers. Only let it explain numbers that are already mathematically guaranteed by SQL.

---

## 2.5 Tech Stack and Why Each Was Chosen

| Tool | Version | Why This? |
|------|---------|-----------|
| **Python** | 3.11 | Dominant ML/data science language, huge ecosystem |
| **MySQL** | 8.0 | ACID-compliant, native window functions & CTEs, industry standard |
| **XGBoost** | 3.2 | State-of-the-art on tabular data, fast, interpretable |
| **Google Gemini** | 2.5 Flash | Fast (2–5 sec), cost-efficient, instruction-following |
| **Streamlit** | 1.67 | Fastest Python-only dashboard — no HTML/CSS/JS needed |
| **pandas** | 2.3 | Industry-standard DataFrame — `.shift()`, `read_sql()`, `fillna()` |
| **scikit-learn** | 1.8 | Metrics, train-test split, cross-validation |
| **python-dotenv** | 1.0.1 | Load secrets from `.env` without hardcoding |

---

# PART 3 — DATABASE DESIGN (LAYER 1)

---

## 3.1 What Is a Relational Database?

A relational database stores data in **tables** (like spreadsheets) where rows are records and columns are attributes. The "relational" part means tables are **linked to each other** through shared keys. MySQL is the most popular relational database in the world for web and business applications.

---

## 3.2 All 11 Tables and What They Store

| Table | Records | Purpose |
|-------|---------|---------|
| `stores` | 10 | Dark store locations, city, zone, rider count |
| `riders` | ~130 | Delivery riders, their store, capacity |
| `products` | ~200 | SKU catalog — name, category, price, weight |
| `customers` | 500 | Customer profiles, segment (Regular/Premium/VIP) |
| `orders` | 3,000+ | Order header — customer, store, timestamp, subtotal |
| `order_items` | ~9,000 | Line items — product, quantity, price per order |
| `inventory` | **54,900** | Daily closing stock per SKU per store (90 days) |
| `delivery_logs` | 2,848 | Actual delivery times, rider, distance, outcome |
| `demand_forecasts` | ML output | 7-day predicted demand (written by ML pipeline) |
| `churn_scores` | ML output | Churn probability per customer (written by ML) |
| `delivery_predictions` | ML output | Predicted ETA + SLA risk (written by ML) |

The first 8 are **source tables** (raw data). The last 3 are **ML output tables** — written by the ML pipeline and read by the dashboard.

---

## 3.3 Database Normalization — 1NF, 2NF, 3NF

**What is normalization?** The process of organizing tables to remove redundancy and prevent data anomalies.

### 1NF — First Normal Form
**Rule:** Each cell has one atomic value. No repeating groups.

**Violation example:**
```
orders: order_id, customer_id, product_1, qty_1, product_2, qty_2, product_3, qty_3
```
Problem: What if someone orders 15 items? You need 15 column pairs. What if they order 1 item? 14 columns are empty. This is a repeating group — violates 1NF.

**Fix:** Separate into `orders` and `order_items` tables.

### 2NF — Second Normal Form
**Rule:** Every non-key column must depend on the WHOLE primary key (not just part of it).

**Violation example (composite key):**
```
order_items: (order_id, product_id), quantity, unit_price, product_name
```
Here, `product_name` depends only on `product_id` — not on the full composite key `(order_id, product_id)`. Partial dependency → violates 2NF.

**Fix:** Move `product_name` to `products` table.

### 3NF — Third Normal Form
**Rule:** No transitive dependencies. Non-key columns depend ONLY on the primary key — not on another non-key column.

**Violation example:**
```
order_items: item_id, product_id, product_name, product_category
```
Here: `item_id → product_id → product_name`. `product_name` depends on `product_id`, not directly on `item_id`. This is a transitive dependency → violates 3NF.

**Fix:** `order_items` only has `item_id, order_id, product_id, quantity, unit_price`. Product details live in `products`.

**Why it matters practically:** If Amul Milk is renamed to "Amul Full Cream Milk 1L Premium," you update **ONE row** in `products`. Without normalization, you'd have to update it in thousands of `order_items` rows — missing even one creates inconsistent data.

---

## 3.4 Why Separate `orders` and `order_items`?

This is one of the most common viva questions. The answer is in the relational model's core principle: **one fact, one place**.

An order is one event (who ordered, when, from where, total cost). The items in that order are separate facts (which products, how many, at what price). Mixing them causes repeating groups (1NF violation).

```
orders:      order_id | customer_id | store_id | order_date  | subtotal
             1001     | C001        | 3        | 2025-01-15  | 342.00

order_items: item_id | order_id | product_id | quantity | unit_price
             5001    | 1001     | P012       | 2        | 85.00
             5002    | 1001     | P034       | 1        | 172.00
```

Order 1001 had 2 products. No wasted columns. No arbitrary limits on item count.

---

## 3.5 Foreign Keys and Referential Integrity

A **foreign key (FK)** is a column in one table that references the **primary key** of another table. It enforces that you can't have an order for a non-existent customer.

```
orders.customer_id  → customers.customer_id  (FK)
orders.store_id     → stores.store_id        (FK)
order_items.order_id   → orders.order_id     (FK)
order_items.product_id → products.product_id (FK)
delivery_logs.rider_id → riders.rider_id     (FK)
```

If you try to `INSERT INTO orders (customer_id=9999)` and customer 9999 doesn't exist → MySQL throws a **foreign key constraint violation** error. This is **referential integrity** — it keeps the database consistent automatically.

---

## 3.6 Why MySQL, Not MongoDB or PostgreSQL?

**Why not MongoDB?**
MongoDB is a NoSQL document database. It's excellent for schema-less, unstructured data (logs, social media posts, JSON documents). But our data is fundamentally **relational** — an order links to a customer links to a store links to delivery_logs links to riders. MongoDB requires you to perform joins at the application level (in Python), which is slower and error-prone. MySQL's JOIN engine is natively optimized for exactly this pattern. Also, our SQL analytics uses window functions (LAG, RANK, ROW_NUMBER) and CTEs — these are SQL-specific features not available in MongoDB.

**Why not PostgreSQL?**
PostgreSQL is excellent and also supports window functions. We chose MySQL 8.0 because it's more widely deployed in Indian quick-commerce production environments, integrates seamlessly with `mysql-connector-python`, and our team was more familiar with it. The technical capabilities needed for this project are identical in both.

---

# PART 4 — SQL ANALYTICS (LAYER 2)

---

## 4.1 What Is "Deterministic" and Why Does It Matter?

**Deterministic** means the same input always produces the same output — mathematically guaranteed. SQL is deterministic: `SUM(subtotal)` on a fixed dataset returns the same number every time, forever.

This is the foundation of our anti-hallucination architecture. Because SQL is deterministic, we **trust these numbers completely**. When we give them to Gemini, we know they're correct — Gemini's job is only to explain them in English.

---

## 4.2 The 15 SQL Analytics Queries — What They Compute

| Query | KPI Computed | Key Technique |
|-------|-------------|---------------|
| Q01 | Monthly revenue per store (MoM %) | LAG() window function |
| Q02 | Order volume MoM % | LAG() window function |
| Q03 | Average delivery time per store | AVG() aggregation |
| Q04 | Customer rating per store | AVG() from delivery_logs |
| Q05 | Stockout rate per store | COUNT(stock=0) / COUNT(*) |
| Q06 | Gross margin % | (revenue - COGS) / revenue |
| Q07 | Top revenue-generating SKUs | RANK() window function |
| Q08 | Customer segment breakdown | GROUP BY segment |
| Q09 | Rider utilization rate | orders / riders |
| Q10 | 7-day rolling sales average | ROWS BETWEEN 6 PRECEDING |
| Q11 | Store performance ranking | RANK() OVER ORDER BY revenue |
| Q12 | Category-wise sales split | GROUP BY category |
| Q13 | Repeat vs new customer ratio | customer order frequency |
| Q14 | Average order value by segment | AVG(subtotal) GROUP BY segment |
| Q15 | SLA compliance rate | % deliveries ≤ 15 min |

---

## 4.3 Window Functions — The Most Important SQL Concept

A **window function** performs a calculation across a set of rows related to the current row — without collapsing the rows like GROUP BY does.

**The best analogy:** Imagine you have monthly temperature data. GROUP BY month gives you one average row per month. A window function gives you EVERY day's temperature AND the previous month's average on the same row simultaneously.

### LAG() — Used for Month-over-Month Comparison

```sql
SELECT 
    store_id,
    month,
    revenue,
    LAG(revenue, 1) OVER (PARTITION BY store_id ORDER BY month) AS prev_month_revenue
FROM monthly_revenue;
```

`LAG(revenue, 1)` returns the revenue from 1 row before the current row, within the same `store_id` partition. If this month's revenue is 91,656 and last month was 120,000:

```
MoM% = (91,656 - 120,000) / 120,000 × 100 = -23.57%
```

That's how we know Store 3 is in crisis.

### RANK() — Ranking Stores by Performance

```sql
RANK() OVER (ORDER BY total_revenue DESC)
```

Returns store rankings — Store 1 is #1, Store 3 might be #10 (last).

### ROW_NUMBER() — Sequential unique numbering

```sql
ROW_NUMBER() OVER (PARTITION BY store_id ORDER BY order_date)
```

Gives each order within a store a sequential number, useful for identifying "first order," "50th order," etc.

### Rolling Sum — 7-day rolling sales

```sql
SUM(daily_sales) OVER (
    PARTITION BY store_id 
    ORDER BY sale_date 
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
)
```

This calculates the sum of the past 7 days (including today) for each row — without GROUP BY collapsing the data.

---

## 4.4 CTEs — Common Table Expressions

A **CTE (Common Table Expression)** uses the `WITH` keyword to define a named temporary result set that you can reference later in the same query. It makes complex multi-step queries readable.

**Without CTE (deeply nested subqueries — unreadable):**
```sql
SELECT store_id, (revenue - prev) / prev * 100
FROM (SELECT store_id, revenue, LAG(revenue,1) OVER (...) prev
      FROM (SELECT store_id, SUM(subtotal) revenue FROM orders GROUP BY store_id, month) m) x;
```

**With CTE (readable, maintainable):**
```sql
WITH monthly_revenue AS (
    SELECT store_id, 
           DATE_FORMAT(order_date, '%Y-%m') AS month,
           SUM(subtotal) AS revenue
    FROM orders
    GROUP BY store_id, month
),
mom_comparison AS (
    SELECT store_id, month, revenue,
           LAG(revenue, 1) OVER (PARTITION BY store_id ORDER BY month) AS prev_revenue
    FROM monthly_revenue
)
SELECT store_id, month,
       ROUND((revenue - prev_revenue) / prev_revenue * 100, 2) AS mom_pct
FROM mom_comparison
WHERE prev_revenue IS NOT NULL;
```

Three named steps. Each CTE is readable on its own. This is exactly how we compute MoM revenue change for all 10 stores in one query.

---

## 4.5 KPI Thresholds — Healthy vs Crisis

| KPI | Formula | Healthy | Store 3 | Store 7 |
|-----|---------|---------|---------|---------|
| Revenue MoM % | (curr-prev)/prev × 100 | > -10% | **-23.57% 🔴** | +17.41% 🟢 |
| Orders MoM % | Same formula | > -15% | **-30.23% 🔴** | +16.0% 🟢 |
| Stockout Rate | (SKU-days stock=0 / total) × 100 | < 8% | **33.48% 🔴** | 5.54% 🟢 |
| Avg Delivery Time | AVG(actual_time) | < 15 min | **30.5 min 🔴** | 13.78 min 🟢 |
| Customer Rating | AVG(rating) | > 4.2 | **2.15/5.0 🔴** | 4.17/5.0 🟢 |
| Gross Margin % | (rev - COGS) / rev × 100 | > 35% | N/A | **28.13% 🔴** |

---

# PART 5 — ML MODEL 1: DEMAND FORECASTING (LAYER 3)

---

## 5.1 What Problem Does This Model Solve?

Every morning, a store manager asks: **"How much of each product should I order from the supplier today?"**

Order too little → stockout → lost sales → angry customers.
Order too much → perishables expire → wasted money.

Our model predicts the **next 7 days of demand** for every product at every store — 610 store-SKU combinations — and automatically triggers restock alerts when predicted demand exceeds current stock.

---

## 5.2 The Data

- Source: MySQL `inventory` table
- **54,900 records** = 90 days × 10 stores × ~61 SKUs
- Each record: `(store_id, product_id, date, closing_stock, units_sold)`
- Processed into **610 unique time series** — one per store-SKU combination

---

## 5.3 What Is Feature Engineering?

**Feature engineering** is the process of creating new input variables from raw data that help the model learn better. For time series, the most important technique is **lag features**.

A **lag feature** is a past value of the target variable, used as an input feature:

| Feature | What It Captures | Example |
|---------|-----------------|---------|
| `y_lag_1` | Yesterday's sales | Sold 42 units yesterday |
| `y_lag_7` | Same day last week | Last Monday sold 38 units |
| `y_lag_14` | Two weeks ago | 2 Mondays ago sold 45 units |
| `rolling_mean_7` | 7-day rolling average | Avg 41 units/day this week |
| `rolling_std_7` | 7-day std deviation | Demand varies by ±5 units |
| `day_of_week` | Day pattern | Monday=0 to Sunday=6 |

**Why are lag features necessary?** Without them, the model only sees the date — it has no "memory" of what sold recently. With lag features, the model knows: yesterday sold 55, last week this day sold 48, 7-day average is 42 → tomorrow will likely be ~50–55. This is how time series forecasting works at industry level.

---

## 5.4 The Algorithm — XGBoost Regressor

**XGBoost (eXtreme Gradient Boosting)** is an ensemble of decision trees built sequentially. Each tree corrects the errors of the previous ones. The "gradient" refers to gradient descent — each new tree takes a step in the direction that most reduces prediction error.

**Simple analogy:** Imagine 100 junior analysts each predicting tomorrow's milk demand. Analyst 1 makes a rough guess of 50 units. Analyst 2 looks at Analyst 1's errors and corrects them, predicting 48. Analyst 3 corrects Analyst 2's remaining errors... After 100 iterations, you combine all 100 predictions → highly accurate final answer.

**Why XGBoost, not Linear Regression?**
- Demand is NOT linear. Friday milk sales ≠ Monday milk sales × 2
- Complex interactions: (weekend + near-festival + monsoon) all together affect demand
- XGBoost handles non-linear patterns, feature interactions, missing values natively
- Built-in L1/L2 regularization prevents overfitting

**Why XGBoost, not Neural Networks?**
- Neural networks are built for high-dimensional data (images, audio, text)
- Our data is low-dimensional: 6 features per time step
- For tabular data with <10K rows, XGBoost consistently outperforms neural networks
- XGBoost trains in seconds, requires no GPU, provides interpretable feature importance

---

## 5.5 Restock Alert Logic

```python
# For each store-SKU pair:
predicted_7day_demand = sum(daily_predictions_next_7_days)
current_closing_stock = latest_stock_from_mysql

if predicted_7day_demand > current_closing_stock:
    # ALERT TRIGGERED
    days_until_stockout = closing_stock / (predicted_7day_demand / 7)
    priority = "HIGH" if days_until_stockout < 3 else "MEDIUM"
```

**Example — Store 3, Amul Paneer 200g:**
- Closing stock: 20 units
- 7-day predicted demand: 67 units
- 20 < 67 → RESTOCK ALERT triggered
- Days until stockout = 20 / (67/7) = **2.1 days** → HIGH priority emergency

---

## 5.6 Results

| Metric | Value |
|--------|-------|
| Store-SKU models trained | **610** |
| Restock alerts triggered | **577** |
| Written to MySQL | `demand_forecasts` table |
| CSV exported | `ml/demand_forecasts.csv` |
| JSON exported | `ml/demand_forecasts_latest.json` |

---

# PART 6 — ML MODEL 2: CUSTOMER CHURN PREDICTION (LAYER 3)

---

## 6.1 What Is Churn and Why Does It Matter?

**Churn** = a customer stops using your service. In quick-commerce, a "churned" customer is one who hasn't placed an order in 30+ days.

Why it matters financially:
- It costs **5–7× more** to acquire a new customer than to retain an existing one
- Average customer LTV (Lifetime Value) in quick-commerce: **Rs. 3,000**
- If we can identify WHO is about to churn and intervene BEFORE they leave — with a Rs. 100 voucher, for example — we save Rs. 3,000 in LTV at Rs. 100 cost

---

## 6.2 The Dataset

- **500 customers** total, from MySQL `customers` table
- **421 active** (84.2%) — haven't churned
- **79 churned** (15.8%) — inactive for 30+ days
- **Split:** 80% training (400 customers), 20% test (100 customers)
- Stratified split — maintains 84.2%/15.8% ratio in both sets

This is a **class imbalance problem** — 84.2% vs 15.8%. We need to handle this carefully in evaluation.

---

## 6.3 Input Features (12 Behavioral Signals)

| Feature | Importance | What It Tells Us |
|---------|-----------|-----------------|
| `days_since_last_order` | **45.6%** | Most powerful churn signal — inactivity = leaving |
| `orders_last_30_days` | 19.5% | Recent activity — recency is king |
| `total_spend` | 4.7% | Lifetime value — high spenders less likely to churn |
| `avg_delivery_time` | 4.3% | Service quality — slow delivery drives churn |
| `chan_enc` | 4.2% | Acquisition channel predicts retention |
| `total_orders` | ~4% | Overall engagement level |
| `avg_order_value` | ~3% | Spending pattern |
| `cancellation_rate` | ~3% | Frustration signal |
| `avg_delay_rate` | ~3% | Service quality experienced |
| `avg_rating` | ~3% | Satisfaction — low rating = churn risk |
| `segment_enc` | ~3% | Regular/Premium/VIP retention differs |
| `city_enc` | ~3% | City-level patterns |

**Why is `days_since_last_order` so dominant at 45.6%?** Because churn is defined as inactivity — this feature directly captures the definition. It's not data leakage; it's a genuinely valid business signal. A customer who hasn't ordered in 45 days is factually more likely to never order again than one who ordered yesterday.

---

## 6.4 The Algorithm — XGBoost Classifier

Same XGBoost framework, but this time:
- **Output:** Binary — 0 (active) or 1 (churned), plus a probability score
- **Loss function:** Log-loss (cross-entropy) instead of MSE
- **Threshold:** 0.70 — customers with churn probability > 70% → flagged HIGH-risk

**Label noise:** We deliberately flipped 4% of training labels randomly. This forces the model to learn **population-level patterns** rather than memorizing individual customers. Without label noise, accuracy would be 98%+ (overfitting). With 4% noise, we get a more realistic and generalizable 94.4%.

---

## 6.5 Model Evaluation Metrics — Explained Clearly

### Accuracy
```
Accuracy = Correct predictions / Total predictions × 100 = 94.40%
```
94 of every 100 test customers correctly classified (active or churned).

**Why isn't this suspicious?** The naive baseline — predict everyone as "active" (since 84.2% are active) — gets 84.2% accuracy. Our model beats the baseline by **10 percentage points**. That's a meaningful improvement, not coincidence.

### ROC-AUC = 0.8357
**ROC curve:** A plot of True Positive Rate (correctly catching churners) vs False Positive Rate (incorrectly flagging active customers as churners) at every possible threshold (0.0 to 1.0).

**AUC (Area Under the Curve):**
- AUC = 1.0 → Perfect model
- AUC = 0.5 → Random guessing (a coin flip)
- Our AUC = **0.8357** → If you randomly pick one actual churner and one actual active customer, our model correctly ranks the churner as higher-risk **83.57%** of the time.

Industry benchmark for e-commerce churn: 0.75–0.85 AUC. We're solidly in range.

### Precision = 93.33%
Of all customers our model flagged as "will churn" — 93.33% actually churned.
(Very few false alarms — we don't waste vouchers on loyal customers.)

### Recall = 70.00%
Of all customers who actually churned — we caught 70% of them.
(We miss 30% — but those customers receive no voucher, not a disaster.)

### Why Recall Matters More Than Precision for Churn
- **Missed churner (False Negative):** Customer leaves forever. Cost = Rs. 3,000 LTV lost.
- **False alarm (False Positive):** We send a voucher to someone who wasn't going to churn. Cost = Rs. 100 voucher.

The asymmetry is 30:1. Missing a churner costs 30× more than a false alarm. So for churn prediction, **recall is more important** — we want to catch as many churners as possible, even at the cost of some false alarms.

### 5-Fold Cross-Validation AUC = 0.8684 ± 0.0600

**Why cross-validation?** With only 500 customers, a single 80/20 split might give an optimistic or pessimistic score depending on which 100 customers happened to be in the test set.

**5-fold CV:** Divide 500 customers into 5 groups of 100. Train on 4 groups (400 customers), test on 1 (100). Repeat 5 times with different test groups. Average the 5 AUC scores.

**Result: 0.8684 ± 0.0600** means the model scores between 0.81 and 0.93 AUC across all five different held-out sets. The **low variance (±0.06)** proves the model genuinely generalizes — it's not just lucky on one specific test split.

---

## 6.6 Risk Segmentation and Business Impact

| Risk Level | Threshold | Count | Action | Cost |
|-----------|----------|-------|--------|------|
| HIGH | > 70% churn probability | **61 customers** | Rs. 100 voucher + WhatsApp | Rs. 6,100 |
| MEDIUM | 40–70% | 1 customer | Email re-engagement | Rs. 50 |
| LOW | < 40% | 438 customers | No action | Rs. 0 |

**ROI Calculation:**
- Cost of intervention: 61 × Rs. 100 = **Rs. 6,100**
- If 30% of HIGH-risk customers are retained: 0.30 × 61 = ~18 customers retained
- LTV per customer: Rs. 3,000
- Value recovered: 18 × Rs. 3,000 = **Rs. 54,900**
- Net ROI: (54,900 - 6,100) / 6,100 = **~800%**

---

# PART 7 — ML MODEL 3: DELIVERY ETA PREDICTION (LAYER 3)

---

## 7.1 What Problem Does This Model Solve?

The core Q-commerce promise is "delivery in 15 minutes." This is the **SLA (Service Level Agreement).**

If a store consistently delivers in 30 minutes, customers switch to competitors (Blinkit, Zepto). Our model **predicts which stores will breach their SLA today** — giving operations managers time to deploy additional riders before orders pile up.

---

## 7.2 The Data

- Source: MySQL `delivery_logs` table
- **2,848 delivery records** across all 10 stores
- Features from `delivery_logs`, `stores`, `riders`, and `orders` tables joined together

---

## 7.3 Input Features

| Feature | Importance | Meaning |
|---------|-----------|---------|
| `rider_capacity` | **89%** | Number of active riders at the store |
| `order_hour` | ~1% | Hour of day (0–23) |
| `day_of_week` | ~1% | Monday=0 to Sunday=6 |
| `delivery_distance_km` | ~1% | Distance from store to customer |
| `subtotal` | ~1% | Order value (larger order = longer packing time) |
| `is_peak_hour` | ~1% | 1 if 12–2pm or 7–9pm |
| `rider_pressure` | ~1% | orders_per_rider = active_orders / rider_count |
| `store_id_enc` | ~1% | Store-level fixed effect |
| `dist_peak` | ~1% | distance × is_peak_hour interaction |
| `low_riders` | ~1% | 1 if rider_count < 8 |

**Why is `rider_capacity` so dominant at 89%?** This makes perfect intuitive sense. With 5 riders and high order volume (Store 3), every rider handles multiple orders simultaneously → delivery times spike. With 15 riders (Connaught Place), each rider handles 1 order at a time → delivery is fast. The model correctly identified rider shortage as the dominant variable.

---

## 7.4 Performance Metrics

| Metric | Value | What It Means |
|--------|-------|--------------|
| **MAE** | **±2.74 min** | On average, predictions are 2.74 minutes off from actual |
| **RMSE** | **±3.22 min** | Penalizes large errors more (outliers matter more here) |
| **R²** | **42.6%** | Model explains 42.6% of delivery time variance |

---

## 7.5 Defending R² = 42.6% — This Will Definitely Be Asked

This is the most likely "trap question" in your viva. Here is the complete defense:

> **"R² of 42.6% is appropriate for three reasons:**
>
> **First**, delivery time has irreducible stochastic noise that cannot be captured from our available features: traffic signals changing, elevator wait times, customers not answering the door, rider routing choices. These events are **unmeasurable** from order/rider data — they constitute the unexplained 57.4%.
>
> **Second**, the business-critical metric is **MAE ±2.74 minutes** — predictions within 3 minutes of actual delivery time. For managing a 15-minute SLA and triggering fleet overflow alerts, 3-minute precision is fully sufficient.
>
> **Third**, this aligns with **published academic literature**: 40–60% R² is typical for urban logistics prediction without real-time GPS data and traffic APIs. Our top feature — rider_capacity at 89% — correctly captures why Store 3 (5 riders) gets 30.5 minutes while other stores (12–15 riders) get under 14 minutes."

---

## 7.6 Results by Store

| Store | Riders | Predicted ETA | SLA Risk |
|-------|--------|-------------|---------|
| **QuickMart Koramangala (Store 3)** | **5** | **30.5 min** | **100%** 🔴 |
| QuickMart Sector 56 Gurugram (Store 7) | 13 | 13.5 min | 0% 🟢 |
| QuickMart Connaught Place | 15 | 13.0 min | 0% 🟢 |
| QuickMart Lajpat Nagar | 12 | 12.9 min | 0% 🟢 |
| QuickMart Whitefield | 13 | 13.0 min | 0% 🟢 |

Store 3 is a clear outlier — 2× the SLA, 100% breach probability. Every other store is healthy.

---

# PART 8 — THE GEMINI AI LAYER (LAYER 4)

---

## 8.1 What Is a Large Language Model (LLM)?

An LLM is a neural network trained on billions of text documents. It learns statistical patterns of language — which words follow which words, which ideas are connected, how to reason about text. When you give it a prompt, it generates the most statistically likely continuation.

**Google Gemini 2.5 Flash** is Google DeepMind's LLM optimized for speed (2–5 second responses) and cost efficiency — making it suitable for production API calls in our dashboard.

---

## 8.2 What Is AI Hallucination?

**Hallucination** = an LLM confidently generates text that is factually incorrect or entirely invented.

**Why does it happen?** LLMs generate the statistically likely next word — they don't have a database connection or access to your specific data. If you ask Gemini "What was Store 3's revenue last month?" without providing any data, it generates a plausible-sounding number based on patterns in its training data. That number is completely made up.

**Example of hallucination:**
You ask: "What was QuickMart Store 3's revenue last month?"
Gemini says: "Rs. 1,45,000 with 12% month-on-month growth."
Reality: Rs. 91,656 with -23.57% decline.

A store manager who reads the hallucinated answer might order more stock (unnecessary cost) or ignore the actual crisis. Business decisions worth lakhs of rupees made on fictional data.

---

## 8.3 Our Anti-Hallucination Architecture

**The fundamental rule: SQL computes ALL numbers → Gemini only INTERPRETS.**

```
Step 1: SQL queries run → extract exact KPIs from MySQL
        (revenue: Rs.91,656, MoM: -23.57%, stockout: 33.48%, rating: 2.15)

Step 2: ML models run → generate predictions
        (demand: 577 restock alerts, churn: 61 HIGH-risk, ETA: 30.5 min)

Step 3: All numbers assembled into a structured JSON payload

Step 4: JSON + instruction sent to Gemini:
        "Use ONLY these figures. Do NOT invent or extrapolate any number."

Step 5: Gemini generates a diagnosis using ONLY the provided data
```

Gemini in our system is like a highly articulate analyst who is handed a complete data report and asked to write an executive summary. All the numbers are already in the report — the analyst cannot invent new ones.

---

## 8.4 What the Gemini Prompt Looks Like

```python
prompt = f"""
You are a Senior Business Intelligence Analyst specializing in quick-commerce.

The following data has been computed from SQL queries against a live MySQL database 
and from trained XGBoost ML models. Use ONLY these figures.
Do NOT extrapolate, estimate, or introduce any metric not explicitly provided.

STORE DIAGNOSTICS — Store {store_id}:
{json.dumps(diagnostics_payload, indent=2)}

Provide: (1) Executive summary, (2) Root cause analysis, (3) Priority recommendations.
"""
response = model.generate_content(prompt)
```

Three key components:
1. **Persona** — sets the expert context
2. **Data** — the verified JSON payload
3. **Instructions** — the anti-hallucination boundary

---

## 8.5 The Deterministic Fallback System

**Problem:** Gemini API could be offline during your demo. What then?

**Our solution:** Before every Gemini call, `ai/insights.py` performs a **1-second timeout probe** to the Gemini endpoint. If the probe fails:

1. System instantly activates the **deterministic fallback engine**
2. Pre-programmed IF-THEN rules analyze the same JSON data:
   - stockout rate > 25% → flag: INVENTORY_CRISIS
   - delivery time > 20 min → flag: FLEET_CRISIS
   - MoM revenue < -15% → flag: REVENUE_DECLINE
   - margin < 30% → flag: MARGIN_EROSION
3. Output is analytically equivalent — same root cause, same recommendations, just rule-based instead of AI-generated
4. Added latency: **under 1 second**

**What to say if asked "What if Gemini is offline during your demo?"**
> "We specifically engineered for this. A 1-second timeout probe runs before every Gemini call. If it fails, the deterministic fallback activates instantly — same diagnosis, same recommendations, under 1 second of added latency. This demonstrates a production-engineering principle: systems must be resilient to external service dependencies."

---

## 8.6 Our System vs "Just Asking ChatGPT"

| Dimension | ChatGPT / Gemini.com | Our System |
|-----------|---------------------|-----------|
| Data freshness | Training data (months/years old) | Live MySQL, seconds old |
| Numbers | Hallucinated | SQL-verified, guaranteed |
| Store specificity | Generic advice | Store 3-specific diagnosis |
| Actionability | Vague suggestions | Specific alerts auto-dispatched |
| ML predictions | None | 7-day demand, churn, ETA |
| Auditability | Blackbox | Full SQL audit trail |

---

## 8.7 What Is RAG? How Does Our System Relate?

**RAG (Retrieval-Augmented Generation):** A pattern where an LLM retrieves relevant documents from a knowledge base and uses them as context before generating a response. Used in systems like enterprise chatbots that search company documents.

**Our system is structurally similar:** We retrieve SQL-verified numerical data from MySQL and inject it into the Gemini prompt as grounding context. The difference is our "knowledge base" is a live transactional SQL database rather than pre-indexed text documents. We retrieve KPIs via SQL queries rather than vector search.

---

# PART 9 — DASHBOARD AND ALERTS (LAYER 5)

---

## 9.1 The Streamlit Dashboard — 5 Tabs

| Tab | Icon | What It Shows |
|-----|------|-------------|
| AI Decision Synthesis | 🧠 | Gemini diagnosis, root causes, recommendations, severity badge |
| 7-Day SKU Demand Forecast | 📦 | All SKUs with predicted demand, stock, days-to-stockout (color-coded) |
| Customer Churn Retention Engine | 👥 | HIGH/MEDIUM/LOW risk customers, intervention actions |
| Dynamic Delivery ETA & SLA Risk | 🚴 | All stores ranked by predicted ETA, SLA breach risk |
| Automated Operational Alert Center | 🔔 | All 12 notifications with priority, recipient, channel |

**What Is Streamlit?** A Python library that generates interactive web applications from pure Python code. No HTML, CSS, or JavaScript required. When a user interacts with a widget (dropdown, button), Python re-executes from the top — this "reactive" execution model automatically re-renders the dashboard with new data.

---

## 9.2 Why Not Power BI?

This question will come up. Know this table cold:

| Dimension | Power BI | Our System |
|-----------|----------|-----------|
| Cost | Rs. 1,200–2,400/user/month | Open source (free) |
| Analytics level | Descriptive only | All 4 levels (D/D/P/P) |
| ML integration | Plugin-based, limited | Native XGBoost |
| Gemini AI | No | Yes |
| Alert dispatch | No | Yes — automated WhatsApp/SMS/Email |
| Programming | No-code / low-code | Full Python = more flexible |

Power BI shows what happened. Our system shows what happened, why, what will happen, and what to do — automatically.

---

## 9.3 The 4 Analytics Maturity Levels (Critical Concept)

| Level | Type | Question Answered | Example |
|-------|------|------------------|---------|
| 1 | **Descriptive** | What happened? | Revenue last month: Rs. 91,656 |
| 2 | **Diagnostic** | Why did it happen? | Revenue fell because rider shortage drove churn |
| 3 | **Predictive** | What will happen? | Amul Paneer stocks out in 2.1 days |
| 4 | **Prescriptive** | What should I do? | Emergency PO auto-generated, fleet overflow alert sent |

**Power BI covers only Level 1 (and partial Level 2). Our system covers all 4.**

This is one of the most important differentiators to mention in your viva.

---

## 9.4 The 12 Automated Notifications

| Priority | Alert Type | Recipient | Channel |
|---------|-----------|----------|---------|
| HIGH | INVENTORY_RESTOCK_ALERT | Store Manager | WhatsApp + SMS + POS |
| HIGH | FLEET_OVERFLOW_ALERT | Regional Ops Head | WhatsApp + Email |
| HIGH | CUSTOMER_CHURN_VOUCHER | At-risk Customer | WhatsApp |
| HIGH | REVENUE_DECLINE_ALERT | City Manager | Email |
| HIGH | STOCKOUT_CRISIS | Procurement Team | Email + Slack |
| MEDIUM | MARGIN_EROSION_ALERT | Finance Head | Email |
| MEDIUM | DELIVERY_SLA_WARNING | Ops Team | SMS |
| MEDIUM | RATING_DROP_ALERT | Quality Team | Email |
| LOW | DEMAND_FORECAST_REPORT | Store Manager | Email |
| LOW | CHURN_WEEKLY_REPORT | CRM Team | Email |
| LOW | INVENTORY_REPLENISHMENT | Store Manager | POS |
| LOW | DELIVERY_PERFORMANCE | Ops Head | Dashboard |

**Alert Logic:**
```python
if predicted_7day_demand > closing_stock:
    priority = "HIGH" if days_until_stockout < 3 else "MEDIUM"

if predicted_eta > 20:        # minutes
    trigger FLEET_OVERFLOW_ALERT priority HIGH

if churn_probability > 0.70:
    dispatch Rs.100 voucher

if mom_revenue_pct < -15:     priority = HIGH
elif mom_revenue_pct < -5:    priority = MEDIUM
```

---

# PART 10 — THE TWO DEMO STORES

---

## 10.1 Store 3 — QuickMart Koramangala 🔴 CRITICAL

This is your primary demo case. Know every number and the causal chain.

| Metric | Value | Status |
|--------|-------|--------|
| Monthly Revenue | Rs. 91,656 | 🔴 -23.57% MoM |
| Total Orders | 83 | 🔴 -30.23% MoM |
| Stockout Rate | **33.48%** | 🔴 Target < 8% |
| Avg Delivery Time | **30.5 min** | 🔴 Target < 15 min |
| Customer Rating | **2.15 / 5.0** | 🔴 Benchmark > 4.2 |
| Active Riders | **5** | 🔴 Healthy: 12–15 |

### The Root Cause Chain (This Is What Makes It Impressive)

```
Only 5 riders
    → Delivery time = 30.5 min (2× the 15-min SLA)
        → Customer rating collapses to 2.15 / 5.0
            → Customers switch to Blinkit / Zepto
                → Orders drop 30.23% MoM
                    → Revenue drops 23.57% MoM
                        → Store can't restock properly
                            → Stockout rate reaches 33.48% (4× threshold)
```

One root cause (5 riders) cascades into 5 crisis indicators. Our system traces the entire chain automatically.

### What to Say When Showing Store 3

> "Look at Store 3 — Koramangala, Bengaluru. The system has flagged it CRITICAL. Revenue is down 23.57% month-over-month. Orders dropped 30%. Stockout rate is 33.48% — target is under 8%. Rating collapsed to 2.15 out of 5. Why? Our system traces the root cause to just 5 delivery riders. With only 5 riders, delivery takes 30 minutes instead of 13. Customers are frustrated. They leave. And our churn model has identified 23 of their customers as HIGH-risk — meaning we can still save them, but only if we act today."

---

## 10.2 Store 7 — QuickMart Sector 56 Gurugram 🟡 PROFITABILITY WARNING

This is your second demo case — it looks healthy on the surface but has a hidden problem.

| Metric | Value | Status |
|--------|-------|--------|
| Monthly Revenue | Rs. 45,337 | 🟢 +17.41% MoM |
| Total Orders | 116 | 🟢 +16.0% MoM |
| Stockout Rate | 5.54% | 🟢 Healthy |
| Avg Delivery Time | **13.78 min** | 🟢 Healthy |
| Customer Rating | 4.17 / 5.0 | 🟢 Healthy |
| Gross Margin | **28.13%** | 🔴 Target > 35% |

### Why This Is the "Growth Trap"

Revenue is growing, orders are growing, delivery is fast, rating is good. Without our system, the city manager celebrates this store. But the gross margin is only 28% (target is 35%+).

This means: for every Rs. 100 of revenue, the company is spending Rs. 72 on cost of goods. The store is likely giving excessive discounts or absorbing delivery costs. It is growing — but **losing money on every order**.

### What to Say When Showing Store 7

> "Contrast with Store 7 — Gurugram. Revenue up 17%, orders up 16%, delivery 13.78 minutes, rating 4.17. This looks like a star performer. But the system flags it PROFITABILITY WARNING. Gross margin is only 28%. The company is subsidizing customers through excessive discounts. Without our system, the city manager celebrates. With our system, the CFO knows they need to rethink the discount strategy immediately — this store is on a 'growth trap' trajectory losing money on every order it delivers."

---

# PART 11 — BUSINESS ROI AND COMPETITIVE ADVANTAGE

---

## 11.1 Annual ROI Calculation

| Value Driver | Calculation | Annual Value |
|-------------|------------|-------------|
| Stockout prevention | 577 alerts × 20% prevent stockout × Rs. 500 avg lost sale | Rs. 57,700 |
| Churn reduction | 61 customers × 30% retained × Rs. 3,000 LTV | Rs. 54,900 |
| Delivery optimization | Avoided SLA breach penalties | Rs. 1,00,000 |
| Analyst time saved | 4 hrs/day × Rs. 2,000/hr × 250 working days | Rs. 20,00,000 |
| **Total annual value** | | **Rs. 23,43,400** |
| System cost (cloud + API) | | Rs. 90,000/yr |
| **Net ROI** | | **~2,500%** |

---

## 11.2 Why This Is Better Than Existing Solutions

1. **vs Manual analysis:** 65 seconds vs 4–6 hours. Zero analyst time for routine diagnosis.
2. **vs Power BI:** All 4 analytics levels vs Level 1 only. ML predictions + AI synthesis + auto-alerts.
3. **vs ChatGPT/Gemini.com:** SQL-grounded numbers vs hallucinated numbers. Store-specific vs generic.
4. **vs No system:** Proactive intervention before crisis worsens vs reactive firefighting.

---

## 11.3 Scalability Path (If Asked)

Current: 10-store academic prototype.

| Component | Current | At Scale (1,000 stores) |
|-----------|---------|------------------------|
| Database | MySQL single instance | AWS Aurora / RDS read replicas |
| ML pipeline | Sequential Python | Apache Spark (200K models) |
| Gemini calls | Direct API | Redis + Celery job queue |
| Dashboard | Streamlit | React + FastAPI |
| Alerts | JSON files | Apache Kafka event streams |

The modular layer design means each layer scales independently.

---

# PART 12 — IMPLEMENTATION DETAILS (CODE-LEVEL QUESTIONS)

---

## 12.1 How to Run the System

```powershell
# Step 1: Start MySQL (via XAMPP Control Panel)

# Step 2: Navigate to project root
cd "D:\Desktop\Major Project Updated\Major Project"

# Step 3: Run the ML pipeline (~65 seconds)
python ml\run_all_ml.py

# Step 4: Launch the dashboard
python -m streamlit run app\streamlit_app.py
# Opens at: http://localhost:8501
```

---

## 12.2 What Does `run_all_ml.py` Do?

It is the **master pipeline orchestrator**. Uses Python's `subprocess.run()` to execute each module as a separate process, in sequence:

```
Module 1: demand_forecast.py    → 610 models, 577 alerts, writes demand_forecasts
Module 2: churn_model.py        → 500 customers scored, writes churn_scores
Module 3: delivery_predictor.py → 2,848 records, ETA per store, writes delivery_predictions
Module 4: alert_notifier.py     → reads all 3 outputs, generates 12 notifications JSON
```

After each module, it checks the return code (0 = success). Each module is independent — single-responsibility principle.

---

## 12.3 What Is `.env` and Why?

```
# .env file
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=quickcommerce_db
GEMINI_API_KEY=AIza...
```

We use `python-dotenv` — `load_dotenv()` reads the file and injects values as environment variables accessed via `os.getenv('DB_PASSWORD')`.

**Why not hardcode?** If code is committed to GitHub, hardcoded credentials expose the database password publicly. `.env` is listed in `.gitignore` to prevent accidental commit. Industry standard for production: AWS Secrets Manager, HashiCorp Vault.

---

## 12.4 Why JSON for ML Output?

ML results are written to both MySQL and JSON files (`ml/*.json`).

**Three reasons for JSON:**
1. **Dashboard speed:** Streamlit reads pre-computed JSON directly instead of running SQL queries on every page load — much faster
2. **API readiness:** JSON is the universal API format; deploying as a REST API requires zero format conversion
3. **Debuggability:** JSON files are human-readable — anyone can inspect ML outputs without a database client

---

## 12.5 What Is `store_3_insight.json`?

Pre-computed AI diagnosis from the most recent pipeline run. When Streamlit loads, it reads this JSON instantly (< 10ms) instead of making a live Gemini API call (2–5 seconds). This is a **caching pattern** — the dashboard loads fast, Gemini is only called when the user clicks "Re-Run Executive Diagnosis." Also enables offline demo.

---

## 12.6 How Does pandas Help?

pandas provides the DataFrame — a 2D in-memory table like a spreadsheet. Used throughout:

```python
# Reading SQL query results
df = pd.read_sql("SELECT * FROM inventory WHERE store_id=3", conn)

# Lag feature engineering
df['y_lag_7'] = df.groupby('product_id')['units_sold'].shift(7)

# Cleaning
df = df.dropna()                    # remove rows with missing lag values
df['cancel_rate'] = df['cancel_rate'].fillna(0)  # fill missing with 0

# Preparing ML inputs
X = df[['y_lag_1', 'y_lag_7', 'rolling_mean_7', 'day_of_week']]
y = df['units_sold']

# Writing output
df.to_csv('demand_forecasts.csv', index=False)
```

---

## 12.7 Test Cases (TC-01 to TC-10)

| Test | What It Verifies |
|------|----------------|
| TC-01 | MySQL connection — all 11 tables present |
| TC-02 | SQL accuracy — KPIs match manually verified expected values |
| TC-03 | Demand forecast end-to-end — 610 models, 577 alerts |
| TC-04 | Churn model — accuracy ≥ 90%, AUC ≥ 0.80 |
| TC-05 | Delivery ETA — MAE ≤ 5 minutes (achieved ±2.74 min) |
| TC-06 | Anti-hallucination — parse Gemini output, cross-check every number against input JSON |
| TC-07 | Alert dispatch — 12 notifications in `active_notifications.json` |
| TC-08 | Fallback activation — Gemini blocked → deterministic fallback activates correctly |
| TC-09 | Store switching — Streamlit updates all 5 tabs correctly |
| TC-10 | Full pipeline timing — end-to-end completes under 120 seconds |

---

# PART 13 — TEAM ROLES (Each Person Must Know Their Layer)

---

| Team Member | Layer | What They Built |
|-------------|-------|----------------|
| **Tanya Jain (23104034)** | Layer 1 + 2 | MySQL schema (11 tables, 3NF, FK constraints), seed data generation, 15 SQL analytics queries (window functions, CTEs, all KPIs) |
| **Tanmay Tiwari (23104032)** | Layer 3 | All 3 XGBoost models, feature engineering (lag features, behavioral signals), `run_all_ml.py` master orchestrator, hyperparameter tuning |
| **Tanishq Jain (23104060)** | Layer 4 + 5 | Google Gemini API integration, anti-hallucination architecture, deterministic fallback, Streamlit dashboard (5 tabs), alert notification dispatcher |

**Rule for viva:** Only explain YOUR layer in full depth. For other layers, say: "That was [name]'s component — I can describe how it integrates with my layer."

---

# PART 14 — DEFENDING WEAK POINTS

---

## "Your data is synthetic"

> "Our data is calibrated to real-world quick-commerce unit economics from published industry research. The system's architectural and algorithmic value is independent of specific numbers. We embedded two analytically distinct failure modes — Store 3 (operational crisis) and Store 7 (margin erosion) — that the ML models discover from data patterns, not from hardcoded rules. The pipeline works identically with real data: replace the MySQL connection string and every query, model, and prompt functions unchanged. Using synthetic data was necessary due to absence of an NDA with a production operator — a realistic constraint shared by virtually all academic capstone projects."

---

## "R² = 42.6% is too low"

> "R² of 42.6% is appropriate for urban delivery time prediction. The 57.4% unexplained variance represents genuine stochastic noise — traffic signals, elevator waits, customer response delays — factors unmeasurable from our features. The operationally meaningful metric is MAE ±2.74 minutes: predictions within 3 minutes of actual delivery, fully sufficient for 15-minute SLA management. This aligns with academic literature where 40–60% R² is typical for urban logistics without real-time GPS/traffic data."

---

## "94.4% churn accuracy is suspiciously high / data leakage"

> "The 94.4% is legitimate. Baseline (predict everyone active): 84.2% — we beat it by 10 points. `days_since_last_order` with 45.6% importance directly reflects the definition of churn — this is a valid forward-looking business signal, not leakage. We added 4% label noise — without it, accuracy would be 98%+. 5-fold CV AUC 0.8684 ± 0.0600 (low variance) confirms genuine generalization."

---

## "This was an MBA project, not CS/IT"

> "Every solution artifact is a CS and software engineering deliverable: 3NF relational schema with 11 tables and foreign key constraints; SQL window functions (LAG, RANK, ROW_NUMBER) and CTEs; three XGBoost gradient boosting models with cross-validation and ROC-AUC evaluation; LLM API integration with an anti-hallucination architectural pattern; full-stack reactive web application. The business problem provides context; the CS curriculum provides every tool we used to solve it."

---

## "What if Gemini is offline?"

> "We anticipated this. A 1-second timeout probe runs before every Gemini call. If it fails, the deterministic fallback activates instantly with IF-THEN rules. Output is analytically equivalent — same root causes, same recommendations. Total added latency: under 1 second. This demonstrates a production engineering principle: systems must be resilient to external service dependencies."

---

## "Gemini can still hallucinate even with your prompt"

> "Correct — prompt engineering isn't a mathematical guarantee. We mitigate through: (1) structured JSON leaves no ambiguity — Gemini references exact values directly; (2) explicit instruction 'do NOT introduce any metric not in this JSON' triggers instruction-following training; (3) TC-06 test case cross-checks every number in AI output against input JSON for each pipeline run. Production extension: Gemini grounding + post-processing validation layer."

---

## "No real deployment"

> "Our system runs as a fully functional end-to-end pipeline on a local MySQL instance with 11 populated tables and live ML execution. The distinction from production is infrastructure: MySQL → AWS RDS, Streamlit → cloud server, ML pipeline → cron job, Gemini → production API key. These are DevOps changes, not algorithmic ones. The diagnostic logic, ML models, anti-hallucination architecture, and alert rules are all production-ready."

---

# PART 15 — COMPLETE Q&A MASTER LIST (All 70 Questions)

---

> This section has the question and the key points to cover. Full answers are in VIVA_STUDY_GUIDE.md sections.

### Category A — Basic / Intro

**Q1. What is quick-commerce?** Ultra-fast 10–15 min delivery using dark stores. Blinkit, Zepto, Swiggy Instamart. No walk-in customers. 2–3 km radius.

**Q2. What is a dark store?** Small 1,000–3,000 sqft hyper-local warehouse. No customer floor. Only for order fulfilment by riders.

**Q3. What problem does your project solve?** Manual diagnosis takes 4–6 hours. We do it in 65 seconds with SQL+ML+AI.

**Q4. Who are the users?** Store manager, regional ops head, analytics team. Secondary: procurement, CRM, finance.

**Q5. Each member's role?** Tanya = DB+SQL, Tanmay = ML models, Tanishq = Gemini+Streamlit+Alerts.

**Q6. How long to build?** ~4 months. Month 1: problem + DB. Month 2: data + SQL + ML prototype. Month 3: ML refinement + Gemini. Month 4: Streamlit + alerts + testing + docs.

**Q7. Tech stack and why?** Python 3.11, MySQL 8.0, XGBoost 3.2, Gemini 2.5 Flash, Streamlit 1.67, pandas 2.3. Each chosen for industry dominance and fit to use case.

---

### Category B — Architecture

**Q8. Explain 5-layer architecture in 2 minutes.** DB → SQL analytics → ML predictions → Gemini interpretation → Streamlit + alerts. 65 seconds total.

**Q9. Why MySQL not MongoDB/PostgreSQL?** Relational data needs native JOINs. Window functions and CTEs are SQL-native. MongoDB: app-level joins (slow). MySQL 8.0 = industry standard in India.

**Q10. What is a window function?** Calculation across related rows without collapsing them. LAG() for MoM: `LAG(revenue,1) OVER (PARTITION BY store_id ORDER BY month)`.

**Q11. What is a CTE?** `WITH` keyword creates named temp result sets. Makes complex queries readable. Used for 3-stage MoM analysis.

**Q12. What does 3NF mean?** 1NF: atomic values, no repeating groups. 2NF: depends on WHOLE key. 3NF: no transitive dependencies (non-key → non-key → key).

**Q13. Why separate orders and order_items?** Avoid repeating groups (1NF violation). One order can have many items — flexible, normalized.

**Q14. Data flow from MySQL to Gemini output?** MySQL → SQL queries → KPI DataFrames → ML models → JSON payload → Gemini prompt → NL synthesis → Streamlit.

---

### Category C — Machine Learning

**Q15. What is XGBoost? Why not linear regression?** Sequential ensemble of trees, each corrects previous errors. Demand is non-linear; XGBoost handles non-linearity, feature interactions, L1/L2 regularization.

**Q16. What are lag features?** Past values of target as model inputs. y_lag_1, y_lag_7, y_lag_14, rolling_mean_7. Gives model "memory" of recent history.

**Q17. Training vs test set?** Train on 80% (model learns). Test on 20% (never seen during training — honest performance estimate).

**Q18. What does ROC-AUC 0.8357 mean?** Model correctly ranks a churner above an active customer 83.57% of the time. Industry benchmark 0.75–0.85 AUC.

**Q19. Precision vs Recall — which matters for churn?** Recall matters more. Missed churner = Rs. 3,000 LTV lost. False alarm = Rs. 100 voucher cost. Asymmetry 30:1 favors catching more churners.

**Q20. Why is 94.4% not suspicious?** Baseline 84.2%. Beat by 10 points. 4% label noise added. 5-fold CV AUC 0.8684±0.0600 confirms generalization.

**Q21. What is 5-fold CV?** 5 rounds, each using different 20% as test set. Average score. Proves model isn't just lucky on one split. 500 customers — single split unreliable.

**Q22. Defend R²=42.6%** Stochastic noise is real (traffic, elevators). MAE ±2.74 min is the business metric. 40–60% typical in literature. rider_capacity at 89% explains the Store 3 outlier.

**Q23. What is overfitting? How prevented?** Model memorizes training data, fails on new data. Prevention: L1/L2 regularization, max_depth=4, 4% label noise.

**Q24. What is gradient boosting?** Sequential trees, each corrects residuals of previous. Learning rate × tree prediction added to ensemble. Gradient descent on loss function.

**Q25. Why not neural networks?** Our data: 12 features, 500 rows — too low-dimensional. XGBoost dominates tabular benchmarks. Interpretable. Trains in seconds. No GPU needed.

**Q26. Show restock alert logic.** `if predicted_7day > closing_stock: alert`. `days_until_stockout = stock / (demand/7)`. HIGH if < 3 days. Store 3 Paneer: 20 stock, 67 demand, 2.1 days.

**Q27. Classification vs regression?** Classification: discrete category output (churned/not). Regression: continuous number (units/minutes). Loss: log-loss vs MSE.

---

### Category D — AI/Gemini

**Q28. What is the Gemini API?** Google DeepMind's LLM API. Gemini 2.5 Flash = fast (2–5 sec), cost-efficient. `google-generativeai` Python SDK. API key in `.env`.

**Q29. What is hallucination?** LLM confidently generates factually wrong text. Example: inventing Rs. 1,45,000 revenue when real is Rs. 91,656. Pattern-matching, not database access.

**Q30. How did you prevent hallucination?** Anti-hallucination boundary: SQL computes all numbers → Gemini only interprets. JSON payload + explicit instruction "do NOT invent any metric."

**Q31. What if Gemini is offline?** 1-second timeout probe → deterministic fallback → IF-THEN rules → analytically equivalent output. < 1 second added latency.

**Q32. vs ChatGPT?** ChatGPT: hallucinated, generic, stale training data. Ours: SQL-verified, store-specific, live data, ML predictions, auto-alerts.

---

### Category E — Results & Validation

**Q33. How do you know it works?** 10-test case suite: TC-01 to TC-10. Database, SQL accuracy, demand, churn, delivery, anti-hallucination, alerts, fallback, store switching, pipeline timing.

**Q34. Business ROI?** Rs. 23 lakhs value / Rs. 90,000 cost = ~2,500% annual ROI. Churn alone: 800% ROI. Analyst time saved: Rs. 20 lakhs/year.

**Q35. vs Power BI?** Power BI: descriptive only, Rs. 1,200–2,400/user/month, no ML, no AI, no auto-alerts. Ours: all 4 analytics levels, free, native ML+AI+alerts.

---

### Category F — Code/Implementation

**Q36. What happens when I select Store 3 in Streamlit?** store_id=3 → SQL queries → demand/churn/delivery filtered for Store 3 → JSON loaded → 5 tabs re-render.

**Q37. Command to start the system?** `python ml\run_all_ml.py` then `python -m streamlit run app\streamlit_app.py` from project root.

**Q38. What is .env and why?** Stores secrets (DB credentials, Gemini API key) outside code. `python-dotenv` loads them. Prevents credential exposure in GitHub.

**Q39. How does `run_all_ml.py` work?** `subprocess.run()` executes 4 modules in sequence. Checks return codes. Single-responsibility: each module connects to DB, runs its model, writes output.

**Q40. Why JSON for ML output?** Dashboard speed (no SQL on every load), API readiness (zero format conversion), debuggability (human-readable).

---

### Category G — Design Decisions

**Q41. Why synthetic data?** Calibrated to real unit economics. Architecture value is independent of specific numbers. No NDA available. Pipeline works identically with real data.

**Q42. What would change with real data?** Better ML accuracy (richer variation), expanded features (GPS tracks, weather), MLOps pipeline (drift detection, A/B testing).

**Q43. How does it handle all 10 stores?** ML runs for all 10. 610 models = all stores × all SKUs. Dropdown shows all 10. Store 3 and 7 highlighted as interesting cases.

**Q44. Scalable to 1,000 stores?** See scalability table in Part 11. MySQL → Aurora, sequential ML → Spark, Gemini → job queue, Streamlit → React+FastAPI.

**Q45. 6 more months — what would you add?** Real data NDA, MLOps (Evidently AI drift detection), NLP on reviews for churn, transformer models (N-BEATS/TFT).

---

### Category H — MBA→IT / Curriculum

**Q46. What CS skills did this require?** DBMS (3NF, FK, SQL), ML/AI (XGBoost, CV, AUC), Software Engineering (layered architecture, single-responsibility, test cases), API Integration (REST, JSON, timeout/fallback), Data Structures (time series arrays, rolling windows, priority queues).

**Q47. 4 analytics levels?** Descriptive (what) → Diagnostic (why) → Predictive (what will) → Prescriptive (what to do). We implement all 4.

**Q48. Curriculum mapping?** DBMS → Layer 1+2. ML/AI → Layer 3+4. Software Engineering → modular design + test cases. Distributed Systems → Gemini API + fallback design.

**Q49. PO/PSO outcomes?** PO1 (Engineering Knowledge), PO2 (Problem Analysis), PO3 (Design/Development), PO5 (Modern Tool Usage), PSO1 (Domain Application).

**Q50. Most impressive aspect?** Anti-hallucination architecture + closed-loop prescriptive pipeline. Demonstrates two distinct failure modes. 65-second end-to-end. All 4 analytics levels in one integrated system.

---

### Additional Technical Questions (Q51–Q70)

**Q51. Feature importance in XGBoost?** How often each feature is used in tree splits, weighted by improvement to loss. rider_capacity 89% — intuitively explains Store 3 (5 riders) vs others (12–15 riders).

**Q52. How handle missing data?** XGBoost handles natively. `dropna()` after lag creation. `fillna(0)` for cancellation_rate. `pd.notna()` validation before MySQL insert.

**Q53. Supervised vs unsupervised?** Supervised: labeled data, known outcomes. All 3 models = supervised. Unsupervised: no labels (K-Means). Extension: cluster stores by performance tier.

**Q54. Stockout rate formula?** `(SKU-days with stock=0 / total SKU-days) × 100`. Store 3: 33.48% of 5,490 product-days had zero stock.

**Q55. What is a prompt?** Input text to LLM defining task + context. Ours: Persona + verified JSON data + "use only these figures" instruction.

**Q56. Real-time capability?** Current: batch pipeline. Real-time: Kafka streaming + online ML + webhook alerts + auto-refresh dashboard. Modular design makes this a component-level swap.

**Q57. Purpose of `store_3_insight.json`?** Pre-computed AI diagnosis for fast dashboard load. Avoids live API call on every page load. Enables offline demo.

**Q58. What happens to ML tables when pipeline reruns?** Tables are truncated and repopulated. Fresh predictions always. Historical tracking requires adding `run_timestamp` column — standard MLOps "prediction logging."

**Q59. What is pandas?** Python DataFrame library. `read_sql()`, `.shift()` for lags, `dropna()`, `fillna()`, `to_csv()`. Lingua franca of Python data science.

**Q60. JSON — why export ML results?** Dashboard speed + API readiness + debuggability.

**Q61. Churn ROI specifically?** 61 × Rs. 100 = Rs. 6,100 cost. 30% × 61 × Rs. 3,000 = Rs. 54,900 recovered. Net ROI = 800%.

**Q62. How validate SQL queries?** Manual calculation verification for small samples. Sanity checks (revenue > 0, stockout 0–100%). Cross-reference ML inputs vs SQL KPIs.

**Q63. What is Streamlit vs traditional website?** Pure Python, no HTML/CSS/JS. Reactive re-execution on widget interaction. Not for production-grade multi-user apps (use React+FastAPI for that).

**Q64. Environmental impact?** Fewer stockouts → fewer emergency restocking deliveries. Better ETA → fewer failed deliveries (fewer round trips). Maps to PO7 (Environment & Sustainability).

**Q65. Biggest limitation?** Synthetic data — ML performance not validated against real distribution. Solution: NDA with startup, or Instacart public dataset as proxy. MLOps drift detection for production.

**Q66. What is a Foreign Key?** References PK of another table. Enforces referential integrity. Prevents orphaned records. `orders.customer_id → customers.customer_id`.

**Q67. Accuracy vs ROC-AUC — which for imbalanced data?** ROC-AUC. Accuracy is misleading when 84.2% are one class. AUC evaluates ranking ability independent of class imbalance.

**Q68. How does alert dispatcher decide notifications?** Reads all 3 ML JSON outputs + SQL KPIs. Applies threshold logic per alert type. Constructs notification dictionaries. Sorts by priority. Writes to `active_notifications.json`.

**Q69. Purpose of `requirements.txt`?** Lists exact package versions. `pip install -r requirements.txt` for reproducible environment. Exact versions ensure identical ML outputs across machines.

**Q70. Mean vs median — which for delivery time?** Median — delivery time is right-skewed (most are 13–15 min, rare outliers at 60+ min pull the mean up). We also recommend P95 for production: delivery time experienced by worst 5% of customers.

---

# PART 16 — POWER PHRASES AND KEY NUMBERS

---

## Numbers to Know Cold

| Number | Context |
|--------|---------|
| **65 seconds** | End-to-end pipeline |
| **54,900** | Inventory records |
| **610** | Store-SKU models |
| **577** | Restock alerts |
| **94.40%** | Churn accuracy |
| **0.8357** | Churn ROC-AUC |
| **0.8684 ± 0.0600** | 5-fold CV AUC |
| **±2.74 min** | Delivery MAE |
| **42.6%** | Delivery R² |
| **30.5 min** | Store 3 predicted ETA |
| **13.78 min** | Store 7 delivery (healthy) |
| **33.48%** | Store 3 stockout rate |
| **5.54%** | Store 7 stockout rate |
| **2.15/5.0** | Store 3 customer rating |
| **4.17/5.0** | Store 7 customer rating |
| **-23.57%** | Store 3 revenue MoM |
| **+17.41%** | Store 7 revenue MoM |
| **28.13%** | Store 7 gross margin (problem) |
| **61** | HIGH-risk churn customers |
| **12** | Automated notifications |
| **~2,500%** | Annual system ROI |
| **5 riders** | Store 3 root cause |
| **45.6%** | days_since_last_order importance |
| **89%** | rider_capacity importance |
| **2.1 days** | Amul Paneer stockout (Store 3) |

---

## Power Phrases — Use These Exact Words

| Instead of... | Say... |
|--------------|--------|
| "our ML model" | "our XGBoost gradient boosting ensemble" |
| "it predicts things" | "recursive multi-step time-series forecasting with lag features" |
| "AI doesn't make up numbers" | "anti-hallucination architecture with SQL-grounded semantic boundary" |
| "the backup plan" | "deterministic fail-safe with 1-second timeout probe" |
| "accuracy of our model" | "94.40% accuracy with 0.8357 ROC-AUC on a stratified held-out test set" |
| "our DB is organized" | "schema normalized to Third Normal Form with referential integrity via FK constraints" |
| "it shows charts" | "Layer 5: Streamlit-based prescriptive analytics dashboard with 5 interactive operational tabs" |
| "we compared months" | "month-over-month variance via LAG() window function over PARTITION BY store_id" |
| "the data is fake" | "domain-calibrated synthetic data with two embedded analytical failure modes" |
| "all 4 types of analytics" | "all four analytics maturity levels: descriptive, diagnostic, predictive, prescriptive" |

---

## Recovery Lines (If You Blank Out)

- *"Let me anchor this in our specific results — [state a number from above]"*
- *"In our implementation, we specifically chose X because [one clear reason]"*
- *"That's an excellent point. In our current scope we addressed this by [what you did], and an extension would be [future work]. Our current approach achieves [metric] which satisfies [business requirement]."*
- *"Let me walk you through the data flow to answer that..."*

---

## "I Don't Know" Protocol

> "That's an excellent question. In our implementation we used [what you did]. An alternative approach [mention one] could potentially improve [specific metric], and that's something we've identified as future work. However, our current approach achieves [specific metric] which meets the production requirement for [business use case]."

---

# PART 17 — DEMO SCRIPT (Full Run-Through)

---

## Pre-Demo Checklist (5 minutes before viva)

```
□ MySQL service running (XAMPP Control Panel → MySQL → Start)
□ Terminal open at: D:\Desktop\Major Project Updated\Major Project\
□ Browser ready (Chrome recommended)
□ Nothing else running that slows the machine
```

## Step 1 — Run the ML Pipeline (0:00 to 1:30)

```powershell
cd "D:\Desktop\Major Project Updated\Major Project"
python ml\run_all_ml.py
```

**Say as it runs:**
> "I'm starting the master ML pipeline. This runs against our live MySQL database — 54,900 inventory records, 500 customers, 2,848 delivery logs across 10 dark stores."

*(Module 1 completes)*
> "The demand forecasting model just trained 610 XGBoost models — one per store-SKU combination — and identified 577 products that will run out within 7 days. Highest priority: Amul Paneer at Store 3 — only 2.1 days of stock remaining."

*(Module 2 completes)*
> "The churn classifier has scored all 500 customers. 61 are HIGH-risk — above 70% churn probability. The model achieves 94.4% accuracy and 0.8357 ROC-AUC."

*(Module 3 completes)*
> "The delivery model predicts 30.5 minutes average for Store 3 — double our 15-minute SLA. Every other store is under 14 minutes. Root cause: Store 3 has only 5 riders."

*(Alert module completes)*
> "12 operational notifications have been dispatched — restock orders, fleet overflow alerts, churn vouchers. The entire pipeline took 65 seconds."

## Step 2 — Launch Streamlit (1:30 to 2:00)

```powershell
python -m streamlit run app\streamlit_app.py
```

> "Starting the decision intelligence dashboard — built entirely in Python."
*(Browser opens at http://localhost:8501)*

## Step 3 — Store 3: The Crisis (2:00 to 7:00)

Select **Store 3 — QuickMart Koramangala** from dropdown.

> "Store 3, Koramangala, Bengaluru. Notice the red CRITICAL badge. Revenue down 23.57% month-over-month. Orders dropped 30%. Stockout rate: 33.48% — target is under 8%. Delivery: 30.5 minutes — target is under 15. Rating: 2.15 out of 5 — benchmark is above 4.2. Root cause: 5 riders. Every healthy store has 12–15."

**Tab 1 (AI Synthesis):**
> "Gemini AI synthesis — grounded in SQL-verified numbers. Every figure matches our database exactly — this is our anti-hallucination architecture."

**Tab 2 (Demand):**
> "Red rows: stockout in under 3 days. Amul Paneer: 20 units on hand, 67 needed over 7 days — 2.1 days to stockout. Emergency purchase order already dispatched."

**Tab 3 (Churn):**
> "23 of Store 3's customers are HIGH-risk. Primary driver: inactivity after one bad delivery. The model is 94.4% accurate. These are customers we can still save with an intervention voucher."

**Tab 4 (Delivery ETA):**
> "100% SLA delay risk for Store 3. Every order will be late. Fix: deploy 8 additional riders. Fleet overflow alert already sent to Regional Ops Head."

**Tab 5 (Alerts):**
> "All 12 alerts automatically dispatched. Store manager, procurement, ops head — all notified. Zero manual reports. 65 seconds."

## Step 4 — Store 7: The Margin Trap (7:00 to 10:00)

Select **Store 7 — QuickMart Sector 56 Gurugram:**

> "Contrast with Store 7 — Gurugram. Revenue up 17%, orders up 16%, delivery 13.78 minutes, rating 4.17. Looks like a star performer. But the system flags it PROFITABILITY WARNING. Gross margin only 28%. The company is subsidizing customers through excessive discounts. Without our system, the city manager celebrates. With our system, the CFO knows they need to rethink the discount strategy immediately — this is a growth trap."

---

*End of Complete Study Notes | QuickCommerce AI | JIIT Noida | Project 15B29CI692*
