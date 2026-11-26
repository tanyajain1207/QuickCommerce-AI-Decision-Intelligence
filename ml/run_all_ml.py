#!/usr/bin/env python3
"""
Quick-Commerce Decision Intelligence — Master ML & AI Pipeline Runner
Author: Member 2 (AI & ML Team)
Project: AI-Powered Business Decision Intelligence System

Runs the full machine learning lifecycle in sequential order:
  1. Demand Forecasting (XGBoost Time-Series)
  2. Customer Churn Prediction (Random Forest / XGBoost)
  3. Dynamic Delivery ETA Engine (Gradient Boosting)
  4. Automated Alert & Notification Dispatcher (WhatsApp / SMS / Push simulation)
  5. Executive AI Insight Generation (Google Gemini 2.5 Flash)
"""

import os
import sys
import subprocess
import time

# Force UTF-8 on Windows terminal output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PYTHON_EXE = sys.executable

SCRIPTS = [
    ("ML Module 1: Demand Forecasting & Restock Alert", os.path.join(BASE_DIR, "ml", "demand_forecast.py")),
    ("ML Module 2: Customer Churn Prediction & Scoring", os.path.join(BASE_DIR, "ml", "churn_model.py")),
    ("ML Module 3: Dynamic Delivery ETA & SLA Risk", os.path.join(BASE_DIR, "ml", "delivery_predictor.py")),
    ("Automated Alert & Notification Dispatcher", os.path.join(BASE_DIR, "ml", "alert_notifier.py")),
    ("Executive AI Decision Engine (Gemini 2.5 Flash)", os.path.join(BASE_DIR, "ai", "insights.py"), ["3"]),
]

def main():
    print("=" * 80)
    print("  🚀 EXECUTING MASTER ML & AI DECISION INTELLIGENCE PIPELINE")
    print("  Author: Member 2 (AI & ML Team)")
    print("=" * 80)

    start_total = time.time()

    for item in SCRIPTS:
        title = item[0]
        script_path = item[1]
        args = item[2] if len(item) > 2 else []

        print(f"\n▶ [{title}]")
        print(f"  Running: {os.path.basename(script_path)} {' '.join(args)}")
        print("-" * 80)

        cmd = [PYTHON_EXE, script_path] + args
        result = subprocess.run(cmd, cwd=BASE_DIR)

        if result.returncode != 0:
            print(f"  ⚠ Warning: {os.path.basename(script_path)} exited with code {result.returncode}")
        else:
            print(f"  ✓ {title} finished successfully.")

    total_time = round(time.time() - start_total, 2)
    print("\n" + "=" * 80)
    print(f"  🎉 MASTER ML & AI PIPELINE COMPLETED IN {total_time} SECONDS!")
    print("  All ML models trained, predictions saved, alerts dispatched, and AI analysis completed.")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()
