# 📦 PROJECT HANDOVER DOCUMENT
## AI-Powered Business Decision Intelligence System for Quick-Commerce Operations

> **For:** Group Members continuing the project for Mid-Sem & Final Viva  
> **Prepared by:** [Your Name] | Date: October 2026  
> **Status at Handover:** Mid-Semester Review Ready ✅

---

## 🗂️ Table of Contents

1. [Project Identity & Scope](#1-project-identity--scope)
2. [What Has Been Built — Complete Inventory](#2-what-has-been-built--complete-inventory)
3. [System Architecture](#3-system-architecture)
4. [How to Run the Project (Step-by-Step)](#4-how-to-run-the-project-step-by-step)
5. [What is Pending for Final Viva](#5-what-is-pending-for-final-viva)
6. [ML Integration Roadmap — Making It Outstanding](#6-ml-integration-roadmap--making-it-outstanding)
7. [Suggested New Files to Build](#7-suggested-new-files-to-build)
8. [Viva Q&A Preparation](#8-viva-qa-preparation)
9. [Team Task Division (Going Forward)](#9-team-task-division-going-forward)
10. [File Reference Map](#10-file-reference-map)

---

## 1. Project Identity & Scope

| Field | Detail |
|---|---|
| **Full Title** | AI-Powered Business Decision Intelligence System for Quick-Commerce Operations |
| **Domain** | Quick-Commerce (same as Blinkit, Zepto, Swiggy Instamart) |
| **Core Problem** | Store managers in quick-commerce can't quickly identify *why* a store is underperforming — this system automates that diagnosis |
| **Audience** | Non-technical business managers (MBA/Operations level) |
| **Tech Stack** | MySQL · Python · Google Gemini AI API · Power BI · SQL Analytics |
| **Data** | Synthetic but realistic — 3,000 orders, 10 stores, 90 days of data |
| **Key USP** | Anti-hallucination AI: SQL computes all numbers → Gemini only interprets → No hallucinated metrics |

---

## 2. What Has Been Built — Complete Inventory

### ✅ DONE — Database Layer (`database/`)

**`database/schema.sql`** — MySQL schema with **8 fully designed tables**:

| Table | Records | Purpose |
|---|---|---|
| `customers` | ~500 | Customer demographics, segment, acquisition channel |
| `stores` | 10 | Dark store info, city, zone, rider capacity |
| `products` | ~80 | Product catalog with cost price, shelf life, perishability |
| `orders` | ~3,000 | Main transaction table with status, discounts, delivery fees |
| `order_items` | ~9,000 | Line items per order with revenue |
| `inventory` | ~7,200 | Daily stock records with stockout flags |
| `deliveries` | ~2,700 | Rider delivery times with delay flags |
| `customer_feedback` | ~1,500 | Ratings + sentiment (Positive/Negative/Neutral) |

**`database/seed_data.py`** — Python synthetic data generator:
- Uses `Faker` for realistic Indian names, cities, addresses
- **Embeds 2 real business problems** intentionally:
  - **Store 3 (QuickMart Koramangala)**: High stockout (~35%) + slow delivery (~28 min) + declining revenue
  - **Store 7 (QuickMart Sector 56, Gurugram)**: High discount rate (~22%) eroding margin
- 90 days of data (January–March 2025)
- Generates customer feedback with matching sentiments

---

### ✅ DONE — Analytics Layer (`analytics/`)

**`analytics/queries.sql`** — **15 Business Intelligence SQL Queries**:

| Query | Business Question | SQL Features Used |
|---|---|---|
| Q1 | Monthly Revenue, Order Volume, AOV | GROUP BY, CASE |
| Q2 | Top & Bottom Store Performers | RANK() OVER |
| Q3 | Month-over-Month Revenue by City | CTE + LAG() |
| Q4 | Stores with Highest Stockout Rate | RANK() OVER |
| Q5 | Products Causing Most Stockouts | JOIN, GROUP BY |
| Q6 | High-Demand, Low-Availability Products | CTE + PERCENT_RANK() |
| Q7 | Stores with Slowest Delivery | RANK() OVER |
| Q8 | Delivery Delay vs Cancellation Correlation | CTE + CASE classification |
| Q9 | Peak Ordering Hours by Store | HOUR() + RANK() |
| Q10 | Customer Segment Revenue Breakdown | SUM() OVER() |
| Q11 | Customers with Declining Purchase Frequency | LAG() + CTE |
| Q12 | Repeat Customer Revenue % | Nested CTEs |
| Q13 | Products Ranked by Revenue AND Margin | Dual RANK() |
| Q14 | High-Sales, Low-Margin "Hidden Loss" Products | PERCENT_RANK() |
| Q15 | Root-Cause Diagnosis for a Specific Store | Multi-CTE + LAG() |

> **Note for MBA team**: These 15 queries directly answer the 15 most common Operations/Retail Management business questions. Each query is well-commented — read the business question comment above each query.

---

### ✅ DONE — AI Engine (`ai/`)

**`ai/insights.py`** — The core AI pipeline:

```
MySQL Database
      ↓
get_store_diagnostics(store_id)   ← Runs 7 SQL queries, returns structured dict
      ↓
build_prompt(diagnostics)          ← Formats verified numbers into LLM prompt
      ↓
Google Gemini 1.5 Flash API        ← Interprets + recommends (no raw data access)
      ↓
Performance Summary + Root Causes + Recommended Actions + Priority Alert
      ↓
Saved to store_{id}_insight.json   ← Can be loaded into Power BI
```

**Metrics the AI engine computes from SQL (per store):**
- Month-over-Month Revenue Change %
- Month-over-Month Order Change %
- Stockout Rate % + Total Stockout Events
- Average Delivery Time (minutes)
- Delay Rate %
- Average Customer Rating
- Negative Feedback Count
- Gross Margin %
- Top 5 Stockout Products (named)

**Sample Output (Store 3 — already generated):**
- Revenue down 23.57% MoM
- Stockout rate: 33.48% (benchmark: <8%)
- Delivery time: 30.53 min (benchmark: <15 min)
- 100% delay rate
- Rating: 2.15/5 (benchmark: >4.2)
- AI correctly identified root causes and recommended fleet expansion + emergency restocking

---

### ✅ DONE — Dashboard Layer (`dashboard/`)

**`dashboard/index.html`** — A complete **web-based dashboard** (HTML/CSS/JS):
- Works standalone in any browser — no server needed
- Designed to simulate the Power BI view or be used as a demo backup
- Size: 45 KB (feature-rich)

---

### ✅ DONE — Documentation (`docs/` + `powerbi/`)

**`docs/kpi_dictionary.md`** — All 13 KPIs defined:
- Formula, source table, Power BI measure name, and benchmark for every KPI
- Industry benchmark table (Healthy / Warning / Critical thresholds)

**`powerbi/connection_guide.md`** — Complete Power BI setup guide:
- ODBC connector setup
- All 8 table imports
- All relationships (9 relationships documented)
- All DAX measures (12 measures with exact DAX code)
- 3-page dashboard blueprint (Executive Overview, Store Intelligence, Product & Inventory)

**`docs/presentation.html`** — A polished HTML presentation (45 KB)

**`docs/synopsis_major.docx`** — Project synopsis document

---

### ✅ DONE — Supporting Files

| File | Purpose |
|---|---|
| `README.md` | Complete setup instructions, architecture, demo scenario |
| `requirements.txt` | All Python dependencies (`mysql-connector`, `Faker`, `google-generativeai`, etc.) |
| `.env` | Environment variables (DB credentials + Gemini API key) |
| `store_3_insight.json` | Pre-generated AI analysis output for Store 3 (ready to use in demo) |
| `SYNOPSIS.pdf` | Project synopsis PDF |

---

## 3. System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     DATA FOUNDATION                             │
│  database/seed_data.py → MySQL (quickcommerce_db, 8 tables)    │
└───────────────────────┬─────────────────────────────────────────┘
                        │
           ┌────────────┴────────────┐
           ▼                         ▼
┌──────────────────┐       ┌──────────────────────────┐
│  SQL Analytics   │       │      AI Engine           │
│  analytics/      │       │   ai/insights.py         │
│  queries.sql     │       │   (7 SQL queries →       │
│  (15 queries)    │       │    Gemini API →           │
└──────┬───────────┘       │    Insight JSON)          │
       │                   └──────────────┬────────────┘
       │                                  │
       ▼                                  ▼
┌──────────────────┐       ┌──────────────────────────┐
│  Power BI        │       │  store_{id}_insight.json │
│  Dashboard       │       │  (used in Power BI       │
│  (3 pages)       │       │   as text box or API)    │
└──────────────────┘       └──────────────────────────┘
       │
       ▼
┌──────────────────┐
│  dashboard/      │
│  index.html      │
│  (standalone     │
│  web backup)     │
└──────────────────┘
```

**Anti-Hallucination Design (Key Differentiator):**
> SQL computes ALL numbers deterministically. Gemini ONLY receives structured, verified outputs and is used for interpretation and recommendation — never for calculation. This is the answer to the viva question "How do you prevent AI hallucination?"

---

## 4. How to Run the Project (Step-by-Step)

### Prerequisites
| Tool | Version | Where to Get |
|---|---|---|
| XAMPP (MySQL) | 8.0+ | https://www.apachefriends.org/ |
| Python | 3.10+ | https://www.python.org/ |
| Power BI Desktop | Latest (free) | Microsoft Store |
| MySQL ODBC Connector | 8.0 (64-bit) | https://dev.mysql.com/downloads/connector/odbc/ |

### Step 1 — Install Python packages
```bash
pip install -r requirements.txt
```

### Step 2 — Set up environment
Create a `.env` file in the project root with:
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=quickcommerce_db
GEMINI_API_KEY=your_key_here
```
> Get a FREE Gemini API key at: https://aistudio.google.com/app/apikey

### Step 3 — Start XAMPP MySQL, create database & seed data
```bash
# Start MySQL from XAMPP Control Panel first!
mysql -u root -p < database/schema.sql
python database/seed_data.py
```

### Step 4 — Run AI analysis
```bash
python ai/insights.py 3        # Analyze Store 3 (underperformer)
python ai/insights.py 7        # Analyze Store 7 (discount problem)
python ai/insights.py 3 7 1    # Analyze multiple stores
```

### Step 5 — Connect Power BI
Follow `powerbi/connection_guide.md` step by step.

---

## 5. What is Pending for Final Viva

### 🔴 HIGH PRIORITY (Must-Have Before Viva)

| # | Task | Who | Why Critical |
|---|---|---|---|
| 1 | **Build Power BI dashboard** (3 pages per `powerbi/connection_guide.md`) | Member 3 | This is the visual centerpiece of the demo |
| 2 | **Connect Power BI to MySQL** | Member 3 | Required for live data in dashboard |
| 3 | **Practice the Viva Demo Flow** (all 3 members together) | All | Judges will ask specific questions mid-demo |
| 4 | **Upgrade Gemini model name** in `ai/insights.py` line 241 | Member 2 | Current model string may be outdated; test with latest stable model |

### 🟡 MEDIUM PRIORITY (Will Significantly Improve Score)

| # | Task | Who | Detail |
|---|---|---|---|
| 5 | **ML: Demand Forecasting Model** | Member 2 | Train a time-series model to predict next week's demand per product per store (see Section 6) |
| 6 | **ML: Churn Prediction** | Member 2 | Flag customers likely to stop ordering (see Section 6) |
| 7 | **Streamlit Web App** | Member 2 | Wrap the AI engine in a web UI so judges can interact without terminal |
| 8 | **Expand data to 6 months** | Member 1 | More data = richer trends in Power BI |
| 9 | **Add a `riders` table** | Member 1 | Track individual rider performance; enables rider-level analytics |

### 🟢 NICE-TO-HAVE (Bonus Points)

| # | Task | Detail |
|---|---|---|
| 10 | Email/WhatsApp alert simulation | Show that the AI can "send" a priority alert |
| 11 | Multi-store comparison page in Power BI | Side-by-side KPI benchmarking |
| 12 | Sentiment word cloud from feedback_text | Visually powerful; easy with Python `wordcloud` |

---

## 6. ML Integration Roadmap — Making It Outstanding

> **Context for MBA team**: Adding actual ML models (not just rule-based SQL + AI text) transforms this from a "BI tool" into a true "Decision Intelligence System." This is what will separate you at the final viva.

---

### ML Module 1: Demand Forecasting (Highest Impact)

**Business Problem**: "We run out of Amul Milk every Friday because we don't know how much to stock."

**What to Build**: A model that predicts units sold for the next 7 days, per product per store.

**Algorithm**: `Prophet` (by Meta/Facebook) — best for time-series with seasonality. Alternatively, `XGBoost` with lag features.

**New File**: `ml/demand_forecast.py`

```python
# Suggested structure for ml/demand_forecast.py

# Step 1: Pull historical daily sales from MySQL
# SELECT record_date, store_id, product_id, units_sold FROM inventory

# Step 2: For each (store_id, product_id) pair, train a Prophet model
# model = Prophet(weekly_seasonality=True)
# model.fit(df.rename(columns={'record_date': 'ds', 'units_sold': 'y'}))

# Step 3: Predict next 7 days
# forecast = model.predict(future)

# Step 4: Compare predicted demand with current reorder_level
# If forecast['yhat'] > current_stock + reorder_level → flag as "REORDER NOW"

# Step 5: Save predictions to new MySQL table: demand_forecasts
# Or export to CSV for Power BI import
```

**Power BI Integration**: Import the `demand_forecasts` table → Add a "Predicted Stockout Risk" column to the product table → Color-code in dashboard.

**Viva Talking Point**: *"Our ML model predicts demand 7 days ahead. If the forecast exceeds current stock + reorder threshold, the system automatically flags which products to restock and when — before a stockout occurs."*

**Packages to add to requirements.txt**:
```
prophet==1.1.5
scikit-learn==1.4.1
matplotlib==3.8.3
seaborn==0.13.2
```

---

### ML Module 2: Customer Churn Prediction (Medium Impact)

**Business Problem**: "We don't know which customers are about to stop ordering until they already have."

**What to Build**: Binary classifier that predicts `will_churn_next_month` (Yes/No) for each customer.

**Algorithm**: `Random Forest` or `XGBoost` (both work well on tabular customer data).

**Features to use** (all already in the database):
- `days_since_last_order`
- `total_orders_last_30_days`
- `avg_order_value`
- `cancellation_rate`
- `avg_delivery_time_experienced`
- `avg_rating_given`
- `customer_segment`

**New File**: `ml/churn_model.py`

```python
# Suggested structure for ml/churn_model.py

# Step 1: Build customer feature table from MySQL (the SQL is in analytics/queries.sql Q11)
# Step 2: Label customers: 1 = churned (no order in last 30 days), 0 = active
# Step 3: Train/test split (80/20)
# Step 4: Train XGBClassifier or RandomForestClassifier
# Step 5: Output: churn_probability for each customer
# Step 6: Flag top 100 at-risk customers for marketing intervention
```

**Viva Talking Point**: *"Our churn model identifies at-risk customers with X% accuracy before they leave. Marketing can then target them with personalized offers, increasing retention rate."*

---

### ML Module 3: Delivery Time Prediction (Bonus, Impressive)

**Business Problem**: "Customers are given a fixed '15-minute' promise. Can we give a more accurate, dynamic ETA?"

**What to Build**: Regression model predicting actual delivery time.

**Algorithm**: `Linear Regression` or `XGBoost Regressor`

**Features**: `order_hour`, `day_of_week`, `store_id`, `rider_capacity`, `delivery_distance_km`, `current_stockout_rate`

**Viva Talking Point**: *"Instead of a fixed 15-minute promise, our model dynamically estimates delivery time based on real conditions — resulting in better customer expectations and fewer cancellations."*

---

### Where ML Outputs Go (Integration Points)

```
ml/demand_forecast.py
        ↓
demand_forecasts table (MySQL)
        ↓
Power BI Page 3 (Inventory): "Predicted Restock Needed" visual
        ↓
ai/insights.py: Add forecast data to the Gemini prompt
  "ML predicts stockout risk for [product] in next 3 days..."
```

---

## 7. Suggested New Files to Build

```
Major Project/
│
├── ml/                          ← NEW: ML module folder
│   ├── demand_forecast.py       ← Demand prediction (Prophet)
│   ├── churn_model.py           ← Customer churn (XGBoost)
│   └── delivery_predictor.py   ← Delivery time regression (optional)
│
├── app/                         ← NEW: Streamlit web app (optional but impressive)
│   └── streamlit_app.py         ← Interactive UI for AI insights
│
├── database/
│   ├── schema.sql               ← EXISTING ✅
│   ├── seed_data.py             ← EXISTING ✅
│   └── add_ml_tables.sql        ← NEW: Tables for demand_forecasts, churn_scores
│
└── ml_requirements.txt          ← NEW: ML-specific packages
```

### New ML Database Tables (add to MySQL)

```sql
-- TABLE: demand_forecasts
CREATE TABLE demand_forecasts (
    forecast_id     BIGINT AUTO_INCREMENT PRIMARY KEY,
    store_id        INT NOT NULL,
    product_id      INT NOT NULL,
    forecast_date   DATE NOT NULL,
    predicted_units INT NOT NULL,
    confidence_low  INT,
    confidence_high INT,
    restock_alert   TINYINT(1) DEFAULT 0,
    generated_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (store_id)   REFERENCES stores(store_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- TABLE: churn_scores
CREATE TABLE churn_scores (
    score_id         BIGINT AUTO_INCREMENT PRIMARY KEY,
    customer_id      INT NOT NULL,
    churn_probability DECIMAL(5,4),
    risk_label       VARCHAR(20),   -- 'HIGH', 'MEDIUM', 'LOW'
    model_version    VARCHAR(20),
    scored_at        DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
```

---

### Streamlit Web App (`app/streamlit_app.py`)

A simple Streamlit app makes the project interactive for the viva panel:

```python
# Install: pip install streamlit
# Run: streamlit run app/streamlit_app.py

import streamlit as st
# Store selector → calls ai/insights.py → displays AI output live
# Chart section → uses matplotlib/plotly to show SQL query results
# ML section → shows demand forecast chart + churn risk table
```

---

## 8. Viva Q&A Preparation

### Questions You Will Definitely Be Asked

**Q1: What is the core business problem this solves?**
> *"Quick-commerce store managers have access to dashboards but cannot quickly determine WHY a store is underperforming or WHAT to do about it. Our system automates root cause diagnosis by combining SQL analytics with AI interpretation — giving managers a plain-English explanation and actionable recommendations within seconds."*

**Q2: How is AI used? Isn't it just SQL + report?**
> *"The SQL layer computes verified, deterministic metrics. The Gemini AI layer receives only these structured metrics — never raw data — and provides business interpretation, root cause analysis, and recommended actions written for a non-technical manager. The AI handles language; SQL handles numbers."*

**Q3: How do you prevent hallucination?**
> *"By design — the LLM never touches the database. All numerical metrics are SQL-computed. Gemini only receives verified, structured JSON output. It cannot invent numbers because none are requested from it."*

**Q4: Why synthetic data?**
> *"Real quick-commerce data is proprietary and NDA-protected. Our synthetic data is generated to match real operational patterns — we've embedded two real business scenarios (stockout problem in Store 3, margin erosion in Store 7) to ensure the analytics produce meaningful, realistic insights."*

**Q5: What ML models did you add?** *(Answer after building ML modules)*
> *"We added a demand forecasting model using Facebook Prophet that predicts product-level demand 7 days ahead. It generates restock alerts before a stockout occurs. We also built a customer churn model using XGBoost that flags customers likely to stop ordering, enabling proactive retention campaigns."*

**Q6: How does this differ from just using Power BI?**
> *"Power BI shows what happened. Our AI engine explains WHY it happened and tells management what to do next. The ML modules predict what WILL happen. Together: Past → Present → Future, which is the full decision intelligence cycle."*

**Q7: What is the business impact?**
> *"For Store 3 alone: If stockout rate is reduced from 33% to <8%, we estimate revenue recovery of approximately ₹50,000/month per store based on the MoM decline data. Across 10 stores, systematic AI-driven operations monitoring could prevent millions in revenue loss annually."*

---

## 9. Team Task Division (Going Forward)

### Member 1 — Data & Database
- [ ] Re-run `seed_data.py` to expand data to 6 months if possible
- [ ] Create `ml/add_ml_tables.sql` (demand_forecasts + churn_scores tables)
- [ ] Add a `riders` table to schema for individual rider performance tracking
- [ ] Verify all 8 tables load correctly in Power BI

### Member 2 — AI & ML
- [x] Update Gemini model name in `ai/insights.py` to `gemini-2.5-flash` and verified live API generation
- [x] Build `ml/demand_forecast.py` using multi-step XGBoost/RF time-series with 7-day recursive lag features (Completed)
- [x] Build `ml/churn_model.py` using XGBoost/Random Forest with behavioral feature engineering (Completed)
- [x] Build `ml/delivery_predictor.py` for dynamic ETA and SLA breach risk estimation (Completed)
- [x] Build `ml/alert_notifier.py` for automated simulated alert dispatching via WhatsApp/SMS/Email (Completed)
- [x] Integrate ML predictions into the Gemini prompt in `ai/insights.py` (Completed)
- [x] Create master runner `ml/run_all_ml.py` for seamless viva execution (Completed)
- [x] Build Streamlit app in `app/streamlit_app.py` (Completed)

### Member 3 — Power BI & Presentation
- [x] Enhanced Web Dashboard with all ML tabs (`dashboard/index.html` - Demand Forecast, Churn, Delivery ETA, Alerts) (Completed)
- [x] Author Comprehensive Major Project Report (`MAJOR_PROJECT_REPORT.docx` & `MAJOR_PROJECT_REPORT.md`) (Completed)
- [x] Update `docs/presentation.html` with ML slides for Final Viva (Completed)
- [x] Prepare 20-Question Viva Voce Defense Master Guide in Report Chapter 10 (Completed)
- [ ] Connect Power BI Desktop with MySQL ODBC using `powerbi/connection_guide.md` (Optional bonus)

---

## 10. File Reference Map

| File | Status | Priority |
|---|---|---|
| [`database/schema.sql`](database/schema.sql) | ✅ Complete | — |
| [`database/seed_data.py`](database/seed_data.py) | ✅ Complete | — |
| [`analytics/queries.sql`](analytics/queries.sql) | ✅ Complete (15 queries) | — |
| [`ai/insights.py`](ai/insights.py) | ✅ Complete (Live Gemini 2.5 Flash + Offline Fail-Safe) | — |
| [`dashboard/index.html`](dashboard/index.html) | ✅ Complete (Upgraded with 7 Interactive ML Tabs) | — |
| [`docs/kpi_dictionary.md`](docs/kpi_dictionary.md) | ✅ Complete | — |
| [`docs/presentation.html`](docs/presentation.html) | ✅ Complete (Upgraded Final Viva Deck) | — |
| [`powerbi/connection_guide.md`](powerbi/connection_guide.md) | ✅ Complete | Follow to build PBI |
| [`store_3_insight.json`](store_3_insight.json) | ✅ Sample output | Use in demo |
| [`store_7_insight.json`](store_7_insight.json) | ✅ Sample output | Use in demo |
| [`ml/demand_forecast.py`](ml/demand_forecast.py) | ✅ Complete (XGBoost/RF 7-Day Forecast) | — |
| [`ml/churn_model.py`](ml/churn_model.py) | ✅ Complete (Customer Churn Classifier) | — |
| [`ml/delivery_predictor.py`](ml/delivery_predictor.py) | ✅ Complete (Dynamic ETA Regressor) | — |
| [`ml/alert_notifier.py`](ml/alert_notifier.py) | ✅ Complete (Automated Notification Dispatcher) | — |
| [`ml/run_all_ml.py`](ml/run_all_ml.py) | ✅ Complete (Master Pipeline Runner) | — |
| [`database/add_ml_tables.sql`](database/add_ml_tables.sql) | ✅ Complete | Run in MySQL |
| [`app/streamlit_app.py`](app/streamlit_app.py) | ✅ Complete (Interactive Operations Console) | — |
| [`MAJOR_PROJECT_REPORT.docx`](MAJOR_PROJECT_REPORT.docx) | ✅ Complete (University-Grade 15,000+ Word Formal Report) | — |
| [`MAJOR_PROJECT_REPORT.md`](MAJOR_PROJECT_REPORT.md) | ✅ Complete (Full Markdown Thesis) | — |

---

## 📌 Key Notes for the Group

1. **The project title stays the same** — "AI-Powered Business Decision Intelligence System for Quick-Commerce Operations"

2. **The business context stays the same** — Quick-commerce (Blinkit/Zepto-style), Store 3 and Store 7 as demo stores

3. **ML is additive** — Don't replace anything, just add new files in a `ml/` folder and integrate outputs into the existing pipeline

4. **The Gemini API key in `.env`** — Each team member needs their own free key from https://aistudio.google.com/app/apikey (free tier: 15 req/min, sufficient for demo)

5. **For the viva demo**, the most impressive sequence is:
   - Power BI (visual "what happened")
   - Terminal: `python ai/insights.py 3` (real-time AI analysis)
   - ML chart (demand forecast showing predicted stockout risk)
   - Explain the anti-hallucination architecture

6. **The `.env` file in the zip** — Update it with your own DB password and Gemini key before running

---

*Document prepared for group handover — Mid-Semester 2026*  
*Project: Major Project | 4th Year IT Students | MBA/BBA Collaboration*
