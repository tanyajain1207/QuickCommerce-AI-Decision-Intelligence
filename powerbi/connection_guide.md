# Power BI Connection & Dashboard Guide
## Quick-Commerce AI Decision Intelligence System

---

## Step 1 — Install MySQL ODBC Connector (One-time)

1. Download **MySQL Connector/ODBC 8.0** (64-bit) from:  
   https://dev.mysql.com/downloads/connector/odbc/

2. Install it. Keep all defaults.

3. Restart your PC if prompted.

---

## Step 2 — Connect Power BI to MySQL

1. Open **Power BI Desktop**

2. Click **Home → Get Data → More...**

3. Search `MySQL` → Select **MySQL database** → Click **Connect**

4. Fill in:
   - **Server**: `localhost`
   - **Database**: `quickcommerce_db`

5. Click **OK** → Select **Database** authentication

6. Enter:
   - Username: `root`
   - Password: *(leave blank if XAMPP default)*

7. Click **Connect**

---

## Step 3 — Import These Tables

In the Navigator, select all 8 tables:

- [x] `customers`
- [x] `stores`
- [x] `products`
- [x] `orders`
- [x] `order_items`
- [x] `inventory`
- [x] `deliveries`
- [x] `customer_feedback`

Click **Load** (not Transform — data is already clean).

---

## Step 4 — Set Up Relationships in Power BI Model View

Go to **Model View** (left sidebar) and confirm these relationships:

| From Table | Column | → | To Table | Column |
|---|---|---|---|---|
| `orders` | `customer_id` | Many→1 | `customers` | `customer_id` |
| `orders` | `store_id` | Many→1 | `stores` | `store_id` |
| `order_items` | `order_id` | Many→1 | `orders` | `order_id` |
| `order_items` | `product_id` | Many→1 | `products` | `product_id` |
| `inventory` | `store_id` | Many→1 | `stores` | `store_id` |
| `inventory` | `product_id` | Many→1 | `products` | `product_id` |
| `deliveries` | `order_id` | Many→1 | `orders` | `order_id` |
| `customer_feedback` | `order_id` | Many→1 | `orders` | `order_id` |
| `customer_feedback` | `customer_id` | Many→1 | `customers` | `customer_id` |

Power BI usually auto-detects these. Verify they are all active (solid lines).

---

## Step 5 — DAX Measures to Create

In the `orders` table (or a dedicated `Measures` table), create these DAX measures:

```dax
Total Revenue = SUM(orders[total_amount])

Total Orders = COUNT(orders[order_id])

AOV = DIVIDE([Total Revenue], [Total Orders])

Fulfilment Rate % = 
DIVIDE(
    COUNTROWS(FILTER(orders, orders[order_status] = "Delivered")),
    [Total Orders]
) * 100

Cancellation Rate % = 
DIVIDE(
    COUNTROWS(FILTER(orders, orders[order_status] = "Cancelled")),
    [Total Orders]
) * 100

Discount Rate % = 
DIVIDE(SUM(orders[discount_amount]), SUM(orders[subtotal])) * 100

Stockout Rate % = 
DIVIDE(SUM(inventory[stockout_flag]), COUNTROWS(inventory)) * 100

Avg Delivery Time (min) = AVERAGE(deliveries[delivery_time_min])

Delay Rate % = 
DIVIDE(SUM(deliveries[delay_flag]), COUNTROWS(deliveries)) * 100

On-Time Delivery % = 100 - [Delay Rate %]

Gross Margin = 
SUMX(
    order_items,
    order_items[item_revenue] - (order_items[quantity] * RELATED(products[unit_cost]))
)

Gross Margin % = DIVIDE([Gross Margin], SUMX(order_items, order_items[item_revenue])) * 100

Avg Rating = AVERAGE(customer_feedback[rating])
```

---

## Step 6 — Build the MVP Dashboard (3 Pages)

### Page 1 — Executive Overview

**Top Row — KPI Cards** (8 cards):
- Total Revenue
- Total Orders
- AOV
- Fulfilment Rate %
- Stockout Rate %
- Cancellation Rate %
- Avg Delivery Time
- Gross Margin %

**Charts:**
1. **Line Chart** — Revenue by Month (`orders[order_datetime]` → Month on X, `Total Revenue` on Y)
2. **Bar Chart** — Top/Bottom Stores (`stores[store_name]` on Y, `Total Revenue` on X) — sort descending
3. **Donut Chart** — Order Status breakdown (`orders[order_status]`, Count)
4. **Scatter Plot** — Stockout Rate vs Revenue by Store (shows the Store 3 problem instantly)

**Slicers (top of page):**
- Date range (from `orders[order_datetime]`)
- City (from `stores[city]`)
- Store (from `stores[store_name]`)

---

### Page 2 — Store Intelligence (Drill-Down)

**Filter/Slicer**: Store selector

**KPI Cards** for selected store:
- Revenue, Orders, AOV, Cancellation %, Stockout %, Avg Delivery Time, Avg Rating

**Charts:**
1. **Column Chart** — Monthly Revenue for selected store
2. **Gauge** — Delivery time vs 15-min SLA target
3. **Bar Chart** — Top stockout products for selected store
4. **Table** — Monthly KPIs side-by-side (Month | Revenue | Stockout % | Delay % | Cancellation %)

**Conditional formatting tip**:  
Color stockout_rate_pct RED if > 15%, AMBER if 8–15%, GREEN if < 8%.

---

### Page 3 — Product & Inventory

**Charts:**
1. **Bar Chart** — Top 10 Products by Revenue
2. **Bar Chart** — Top 10 Products by Stockout Events
3. **Scatter Plot** — Revenue vs Gross Margin % (reveals high-sales, low-margin products)
4. **Table** — Product, Category, Units Sold, Revenue, Margin % — with conditional color on Margin %

---

## Step 7 — Adding AI Insight Text (MVP approach)

Since Power BI cannot call Gemini directly in the MVP, use this workflow:

1. Run `python ai/insights.py 3` in your terminal
2. Open the generated `store_3_insight.json`
3. Copy the `ai_insight` text
4. In Power BI: Insert → **Text Box** on Page 2 → Paste the insight text
5. Style it with a colored border box (makes it look like a live AI panel)

**For the viva demo**, run the script live in a terminal window alongside Power BI —  
it shows the real-time AI generation which is visually impressive.

---

## Viva Demo Flow

```
1. Open Power BI → Page 1 (Executive Overview)
   → Show that Store 3 is the worst performer on the scatter plot

2. Click Store 3 slicer → Switch to Page 2 (Store Intelligence)
   → Show declining revenue, high stockout rate, slow delivery

3. Open terminal → Run: python ai/insights.py 3
   → AI reads MySQL data and generates the business explanation in real time

4. Read/paste AI insight into Power BI text box

5. Tell panel: "SQL computes the numbers. Gemini interprets and recommends.
   The LLM never touches raw data — this prevents hallucination."
```

---

## Refresh Data After Re-seeding

If you re-run `seed_data.py`, click **Home → Refresh** in Power BI to reload all tables.
