#!/usr/bin/env python3
"""
Synthetic Data Generator
AI-Powered Business Decision Intelligence System — Quick-Commerce MVP

Scale: 500 customers | 60 products | 10 stores | 3,000 orders | 90 days
Run:   python seed_data.py

Embedded business patterns (for AI to discover):
  Store 3 (QuickMart Koramangala) — HIGH STOCK-OUTS, DELIVERY DELAYS, DECLINING REVENUE
  Store 7 (QuickMart Gurugram)    — HIGH DISCOUNTS, LOW PROFIT MARGIN
"""

import mysql.connector
import random
from datetime import datetime, date, timedelta
import os
from dotenv import load_dotenv

load_dotenv()
random.seed(42)

# ── Config ───────────────────────────────────────────────────
DB_CONFIG = {
    "host":     os.getenv("DB_HOST", "localhost"),
    "user":     os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "quickcommerce_db"),
}

NUM_CUSTOMERS = 500
NUM_ORDERS    = 3000
START_DATE    = date(2025, 1, 1)
END_DATE      = date(2025, 3, 31)   # 90 days of data

# ── Store behaviour patterns ─────────────────────────────────
#   cancel_rate  : fraction of orders cancelled
#   stockout_prob: daily probability a product is out of stock
#   del_range    : (min, max) delivery time in minutes
#   delay_prob   : probability of a delay flag
#   disc_range   : (min, max) discount as fraction of subtotal
#   rating_range : (min, max) customer rating
#   weight       : relative share of orders going to this store
STORE_PATTERNS = {
    3: {  # UNDERPERFORMING — high stockouts, slow delivery
        "cancel_rate":  0.15,
        "stockout_prob": 0.35,
        "del_range":    (22, 38),
        "delay_prob":   0.45,
        "disc_range":   (0.04, 0.09),
        "rating_range": (1, 3),
        "weight":       0.5,
    },
    7: {  # HIGH DISCOUNT — hurts margin
        "cancel_rate":  0.04,
        "stockout_prob": 0.06,
        "del_range":    (10, 18),
        "delay_prob":   0.08,
        "disc_range":   (0.18, 0.28),
        "rating_range": (3, 5),
        "weight":       1.2,
    },
}
DEFAULT_PATTERN = {
    "cancel_rate":  0.05,
    "stockout_prob": 0.07,
    "del_range":    (8, 18),
    "delay_prob":   0.10,
    "disc_range":   (0.03, 0.10),
    "rating_range": (3, 5),
    "weight":       1.0,
}

def pat(store_id):
    return STORE_PATTERNS.get(store_id, DEFAULT_PATTERN)

# ── Static store data ────────────────────────────────────────
STORES = [
    ("QuickMart Connaught Place",  "Delhi",     "Central",   3.0,  10000, 15),
    ("QuickMart Lajpat Nagar",     "Delhi",     "South",     2.5,  8000,  12),
    ("QuickMart Koramangala",      "Bengaluru", "South",     2.0,  7000,  5),   # Store 3 — PROBLEM
    ("QuickMart Sector 18 Noida",  "Noida",     "Sector 18", 3.0,  9000,  14),
    ("QuickMart Indiranagar",      "Bengaluru", "East",      2.5,  8500,  13),
    ("QuickMart Dwarka",           "Delhi",     "West",      3.5,  9500,  14),
    ("QuickMart Sector 56 Gurugram","Gurugram", "Sector 56", 3.0,  9000,  13),  # Store 7 — HIGH DISC
    ("QuickMart Malviya Nagar",    "Delhi",     "South",     2.5,  8000,  12),
    ("QuickMart Whitefield",       "Bengaluru", "East",      3.0,  9000,  13),
    ("QuickMart Cyber City",       "Gurugram",  "DLF",       2.5,  8500,  13),
]

# ── Realistic Indian quick-commerce products ─────────────────
PRODUCTS = [
    # name, category, subcategory, brand, price, cost, shelf_days, is_perishable
    ("Amul Full Cream Milk 1L",        "Dairy",            "Milk",          "Amul",       68,  52,   3,  1),
    ("Amul Butter 500g",               "Dairy",            "Butter",        "Amul",      260, 200,  60,  0),
    ("Mother Dairy Curd 500g",         "Dairy",            "Curd",          "Mother Dairy",50,  38,   5,  1),
    ("Amul Paneer 200g",               "Dairy",            "Paneer",        "Amul",       90,  68,   7,  1),
    ("Amul Cheese Slices 750g",        "Dairy",            "Cheese",        "Amul",      385, 295,  90,  0),
    ("Amul Taaza Milk 500ml",          "Dairy",            "Milk",          "Amul",       30,  22,   3,  1),
    ("Epigamia Greek Yogurt 90g",      "Dairy",            "Yogurt",        "Epigamia",   55,  38,  14,  1),
    ("Amul Kool Milk 200ml",           "Dairy",            "Flavored Milk", "Amul",       30,  20,  30,  0),
    ("Tomatoes (1 kg)",                "Fruits & Veggies", "Vegetables",    "Fresh",      40,  25,   7,  1),
    ("Onions (1 kg)",                  "Fruits & Veggies", "Vegetables",    "Fresh",      35,  22,  14,  0),
    ("Potatoes (1 kg)",                "Fruits & Veggies", "Vegetables",    "Fresh",      30,  18,  21,  0),
    ("Bananas (Dozen)",                "Fruits & Veggies", "Fruits",        "Fresh",      50,  32,   5,  1),
    ("Green Capsicum 500g",            "Fruits & Veggies", "Vegetables",    "Fresh",      45,  28,   5,  1),
    ("Apples (1 kg)",                  "Fruits & Veggies", "Fruits",        "Shimla Fresh",140,  98,  14,  1),
    ("Spinach 250g",                   "Fruits & Veggies", "Vegetables",    "Fresh",      25,  14,   3,  1),
    ("Coca-Cola 2L",                   "Beverages",        "Soft Drinks",   "Coca-Cola",  95,  65, 180,  0),
    ("Pepsi 2L",                       "Beverages",        "Soft Drinks",   "PepsiCo",    90,  62, 180,  0),
    ("Bisleri Water 1L",               "Beverages",        "Water",         "Bisleri",    20,  10, 365,  0),
    ("Real Orange Juice 1L",           "Beverages",        "Juices",        "Dabur",     120,  85,  90,  0),
    ("Red Bull 250ml",                 "Beverages",        "Energy Drinks", "Red Bull",  125,  90, 365,  0),
    ("Nescafe Classic 50g",            "Beverages",        "Coffee",        "Nestle",    195, 140, 180,  0),
    ("Tata Tea Premium 500g",          "Beverages",        "Tea",           "Tata",      185, 128, 365,  0),
    ("Frooti 600ml",                   "Beverages",        "Juices",        "Parle Agro", 45,  28, 120,  0),
    ("Lays Classic Salted 26g",        "Snacks",           "Chips",         "PepsiCo",    20,  12,  90,  0),
    ("Kurkure Masala Munch 90g",       "Snacks",           "Puffed Snacks", "PepsiCo",    30,  18,  90,  0),
    ("Parle-G Original 800g",          "Snacks",           "Biscuits",      "Parle",      55,  35, 180,  0),
    ("Britannia Good Day 216g",        "Snacks",           "Biscuits",      "Britannia",  45,  28, 180,  0),
    ("Maggi Noodles 420g (6-pack)",    "Snacks",           "Noodles",       "Nestle",     99,  68, 180,  0),
    ("Haldiram Bhujia 400g",           "Snacks",           "Namkeen",       "Haldiram",   90,  60, 120,  0),
    ("Cadbury Dairy Milk 90g",         "Snacks",           "Chocolates",    "Mondelez",   85,  55, 180,  0),
    ("Kit Kat 4-Finger 41.5g",         "Snacks",           "Chocolates",    "Nestle",     50,  32, 180,  0),
    ("Hide & Seek Fab Vanilla 100g",   "Snacks",           "Biscuits",      "Parle",      45,  28, 180,  0),
    ("Lay's Wafer 52g",                "Snacks",           "Chips",         "PepsiCo",    30,  18,  90,  0),
    ("Dove Soap 75g (3-pack)",         "Personal Care",    "Soap",          "HUL",       120,  82, 365,  0),
    ("Colgate Strong Teeth 300g",      "Personal Care",    "Toothpaste",    "Colgate",   112,  74, 365,  0),
    ("Head & Shoulders 340ml",         "Personal Care",    "Shampoo",       "P&G",       310, 218, 365,  0),
    ("Nivea Body Lotion 400ml",        "Personal Care",    "Skin Care",     "Nivea",     290, 195, 365,  0),
    ("Lifebuoy Handwash 215ml",        "Personal Care",    "Handwash",      "HUL",        95,  62, 365,  0),
    ("Gillette Vector Plus Razor",     "Personal Care",    "Grooming",      "P&G",       145,  95, 1095, 0),
    ("Always Dry Regular 30-pack",     "Personal Care",    "Feminine Care", "P&G",       175, 118, 1095, 0),
    ("Surf Excel Easy Wash 1kg",       "Household",        "Detergent",     "HUL",       175, 120, 730,  0),
    ("Vim Bar 155g (3-pack)",          "Household",        "Dishwash",      "HUL",        60,  38, 730,  0),
    ("Dettol Original 500ml",          "Household",        "Disinfectant",  "Reckitt",   220, 150, 730,  0),
    ("Colin Glass Cleaner 500ml",      "Household",        "Cleaner",       "Reckitt",   135,  88, 365,  0),
    ("Scotch-Brite Scrubber 3-pack",   "Household",        "Cleaning Tools","3M",         55,  32, 730,  0),
    ("Harpic Power Plus 1L",           "Household",        "Cleaner",       "Reckitt",   165, 108, 730,  0),
    ("Britannia Brown Bread 400g",     "Bakery & Eggs",    "Bread",         "Britannia",  45,  28,   7,  1),
    ("Eggs Tray of 30",                "Bakery & Eggs",    "Eggs",          "Country Fresh",165, 118, 21, 1),
    ("Modern White Bread 400g",        "Bakery & Eggs",    "Bread",         "Modern",     40,  25,   7,  1),
    ("Aashirvaad Atta 5kg",            "Staples",          "Flour",         "ITC",       285, 210, 180,  0),
    ("India Gate Basmati Rice 1kg",    "Staples",          "Rice",          "KRBL",      155, 110, 365,  0),
    ("Tata Salt 1kg",                  "Staples",          "Salt",          "Tata",       25,  14, 730,  0),
    ("Fortune Sunflower Oil 1L",       "Staples",          "Oil",           "Adani Wilmar",145, 105, 365, 0),
    ("Tata Sugar 1kg",                 "Staples",          "Sugar",         "Tata",       48,  32, 365,  0),
    ("MDH Garam Masala 100g",          "Staples",          "Spices",        "MDH",        85,  55, 365,  0),
    ("Dabur Honey 500g",               "Staples",          "Condiments",    "Dabur",     280, 195, 730,  0),
    ("Kissan Mixed Fruit Jam 500g",    "Staples",          "Condiments",    "HUL",       130,  88, 365,  0),
    ("Maggi Hot Sweet Ketchup 500g",   "Staples",          "Condiments",    "Nestle",     90,  58, 365,  0),
    ("Lipton Green Tea 25 bags",       "Beverages",        "Tea",           "HUL",        95,  62, 365,  0),
    ("Amul Gold Milk 500ml",           "Dairy",            "Milk",          "Amul",       32,  24,   3,  1),
    ("Bournvita 500g",                 "Beverages",        "Health Drinks", "Mondelez",  320, 228, 365,  0),
]

# ── Helpers ──────────────────────────────────────────────────
def rand_date(start: date, end: date) -> date:
    return start + timedelta(days=random.randint(0, (end - start).days))

def rand_dt(start: date, end: date) -> datetime:
    """Random datetime with realistic hour distribution (peak at 9AM, 1PM, 8PM)."""
    d = rand_date(start, end)
    # Weighted hour bins: morning 7-10, afternoon 12-14, evening 19-22
    hour_weights = [1,1,0,0,0,0,1,3,5,4,3,2,4,4,3,2,2,3,4,6,6,4,2,1]
    hour = random.choices(range(24), weights=hour_weights)[0]
    minute = random.randint(0, 59)
    return datetime(d.year, d.month, d.day, hour, minute)

def batch_insert(cursor, table, columns, rows, batch=500):
    if not rows:
        return
    placeholders = ", ".join(["%s"] * len(columns))
    col_str = ", ".join(columns)
    sql = f"INSERT INTO {table} ({col_str}) VALUES ({placeholders})"
    for i in range(0, len(rows), batch):
        cursor.executemany(sql, rows[i:i + batch])

# ── Main generation ──────────────────────────────────────────
def main():
    print("=" * 60)
    print("  Quick-Commerce Synthetic Data Generator")
    print("=" * 60)
    confirm = input("\n[!] This will DROP and recreate all tables. Continue? (y/n): ")
    if confirm.lower() != 'y':
        print("Aborted.")
        return

    conn = mysql.connector.connect(**DB_CONFIG)
    conn.autocommit = False
    cur  = conn.cursor()

    # ── 1. STORES ────────────────────────────────────────────
    print("\n[1/8] Inserting stores...")
    store_rows = []
    for i, (name, city, zone, radius, storage, riders) in enumerate(STORES, 1):
        open_date = date(2024, random.randint(1, 6), random.randint(1, 28))
        store_rows.append((name, city, zone, open_date, "Dark Store", radius, storage, riders))
    batch_insert(cur, "stores",
        ["store_name","city","zone","opening_date","store_type",
         "delivery_radius_km","storage_capacity","rider_capacity"],
        store_rows)
    conn.commit()
    num_stores = len(STORES)
    print(f"   ✓ {num_stores} stores inserted")

    # ── 2. CUSTOMERS ─────────────────────────────────────────
    print("[2/8] Generating customers...")
    cities_zones = {
        "Delhi":     ["Central", "South", "West", "North", "East"],
        "Noida":     ["Sector 18", "Sector 62", "Sector 137"],
        "Bengaluru": ["South", "East", "North", "Whitefield"],
        "Gurugram":  ["Sector 56", "DLF", "Sector 14"],
    }
    segments   = ["New","Regular","Regular","Regular","Premium","At-Risk"]
    age_groups = ["18-25","18-25","26-35","26-35","26-35","36-50","50+"]
    channels   = ["Organic","Organic","Paid Ads","Referral","Referral","Influencer"]

    cust_rows = []
    for _ in range(NUM_CUSTOMERS):
        city = random.choice(list(cities_zones.keys()))
        zone = random.choice(cities_zones[city])
        signup = rand_date(date(2024, 1, 1), date(2024, 12, 31))
        cust_rows.append((
            signup, city, zone,
            random.choice(age_groups),
            random.choice(segments),
            random.choice(channels),
        ))
    batch_insert(cur, "customers",
        ["signup_date","city","zone","age_group","customer_segment","acquisition_channel"],
        cust_rows)
    conn.commit()
    print(f"   ✓ {NUM_CUSTOMERS} customers inserted")

    # ── 3. PRODUCTS ──────────────────────────────────────────
    print("[3/8] Inserting products...")
    prod_rows = [
        (name, cat, subcat, brand, price, cost, shelf, perishable)
        for name, cat, subcat, brand, price, cost, shelf, perishable in PRODUCTS
    ]
    batch_insert(cur, "products",
        ["product_name","category","subcategory","brand",
         "unit_price","unit_cost","shelf_life_days","is_perishable"],
        prod_rows)
    conn.commit()
    num_products = len(PRODUCTS)
    print(f"   ✓ {num_products} products inserted")

    # ── 4. ORDERS ────────────────────────────────────────────
    print("[4/8] Generating orders...")

    # Build weighted store list
    store_ids = list(range(1, num_stores + 1))
    weights   = [pat(sid)["weight"] for sid in store_ids]
    cancel_reasons = [
        "Out of stock", "Long wait time", "Changed my mind",
        "Duplicate order", "App error", "Payment issue",
    ]
    payment_methods = ["UPI","UPI","UPI","Card","Card","COD","Wallet"]

    order_rows = []
    # Store 3 gets declining orders in March (last month) — embed the pattern
    for i in range(NUM_ORDERS):
        store_id  = random.choices(store_ids, weights=weights)[0]
        customer_id = random.randint(1, NUM_CUSTOMERS)
        p = pat(store_id)

        # Store 3: reduce order volume in March (declining trend)
        order_dt = rand_dt(START_DATE, END_DATE)
        if store_id == 3 and order_dt.month == 3 and random.random() < 0.40:
            continue  # drop 40% of March orders for store 3

        status = "Delivered"
        cancel_reason = None
        actual_del = None

        if random.random() < p["cancel_rate"]:
            status = random.choice(["Cancelled", "Returned"])
            cancel_reason = random.choice(cancel_reasons)
        elif random.random() < 0.02:
            status = "Pending"
        else:
            actual_del = random.randint(*p["del_range"])

        disc_pct  = random.uniform(*p["disc_range"])
        subtotal  = round(random.uniform(80, 900), 2)
        discount  = round(subtotal * disc_pct, 2)
        del_fee   = 0.0 if subtotal > 199 else round(random.uniform(10, 30), 2)
        total     = round(subtotal - discount + del_fee, 2)

        order_rows.append((
            customer_id, store_id, order_dt,
            status, random.choice(payment_methods),
            subtotal, discount, del_fee, total,
            random.randint(10, 20), actual_del, cancel_reason,
        ))

    batch_insert(cur, "orders",
        ["customer_id","store_id","order_datetime","order_status","payment_method",
         "subtotal","discount_amount","delivery_fee","total_amount",
         "estimated_delivery_min","actual_delivery_min","cancellation_reason"],
        order_rows)
    conn.commit()
    actual_orders = len(order_rows)
    print(f"   ✓ {actual_orders} orders inserted")

    # ── 5. ORDER_ITEMS ────────────────────────────────────────
    print("[5/8] Generating order items...")
    cur.execute("SELECT order_id, store_id FROM orders")
    all_orders = cur.fetchall()

    item_rows = []
    for order_id, store_id in all_orders:
        num_items = random.choices([1,2,3,4], weights=[30,40,20,10])[0]
        chosen_products = random.sample(range(1, num_products + 1), min(num_items, num_products))
        for pid in chosen_products:
            # Fetch product price from PRODUCTS list (0-indexed, pid-1)
            _, _, _, _, price, _, _, _ = PRODUCTS[pid - 1]
            qty   = random.randint(1, 3)
            disc  = round(price * random.uniform(0, 0.08), 2)
            rev   = round((price - disc) * qty, 2)
            item_rows.append((order_id, pid, qty, price, disc, rev))

    batch_insert(cur, "order_items",
        ["order_id","product_id","quantity","unit_price","discount_amount","item_revenue"],
        item_rows)
    conn.commit()
    print(f"   ✓ {len(item_rows)} order items inserted")

    # ── 6. INVENTORY ─────────────────────────────────────────
    print("[6/8] Generating inventory records (this may take ~10 seconds)...")
    inv_rows = []
    date_range = [START_DATE + timedelta(days=d) for d in range((END_DATE - START_DATE).days + 1)]

    for store_id in store_ids:
        p = pat(store_id)
        for pid in range(1, num_products + 1):
            opening = random.randint(50, 200)
            for rec_date in date_range:
                stockout = 1 if random.random() < p["stockout_prob"] else 0
                received = random.randint(0, 30) if opening < 30 else 0
                sold     = random.randint(1, 15) if not stockout else 0
                damaged  = random.randint(0, 2)
                closing  = max(0, opening + received - sold - damaged)
                inv_rows.append((
                    store_id, pid, rec_date,
                    opening, received, sold, damaged, closing,
                    20, stockout,
                ))
                opening = closing

    batch_insert(cur, "inventory",
        ["store_id","product_id","record_date","opening_stock","received_stock",
         "units_sold","damaged_units","closing_stock","reorder_level","stockout_flag"],
        inv_rows, batch=1000)
    conn.commit()
    print(f"   ✓ {len(inv_rows)} inventory records inserted")

    # ── 7. DELIVERIES ────────────────────────────────────────
    print("[7/8] Generating deliveries...")
    cur.execute("SELECT order_id, store_id, order_datetime, actual_delivery_min FROM orders WHERE order_status IN ('Delivered','Returned')")
    delivered_orders = cur.fetchall()

    del_rows = []
    for order_id, store_id, order_dt, del_min in delivered_orders:
        p = pat(store_id)
        del_min   = del_min or random.randint(*p["del_range"])
        delay     = 1 if del_min > 20 else 0
        distance  = round(random.uniform(0.5, pat(store_id)["del_range"][1] / 10), 2)
        rider_id  = random.randint(1, STORES[store_id - 1][5])
        assigned  = order_dt + timedelta(minutes=2)
        pickup    = assigned + timedelta(minutes=random.randint(3, 8))
        delivered = pickup + timedelta(minutes=del_min)
        status    = "Delayed" if delay else "On-Time"
        del_rows.append((
            order_id, rider_id,
            assigned, pickup, delivered,
            distance, del_min, status, delay,
        ))

    batch_insert(cur, "deliveries",
        ["order_id","rider_id","assigned_datetime","pickup_datetime","delivered_datetime",
         "delivery_distance_km","delivery_time_min","delivery_status","delay_flag"],
        del_rows)
    conn.commit()
    print(f"   ✓ {len(del_rows)} delivery records inserted")

    # ── 8. CUSTOMER_FEEDBACK ──────────────────────────────────
    print("[8/8] Generating customer feedback...")
    cur.execute("SELECT order_id, customer_id, store_id, order_datetime FROM orders WHERE order_status = 'Delivered'")
    delivered = cur.fetchall()

    fb_categories = ["Delivery", "Product Quality", "App Experience", "Price"]
    pos_texts = [
        "Really fast delivery, impressed!",
        "Products were fresh and well packed.",
        "Great experience, will order again.",
        "Delivery on time, very happy.",
        "Exactly what I ordered. Thank you!",
    ]
    neu_texts = [
        "Delivery was okay, nothing special.",
        "Products were fine.",
        "Average experience overall.",
        "Could be better but acceptable.",
    ]
    neg_texts = [
        "Delivery took way too long.",
        "Item was out of stock and I was not informed.",
        "Poor quality product received.",
        "Order cancelled without reason.",
        "Very disappointed, late delivery again.",
        "Rider was rude and delivery was cold.",
    ]

    fb_rows = []
    for order_id, customer_id, store_id, order_dt in delivered:
        if random.random() > 0.20:   # only 20% leave feedback
            continue
        p = pat(store_id)
        rating    = random.randint(*p["rating_range"])
        sentiment = "Positive" if rating >= 4 else ("Negative" if rating <= 2 else "Neutral")
        text      = random.choice(pos_texts if rating >= 4 else (neg_texts if rating <= 2 else neu_texts))
        fb_date   = (order_dt + timedelta(days=random.randint(0, 2))).date()
        fb_rows.append((
            order_id, customer_id, rating, text,
            fb_date, random.choice(fb_categories), sentiment,
        ))

    batch_insert(cur, "customer_feedback",
        ["order_id","customer_id","rating","feedback_text",
         "feedback_date","feedback_category","sentiment"],
        fb_rows)
    conn.commit()
    print(f"   ✓ {len(fb_rows)} feedback records inserted")

    cur.close()
    conn.close()

    print("\n" + "=" * 60)
    print("  ✅ Database seeded successfully!")
    print("=" * 60)
    print(f"  Stores    : {num_stores}")
    print(f"  Customers : {NUM_CUSTOMERS}")
    print(f"  Products  : {num_products}")
    print(f"  Orders    : {actual_orders}")
    print(f"  Items     : {len(item_rows)}")
    print(f"  Inventory : {len(inv_rows)}")
    print(f"  Deliveries: {len(del_rows)}")
    print(f"  Feedback  : {len(fb_rows)}")
    print("\n  Pattern check:")
    print("  → Store 3 (Koramangala) : high stock-outs + slow delivery")
    print("  → Store 7 (Gurugram)    : high discounts + low margin")
    print("=" * 60)


if __name__ == "__main__":
    main()
