# ⚡ AI-Powered Business Decision Intelligence System
### Quick-Commerce Operations 
**Domain:** Quick-Commerce (Blinkit / Zepto / Swiggy Instamart style)

---

## 🎯 What This System Does

Store managers in quick-commerce cannot quickly identify **why** a store is underperforming. This system automates that entire diagnostic pipeline:

1. **SQL Analytics** — 15 business intelligence queries across 8 database tables
2. **ML Demand Forecasting** — XGBoost time-series predicts next 7 days of SKU demand + restock alerts
3. **ML Churn Prediction** — XGBoost classifies 500 customers into HIGH / MEDIUM / LOW churn risk
4. **ML Delivery ETA** — Gradient Boosting predicts actual fulfillment time vs 15-min SLA
5. **AI Diagnosis** — Google Gemini 2.5 Flash generates a natural-language operational report
6. **Alert Dispatcher** — Automated simulated WhatsApp / SMS / Push notifications to managers

> **Anti-Hallucination Design:** SQL computes all KPIs deterministically → ML adds predictive signals → Gemini only interprets verified numbers → zero hallucinated metrics.

---

## 🗂️ Project Structure

```
Major Project/
├── .env                        # DB credentials + Gemini API key (never commit)
├── requirements.txt            # All Python dependencies
│
├── database/
│   ├── schema.sql              # MySQL schema (8 tables)
│   ├── seed_data.py            # Synthetic data generator (3,000 orders, 90 days)
│   └── add_ml_tables.sql       # ML output tables (demand_forecasts, churn_scores, delivery_predictions)
│
├── analytics/
│   └── queries.sql             # 15 BI SQL queries (Window functions, CTEs, LAG)
│
├── ml/
│   ├── demand_forecast.py      # XGBoost SKU-level 7-day demand forecast
│   ├── churn_model.py          # XGBoost customer churn classifier
│   ├── delivery_predictor.py   # Gradient Boosting delivery ETA + SLA risk
│   ├── alert_notifier.py       # Automated alert dispatcher
│   └── run_all_ml.py           # ⭐ Master pipeline runner (run this for full demo)
│
├── ai/
│   └── insights.py             # Gemini 2.5 Flash AI insight engine
│
├── app/
│   └── streamlit_app.py        # Interactive Streamlit web dashboard
│
├── dashboard/
│   └── index.html              # 7-tab standalone HTML dashboard
│
└── docs/
    ├── MAJOR_PROJECT_REPORT.docx    # Full 15,000+ word formal report
    ├── presentation.html            # 16-slide viva deck (open in browser)
    └── kpi_dictionary.md            # KPI definitions reference
```

---

## 🚀 Setup & Run Guide

### Prerequisites
- Python 3.11.x installed
- MySQL 8.0 running (XAMPP or standalone)
- Gemini API key from https://aistudio.google.com/app/apikey (free)

### Step 1 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2 — Configure Environment
Edit `.env` with your credentials:
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=quickcommerce_db
GEMINI_API_KEY=your_gemini_api_key_here
```

### Step 3 — Set Up MySQL Database
```bash
# Create schema (8 tables)
mysql -u root -p < database/schema.sql

# Generate synthetic data (3,000 orders, 500 customers, 90 days)
python database/seed_data.py

# Create ML output tables
mysql -u root -p quickcommerce_db < database/add_ml_tables.sql
```

### Step 4 — Run the Full ML + AI Pipeline ⭐
```bash
python ml/run_all_ml.py
```
This runs all 5 modules sequentially:
- Demand Forecast → Churn Prediction → Delivery ETA → Alert Dispatcher → AI Insight Engine
- Expected time: ~45–60 seconds (with MySQL) or ~50 seconds (standalone/no-DB mode)

### Step 5 — Launch Streamlit Dashboard
```bash
python -m streamlit run app/streamlit_app.py
```
Opens at `http://localhost:8501`

### Step 6 — Run AI Insight for Specific Store
```bash
python ai/insights.py 3     # Store 3 — QuickMart Koramangala (crisis store)
python ai/insights.py 7     # Store 7 — QuickMart Gurugram (margin erosion)
python ai/insights.py 3 7   # Both stores
```

---

## 🧪 Viva Demo Sequence (Recommended)

| Step | Command / Action | Shows |
|------|-----------------|-------|
| 1 | `python ml/run_all_ml.py` | Full ML pipeline in 45s |
| 2 | `python ai/insights.py 3` | AI diagnosis of crisis store |
| 3 | `python -m streamlit run app/streamlit_app.py` | Live interactive dashboard |
| 4 | Open `docs/presentation.html` in browser | 16-slide presentation |
| 5 | Explain anti-hallucination architecture | SQL → ML → Gemini chain |

---

## 📊 Database Overview

| Table | Records | Purpose |
|-------|---------|---------|
| `customers` | 500 | Demographics, segment, acquisition channel |
| `stores` | 10 | Dark store info, cities, rider capacity |
| `products` | 80 | Catalog with cost price, shelf life |
| `orders` | ~3,000 | Transactions with status, discounts |
| `order_items` | ~9,000 | Line items per order |
| `inventory` | ~7,200 | Daily stock with stockout flags |
| `deliveries` | ~2,700 | Rider delivery times, delay flags |
| `customer_feedback` | ~1,500 | Ratings and sentiment |

**Intentionally embedded anomalies for demo:**
- **Store 3 (Koramangala):** High stockout ~35%, slow delivery ~28 min, declining revenue
- **Store 7 (Gurugram):** High discount ~22% eroding gross margin

---

## 🤖 ML Model Performance

| Model | Algorithm | Key Metric |
|-------|-----------|-----------|
| Demand Forecast | XGBoost Regressor (7-day lag features) | 120 store-SKU models |
| Churn Classifier | XGBoost Classifier | ROC-AUC: 0.84, Accuracy: 94% |
| Delivery ETA | Gradient Boosting Regressor | R²: 95.4%, MAE: ±1.83 min |

---

## ⚠️ Important Notes

- **Offline mode:** All ML scripts work WITHOUT MySQL — they fall back to realistic synthetic data generators that match seed_data.py distributions exactly.
- **Gemini API:** Works with an active internet connection. Falls back to a deterministic rule-based insight engine if API is unreachable.
- **XGBoost vs fallback:** XGBoost is the primary model. If not installed, scripts fall back to Random Forest / Gradient Boosting Regressor with comparable performance.
- **`.env` file:** Never commit this to public GitHub. Each team member needs their own Gemini API key (free at aistudio.google.com).

