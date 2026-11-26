#!/usr/bin/env python3
"""
Quick-Commerce ML Module 3: Dynamic Delivery Time Predictor & SLA Risk Engine
Author: Member 2 (AI & ML Team)
Project: AI-Powered Business Decision Intelligence System

Algorithm:
  XGBoost & Gradient Boosting Regression for Dynamic ETA Prediction.
  Predicts realistic delivery time based on rider capacity, distance, hour, and store load.

Business Value:
  Replaces rigid, failing 15-minute promises with dynamic, realistic ETAs.
  Warns dispatchers when orders have high probability of SLA breach (>20 min).
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

from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score

try:
    from xgboost import XGBRegressor
    HAS_XGBOOST = True
except ImportError:
    HAS_XGBOOST = False

load_dotenv()
warnings.filterwarnings("ignore")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ML_DIR = os.path.join(BASE_DIR, "ml")
os.makedirs(ML_DIR, exist_ok=True)

DB_CONFIG = {
    "host":     os.getenv("DB_HOST", "localhost"),
    "user":     os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "quickcommerce_db"),
    "connection_timeout": 2
}


def get_db_connection():
    try:
        import mysql.connector
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            return conn
    except Exception:
        return None
    return None


def fetch_delivery_data():
    """Pulls delivery records from MySQL or generates realistic baseline."""
    conn = get_db_connection()
    if conn:
        try:
            print("  [DB] Connected to MySQL. Pulling delivery fulfillment records...")
            query = """
                SELECT 
                    d.delivery_id,
                    o.store_id,
                    s.store_name,
                    s.rider_capacity,
                    HOUR(o.order_datetime) AS order_hour,
                    DAYOFWEEK(o.order_datetime) AS day_of_week,
                    d.delivery_distance_km,
                    o.subtotal,
                    d.delivery_time_min,
                    d.delay_flag
                FROM deliveries d
                JOIN orders o ON d.order_id = o.order_id
                JOIN stores s ON o.store_id = s.store_id
                WHERE d.delivery_time_min IS NOT NULL;
            """
            df = pd.read_sql(query, conn)
            conn.close()
            if not df.empty:
                print(f"  ✓ Retrieved {len(df):,} delivery records from MySQL.")
                return df
        except Exception as e:
            print(f"  ⚠ MySQL query error: {e}. Falling back to baseline generator.")
            if conn: conn.close()

    # Baseline generator matching seed_data.py distributions
    print("  [INFO] MySQL not active. Generating 2,700 realistic delivery records...")
    np.random.seed(42)
    n_samples = 2700

    stores = [
        (1, "QuickMart Connaught Place", 15),
        (2, "QuickMart Lajpat Nagar", 12),
        (3, "QuickMart Koramangala", 5),   # Anomaly: severe rider shortage
        (4, "QuickMart Sector 18 Noida", 14),
        (5, "QuickMart Indiranagar", 13),
        (6, "QuickMart Dwarka", 14),
        (7, "QuickMart Sector 56 Gurugram", 13),
        (8, "QuickMart Malviya Nagar", 12),
        (9, "QuickMart Whitefield", 13),
        (10, "QuickMart Cyber City", 13),
    ]

    rows = []
    for _ in range(n_samples):
        store = stores[np.random.choice(len(stores))]
        sid, sname, riders = store

        hour_weights = [1,1,0,0,0,0,1,3,5,4,3,2,4,4,3,2,2,3,4,6,6,4,2,1]
        hour = np.random.choice(range(24), p=np.array(hour_weights)/sum(hour_weights))
        dow = np.random.randint(1, 8)
        dist = round(float(np.random.uniform(0.6, 3.8)), 2)
        subtotal = round(float(np.random.uniform(100, 850)), 2)

        # Operational physics:
        # Distance travel time: ~4 min per km
        # In-store picking: ~3 min
        # Rider availability penalty: fewer riders = longer queue wait
        queue_wait = max(1.0, (18 - riders) * 1.5)
        if sid == 3:  # Store 3 severe backlog
            queue_wait += np.random.uniform(8, 16)
        
        peak_factor = 1.3 if hour in [8, 9, 13, 19, 20, 21] else 1.0
        
        del_time = int(round((3.0 + dist * 3.8 + queue_wait) * peak_factor + np.random.normal(0, 2.0)))
        del_time = max(8, del_time)
        delay_flag = 1 if del_time > 20 else 0

        rows.append({
            "store_id": sid,
            "store_name": sname,
            "rider_capacity": riders,
            "order_hour": hour,
            "day_of_week": dow,
            "delivery_distance_km": dist,
            "subtotal": subtotal,
            "delivery_time_min": del_time,
            "delay_flag": delay_flag
        })

    df = pd.DataFrame(rows)
    print(f"  ✓ Generated {len(df):,} delivery training records.")
    return df


def train_delivery_predictor():
    print("\n" + "=" * 70)
    print("  🚴 QUICK-COMMERCE ML DYNAMIC DELIVERY ETA PREDICTOR")
    print("=" * 70)

    df = fetch_delivery_data()

    # Feature Engineering
    df["is_peak_hour"]   = df["order_hour"].apply(lambda h: 1 if h in [8, 9, 13, 19, 20, 21] else 0)
    df["is_weekend"]     = df["day_of_week"].apply(lambda d: 1 if d in [1, 7] else 0)
    df["rider_pressure"] = (df["delivery_distance_km"] * 10) / df["rider_capacity"].clip(lower=1)
    # store_id encodes store-specific structural delays (e.g. Store 3 always slow)
    df["store_id_enc"]   = df["store_id"].astype(int)
    # distance × peak interaction captures rush-hour distance effect
    df["dist_peak"]      = df["delivery_distance_km"] * df["is_peak_hour"]
    # low rider capacity flag (< 8 = critically short-staffed)
    df["low_riders"]     = (df["rider_capacity"] < 8).astype(int)

    feature_cols = [
        "store_id_enc", "rider_capacity", "order_hour", "day_of_week",
        "delivery_distance_km", "subtotal", "is_peak_hour",
        "is_weekend", "rider_pressure", "dist_peak", "low_riders"
    ]

    X = df[feature_cols]
    y = df["delivery_time_min"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )

    if HAS_XGBOOST:
        model = XGBRegressor(
            n_estimators=100,
            max_depth=4,
            learning_rate=0.08,
            subsample=0.85,
            random_state=42,
            verbosity=0
        )
        model_name = "XGBoost Regressor"
    else:
        model = GradientBoostingRegressor(
            n_estimators=100, max_depth=4, learning_rate=0.08, random_state=42
        )
        model_name = "Gradient Boosting Regressor"

    print(f"  ⏳ Training {model_name}...")
    model.fit(X_train, y_train)

    preds_test = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds_test)
    rmse = root_mean_squared_error(y_test, preds_test)
    r2 = r2_score(y_test, preds_test)

    print(f"\n  🎯 Model Performance Metrics (Test Set):")
    print(f"     • Mean Absolute Error (MAE) : ±{mae:.2f} minutes")
    print(f"     • Root Mean Squared Error   : ±{rmse:.2f} minutes")
    print(f"     • R² Score (Variance Exp.)  : {r2 * 100:.1f}%")

    # Feature importances
    fi_df = pd.DataFrame({"Feature": feature_cols, "Importance": model.feature_importances_}).sort_values("Importance", ascending=False)
    print("\n  🔑 Top Delivery Time Drivers:")
    for _, r in fi_df.head(4).iterrows():
        print(f"     • {r['Feature']:<22}: {r['Importance'] * 100:.1f}% impact")

    # Predict ETA for test set & benchmark against 15-min SLA
    df["predicted_delivery_min"] = np.round(model.predict(X), 1)
    df["sla_risk_flag"] = (df["predicted_delivery_min"] > 20).astype(int)

    # ── Save Outputs ───────────────────────────────────────────
    csv_path = os.path.join(ML_DIR, "delivery_predictions.csv")
    df.to_csv(csv_path, index=False)

    store_stats = []
    for sid, sgroup in df.groupby("store_id"):
        store_stats.append({
            "store_id": int(sid),
            "store_name": sgroup["store_name"].iloc[0],
            "rider_capacity": int(sgroup["rider_capacity"].iloc[0]),
            "avg_actual_delivery": round(float(sgroup["delivery_time_min"].mean()), 1),
            "avg_predicted_delivery": round(float(sgroup["predicted_delivery_min"].mean()), 1),
            "delay_risk_pct": round(float(sgroup["sla_risk_flag"].mean() * 100), 1)
        })

    summary = {
        "generated_at": datetime.now().isoformat(),
        "model_used": model_name,
        "metrics": {"mae_min": round(mae, 2), "rmse_min": round(rmse, 2), "r2_score": round(r2, 4)},
        "store_benchmarks": sorted(store_stats, key=lambda x: x["delay_risk_pct"], reverse=True)
    }

    json_path = os.path.join(ML_DIR, "delivery_summary_latest.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    # Write to MySQL if available
    conn = get_db_connection()
    if conn:
        try:
            print("  [DB] Writing predictions to MySQL `delivery_predictions` table...")
            cur = conn.cursor()
            cur.execute("TRUNCATE TABLE delivery_predictions;")
            insert_sql = """
                INSERT INTO delivery_predictions 
                (store_id, order_hour, day_of_week, delivery_distance_km, predicted_delivery_min, sla_target_min, delay_risk_flag, model_version)
                VALUES (%s, %s, %s, %s, %s, 15, %s, %s);
            """
            sample_df = df.sample(min(1000, len(df)))
            rows_to_insert = [
                (
                    int(r["store_id"]), int(r["order_hour"]), f"Day_{r['day_of_week']}",
                    float(r["delivery_distance_km"]), float(r["predicted_delivery_min"]),
                    int(r["sla_risk_flag"]), model_name
                )
                for _, r in sample_df.iterrows()
            ]
            cur.executemany(insert_sql, rows_to_insert)
            conn.commit()
            cur.close()
            conn.close()
            print("  ✓ MySQL delivery_predictions table successfully populated!")
        except Exception as e:
            print(f"  ⚠ MySQL write skipped: {e}")

    print(f"\n  ✅ Dynamic Delivery Predictor Completed Successfully!")
    print(f"     • Exported CSV  : {csv_path}")
    print(f"     • Exported JSON : {json_path}")

    print("\n  📍 Delivery Time & Delay Risk by Store (Ranking):")
    print(f"     {'Store Name':<32} | {'Riders':<6} | {'Avg Pred ETA':<13} | {'SLA Delay Risk':<14}")
    print("     " + "-" * 75)
    for s in summary["store_benchmarks"]:
        print(f"     {s['store_name'][:30]:<32} | {s['rider_capacity']:<6} | {s['avg_predicted_delivery']:<4} min      | {s['delay_risk_pct']:<5}%")
    print("=" * 70 + "\n")

    return df


if __name__ == "__main__":
    train_delivery_predictor()
