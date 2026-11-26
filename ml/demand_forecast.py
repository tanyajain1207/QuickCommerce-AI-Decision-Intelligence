#!/usr/bin/env python3
"""
Quick-Commerce ML Module 1: SKU-Level Demand Forecasting & Restock Alert Engine
Author: Member 2 (AI & ML Team)
Project: AI-Powered Business Decision Intelligence System

Algorithm:
  Multi-feature XGBoost / Random Forest Time-Series Regressor with Lag & Rolling Window Engineering.
  Predicts daily units sold for the next 7 days for each (store, product) pair.

Business Value:
  Proactively identifies stockout risks BEFORE they happen.
  If 7-day predicted demand > (current_stock), triggers an automated RESTOCK ALERT.
"""

import os
import sys
import json
import warnings
from datetime import datetime, date, timedelta

# Force UTF-8 on Windows terminal output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

import numpy as np
import pandas as pd
from dotenv import load_dotenv

# ML libraries
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, root_mean_squared_error

try:
    from xgboost import XGBRegressor
    HAS_XGBOOST = True
except ImportError:
    HAS_XGBOOST = False

load_dotenv()
warnings.filterwarnings("ignore")

# ── Paths & Config ───────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ML_DIR = os.path.join(BASE_DIR, "ml")
os.makedirs(ML_DIR, exist_ok=True)

DB_CONFIG = {
    "host":     os.getenv("DB_HOST", "localhost"),
    "user":     os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "quickcommerce_db"),
}

FORECAST_HORIZON_DAYS = 7


def get_db_connection():
    """Attempts MySQL connection, returns None if unavailable."""
    try:
        import mysql.connector
        cfg = dict(DB_CONFIG)
        cfg["connection_timeout"] = 2
        conn = mysql.connector.connect(**cfg)
        if conn.is_connected():
            return conn
    except Exception:
        return None
    return None


def fetch_historical_sales():
    """
    Pulls historical daily sales from MySQL inventory table.
    If MySQL is not active, generates deterministic operational baseline data
    matching database/seed_data.py distributions so models can always run.
    """
    conn = get_db_connection()
    if conn:
        try:
            print("  [DB] Connected to MySQL. Extracting daily sales data...")
            query = """
                SELECT 
                    i.store_id,
                    s.store_name,
                    s.city,
                    i.product_id,
                    p.product_name,
                    p.category,
                    p.unit_price,
                    p.unit_cost,
                    i.record_date,
                    i.units_sold,
                    i.closing_stock,
                    i.reorder_level,
                    i.stockout_flag
                FROM inventory i
                JOIN stores s ON i.store_id = s.store_id
                JOIN products p ON i.product_id = p.product_id
                ORDER BY i.store_id, i.product_id, i.record_date ASC;
            """
            df = pd.read_sql(query, conn)
            conn.close()
            if not df.empty:
                df['record_date'] = pd.to_datetime(df['record_date'])
                print(f"  ✓ Retrieved {len(df):,} inventory sales records from MySQL.")
                return df
        except Exception as e:
            print(f"  ⚠ MySQL query error: {e}. Falling back to baseline generator.")
            if conn: conn.close()

    # Standalone generator (matches seed_data.py ground truth exactly)
    print("  [INFO] MySQL not active or empty. Generating realistic 90-day time-series baseline...")
    np.random.seed(42)
    stores = [
        (1, "QuickMart Connaught Place", "Delhi"),
        (2, "QuickMart Lajpat Nagar", "Delhi"),
        (3, "QuickMart Koramangala", "Bengaluru"),  # Anomaly store (high stockouts)
        (4, "QuickMart Sector 18 Noida", "Noida"),
        (5, "QuickMart Indiranagar", "Bengaluru"),
        (6, "QuickMart Dwarka", "Delhi"),
        (7, "QuickMart Sector 56 Gurugram", "Gurugram"),
        (8, "QuickMart Malviya Nagar", "Delhi"),
        (9, "QuickMart Whitefield", "Bengaluru"),
        (10, "QuickMart Cyber City", "Gurugram"),
    ]
    products = [
        (1, "Amul Full Cream Milk 1L", "Dairy", 68, 52, 20),
        (2, "Amul Butter 500g", "Dairy", 260, 200, 15),
        (3, "Mother Dairy Curd 500g", "Dairy", 50, 38, 20),
        (4, "Amul Paneer 200g", "Dairy", 90, 68, 15),
        (5, "Britannia Brown Bread 400g", "Bakery & Eggs", 45, 28, 25),
        (6, "Eggs Tray of 30", "Bakery & Eggs", 165, 118, 20),
        (7, "Tomatoes (1 kg)", "Fruits & Veggies", 40, 25, 30),
        (8, "Onions (1 kg)", "Fruits & Veggies", 35, 22, 30),
        (9, "Coca-Cola 2L", "Beverages", 95, 65, 20),
        (10, "Maggi Noodles (6-pack)", "Snacks", 99, 68, 25),
        (11, "Aashirvaad Atta 5kg", "Staples", 285, 210, 15),
        (12, "Fortune Sunflower Oil 1L", "Staples", 145, 105, 20),
    ]

    dates = pd.date_range("2025-01-01", "2025-03-31", freq="D")
    rows = []

    for sid, sname, city in stores:
        is_store_3 = (sid == 3)
        for pid, pname, cat, price, cost, reorder in products:
            base_sales = np.random.randint(6, 18)
            stock = np.random.randint(40, 120)
            
            for d in dates:
                dow = d.dayofweek
                weekend_boost = 1.35 if dow in [5, 6] else 1.0
                
                # Store 3 suffers supply chain starvation
                if is_store_3:
                    stockout_prob = 0.35
                    is_out = np.random.rand() < stockout_prob
                    sold = 0 if is_out else int(np.clip(np.random.poisson(base_sales * weekend_boost * 0.7), 0, stock))
                else:
                    is_out = np.random.rand() < 0.06
                    sold = 0 if is_out else int(np.clip(np.random.poisson(base_sales * weekend_boost), 0, stock))

                received = np.random.randint(15, 35) if stock < 25 else 0
                stock = max(0, stock + received - sold)

                rows.append({
                    "store_id": sid,
                    "store_name": sname,
                    "city": city,
                    "product_id": pid,
                    "product_name": pname,
                    "category": cat,
                    "unit_price": price,
                    "unit_cost": cost,
                    "record_date": d,
                    "units_sold": sold,
                    "closing_stock": stock,
                    "reorder_level": reorder,
                    "stockout_flag": 1 if is_out or stock == 0 else 0
                })

    df = pd.DataFrame(rows)
    print(f"  ✓ Generated {len(df):,} baseline time-series records across 90 days.")
    return df


def engineer_features(group_df):
    """
    Builds lag and moving window features for a single (store, product) time series.
    """
    df = group_df.sort_values("record_date").copy()
    
    # Calendar features
    df["day_of_week"] = df["record_date"].dt.dayofweek
    df["is_weekend"] = df["day_of_week"].apply(lambda x: 1 if x in [5, 6] else 0)
    df["day_of_month"] = df["record_date"].dt.day
    df["month"] = df["record_date"].dt.month
    
    # Lag features
    df["lag_1"] = df["units_sold"].shift(1)
    df["lag_2"] = df["units_sold"].shift(2)
    df["lag_3"] = df["units_sold"].shift(3)
    df["lag_7"] = df["units_sold"].shift(7)  # Same day last week
    
    # Rolling stats
    df["rolling_mean_7"] = df["units_sold"].shift(1).rolling(window=7, min_periods=1).mean()
    df["rolling_std_7"] = df["units_sold"].shift(1).rolling(window=7, min_periods=1).std().fillna(0)
    df["rolling_max_7"] = df["units_sold"].shift(1).rolling(window=7, min_periods=1).max()

    # Fill NA caused by initial lags with backfill/median
    df = df.bfill().ffill()
    return df


def train_and_forecast_demand():
    """
    Main training and 7-day multi-step recursive forecasting pipeline.
    """
    print("\n" + "=" * 70)
    print("  🚀 QUICK-COMMERCE ML DEMAND FORECAST & RESTOCK ALERT ENGINE")
    print("=" * 70)
    
    df = fetch_historical_sales()
    feature_cols = [
        "day_of_week", "is_weekend", "day_of_month", "month",
        "lag_1", "lag_2", "lag_3", "lag_7",
        "rolling_mean_7", "rolling_std_7", "rolling_max_7"
    ]

    all_forecasts = []
    store_product_pairs = df.groupby(["store_id", "product_id"])
    total_pairs = len(store_product_pairs)
    print(f"  ⏳ Training models across {total_pairs} store-SKU time-series pairs...")

    trained_count = 0
    alerts_triggered = 0

    for (sid, pid), group in store_product_pairs:
        engineered = engineer_features(group)
        if len(engineered) < 14:
            continue

        store_name = engineered["store_name"].iloc[0]
        prod_name = engineered["product_name"].iloc[0]
        category = engineered["category"].iloc[0]
        reorder_level = int(engineered["reorder_level"].iloc[-1])
        latest_stock = int(engineered["closing_stock"].iloc[-1])
        last_date = engineered["record_date"].max()

        # Split train / validation (last 7 days as test to measure MAE)
        train_df = engineered.iloc[:-7]
        test_df = engineered.iloc[-7:]

        X_train, y_train = train_df[feature_cols], train_df["units_sold"]
        X_test, y_test = test_df[feature_cols], test_df["units_sold"]

        # Train model (XGBoost preferred, RandomForest as robust alternative)
        if HAS_XGBOOST:
            model = XGBRegressor(
                n_estimators=60,
                max_depth=3,
                learning_rate=0.08,
                random_state=42,
                verbosity=0
            )
        else:
            model = RandomForestRegressor(n_estimators=50, max_depth=5, random_state=42)

        model.fit(X_train, y_train)
        preds_test = model.predict(X_test)
        mae = mean_absolute_error(y_test, preds_test)

        # ── 7-Day Future Forecasting ────────────────────────────
        future_history = engineered["units_sold"].tolist()
        pred_units_7days = []
        forecast_dates = []

        curr_date = last_date
        for step in range(1, FORECAST_HORIZON_DAYS + 1):
            next_date = curr_date + timedelta(days=step)
            forecast_dates.append(next_date)
            dow = next_date.dayofweek
            is_wknd = 1 if dow in [5, 6] else 0
            dom = next_date.day
            mon = next_date.month

            # Build feature vector from recursive lags
            l1 = future_history[-1]
            l2 = future_history[-2] if len(future_history) >= 2 else l1
            l3 = future_history[-3] if len(future_history) >= 3 else l1
            l7 = future_history[-7] if len(future_history) >= 7 else l1
            rm7 = np.mean(future_history[-7:])
            rs7 = np.std(future_history[-7:])
            rx7 = np.max(future_history[-7:])

            feat_vector = pd.DataFrame([{
                "day_of_week": dow, "is_weekend": is_wknd, "day_of_month": dom, "month": mon,
                "lag_1": l1, "lag_2": l2, "lag_3": l3, "lag_7": l7,
                "rolling_mean_7": rm7, "rolling_std_7": rs7, "rolling_max_7": rx7
            }])

            pred_val = max(0, int(round(float(model.predict(feat_vector)[0]))))
            pred_units_7days.append(pred_val)
            future_history.append(pred_val)

        total_predicted_demand = sum(pred_units_7days)
        avg_daily_demand = max(0.5, total_predicted_demand / FORECAST_HORIZON_DAYS)
        days_to_stockout = round(latest_stock / avg_daily_demand, 1)

        # Restock Alert Condition:
        # If predicted 7-day sales exceeds current stock, or stock drops below reorder point
        needs_restock = 1 if (total_predicted_demand >= latest_stock or latest_stock <= reorder_level) else 0
        if needs_restock:
            alerts_triggered += 1

        for fdate, punits in zip(forecast_dates, pred_units_7days):
            all_forecasts.append({
                "store_id": sid,
                "store_name": store_name,
                "product_id": pid,
                "product_name": prod_name,
                "category": category,
                "forecast_date": fdate.strftime("%Y-%m-%d"),
                "predicted_units": punits,
                "confidence_low": max(0, int(punits - mae)),
                "confidence_high": int(punits + mae + 1),
                "current_stock": latest_stock,
                "reorder_level": reorder_level,
                "total_7day_demand": total_predicted_demand,
                "days_to_stockout": days_to_stockout,
                "restock_alert": needs_restock,
                "model_mae": round(mae, 2)
            })

        trained_count += 1

    forecast_df = pd.DataFrame(all_forecasts)

    # ── Save Outputs ───────────────────────────────────────────
    csv_out = os.path.join(ML_DIR, "demand_forecasts.csv")
    forecast_df.to_csv(csv_out, index=False)

    # Save summary JSON by store (for Gemini and Power BI consumption)
    store_summaries = {}
    for sid, sgroup in forecast_df.groupby("store_id"):
        sname = sgroup["store_name"].iloc[0]
        alerts = sgroup[sgroup["restock_alert"] == 1][["product_name", "category", "current_stock", "total_7day_demand", "days_to_stockout"]].drop_duplicates()
        store_summaries[int(sid)] = {
            "store_id": int(sid),
            "store_name": sname,
            "total_skus_tracked": int(sgroup["product_id"].nunique()),
            "critical_restock_count": len(alerts),
            "critical_skus": alerts.to_dict(orient="records")
        }

    json_out = os.path.join(ML_DIR, "demand_forecasts_latest.json")
    with open(json_out, "w", encoding="utf-8") as f:
        json.dump(store_summaries, f, indent=2)

    # ── Write to MySQL if available ───────────────────────────
    conn = get_db_connection()
    if conn:
        try:
            print("  [DB] Writing forecast records to MySQL `demand_forecasts` table...")
            cur = conn.cursor()
            cur.execute("TRUNCATE TABLE demand_forecasts;")
            insert_sql = """
                INSERT INTO demand_forecasts 
                (store_id, product_id, forecast_date, predicted_units, confidence_low, confidence_high, current_stock, reorder_level, restock_alert, model_version)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'XGBoost_v1.0');
            """
            rows_to_insert = [
                (
                    int(r["store_id"]), int(r["product_id"]), r["forecast_date"],
                    int(r["predicted_units"]), int(r["confidence_low"]), int(r["confidence_high"]),
                    int(r["current_stock"]), int(r["reorder_level"]), int(r["restock_alert"])
                )
                for _, r in forecast_df.iterrows()
            ]
            cur.executemany(insert_sql, rows_to_insert)
            conn.commit()
            cur.close()
            conn.close()
            print("  ✓ MySQL demand_forecasts table successfully populated!")
        except Exception as e:
            print(f"  ⚠ MySQL write skipped: {e}")

    # ── Terminal Display ───────────────────────────────────────
    print(f"\n  ✅ Demand Forecasting Completed Successfully!")
    print(f"     • Models Trained           : {trained_count} store-SKU models")
    print(f"     • Horizon Predicted        : Next 7 days")
    print(f"     • Restock Alerts Triggered : {alerts_triggered} SKU-store combinations")
    print(f"     • Exported CSV             : {csv_out}")
    print(f"     • Exported JSON            : {json_out}")

    print("\n  🔍 High-Priority Restock Alerts (Store 3 - Koramangala):")
    st3_alerts = store_summaries.get(3, {}).get("critical_skus", [])
    if st3_alerts:
        print(f"     {'Product Name':<30} | {'Stock':<6} | {'7-Day Demand':<12} | {'Days Left':<10}")
        print("     " + "-" * 65)
        for item in st3_alerts[:6]:
            print(f"     {item['product_name'][:28]:<30} | {item['current_stock']:<6} | {item['total_7day_demand']:<12} | {item['days_to_stockout']:<10} days")
    else:
        print("     No active alerts for Store 3.")
    print("=" * 70 + "\n")

    return forecast_df


if __name__ == "__main__":
    train_and_forecast_demand()
