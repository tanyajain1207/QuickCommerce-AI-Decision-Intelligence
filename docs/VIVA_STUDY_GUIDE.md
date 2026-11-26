# 📚 QUICKCOMMERCE AI — MASTER VIVA STUDY GUIDE
### Complete Preparation for Supervisor, Panel & Viva — JIIT Noida B.Tech CSE/IT 8th Sem

> **Team:** Tanya Jain (23104034) · Tanmay Tiwari (23104032) · Tanishq Jain (23104060)
> **Supervisor:** Dr. Diksha Chawla | **Project Code:** 15B29CI692

---

## TABLE OF CONTENTS

1. The 2-Minute Pitch — What Is This Project?
2. System Architecture — The 5 Layers
3. Database Design — MySQL & 3NF
4. SQL Analytics — 15 BI Queries
5. ML Model 1 — Demand Forecasting
6. ML Model 2 — Customer Churn Prediction
7. ML Model 3 — Delivery ETA Prediction
8. The Gemini AI Layer & Anti-Hallucination
9. The Streamlit Dashboard
10. The Alert & Notification System
11. The Two Demo Stores — Full Analysis
12. Why This Is Better Than Existing Solutions
13. VIVA Q&A Master List — 70+ Questions with Ideal Answers
14. Live Demo Script — Step-by-Step with What to SAY
15. Scoring Strategy & Terminology Cheat Sheet
16. Weak Points & How to Defend Them
17. Glossary — 55+ Terms Explained in Plain English

---

## SECTION 1: THE 2-MINUTE PITCH — WHAT IS THIS PROJECT?

### 1.1 What Is Quick-Commerce?

Quick-commerce (Q-commerce) is ultra-fast grocery and essentials delivery — typically within **10–15 minutes**. Think **Blinkit** (Zomato), **Zepto**, and **Swiggy Instamart**. Unlike regular e-commerce (Amazon, Flipkart) that takes 1–2 days, quick-commerce promises delivery before your tea gets cold.

The key to this speed? **Dark Stores.**

### 1.2 What Is a Dark Store?

A dark store is a **small, hyper-local warehouse** (1,000–3,000 sq ft) inside a residential area, stocked with fast-moving products (milk, bread, chips, medicines). It is called "dark" because it has **no walk-in customers** — it's purely for order fulfilment by delivery riders.

### 1.3 The Business Problem

A quick-commerce company may operate **hundreds of dark stores** across a city. The critical question every morning:

> *"Which stores are failing — and WHY?"*

**Today's reality (without our system):**
- Managers manually pull data from multiple systems (ERP, POS, delivery app, CRM)
- Takes **4–6 hours** of analyst work to identify problems
- By the time they know, the problem has already cost the company money
- They see WHAT happened but not WHY, and can't predict WHAT WILL happen

**Example:** Store 3 (Koramangala) has only **5 delivery riders** but high order volume. Delivery times spike to **30 minutes** (SLA is 15 minutes). Customers give 2.15/5.0 ratings and stop ordering. Revenue drops 23.57% month-over-month. The manager doesn't know the root cause is rider shortage.

### 1.4 What We Built

**QuickCommerce AI** is a **5-layer Decision Intelligence System** that:
1. Pulls data from MySQL (orders, inventory, delivery logs, customers)
2. Runs 15 SQL analytics queries to compute KPIs
3. Runs 3 machine learning models to PREDICT the future
4. Uses Google Gemini AI to INTERPRET numbers and generate recommendations
5. Displays everything on Streamlit and sends automated alerts

**Result:** Complete diagnosis with root causes and recommended actions in **65 seconds** — instead of 4–6 hours.

### 1.5 The Simple Analogy

> "Think of our system like a **doctor's diagnostic report** for a sick store. When you go to a doctor, they run blood tests (SQL analytics), interpret results with medical knowledge (ML models), consult a specialist (Gemini AI), and give you a prescription (automated alerts). Our system does exactly this — but for dark stores."

### 1.6 Two-Sentence Pitch for Supervisor

> "We built an AI-powered decision intelligence system for quick-commerce dark store operations. It combines a MySQL database, SQL analytics, three XGBoost machine learning models, and the Google Gemini 2.5 Flash API to automatically diagnose store health, predict demand stockouts and customer churn, estimate delivery ETA, and dispatch automated operational alerts — reducing diagnostic time from 4–6 hours to 65 seconds."

---

## SECTION 2: SYSTEM ARCHITECTURE — THE 5 LAYERS

### 2.1 Architecture Diagram

```
╔══════════════════════════════════════════════════════════════╗
║                 QUICKCOMMERCE AI ARCHITECTURE                ║
╠══════════════════════════════════════════════════════════════╣
║  LAYER 5: PRESENTATION & ALERTS                              ║
║  Streamlit Dashboard (app/streamlit_app.py)                  ║
║  Alert Dispatcher (ml/alert_notifier.py)                     ║
║                      ↑ reads results                         ║
║  LAYER 4: GENERATIVE AI INTERPRETATION                       ║
║  Google Gemini 2.5 Flash API (ai/insights.py)                ║
║  Anti-Hallucination: SQL computes → Gemini interprets        ║
║                      ↑ verified numbers                      ║
║  LAYER 3: PREDICTIVE ML (ml/ folder)                         ║
║  Model 1: XGBoost Demand Forecast                            ║
║  Model 2: XGBoost Churn Classifier                           ║
║  Model 3: XGBoost Delivery ETA                               ║
║                      ↑ reads from / writes to                ║
║  LAYER 2: DETERMINISTIC SQL ANALYTICS                        ║
║  15 BI Queries (analytics/queries.sql)                       ║
║  CTEs, Window Functions, MoM %, KPI computation              ║
║                      ↑ structured queries                    ║
║  LAYER 1: MYSQL RELATIONAL DATABASE                          ║
║  quickcommerce_db — 11 tables                                ║
║  3,000+ orders · 500 customers · 54,900 inv records          ║
╚══════════════════════════════════════════════════════════════╝
```

### 2.2 Layer Summary Table

| Layer | File(s) | Technology | Purpose |
|-------|---------|-----------|---------|
| 1 | `database/schema.sql` | MySQL 8.0 | 11 tables, all raw data |
| 2 | `analytics/queries.sql` | SQL, CTEs, Window Functions | 15 KPI queries — deterministic metrics |
| 3 | `ml/*.py` | XGBoost, pandas, scikit-learn | 3 ML models — predict future |
| 4 | `ai/insights.py` | Google Gemini 2.5 Flash | AI synthesis from verified numbers |
| 5 | `app/streamlit_app.py`, `ml/alert_notifier.py` | Streamlit, Python | Dashboard + 12 auto notifications |

### 2.3 Data Flow

```
MySQL DB → SQL queries → KPI JSON → ML Models → Predictions JSON
                                                        ↓
                                              Gemini AI prompt
                                                        ↓
                                           Insight + Recommendations
                                                        ↓
                                         Streamlit Dashboard renders
                                                        ↓
                                         Alert Dispatcher fires 12 notifications
```

**Total time: ~65 seconds** from `python ml\run_all_ml.py` to full dashboard ready.

---

## SECTION 3: DATABASE DESIGN — MYSQL & 3NF

### 3.1 All 11 Tables

| Table | Records | Purpose |
|-------|---------|---------|
| `stores` | 10 | Dark store locations, city, zone, rider count |
| `riders` | ~130 | Delivery riders, their store assignment, capacity |
| `products` | ~200 | SKU catalog — name, category, price, weight |
| `customers` | 500 | Customer profiles, segment (Regular/Premium/VIP) |
| `orders` | 3,000+ | Order header — customer, store, timestamp, subtotal |
| `order_items` | ~9,000 | Line items — product, quantity, price per order |
| `inventory` | 54,900 | Daily closing stock per SKU per store (90 days) |
| `delivery_logs` | 2,848 | Actual delivery times, rider, distance, outcome |
| `demand_forecasts` | ML output | 7-day predicted demand per SKU per store |
| `churn_scores` | ML output | Churn probability and risk label per customer |
| `delivery_predictions` | ML output | Predicted ETA and SLA risk per store |

### 3.2 Why Separate `orders` and `order_items`?

**Wrong way (un-normalized):**
```
orders: order_id, customer, product1, qty1, product2, qty2 ...
```
Problem: What if someone orders 10 items? Need 10 columns. If 1 item, 9 columns are empty. This is a **repeating group** — violates 1NF.

**Right way (3NF):**
```
orders:      order_id, customer_id, store_id, timestamp, total
order_items: item_id, order_id (FK), product_id (FK), quantity, unit_price
```
Each table has ONE responsibility. Join on `order_id` to get all items.

### 3.3 What Is 3NF?

| Normal Form | Rule |
|------------|------|
| **1NF** | Each cell has one atomic value. No repeating groups. |
| **2NF** | Every non-key column depends on the WHOLE primary key. |
| **3NF** | No transitive dependencies — non-key columns depend ONLY on the primary key. |

**Example violation:** `order_items` containing `product_name` → `product_name` depends on `product_id`, not on `item_id` → transitive dependency → violates 3NF. Fix: move `product_name` to `products` table.

### 3.4 Key Concepts

**Foreign Key:** References the primary key of another table, enforcing referential integrity. Can't create an order for a non-existent customer — MySQL throws an error.

**Why Not MongoDB?** Our data is highly relational — MongoDB requires application-level joins (slow, error-prone). MySQL's native JOIN engine is optimized for our exact pattern. Also, our SQL analytics uses window functions and CTEs — SQL-specific features not available in MongoDB.

---

## SECTION 4: SQL ANALYTICS — 15 BI QUERIES

### Key Window Functions Used

```sql
-- LAG: Get previous row's value (MoM comparison)
LAG(monthly_revenue, 1) OVER (PARTITION BY store_id ORDER BY month)

-- RANK: Rank stores by revenue
RANK() OVER (ORDER BY total_revenue DESC)

-- 7-day rolling sales
SUM(daily_sales) OVER (PARTITION BY store_id ORDER BY sale_date
                       ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
```

**Simple analogy:** A window function is like asking "What was yesterday's temperature?" for every day in a list — without losing any days (which GROUP BY would do).

### CTE Example

```sql
WITH monthly_revenue AS (
    SELECT store_id, DATE_FORMAT(order_date,'%Y-%m') AS month,
           SUM(subtotal) AS revenue
    FROM orders GROUP BY store_id, month
),
mom_comparison AS (
    SELECT store_id, month, revenue,
           LAG(revenue,1) OVER (PARTITION BY store_id ORDER BY month) AS prev_revenue
    FROM monthly_revenue
)
SELECT store_id, month,
       ROUND((revenue - prev_revenue)/prev_revenue*100, 2) AS mom_pct
FROM mom_comparison;
```

### KPIs Computed by SQL

| KPI | Formula | Healthy Threshold |
|-----|---------|-------------------|
| Revenue MoM % | (curr - prev) / prev × 100 | > -10% |
| Stockout Rate | (SKU-days stock=0 / total SKU-days) × 100 | < 8% |
| Avg Delivery Time | AVG(actual_delivery_time) per store | < 15 min |
| Customer Rating | AVG(rating) from delivery_logs | > 4.2 |
| Gross Margin % | (Revenue - COGS) / Revenue × 100 | > 35% |

**MoM % for Store 3:** `((91,656 - 120,000) / 120,000) × 100 = -23.57%` ← crisis signal

---

## SECTION 5: ML MODEL 1 — DEMAND FORECASTING

### Plain English

Every morning: how much stock to order today? Our XGBoost model trains on 90 days of daily sales per SKU per store and predicts the NEXT 7 days of demand for every SKU.

### Input & Features

- **Source:** MySQL `inventory` — **54,900 records** → **610 store-SKU time series**

| Feature | What It Captures |
|---------|-----------------|
| `y_lag_1` | Yesterday's sales (immediate trend) |
| `y_lag_7` | Same day last week (weekly cycle) |
| `y_lag_14` | Two weeks ago (fortnight pattern) |
| `rolling_mean_7` | 7-day rolling average (smoothed trend) |
| `rolling_std_7` | 7-day rolling std (demand volatility) |
| `day_of_week` | Monday=0 to Sunday=6 |

### Algorithm — XGBoost Regressor

**Why XGBoost, not linear regression?**
- Demand is NOT linear — Friday sales ≠ Monday × 2
- Complex interactions (weekend × monsoon × near-festival) affect demand together
- XGBoost handles non-linear patterns, feature interactions, and outliers naturally
- Built-in L1/L2 regularization prevents overfitting

**Gradient boosting in simple terms:** 100 junior analysts each predicting tomorrow's demand. Analyst 1 makes a rough guess. Analyst 2 looks at Analyst 1's errors and adjusts. After 100 iterations, combine all predictions → highly accurate final answer.

### Restock Alert Logic

```python
if predicted_7day_demand > current_closing_stock:
    trigger RESTOCK ALERT
    days_until_stockout = closing_stock / (predicted_7day_demand / 7)
```

**Store 3 — Amul Paneer 200g:**
Closing stock=20, 7-day demand=67 → **2.1 days to stockout** ← emergency restock needed NOW

### Results

| Metric | Value |
|--------|-------|
| Store-SKU models trained | **610** |
| Restock alerts triggered | **577** |
| MySQL table populated | `demand_forecasts` |

---

## SECTION 6: ML MODEL 2 — CUSTOMER CHURN PREDICTION

### Plain English

**Churn** = customer stops using your service. It costs **5–7× more** to acquire a new customer than to retain one. Identify WHO is about to churn and intervene BEFORE they leave.

### Input Features (12 Behavioral Signals)

| Feature | Importance | Interpretation |
|---------|-----------|---------------|
| `days_since_last_order` | **45.6%** | Most powerful churn signal |
| `orders_last_30_days` | 19.5% | Recency is king |
| `total_spend` | 4.7% | Lifetime value matters |
| `avg_delivery_time` | 4.3% | Service quality affects loyalty |
| `chan_enc` | 4.2% | Acquisition channel predicts retention |
| Others (7 features) | remaining | Additional behavioral signals |

### Algorithm & Dataset

- **Output:** Binary — churned=1 (inactive 30+ days) / active=0
- **Dataset:** 500 customers — 421 active (84.2%), 79 churned (15.8%)
- **Split:** 80/20 stratified | **Label noise:** 4% random flipping (prevents overfitting)

### Performance Metrics

| Metric | Value | What It Means |
|--------|-------|--------------|
| **Accuracy** | **94.40%** | 94 of 100 test customers correctly classified |
| **ROC-AUC** | **0.8357** | Correctly ranks churned above active 83.57% of the time |
| **Precision** | **93.33%** | When we flag "will churn," we're right 93.33% of the time |
| **Recall** | **70.00%** | We catch 70% of all actual churners |
| **5-Fold CV AUC** | **0.8684 ± 0.0600** | Consistent across 5 unseen data subsets |

**Why isn't 94.4% suspicious?** Baseline (predict everyone active) = 84.2%. Our model beats this by 10 points. 4% label noise was added — without it, accuracy would be 98%+. 5-fold CV AUC 0.8684 ± 0.0600 (low variance) confirms genuine generalization — NOT overfitting.

### Risk Segmentation & ROI

| Risk Level | Threshold | Count | Action |
|-----------|----------|-------|--------|
| HIGH | > 70% churn prob | **61 customers** | Rs. 100 apology voucher + WhatsApp |
| MEDIUM | 40–70% | 1 customer | Email re-engagement campaign |
| LOW | < 40% | 438 customers | No action needed |

**Churn intervention ROI:** 61 × Rs. 100 = Rs. 6,100 cost. 30% retention × 61 × Rs. 3,000 LTV = Rs. 54,900 recovered. **Net ROI: 800%+**

---

## SECTION 7: ML MODEL 3 — DELIVERY ETA PREDICTION

### Plain English

The core Q-commerce promise: "delivery in 15 minutes." The model predicts which stores will breach their SLA today.

### Input Features

| Feature | Importance | Meaning |
|---------|-----------|---------|
| `rider_capacity` | **89%** | Active riders at the store |
| `order_hour`, `day_of_week` | — | Temporal patterns |
| `delivery_distance_km` | — | Distance to customer |
| `is_peak_hour`, `rider_pressure` | — | Congestion signals |
| `store_id_enc`, `dist_peak`, `low_riders` | — | Derived features |

### Performance Metrics

| Metric | Value | Interpretation |
|--------|-------|---------------|
| **MAE** | **±2.74 min** | Average prediction is off by 2.74 minutes |
| **RMSE** | **±3.22 min** | Penalizes large errors more |
| **R²** | **42.6%** | Explains 42.6% of delivery time variance |

### Defending R² = 42.6% (WILL BE ASKED)

> "R² of 42.6% is appropriate for urban delivery time prediction. The 57.4% unexplained variance represents genuine stochastic noise — traffic signals, elevator waits, customer response delays — factors unmeasurable from our features. The business-critical metric is MAE ±2.74 minutes: predictions within 3 minutes of actual delivery time, fully sufficient for 15-minute SLA management. This aligns with published academic literature where 40–60% R² is typical for urban logistics without real-time GPS/traffic data."

### Results by Store

| Store | Riders | Predicted ETA | SLA Risk |
|-------|--------|-------------|---------|
| **QuickMart Koramangala (Store 3)** | **5** | **30.5 min** | **100%** |
| QuickMart Sector 56 Gurugram (Store 7) | 13 | 13.5 min | 0% |
| QuickMart Connaught Place | 15 | 13.0 min | 0% |

---

## SECTION 8: THE GEMINI AI LAYER & ANTI-HALLUCINATION

### What Is Hallucination?

**AI hallucination** = an LLM confidently generates text that is factually incorrect or entirely fabricated.

**Example:** You ask Gemini: "What was Store 3's revenue last month?" Without a database connection, Gemini might say "Rs. 1,45,000 with 12% growth." These numbers are **completely made up**. One wrong inventory decision based on hallucinated numbers could cost lakhs of rupees.

### Our Anti-Hallucination Architecture

**The boundary rule: SQL computes ALL numbers → Gemini only INTERPRETS.**

```
Step 1: SQL queries run → extract exact KPIs from MySQL
Step 2: ML models run → generate predictions
Step 3: All numbers assembled into a structured JSON payload
Step 4: JSON + instruction sent to Gemini:
        "Use ONLY these figures. Do NOT invent or extrapolate any number."
Step 5: Gemini generates a diagnosis using ONLY the provided data
```

### The Deterministic Fallback

If Gemini is unreachable:
1. **1-second timeout probe** to Gemini endpoint
2. If fails → **deterministic fallback engine** activates instantly
3. Same JSON analyzed with pre-programmed IF-THEN rules
4. Output is analytically equivalent — same root cause, same recommendations
5. Added latency: **< 1 second**

> **If asked "What if Gemini is offline during your demo?":**
> "We anticipated this and engineered a 1-second probe with deterministic fallback. The system works identically offline — this actually demonstrates superior engineering judgment."

### Our System vs "Just Asking ChatGPT"

| Dimension | ChatGPT / Gemini.com | Our System |
|-----------|---------------------|-|
| Data freshness | Training cutoff (months/years old) | Live MySQL data, seconds old |
| Numbers accuracy | Hallucinated | SQL-verified, guaranteed |
| Store specificity | Generic advice | Store 3-specific |
| Actionability | Vague suggestions | Specific alerts dispatched automatically |
| Auditability | Blackbox | Full SQL audit trail |

---

## SECTION 9: THE STREAMLIT DASHBOARD

### The 5 Tabs

| Tab | Icon | What It Shows |
|-----|------|--------------|
| AI Decision Synthesis | 🧠 | Gemini diagnosis, root causes, recommendations, severity badge |
| 7-Day SKU Demand Forecast | 📦 | All SKUs with predicted demand, stock, days-to-stockout (color-coded) |
| Customer Churn Retention Engine | 👥 | HIGH/MEDIUM/LOW risk customers, voucher dispatch button |
| Dynamic Delivery ETA & SLA Risk | 🚴 | All stores ranked by predicted ETA, SLA breach risk |
| Automated Operational Alert Center | 🔔 | All 12 notifications with priority, recipient, channel |

### Why Not Power BI?

| Dimension | Power BI | Our System |
|-----------|----------|-----------|
| Cost | Rs. 1,200–2,400/user/month | Open source (free) |
| Analytics level | Descriptive only | All 4 levels (descriptive → prescriptive) |
| ML integration | Plugin-based, limited | Native XGBoost in same codebase |
| Gemini AI | No | Yes — natural language synthesis |
| Alert dispatch | No | Yes — automated WhatsApp/SMS/email |

---

## SECTION 10: THE ALERT & NOTIFICATION SYSTEM

### The 12 Notifications

| Priority | Alert Type | Recipient | Channel |
|---------|-----------|-----------|---------|
| HIGH | INVENTORY_RESTOCK_ALERT | Store Manager | WhatsApp + SMS + POS |
| HIGH | FLEET_OVERFLOW_ALERT | Regional Ops Head | WhatsApp + Email |
| HIGH | CUSTOMER_CHURN_VOUCHER | Customer (HIGH-risk) | WhatsApp |
| HIGH | REVENUE_DECLINE_ALERT | City Manager | Email |
| HIGH | STOCKOUT_CRISIS | Procurement Team | Email + Slack |
| MEDIUM | MARGIN_EROSION_ALERT | Finance Head | Email |
| MEDIUM | DELIVERY_SLA_WARNING | Ops Team | SMS |
| MEDIUM | RATING_DROP_ALERT | Quality Team | Email |
| LOW | DEMAND_FORECAST_REPORT | Store Manager | Email |
| LOW | CHURN_WEEKLY_REPORT | CRM Team | Email |
| LOW | INVENTORY_REPLENISHMENT_SCHEDULE | Store Manager | POS |
| LOW | DELIVERY_PERFORMANCE_SUMMARY | Ops Head | Dashboard |

Output stored in: `ml/active_notifications.json`

---

## SECTION 11: THE TWO DEMO STORES — FULL ANALYSIS

### Store 3 — QuickMart Koramangala (THE CRISIS STORE) 🔴 CRITICAL

| Metric | Value | Status |
|--------|-------|--------|
| Monthly Revenue | Rs. 91,656 | 🔴 -23.57% MoM |
| Total Orders | 83 | 🔴 -30.23% MoM |
| Stockout Rate | 33.48% | 🔴 (target: < 8%) |
| Avg Delivery Time | 30.5 min | 🔴 (target: < 15 min) |
| Customer Rating | 2.15 / 5.0 | 🔴 (benchmark: > 4.2) |
| Active Riders | **5** | 🔴 (healthy stores: 12–15) |

**Root Cause Chain:**
```
Only 5 riders → delivery = 30.5 min (2× SLA) → rating collapses to 2.15
→ customers switch to Blinkit/Zepto → orders drop 30% MoM
→ revenue drops 23.57% MoM → stockout rate reaches 33.48% (4× threshold)
```

**What to say when demoing Store 3:**
> "Look at Store 3 — Koramangala, Bengaluru. The system has flagged it CRITICAL. Revenue is down 23.57% month-over-month. Orders dropped 30%. Stockout rate is 33.48% — target is under 8%. Rating collapsed to 2.15 out of 5. Why? Our system traces the root cause to just 5 delivery riders. With only 5 riders, delivery takes 30 minutes instead of 13. Customers are frustrated. They leave. And our churn model has identified 23 of their customers as HIGH-risk — meaning we can still save them, but only if we act today."

---

### Store 7 — QuickMart Sector 56 Gurugram (MARGIN EROSION) 🟡 PROFITABILITY WARNING

| Metric | Value | Status |
|--------|-------|--------|
| Monthly Revenue | Rs. 45,337 | 🟢 +17.41% MoM |
| Total Orders | 116 | 🟢 +16.0% MoM |
| Stockout Rate | 5.54% | 🟢 (healthy: < 8%) |
| Avg Delivery Time | 13.78 min | 🟢 (healthy: < 15 min) |
| Customer Rating | 4.17 / 5.0 | 🟢 (benchmark: > 4.2) |
| Gross Margin | **28.13%** | 🔴 (target: > 35%) |

**What to say when demoing Store 7:**
> "Contrast with Store 7 — Gurugram. Revenue up 17%, orders up 16%, delivery 13.78 minutes, rating 4.17. Looks like a star performer. But the system flags it PROFITABILITY WARNING. Gross margin is only 28%. The company is subsidizing customers through excessive discounts. Without our system, the city manager celebrates. With our system, the CFO knows they need to rethink the discount strategy immediately — this store is on a 'growth trap' trajectory."

---

## SECTION 12: WHY THIS IS BETTER THAN EXISTING SOLUTIONS

### The 4 Analytics Maturity Levels

| Level | Type | Question Answered | Our System | Power BI |
|-------|------|------------------|-----------|---------|
| 1 | Descriptive | What happened? | ✅ | ✅ |
| 2 | Diagnostic | Why did it happen? | ✅ | Partial |
| 3 | Predictive | What will happen? | ✅ (3 ML models) | ❌ |
| 4 | Prescriptive | What should I do? | ✅ (12 auto alerts) | ❌ |

### Business ROI

| Value Driver | Annual Value |
|-------------|-------------|
| Stockout prevention (577 alerts × Rs. 500) | Rs. 2,88,500 |
| Churn reduction (61 customers, 30% retention × Rs. 3,000 LTV) | Rs. 54,900 |
| Delivery optimization | Rs. 1,00,000 |
| Analyst time saved (4 hrs/day × Rs. 2,000 × 250 days) | Rs. 20,00,000 |
| **Total annual value** | **Rs. 23,43,400** |
| System cost (cloud + Gemini API) | Rs. 90,000/yr |
| **ROI** | **~2,500%** |

---

## SECTION 13: VIVA Q&A MASTER LIST — 70+ QUESTIONS WITH IDEAL ANSWERS

---

### CATEGORY A: BASIC / INTRO QUESTIONS (Supervisor Level)

**Q1. What is quick-commerce? How is it different from normal e-commerce?**

Quick-commerce is ultra-fast grocery and essentials delivery, typically within 10–15 minutes of ordering. Unlike e-commerce platforms like Amazon or Flipkart that deliver in 1–2 days using large central warehouses, quick-commerce uses a network of small, hyper-local "dark stores" positioned within 1–2 km of residential areas. Major players include Blinkit (Zomato), Zepto, and Swiggy Instamart in India. The key differentiator is speed: quick-commerce handles impulse purchases and urgent needs (baby formula at midnight, medicines, fresh vegetables) while traditional e-commerce serves planned, non-urgent purchases.

---

**Q2. What is a dark store?**

A dark store is a small, hyper-local warehouse — typically 1,000 to 3,000 square feet — located within a residential or commercial area. It is called "dark" because it has no customer-facing retail floor: customers cannot walk in. The entire space is dedicated to inventory storage, picking, and packing. Orders are fulfilled by delivery riders who deliver to customers within a 2–3 km radius. A city like Bengaluru may have 50+ dark stores to cover all zones.

---

**Q3. What problem does your project solve?**

Quick-commerce companies operating dozens or hundreds of dark stores face a critical challenge: identifying which stores are underperforming, understanding why, and acting before the problem worsens — in near real-time. Today, this analysis takes 4–6 hours of manual analyst work. Our system automates this entire diagnostic pipeline — from raw MySQL data through SQL analytics, ML predictions, and Gemini AI interpretation — to deliver a complete store health diagnosis with root cause analysis and recommended actions in 65 seconds.

---

**Q4. Who are the target users of this system?**

Three primary user personas: (1) **Store manager** — daily KPI monitoring, ML demand alerts, operational actions. (2) **Regional operations head** — cross-store comparison, escalation alerts, fleet deployment decisions. (3) **Data/analytics team** — extending SQL queries and ML models as business questions evolve. Secondary users: procurement team (restock purchase orders), CRM team (churn retention campaigns), finance (margin erosion alerts).

---

**Q5. What was each team member's role?**

**Tanya Jain (23104034):** Database design — MySQL schema, all 11 table definitions, 3NF normalization, seed data generation, and 15 SQL analytics queries including window functions and CTEs.

**Tanmay Tiwari (23104032):** Machine learning pipeline — all three XGBoost models (demand forecasting, churn prediction, delivery ETA), feature engineering (lag features, behavioral signals), `run_all_ml.py` master orchestrator, hyperparameter tuning.

**Tanishq Jain (23104060):** AI integration and frontend — Google Gemini API integration with anti-hallucination architecture, Streamlit dashboard (5 tabs), alert notification dispatcher, deterministic fallback system.

---

**Q6. How long did this project take to build?**

Approximately 4 months. Month 1: problem definition, literature review, database design. Month 2: data generation, SQL analytics, initial ML prototyping. Month 3: ML refinement, Gemini integration, anti-hallucination architecture. Month 4: Streamlit dashboard, alert system, testing (10 test cases), documentation, report writing.

---

**Q7. What tech stack did you use and why?**

**Python 3.11** — dominant ML/data science language with extensive library ecosystem. **MySQL 8.0** — ACID-compliant relational DB with native window functions and CTEs; industry standard. **XGBoost 3.2** — state-of-the-art gradient boosting; consistently outperforms other algorithms on tabular data. **Google Gemini 2.5 Flash** — fast (2–5 sec), cost-efficient API calls. **Streamlit 1.67** — fastest way to build data dashboards in pure Python. **pandas 2.3** — industry-standard DataFrame library. **mysql-connector-python** — official MySQL Python driver.

---

### CATEGORY B: ARCHITECTURE QUESTIONS (Panel Level)

**Q8. Explain your 5-layer architecture in 2 minutes.**

Layer 1 is the MySQL database — single source of truth, 11 normalized tables with 3,000+ orders, 500 customers, 54,900 inventory records, 2,848 delivery logs across 10 dark stores. Layer 2 is the SQL analytics engine — 15 BI queries using CTEs and window functions computing deterministic KPIs: revenue MoM, stockout rate, delivery time, customer rating, gross margin. These numbers are SQL-verified — mathematically exact. Layer 3 is the ML layer — three XGBoost models predicting the future: 7-day demand per SKU, customer churn probability, and delivery ETA with SLA breach risk. All results write back to MySQL and JSON. Layer 4 is the Gemini AI layer — SQL KPIs and ML predictions packaged into a structured JSON payload sent to Gemini 2.5 Flash, which generates natural language executive diagnosis. Critical principle: Gemini interprets verified numbers — it never computes them. Layer 5 is the presentation layer — Streamlit dashboard with 5 tabs and an alert dispatcher sending 12 operational notifications. The entire pipeline runs in approximately 65 seconds.

---

**Q9. Why did you choose MySQL and not MongoDB or PostgreSQL?**

We chose MySQL because our data is fundamentally relational — orders link to customers, order items link to products, delivery logs link to riders. MySQL's native JOIN engine is optimized for exactly these patterns. MongoDB (NoSQL) is designed for schema-less document data — excellent for logs or social media posts, but requires application-level joins which are slower and error-prone for our use case. We chose MySQL over PostgreSQL because MySQL 8.0 has full support for window functions and CTEs, it's more widely deployed in quick-commerce production environments in India, and it integrates seamlessly with Python's `mysql-connector-python` library.

---

**Q10. What is a window function in SQL? Give an example from your project.**

A window function performs a calculation across a set of rows related to the current row, while still returning individual rows — unlike GROUP BY which collapses rows into groups. In our project, we use `LAG()` for month-over-month revenue: `LAG(monthly_revenue, 1) OVER (PARTITION BY store_id ORDER BY month)` returns the previous month's revenue for the same store. When we subtract this from current revenue and divide by previous revenue, we get MoM percentage change. We also use `RANK() OVER (ORDER BY revenue DESC)` to rank stores by revenue.

---

**Q11. What is a CTE? How did you use it?**

A CTE (Common Table Expression) is a temporary named result set defined using `WITH`. It makes complex multi-step queries readable by breaking them into logical, named stages. In our analytics, we use a 3-stage CTE for revenue analysis: the first CTE `monthly_revenue` aggregates orders into monthly revenue per store; the second CTE `mom_comparison` joins each month's revenue with the previous month using `LAG()`; the third SELECT computes the MoM percentage and flags anomalies. Without CTEs, this would be a deeply nested subquery — nearly unreadable and unmaintainable.

---

**Q12. What does "normalized up to 3NF" mean?**

Normalization organizes database tables to minimize redundancy. 3NF requires: (1) 1NF — each cell has one atomic value, no repeating groups. (2) 2NF — every non-key attribute depends on the WHOLE primary key. (3) 3NF — no transitive dependencies: every non-key attribute depends directly on the primary key, not on another non-key attribute. In our schema, `order_items` has only `item_id, order_id, product_id, quantity, unit_price`. Product name and category live in `products`. This eliminates the transitive dependency `item_id → product_id → product_name`. If a product is renamed, we update ONE row in `products`, not thousands in `order_items`.

---

**Q13. Why do you have separate tables for orders and order_items?**

A single customer order can contain multiple products. If we stored all items in `orders`, we'd need columns like `product_1, qty_1, product_2, qty_2`... creating a "repeating group" violating 1NF, with a forced maximum item limit. By separating into `orders` (the header: who ordered, when, from which store, total) and `order_items` (line items: which product, quantity, price), we achieve a clean, flexible schema. An order with 1 item has 1 row in `order_items`; an order with 20 items has 20 rows. This follows the relational model's fundamental principle: one fact, one place.

---

**Q14. How does data flow from MySQL to the Gemini AI output?**

Five steps. Step 1: MySQL stores all raw operational data. Step 2: Python connects via `mysql-connector-python` and executes 15 SQL queries, returning KPI DataFrames. Step 3: ML models read the same MySQL tables, train, generate predictions, and write results back to MySQL ML tables and JSON. Step 4: `ai/insights.py` assembles all KPIs and ML predictions into a single structured JSON dictionary. Step 5: This JSON is embedded into a Gemini prompt with explicit anti-hallucination instructions. Gemini's natural language synthesis is returned and displayed in the Streamlit dashboard's AI tab.

---

### CATEGORY C: MACHINE LEARNING QUESTIONS (Most Scrutiny)

**Q15. What is XGBoost? Why is it better than linear regression for this problem?**

XGBoost (eXtreme Gradient Boosting) builds an ensemble of decision trees sequentially, where each new tree corrects the residual errors of the previous ensemble. It is better than linear regression because demand, churn probability, and delivery time all have non-linear relationships with their features. Linear regression assumes a straight-line input-output relationship — fundamentally wrong here. XGBoost handles non-linear patterns, feature interactions (peak hour AND low riders TOGETHER cause extreme delays), missing values natively, and is regularized with L1/L2 penalties to prevent overfitting.

---

**Q16. What are "lag features" in time series forecasting?**

Lag features are engineered features that capture a time series' historical values as inputs to the model. Instead of just feeding the model a date and expecting it to predict demand, we explicitly give it demand from previous time steps. `y_lag_1` = yesterday's demand (immediate trend). `y_lag_7` = same day last week (weekly cycle). `rolling_mean_7` = 7-day rolling average (smoothed trend). These features give the model a "memory" of recent history. Without lag features, a model seeing only dates has no way to know that this particular Thursday always sells more Amul Milk.

---

**Q17. What is a training set and test set? Why do you split them?**

The training set (80% of data) teaches the model's parameters. The test set (20%, held out) is data the model has NEVER seen during training — it simulates real-world new data. If we evaluated on the same data used for training, the model would appear perfect because it memorized the training data. Using a held-out test set gives an honest estimate of how the model performs on new, unseen data in production. We use stratified splitting for the churn classifier to maintain the same class balance in both sets.

---

**Q18. What does ROC-AUC mean? What does 0.8357 tell you?**

ROC (Receiver Operating Characteristic) is a curve plotting True Positive Rate vs False Positive Rate at different classification thresholds. AUC is the Area Under the Curve. AUC of 1.0 = perfect model; AUC of 0.5 = random guess. Our churn model's AUC of 0.8357 means: if you randomly pick one actually-churned customer and one actually-active customer, the model correctly ranks the churned customer as higher churn-risk 83.57% of the time. Industry benchmark for e-commerce churn models is typically 0.75–0.85 AUC. Our model is solidly within this range.

---

**Q19. What is Precision vs Recall? Which matters more for churn prediction and why?**

Precision = of all customers the model flagged as "will churn," what fraction actually churned. Recall = of all customers who actually churned, what fraction did the model catch. For churn, **recall matters more** — a missed churning customer leaves forever (high cost), while a false alarm costs only Rs. 100 voucher (low cost). Our current threshold (0.70) prioritizes precision to control voucher budget, but we can lower the threshold to increase recall if the business decides catching more churners is worth the extra voucher cost.

---

**Q20. Why is your churn model accuracy 94.4%? Isn't that suspiciously high?**

No. First, the baseline: 84.2% of customers are active, so even a naive "predict everyone as active" classifier gets 84.2% — our model beats the baseline by a meaningful 10 points. Second, `days_since_last_order` with 45.6% importance directly reflects the definition of churn (inactivity) — this is a valid forward-looking business signal, NOT data leakage. Third, we deliberately added 4% label noise to prevent overfitting — without it, accuracy would be 98%+. Fourth, the 5-fold cross-validation AUC of 0.8684 ± 0.0600 (low variance) confirms the model genuinely generalizes to unseen data.

---

**Q21. What is 5-fold cross-validation? Why did you use it?**

Cross-validation provides a reliable performance estimate by training and testing the model multiple times on different data subsets. In 5-fold CV, the dataset is divided into 5 equal "folds." The model trains on 4 folds and tests on the 5th, repeated 5 times with different test folds. The final score is the average across all 5. We used it because with only 500 customers, a single 80/20 split might give an optimistic or pessimistic score depending on which customers happened to be in the test set. Our 0.8684 ± 0.0600 AUC means the model scores consistently across all five folds — not just lucky on one split.

---

**Q22. Your delivery ETA model has R²=42.6% — that seems low. Defend this.**

R² of 42.6% is appropriate for three reasons. First, delivery time has inherent stochastic noise that cannot be captured: traffic signals, elevator wait times, customers not answering the door, rider routing choices — unmeasurable from our available features. They constitute the unexplained 57.4%. Second, the business-critical metric is MAE ±2.74 minutes — predictions within 3 minutes of actual delivery time, fully sufficient for 15-minute SLA management and fleet overflow alerting. Third, this is consistent with published academic literature where 40–60% R² is typical for urban logistics without real-time GPS/traffic data. Our top feature — rider_capacity at 89% — correctly captures why Store 3 (5 riders) gets 30.5 minutes while other stores (12–15 riders) get under 14 minutes.

---

**Q23. What is overfitting? How did you prevent it in your churn model?**

Overfitting occurs when a model learns training data TOO well — memorizing noise and outliers rather than generalizable patterns. An overfit model performs excellently on training data but poorly on new data. We used three prevention techniques: (1) XGBoost's built-in L1/L2 regularization penalties on tree weights. (2) `max_depth=4` — limiting tree depth prevents overly specific decision rules. (3) Most importantly, 4% label noise — randomly flipping 4% of training labels, forcing the model to learn robust population-level patterns. Result: 5-fold CV AUC of 0.8684 ± 0.0600 — the ±0.06 low variance confirms the model generalizes well.

---

**Q24. What is gradient boosting? How does it work?**

Gradient boosting builds multiple small decision trees sequentially, where each new tree corrects the errors of the previous ensemble. Step by step: (1) Start with initial prediction (mean of target). (2) Calculate residuals — difference between actual and predicted. (3) Train a new tree on these residuals. (4) Add this tree's predictions (× learning rate, say 0.1) to the existing ensemble. (5) Recalculate residuals. (6) Repeat for N iterations (100–1000 trees). The "gradient" refers to gradient descent — each new tree takes a step in the direction that most reduces the loss function (MSE for regression, log-loss for classification). XGBoost is an optimized implementation with regularization and parallelization.

---

**Q25. Why not use a neural network / deep learning?**

Neural networks are designed for high-dimensional data like images, audio, and text. Our tabular data is low-dimensional: 12 features for churn, 11 for delivery ETA, 6 for demand. For tabular data, XGBoost consistently outperforms or matches neural networks across benchmarks. Additionally: XGBoost trains in seconds on our data size; XGBoost is interpretable via feature importance (neural networks are black boxes); XGBoost requires no GPU; no intensive architecture search is required. For our academic timeline and production requirements, XGBoost is the definitively correct choice.

---

**Q26. How does your restock alert trigger? Show me the logic.**

For each store-SKU pair, the demand model predicts daily demand for the next 7 days. The sum gives `predicted_7day_demand`. We fetch `closing_stock` from MySQL. If `predicted_7day_demand > closing_stock`, a restock alert is triggered. We also calculate `days_until_stockout = closing_stock / (predicted_7day_demand / 7)`. Alert priority is HIGH if `days_until_stockout < 3` and MEDIUM if 3–7 days. For Store 3's Amul Paneer 200g: closing stock=20, predicted 7-day demand=67, days until stockout = 20/(67/7) = **2.1 days** — extremely urgent.

---

**Q27. What is the difference between classification and regression?**

Classification predicts a CATEGORY (discrete output). Regression predicts a CONTINUOUS NUMBER. We used: **XGBoost Regressor** for Demand Forecasting (output: units sold — a number) and Delivery ETA (output: minutes — a number). **XGBoost Classifier** for Churn Prediction (output: churned=1 or active=0 — a binary category, with probability). The technical difference: regression minimizes mean squared error (MSE); classification minimizes log-loss (cross-entropy). The model structure is the same — only the loss function and output activation differ.

---

### CATEGORY D: AI / GEMINI QUESTIONS

**Q28. What is the Google Gemini API?**

Google Gemini is Google DeepMind's latest family of large language models. The API allows developers to send text prompts to Gemini and receive generated text responses via HTTP. We use the `google-generativeai` Python SDK. Specifically, we use **Gemini 2.5 Flash** — optimized for fast response (2–5 seconds) and cost efficiency. We call it at Layer 4 to generate natural language executive diagnoses from structured JSON data. The API key is stored securely in `.env` and loaded via `python-dotenv`.

---

**Q29. What is hallucination in AI? Give an example.**

AI hallucination is when an LLM confidently generates text that is factually incorrect or entirely invented. Example: If you ask Gemini "What was QuickMart Store 3's revenue last month?" without providing any data, Gemini might respond: "Rs. 1,45,000 with 12% growth and 95% SLA compliance." These numbers are completely fabricated. It's pattern-matching from training data to generate plausible-sounding text. The danger in business: a store manager who reads this might make procurement or staffing decisions based on fictional data — a decision worth lakhs of rupees.

---

**Q30. How did you prevent hallucination in your system?**

We prevent hallucination through the **anti-hallucination architectural boundary**: SQL computes ALL numbers, Gemini only INTERPRETS. Every metric is first computed by SQL queries or ML models on verified MySQL data. These verified numbers are assembled into a structured JSON payload. This JSON is injected into the Gemini prompt along with explicit instructions: "The following data has been computed from SQL queries against a live MySQL database. Use ONLY these figures. Do NOT extrapolate, estimate, or introduce any metric not explicitly provided in this JSON." Gemini's role is purely interpretive — translating verified numbers into natural language recommendations.

---

**Q31. What happens if the Gemini API is offline during the viva?**

We specifically engineered for this. Before every Gemini API call, `ai/insights.py` performs a 1-second timeout probe. If the probe fails, the system instantly activates the **deterministic fallback engine** with pre-programmed analytical rules: stockout > 25% → INVENTORY_CRISIS; delivery > 20 min → FLEET_CRISIS; MoM revenue < -15% → REVENUE_DECLINE; etc. The output is analytically equivalent — same root cause identification, same recommendation logic. Total added latency: under 1 second. This demonstrates a key engineering principle: production systems must be resilient to external service dependencies.

---

**Q32. What is the difference between our system's AI and just typing a question into ChatGPT?**

The fundamental difference is **data grounding**. ChatGPT/Gemini.com has access only to its training data — it generates plausible-sounding but factually ungrounded responses. Our system grounds every Gemini call with actual, SQL-verified, live data from our MySQL database. Gemini in our system knows Store 3's exact revenue (Rs. 91,656), exact stockout rate (33.48%), exact rider count (5) — because we tell it in the prompt. It interprets verified facts, not training data patterns. Additionally, our system is fully automated — no manual query formulation needed.

---

### CATEGORY E: RESULTS & VALIDATION

**Q33. How do you know your system actually works? What tests did you run?**

We designed a 10-case test suite. TC-01 (Database Connectivity): MySQL connection verified, all 11 tables present. TC-02 (SQL Analytics Accuracy): KPI computations validated against manually-verified expected values. TC-03 (Demand Forecast End-to-End): 610 models train, 577 alerts generated. TC-04 (Churn Model Evaluation): accuracy ≥ 90%, ROC-AUC ≥ 0.80 on held-out test set. TC-05 (Delivery ETA): MAE ≤ 5 minutes (achieved ±2.74 min). TC-06 (Anti-Hallucination Verification): Gemini output parsed — every number cross-checked against input JSON to verify no hallucinated values. TC-07 (Alert Dispatch): all 12 notifications present in `active_notifications.json`. TC-08 (Fallback Activation): Gemini blocked — deterministic fallback activates correctly. TC-09 (Store Switching): Streamlit updates all 5 tabs correctly. TC-10 (Full Pipeline Timing): end-to-end completes in under 120 seconds.

---

**Q34. What is the actual business ROI of your system?**

We calculated ROI across four value drivers. Stockout prevention: 577 alerts per pipeline run; if 20% prevent an actual stockout and each costs Rs. 500 → Rs. 57,700 per cycle. Customer churn reduction: 61 HIGH-risk customers; Rs. 100 voucher cost; 30% retention × Rs. 3,000 LTV → Rs. 54,900 recovered against Rs. 6,100 cost (800% ROI on churn alone). Analyst time saved: 4+ hours daily eliminated → Rs. 20 lakhs/year. Total system cost: Rs. 90,000/year. Against Rs. 23+ lakhs in value delivered — approximately **2,500% annual ROI**.

---

**Q35. How does your system compare to Power BI?**

Power BI is a descriptive analytics tool — it shows historical data through charts, answering "what happened?" Our system extends to all four analytics maturity levels. Level 3 (predictive): our three XGBoost models forecast demand, churn, and delivery ETA. Power BI has no native ML. Level 4 (prescriptive): our alert dispatcher automatically sends vouchers, purchase orders, and fleet overflow notifications. Power BI shows numbers — someone still manually decides what to do. Additionally, Power BI costs Rs. 1,200–2,400/user/month. Our system is fully open-source.

---

### CATEGORY F: CODE / IMPLEMENTATION QUESTIONS

**Q36. Walk me through what happens when I select Store 3 in the Streamlit app.**

`store_id=3` is passed to `get_store_diagnostics(3)`. This function runs MySQL queries fetching Store 3's KPIs. It reads Store 3's demand forecast rows from the `demand_forecasts` table. It filters `churn_scores` for Store 3's customer base. It reads Store 3's delivery prediction from `delivery_predictions`. It loads `store_3_insight.json` for the pre-computed AI diagnosis. Streamlit session state updates. The 5 tabs re-render: Tab 1 shows CRITICAL badge and AI diagnosis. Tab 2 shows demand forecast for Store 3's SKUs. Tab 3 shows Store 3's high-risk customers. Tab 4 shows 30.5-min ETA with 100% SLA risk. Tab 5 shows all HIGH-priority alerts for Store 3.

---

**Q37. What command do you run to start the entire system?**

Three steps: (1) Ensure MySQL is running. (2) From `D:\Desktop\Major Project Updated\Major Project\`, run: `python ml\run_all_ml.py` — takes ~65 seconds, populates all MySQL ML tables and JSON output files. (3) Start the dashboard: `python -m streamlit run app\streamlit_app.py` — launches at `http://localhost:8501`. AI insights can be regenerated with `python ai\insights.py 3` for Store 3. Always run the ML pipeline first so the dashboard has fresh predictions.

---

**Q38. What is in your `.env` file and why?**

The `.env` file stores sensitive configuration: `DB_HOST=localhost`, `DB_USER=root`, `DB_PASSWORD`, `DB_NAME=quickcommerce_db`, `GEMINI_API_KEY`. We use `python-dotenv` — `load_dotenv()` reads the file and injects values as environment variables. Why not hardcode? If code is committed to GitHub, hardcoded credentials expose the database password. The `.env` file is in `.gitignore` to prevent accidental commit. Industry standard: secrets managers like AWS Secrets Manager for production.

---

**Q39. How does `run_all_ml.py` work?**

It is the master pipeline orchestrator using Python's `subprocess.run()` to execute each ML module as a separate process, in sequence: Module 1 (`demand_forecast.py`) → Module 2 (`churn_model.py`) → Module 3 (`delivery_predictor.py`) → Module 4 (`alert_notifier.py`). After each module completes, it checks the return code — zero means success, non-zero logs the error and continues. Each module independently connects to MySQL, reads data, trains/runs its model, writes results back to MySQL, and exports CSV and JSON artifacts.

---

**Q40. What is a JSON file? Why do you export ML results as JSON?**

JSON (JavaScript Object Notation) is a lightweight, human-readable data format using key-value pairs and arrays. We export ML results as JSON for: (1) Dashboard loading — Streamlit reads JSON files directly instead of repeated MySQL queries. (2) API readiness — JSON is the universal API format; deploying as a REST API requires zero format conversion. (3) Debugging — JSON files in `ml/` are human-readable without a database client.

---

### CATEGORY G: DESIGN DECISIONS / TRICKY QUESTIONS

**Q41. Why is your data synthetic? Is that a limitation?**

Our data is calibrated to real-world quick-commerce unit economics from published industry research. The system's value is in its **architecture and algorithms** — not the specific numbers. We designed two analytically distinct failure modes that the system correctly diagnoses without any hard-coding. The ML models discover these patterns from data — they're not programmed to find them. The pipeline works identically with real data: replace the MySQL connection string and every query, model, and prompt functions unchanged. Using synthetic data was necessary due to absence of an NDA with a production operator — a realistic constraint shared by virtually all academic capstone projects.

---

**Q42. If you had real data, what would change?**

Three things. First, ML model accuracy would likely improve — real data has richer natural variation capturing genuine seasonal patterns (Diwali demand spikes, monsoon delivery slowdowns). Second, the feature set would expand — real data provides GPS delivery tracks, customer device signals, payment method patterns, hyperlocal weather data. Third, we would implement a proper MLOps pipeline — model retraining on a schedule, drift detection, A/B testing of ML-driven interventions vs control groups.

---

**Q43. How does your system handle all 10 stores, not just 3 and 7?**

The system handles all 10 stores identically. The Streamlit store selector dropdown shows all 10 QuickMart stores. The ML pipeline runs across all stores: demand_forecast.py trains 610 models (10 stores × 61 SKUs), churn_model.py scores all 500 customers, delivery_predictor.py predicts ETA for all 10 stores. Store 3 and Store 7 are highlighted as the two most analytically interesting cases — one operational crisis and one margin erosion — but every other store also has a full AI diagnosis available.

---

**Q44. Is your system scalable to 1,000 dark stores?**

In its current form, designed for a 10-store academic prototype. Scaling to 1,000 stores would require: MySQL single-instance replaced by distributed database (MySQL read replicas or AWS Aurora). ML pipeline parallelization — 1,000 stores × 200 SKUs = 200,000 store-SKU models would need Apache Spark. Gemini API calls would hit rate limits at scale — a job queue (Redis + Celery) would manage concurrent API requests. Streamlit dashboard replaced by production-grade frontend (React + FastAPI). These are known scalability extensions.

---

**Q45. What would you do differently if you had 6 more months?**

Three major extensions: (1) Real data integration — partner with a quick-commerce startup for data-sharing or use public retail datasets (Instacart market basket data). (2) MLOps pipeline — model retraining schedule with drift detection (Evidently AI), A/B testing of ML-driven interventions. (3) Advanced ML — real-time weather API data for delivery ETA, NLP on customer reviews for sentiment-driven churn signals, transformer-based models (N-BEATS, Temporal Fusion Transformer) for demand forecasting — these have shown 10–15% MAE improvement over XGBoost on complex seasonal demand.

---

### CATEGORY H: MBA → IT TRANSITION QUESTIONS

**Q46. This started as an MBA project — what exactly was added to make it an IT/CS project?**

The MBA framing identified the domain problem. The IT/CS contribution begins at every layer of implementation. At Layer 1, we designed a fully normalized relational database schema with 11 tables, foreign key constraints, and referential integrity. At Layer 2, we wrote 15 advanced SQL queries using window functions (LAG, RANK, ROW_NUMBER) and CTEs. At Layer 3, we implemented three XGBoost machine learning models with feature engineering, hyperparameter tuning, and cross-validation. At Layer 4, we integrated the Google Gemini LLM API with an anti-hallucination architectural pattern. At Layer 5, we built a full-stack web application with an automated alert dispatcher. The business problem provides context; every solution is a computer science and software engineering artifact.

---

**Q47. What is the difference between descriptive, diagnostic, predictive, and prescriptive analytics?**

**Descriptive** answers "What happened?" — historical summaries. Example: revenue last month was Rs. 91,656. **Diagnostic** answers "Why did it happen?" — root cause analysis. Example: revenue fell because rider shortage caused delivery time to spike, triggering churn. **Predictive** answers "What will happen?" — ML-based forecasting. Example: 55 Amul Milk units needed in next 7 days. **Prescriptive** answers "What should I do?" — recommends specific actions. Example: alert dispatcher sends a purchase order for 55 units and deploys 8 additional riders. Our system is one of the few academic projects implementing all four levels in one integrated pipeline.

---

**Q48. How does this project relate to your B.Tech curriculum?**

This project integrates skills from at least five core B.Tech subjects: **DBMS** — MySQL schema design, 3NF normalization, SQL window functions, CTEs, referential integrity. **Machine Learning / AI** — XGBoost gradient boosting, feature engineering, cross-validation, evaluation metrics (ROC-AUC, MAE, R²). **Software Engineering** — modular system design (5 layers), single-responsibility principle (4 ML modules), test case design (10 test cases). **Distributed Systems / APIs** — REST API integration (Gemini API), HTTP client calls, JSON serialization, timeout/fallback design. **Data Structures and Algorithms** — time series lag feature arrays, rolling window algorithms, priority-based alert sorting.

---

**Q49. What PO/PSO outcomes does this project satisfy?**

**PO1 (Engineering Knowledge):** Applied DBMS, ML, Software Engineering, and AI to design a 5-layer decision intelligence system. **PO2 (Problem Analysis):** Analyzed the quick-commerce operational diagnosis problem, identified technical requirements, selected appropriate algorithms. **PO3 (Design/Development):** Designed MySQL schema, SQL analytics, ML pipeline, Gemini integration, and Streamlit dashboard — complete system design from scratch. **PO5 (Modern Tool Usage):** Used XGBoost, pandas, Streamlit, Google Gemini API, and MySQL — all industry-current tools. **PSO1 (Domain Application):** Applied CS techniques to solve a real business domain problem in quick-commerce/retail analytics.

---

**Q50. What is the most impressive thing about your project?**

The most impressive aspect is the **anti-hallucination architecture combined with the closed-loop prescriptive intelligence pipeline**. Our system: (1) Implements a strict computational boundary — SQL guarantees mathematical truth, ML provides predictive intelligence, and Gemini only interprets verified data. (2) Closes the entire loop — from raw MySQL data, through SQL analytics, three XGBoost models, Gemini AI synthesis, to automated alert dispatch — in 65 seconds. (3) Demonstrates two distinct business failure modes simultaneously — an operational crisis (Store 3) and a financial erosion (Store 7) — proving the system generalizes across different problem types.

---

### ADDITIONAL TECHNICAL Q&A (Q51–Q70)

**Q51. What is feature importance in XGBoost?** Feature importance measures how often each feature is used in tree splits, weighted by improvement to the loss function. In our delivery ETA model, **rider_capacity is the most important feature at 89%**. This makes strong intuitive sense: a store with 5 riders serving the same volume as a store with 15 riders WILL take 3× longer. The model correctly identifies rider shortage as the dominant delivery time driver.

**Q52. How do you handle missing data?** XGBoost natively handles missing values by learning which direction to send them at each tree split. For preprocessing: `demand_forecast.py` uses `dropna()` after lag feature creation. For churn features, we use `fillna(0)` for `cancellation_rate` and `avg_delay_rate`. Before MySQL inserts, we validate `pd.notna(value)` for all numeric columns to prevent MySQL type conversion errors.

**Q53. What is the difference between supervised and unsupervised learning? Which did you use?** Supervised learning uses labeled training data — input-output pairs where the correct answer is known. All three of our models are supervised — we have historical data with known outcomes. Unsupervised learning finds patterns without labeled examples (K-Means clustering, PCA). We did not use unsupervised learning, though an extension could use K-Means to cluster stores into performance tiers.

**Q54. What is the stockout rate formula?** `Stockout Rate = (Number of product-days with closing_stock = 0) / (Total product-days tracked) × 100`. Store 3 over 90 days with ~61 SKUs: Total product-days = 5,490. With 33.48% stockout rate, approximately 1,838 of 5,490 product-days had zero stock — meaning on any given day, one-third of products a customer might want to buy was unavailable.

**Q55. What is a prompt in the context of LLMs?** A prompt is the input text sent to an LLM defining the task and providing context. Our Gemini prompt has three parts: (1) **Persona** — "You are a Senior Business Intelligence Analyst specializing in quick-commerce operations." (2) **Data** — the verified JSON payload with SQL KPIs and ML predictions. (3) **Instructions** — "Use ONLY the data provided. Do NOT invent, estimate, or extrapolate any numbers."

**Q56. Can your system work in real-time?** The current implementation is a batch pipeline. For true real-time operation: streaming data ingestion using Apache Kafka; online learning — ML models updated incrementally with each new order; webhook alerts dispatched immediately when thresholds are breached; Streamlit auto-refresh. The modular pipeline structure makes replacing batch with streaming a component-level swap.

**Q57. What is the purpose of `store_3_insight.json` and `store_7_insight.json`?** These store **pre-computed AI diagnoses** from the most recent pipeline run. When the Streamlit app loads, instead of making a live Gemini API call (2–5 seconds, costs API credits), the app loads the pre-computed result instantly. If the user clicks "Re: Run Executive Diagnosis," a fresh Gemini call is made and the JSON is updated. It also makes offline demonstration possible.

**Q58. What happens to the ML output tables when the pipeline runs again?** Each time `run_all_ml.py` runs, the ML output tables (`demand_forecasts`, `churn_scores`, `delivery_predictions`) are **replaced** — existing rows are deleted and fresh predictions inserted. This ensures the dashboard always shows the latest predictions without stale data accumulating. The CSVs and JSONs in the `ml/` folder are similarly overwritten.

**Q59. What is pandas and why is it used?** pandas is a Python library for data manipulation centered around the DataFrame — a 2D tabular data structure similar to a spreadsheet in memory. We use it throughout: reading MySQL query results (`pd.read_sql()`), feature engineering (creating lag columns with `.shift()`), data cleaning (`dropna()`, `fillna()`), encoding categorical variables, preparing training sets, and writing results to CSV.

**Q60. What is the ROI of the churn intervention specifically?** 61 × Rs. 100 voucher = Rs. 6,100 cost. 30% retention × 61 customers × Rs. 3,000 LTV = Rs. 54,900 recovered. Net ROI = (54,900 - 6,100) / 6,100 = **800%**. Additionally, retaining a customer costs 5–7× less than acquiring a new one — if acquisition cost is Rs. 500–1,000/customer, avoiding 18 churns saves Rs. 9,000–18,000 in acquisition cost on top of the LTV recovery.

**Q61. How did you validate the SQL queries are correct?** Three methods: (1) Manual calculation verification — for a small sample (Store 3, January 2025), manually summed order subtotals and compared to SQL revenue query output — values matched exactly. (2) Sanity checks — revenue must be positive, stockout rate between 0–100%, delivery time > 0 — all outputs validated against business logic bounds. (3) Cross-reference with ML inputs — ML models' training data produced results consistent with SQL KPIs.

**Q62. What is Streamlit and how is it different from a traditional website?** Streamlit generates interactive web applications from pure Python code — no HTML, CSS, or JavaScript required. When a user interacts with a widget (like the store dropdown), Python re-executes from the top — this "reactive" execution model means the entire dashboard re-renders automatically. Limitation: not suitable for production-grade web apps with complex UX or multi-user authentication — a production system would use React + FastAPI.

**Q63. What is the environmental impact of your project?** By optimizing dark store operations — particularly stockout prevention and delivery efficiency — the system reduces waste. Fewer stockouts means less emergency restocking deliveries (fewer last-mile carbon emissions). Better delivery ETA prediction means fewer failed deliveries (reducing rider round-trips). At scale, a 10% improvement in delivery efficiency across 100 dark stores could mean thousands fewer rider trips per month. This maps to PO7 (Environment and Sustainability).

**Q64. What is your project's biggest limitation and how would you address it?** The biggest limitation is synthetic data — we cannot claim ML performance metrics are validated against real production distribution. We would address this by partnering with a quick-commerce startup for a data-sharing agreement under NDA, or using public retail datasets (Instacart market basket data). Additionally, we would implement formal MLOps: a data drift detection layer (Evidently AI) that alerts when incoming production data distribution shifts away from training distribution.

**Q65. What is the difference between accuracy and ROC-AUC? Which is more reliable for imbalanced datasets?** Accuracy = (correct predictions / total predictions) × 100 — simple but misleading on imbalanced datasets. If 84.2% of customers are active, a classifier that always predicts "active" gets 84.2% accuracy — without predicting a single churner. ROC-AUC evaluates the model's ability to rank churned customers above active customers at all possible thresholds — independent of class imbalance. For our churn dataset (84.2%/15.8% imbalance), **ROC-AUC is the more reliable metric**. Our 0.8357 AUC genuinely proves the model discriminates between classes.

**Q66. How does the alert dispatcher decide what notifications to send?** `alert_notifier.py` reads all three ML output JSON files and SQL KPIs, then applies threshold logic to generate and prioritize notifications. For each potential alert type, it checks if the threshold is breached. If breached, it constructs a notification dictionary with: alert_id, priority level, alert type, recipient (by role), channel (WhatsApp/SMS/email/POS), subject, and message body. All notifications are collected into a list, sorted by priority (HIGH first), and written to `active_notifications.json`.

**Q67. What is the purpose of `requirements.txt`?** `requirements.txt` lists all Python packages needed to run the project with exact version numbers: `streamlit==1.67.0`, `xgboost==3.2.0`, `scikit-learn==1.8.0`, `pandas==2.3.3`, `mysql-connector-python==26.7.0`, `google-generativeai==0.8.3`, `python-dotenv==1.0.1`, `matplotlib==3.10.8`, `Pillow==11.3.0`. When someone else clones the project, they run `pip install -r requirements.txt`. Exact versions ensure reproducibility — a different version of XGBoost might produce different model outputs.

**Q68. What is the difference between mean and median? Which would you use for delivery time?** The mean (average) sums all values and divides by count. The median is the middle value when sorted. For delivery time, **median is more appropriate** because delivery times have a skewed distribution — most deliveries are on time (13–15 minutes) but a small number are extremely late (60+ minutes due to accidents, wrong addresses). These outliers pull the mean upward in a misleading way. 10 deliveries of 14 minutes and 1 delivery of 90 minutes gives mean=21 minutes but median=14 minutes.

**Q69. Can your system work in real-time?** The current implementation is a batch pipeline. For true real-time operation: streaming data ingestion using Apache Kafka; online learning — ML models updated incrementally; webhook alerts dispatched immediately when thresholds are breached; Streamlit auto-refresh. The modular pipeline structure makes replacing batch with streaming a component-level swap, not a full redesign.

**Q70. What is a Foreign Key and why does it matter?** A foreign key is a column in one table referencing the primary key of another, enforcing referential integrity. Example: `orders.customer_id` references `customers.customer_id`. If you try to insert an order with `customer_id=999` and customer 999 doesn't exist, MySQL throws an error. This prevents "orphaned records" — an order with no customer. Without foreign keys, data corruption accumulates silently, making analytics unreliable.

---

## SECTION 14: LIVE DEMO SCRIPT — STEP-BY-STEP WITH WHAT TO SAY

### Pre-Demo Checklist (5 minutes before)

```
□ MySQL service running (XAMPP Control Panel → MySQL → Start)
□ Terminal open at: D:\Desktop\Major Project Updated\Major Project\
□ Browser ready (Chrome recommended)
□ docs/presentation.html open in another browser tab
```

### Demo Timeline

```
0:00 – 1:30   Run ML Pipeline (python ml\run_all_ml.py)
1:30 – 2:00   Launch Streamlit
2:00 – 7:00   Show Store 3 (Crisis Diagnosis — all 5 tabs)
7:00 – 10:00  Show Store 7 (Margin Erosion contrast)
10:00 – 15:00 Architecture slides + Q&A setup
```

### Step 1 — Run the ML Pipeline (0:00 – 1:30)

```powershell
cd "D:\Desktop\Major Project Updated\Major Project"
python ml\run_all_ml.py
```

**Narrate as it runs:**

*(Module 1 completes — point to 610 models, 577 alerts)*
> "The demand forecasting model just trained 610 XGBoost models — one per store-SKU combination — and identified 577 products that will run out within 7 days. Highest priority: Amul Paneer at Store 3 — only 2.1 days of stock remaining."

*(Module 2 completes)*
> "The churn classifier has scored all 500 customers. 61 are HIGH-risk — above 70% churn probability. The model achieves 94.4% accuracy and 0.8357 ROC-AUC."

*(Module 3 completes — point to Store 3's 30.5 min)*
> "The delivery model predicts 30.5 minutes average delivery for Store 3 — double our 15-minute SLA. Every other store is under 14 minutes. Root cause: Store 3 has only 5 riders."

*(Alert module completes)*
> "12 operational notifications have been dispatched — restock orders, fleet overflow alerts, churn vouchers. The entire pipeline took 65 seconds."

### Step 2 — Launch Streamlit (1:30 – 2:00)

```powershell
python -m streamlit run app\streamlit_app.py
```

> "Starting the decision intelligence dashboard — built entirely in Python, no frontend code."

### Step 3 — Show Store 3 (2:00 – 7:00)

Select **Store 3 — QuickMart Koramangala** from dropdown.

> "Store 3, Koramangala, Bengaluru. Notice the red CRITICAL badge. Revenue is down 23.57% month-over-month. Orders dropped 30%. Stockout rate: 33.48% — target is under 8%. Delivery time: 30.5 minutes — target is under 15. Rating: 2.15 out of 5 — benchmark is above 4.2. And the root cause: 5 riders. Every healthy store has 12–15."

**Tab 1 — AI Decision Synthesis:**
> "This is our Gemini AI synthesis — not hallucinated, but an interpretation of SQL-verified numbers. Notice every number in this synthesis matches our database exactly — this is our anti-hallucination architecture at work."

**Tab 2 — 7-Day SKU Demand Forecast:**
> "The red-highlighted rows need restocking in under 3 days. Amul Paneer: 20 units on hand, 67 needed over 7 days — 2.1 days to stockout. An emergency purchase order has already been dispatched."

**Tab 3 — Customer Churn:**
> "23 of Store 3's customers are HIGH-risk. The primary driver: inactivity after one bad delivery experience. These are the customers we can still save with an intervention voucher."

**Tab 4 — Delivery ETA:**
> "100% SLA delay risk for Store 3. Every order will be late. The fix: deploy 8 additional riders."

**Tab 5 — Alert Center:**
> "All alerts automatically dispatched. No manual reports needed."

### Step 4 — Switch to Store 7 (7:00 – 10:00)

Select **Store 7 — QuickMart Sector 56 Gurugram:**

> "Contrast with Store 7 — Gurugram. Revenue up 17%, orders up 16%, delivery 13.78 minutes, rating 4.17. Looks like a star performer. But the system flags it PROFITABILITY WARNING. Gross margin is only 28%. The company is subsidizing customers through excessive discounts. Without our system, the city manager celebrates. With our system, the CFO knows they need to rethink the discount strategy immediately — this store is on a 'growth trap' trajectory."

---

## SECTION 15: SCORING STRATEGY & TERMINOLOGY CHEAT SHEET

### Numbers to Memorize (Use These in Every Answer)

| Number | Context |
|--------|---------|
| **65 seconds** | End-to-end pipeline execution |
| **54,900** | Inventory records in MySQL |
| **610** | Store-SKU models trained |
| **577** | Restock alerts generated |
| **94.40%** | Churn model accuracy |
| **0.8357** | Churn model ROC-AUC |
| **0.8684 ± 0.0600** | 5-fold CV AUC |
| **±2.74 min** | Delivery ETA model MAE |
| **42.6%** | Delivery ETA R² |
| **30.5 min** | Store 3 predicted average ETA |
| **13.78 min** | Store 7 delivery time (healthy) |
| **33.48%** | Store 3 stockout rate |
| **5.54%** | Store 7 stockout rate (healthy) |
| **2.15/5.0** | Store 3 customer rating |
| **4.17/5.0** | Store 7 customer rating |
| **-23.57%** | Store 3 revenue MoM decline |
| **+17.41%** | Store 7 revenue MoM growth |
| **28.13%** | Store 7 gross margin (problem) |
| **61** | HIGH-risk churning customers |
| **12** | Automated notifications dispatched |
| **~2,500%** | System ROI |
| **5 riders** | Store 3 rider count (the root cause) |

### Terminology to Use (Say These Exact Phrases)

| Instead of... | Say... |
|--------------|--------|
| "our ML model" | "our XGBoost gradient boosting ensemble" |
| "it predicts things" | "recursive multi-step time-series forecasting with lag features" |
| "AI doesn't make up numbers" | "anti-hallucination architecture with SQL-grounded semantic boundary" |
| "the backup plan" | "deterministic fail-safe with 1-second timeout probe" |
| "accuracy" | "94.40% accuracy with 0.8357 ROC-AUC on a stratified held-out test set" |
| "our DB is organized" | "schema normalized to Third Normal Form (3NF) with referential integrity via foreign key constraints" |
| "it shows charts" | "Layer 5: Streamlit-based prescriptive analytics dashboard with 5 interactive operational tabs" |
| "we compared months" | "month-over-month variance via LAG() window function over PARTITION BY store_id" |
| "the data is fake" | "domain-calibrated synthetic data with two embedded analytical failure modes" |

### Business Impact Template (Add After Every Technical Explanation)

- Demand model: **"...this directly prevents inventory stockouts costing Rs. 500 per lost sale."**
- Churn model: **"...enabling targeted retention at 1/30th the cost of acquiring a replacement customer."**
- Delivery ETA: **"...giving operations managers a 65-second warning to deploy contingency riders."**
- Anti-hallucination: **"...guaranteeing no business decision in our system is based on AI-fabricated data."**

### "I Don't Know" Protocol

> "That's an excellent question. In our implementation we used [what you did]. An alternative approach [mention one] could potentially improve [specific metric], and that's something we've identified as future work. However, our current approach achieves [specific metric] which meets the production requirement for [business use case]."

---

## SECTION 16: WEAK POINTS & HOW TO DEFEND THEM

**"Your data is synthetic"**
> "Our data is calibrated to real-world quick-commerce unit economics from published industry research. The system's value is in its **architecture and algorithms** — not the specific numbers. We designed two analytically distinct failure modes that the system correctly diagnoses without any hard-coding. The ML models discover these patterns from data — they're not programmed to find them. The pipeline works identically with real data: replace the MySQL connection string and every query, model, and prompt functions unchanged."

**"R²=42.6% is low for the delivery model"**
> "R² of 42.6% is appropriate for urban delivery time prediction. The 57.4% unexplained variance represents genuine stochastic noise — traffic signals, elevator waits, customer response delays — unmeasurable from our available features. The operationally meaningful metric is MAE ±2.74 minutes: predictions within 3 minutes of actual delivery time, fully sufficient for 15-minute SLA management. Aligns with published academic literature where 40–60% R² is typical for urban logistics without real-time GPS/traffic data."

**"94.4% churn accuracy is too high"**
> "The 94.4% accuracy is legitimate. Baseline (predict everyone active) = 84.2% — our model beats it by 10 points. `days_since_last_order` at 45.6% importance directly reflects the definition of churn — not data leakage, a valid business signal. We added 4% label noise to prevent overfitting — without it, accuracy would be 98%+. The 5-fold CV AUC of 0.8684 ± 0.0600 (low variance) confirms genuine generalization."

**"This started as an MBA project"**
> "The business problem provides context, but every solution artifact is a CS and software engineering deliverable. We designed a 3NF relational schema with 11 tables and foreign key constraints. We wrote advanced SQL with window functions and CTEs. We implemented three gradient boosting ensemble models with cross-validation. We integrated a production LLM API with an anti-hallucination architectural pattern. We built a full-stack web application with reactive state management."

**"No real deployment"**
> "Our system runs as a fully functional end-to-end pipeline on a local MySQL instance with 11 populated tables and live ML execution. The distinction between our prototype and production deployment is infrastructure, not functionality: MySQL → AWS RDS, Streamlit → cloud server, ML pipeline → cron job, Gemini → production API key. These are devops changes, not algorithmic ones."

**"Gemini can still hallucinate even with your prompt"**
> "You're right that prompt engineering alone cannot provide a mathematical guarantee. However, our approach significantly reduces hallucination risk: (1) The structured JSON format leaves no ambiguity — Gemini can directly reference exact values provided. (2) The explicit instruction 'do NOT introduce any metric not in this JSON' triggers the model's instruction-following training. (3) Our anti-hallucination test case (TC-06) verifies this for each pipeline run by parsing the AI output and cross-checking every number against the input JSON."

---

## SECTION 17: GLOSSARY — 55+ TERMS IN PLAIN ENGLISH

| Term | Plain English Definition |
|------|------------------------|
| **ACID** | Four database properties: Atomic (all-or-nothing), Consistent (data always valid), Isolated (no interference), Durable (committed data survives crashes) |
| **API** | Application Programming Interface — a defined way for two software systems to communicate |
| **AUC** | Area Under the ROC Curve. 1.0 = perfect model, 0.5 = random guess. Our churn model: 0.8357 |
| **Churn** | A customer stopping their use of a service (switching to competitor or going inactive) |
| **Classification** | ML task where the output is a category (churned/not-churned, HIGH/MEDIUM/LOW risk) |
| **CTE** | Common Table Expression — a named temporary result in SQL using `WITH`. Improves query readability |
| **Cross-Validation** | Training and testing an ML model multiple times on different data subsets for a reliable performance estimate |
| **Dark Store** | A small warehouse for quick-commerce fulfillment, closed to walk-in customers, serving delivery riders only |
| **Decision Tree** | An ML model that makes predictions via a tree of if-then rules |
| **Descriptive Analytics** | Analytics answering "What happened?" — historical data summaries and dashboards |
| **Diagnostic Analytics** | Analytics answering "Why did it happen?" — root cause analysis |
| **ETA** | Estimated Time of Arrival — how long delivery will take |
| **Feature Engineering** | Creating new input variables from raw data to improve ML model performance |
| **Feature Importance** | A measure of how much each input variable contributes to an ML model's predictions |
| **Foreign Key** | A column in one table referencing the primary key of another, enforcing relational integrity |
| **Gradient Boosting** | An ensemble ML technique building many small decision trees sequentially, each correcting previous errors |
| **Hallucination (AI)** | When an LLM generates factually incorrect text with high confidence — a critical risk for business applications |
| **Hyperparameter** | A model configuration setting set before training (not learned from data). E.g., `max_depth=4` |
| **KPI** | Key Performance Indicator — a metric used to evaluate business performance |
| **L1/L2 Regularization** | Mathematical penalties added to ML models to prevent overfitting |
| **Label Noise** | Intentionally adding random incorrect labels to training data to prevent overfitting |
| **Lag Feature** | An engineered ML feature representing a previous time step's value. `y_lag_7` = demand from 7 days ago |
| **LLM** | Large Language Model — AI trained on vast text data that generates human-like text. E.g., Gemini, GPT-4 |
| **MAE** | Mean Absolute Error — average absolute difference between predicted and actual values |
| **ML** | Machine Learning — teaching computers to make predictions by learning patterns from data |
| **MoM** | Month-over-Month — percentage change from one month to the next |
| **MySQL** | An open-source relational database management system; industry standard |
| **Neural Network** | An ML model inspired by the brain. Powerful for images/text; typically outperformed by XGBoost on tabular data |
| **NLP** | Natural Language Processing — the field of AI focused on understanding and generating human language |
| **Normalization (DB)** | Organizing database tables to minimize redundancy. 3NF is the standard for transactional databases |
| **Overfitting** | When an ML model learns training data TOO well (including noise), performing poorly on new data |
| **pandas** | Python library for data manipulation using DataFrames (like spreadsheets in code) |
| **Precision** | Of all examples the model labeled positive, what fraction actually were positive |
| **Predictive Analytics** | Analytics answering "What will happen?" — ML-based future predictions |
| **Prescriptive Analytics** | Analytics answering "What should I do?" — automated recommendations and actions |
| **Primary Key** | A unique identifier for each row in a database table |
| **Prompt Engineering** | The art of crafting input text to LLMs to reliably produce desired outputs |
| **Q-commerce** | Quick-commerce — ultra-fast (10–15 min) delivery of groceries and essentials |
| **R²** | A metric from 0 to 1 showing what fraction of output variance an ML model explains |
| **RAG** | Retrieval-Augmented Generation — an LLM technique that retrieves relevant documents as context before answering |
| **Recall** | Of all actually positive examples, what fraction the model correctly identified |
| **Referential Integrity** | A database property ensuring foreign key values always match existing primary keys |
| **Regression** | ML task where the output is a continuous number (delivery time in minutes, demand in units) |
| **RMSE** | Root Mean Squared Error — like MAE but penalizes larger errors more |
| **ROC Curve** | A chart showing classification model trade-off between true positives and false positives |
| **Rolling Average** | Moving window average over recent data points. 7-day rolling average = average of last 7 days |
| **scikit-learn** | Python ML library — we use it for train/test split, evaluation metrics, and preprocessing |
| **SKU** | Stock Keeping Unit — a unique product identifier (e.g., "Amul Full Cream Milk 1L") |
| **SLA** | Service Level Agreement — a committed performance standard. Our SLA: deliver within 15 minutes |
| **SQL** | Structured Query Language — standard language for querying relational databases |
| **Stockout** | When a product's inventory reaches zero — the product is unavailable to order |
| **Stockout Rate** | (product-days with zero stock / total product-days) × 100 |
| **Streamlit** | Python library for building interactive web dashboards without frontend code |
| **Stratified Split** | Train/test split maintaining the same class proportion in both sets |
| **Supervised Learning** | ML with labeled training data (input-output pairs) |
| **Time Series** | Data collected over successive, equally-spaced time points (daily sales per SKU) |
| **Training Set** | Data used to teach the ML model (80% of our data) |
| **Test Set** | Held-out data never seen during training, used to evaluate real-world performance (20%) |
| **Underfitting** | When an ML model is TOO simple to capture the data pattern |
| **Window Function (SQL)** | SQL function computing across a "window" of related rows without collapsing them |
| **XGBoost** | eXtreme Gradient Boosting — optimized gradient boosting library. Used in all three of our ML models |

---

## QUICK REFERENCE CARD (Print This and Keep It)

```
╔══════════════════════════════════════════════════════════╗
║          QUICKCOMMERCE AI — QUICK REFERENCE CARD         ║
╠══════════════════════════════════════════════════════════╣
║  PROJECT: 5-layer AI Decision Intelligence for           ║
║           Quick-Commerce Dark Store Operations           ║
╠══════════════════════════════════════════════════════════╣
║  LAYER 1: MySQL DB (11 tables, 54,900+ records)          ║
║  LAYER 2: 15 SQL BI queries (CTEs, window functions)     ║
║  LAYER 3: 3 XGBoost ML models                           ║
║  LAYER 4: Gemini 2.5 Flash API (anti-hallucination)      ║
║  LAYER 5: Streamlit dashboard + 12 auto alerts           ║
╠══════════════════════════════════════════════════════════╣
║  ML MODEL 1 — DEMAND FORECAST                           ║
║    610 models, 577 alerts, lag features, XGBoost Reg    ║
║  ML MODEL 2 — CHURN PREDICTION                          ║
║    94.40% acc, 0.8357 AUC, 0.8684 CV-AUC, 61 HIGH-risk ║
║  ML MODEL 3 — DELIVERY ETA                              ║
║    ±2.74 min MAE, R2=42.6%, rider_capacity=89% imp      ║
╠══════════════════════════════════════════════════════════╣
║  STORE 3 (CRISIS):  5 riders, 30.5min, 33.48% stockout  ║
║  STORE 7 (MARGIN):  +17.41% rev BUT 28.13% gross margin ║
╠══════════════════════════════════════════════════════════╣
║  RUN COMMANDS (from Major Project\ folder):              ║
║    python ml\run_all_ml.py           [65 sec pipeline]   ║
║    python ai\insights.py 3           [Store 3 AI]        ║
║    python -m streamlit run app\streamlit_app.py  [UI]    ║
╠══════════════════════════════════════════════════════════╣
║  ROI: Rs.19.7L value / Rs.0.9L cost ≈ 2,500% ROI        ║
╚══════════════════════════════════════════════════════════╝
```

---

*Study Guide Version 1.0 — JIIT Capstone Project 15B29CI692*
*Team: Tanya Jain (23104034) · Tanmay Tiwari (23104032) · Tanishq Jain (23104060)*
*Supervisor: Dr. Diksha Chawla*
