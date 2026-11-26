# KPI Dictionary — Quick-Commerce AI Decision Intelligence System

> All KPIs are computed via SQL from the `quickcommerce_db` database.
> Agreed definitions prevent discrepancies between SQL outputs and Power BI visuals.

---

## Core Business KPIs

| KPI | Formula | Source Table(s) | Power BI Measure Name |
|---|---|---|---|
| **Total Revenue** | `SUM(total_amount)` | `orders` | `Total Revenue` |
| **Total Orders** | `COUNT(order_id)` | `orders` | `Total Orders` |
| **AOV (Avg Order Value)** | `Total Revenue / Total Orders` | `orders` | `AOV` |
| **Fulfilment Rate** | `COUNT(Delivered) / COUNT(*) × 100` | `orders` | `Fulfilment Rate %` |
| **Cancellation Rate** | `COUNT(Cancelled) / COUNT(*) × 100` | `orders` | `Cancellation Rate %` |
| **Discount Rate** | `SUM(discount_amount) / SUM(subtotal) × 100` | `orders` | `Discount Rate %` |

---

## Inventory KPIs

| KPI | Formula | Source Table(s) | Power BI Measure Name |
|---|---|---|---|
| **Stock-out Rate** | `SUM(stockout_flag) / COUNT(*) × 100` | `inventory` | `Stockout Rate %` |
| **Total Stockout Events** | `SUM(stockout_flag)` | `inventory` | `Stockout Events` |

> A `stockout_flag = 1` means the product was out of stock on that date at that store.

---

## Delivery KPIs

| KPI | Formula | Source Table(s) | Power BI Measure Name |
|---|---|---|---|
| **Avg Delivery Time** | `AVG(delivery_time_min)` | `deliveries` | `Avg Delivery Time (min)` |
| **Delay Rate** | `SUM(delay_flag) / COUNT(*) × 100` | `deliveries` | `Delay Rate %` |
| **On-time Delivery %** | `(1 - Delay Rate) × 100` | `deliveries` | `On-Time Delivery %` |

> **SLA Threshold**: `delivery_time_min > 20` is considered delayed (`delay_flag = 1`).

---

## Customer KPIs

| KPI | Formula | Source Table(s) | Power BI Measure Name |
|---|---|---|---|
| **Avg Customer Rating** | `AVG(rating)` | `customer_feedback` | `Avg Rating` |
| **Repeat Customer Rate** | `COUNT(customers with >1 order) / COUNT(active customers) × 100` | `orders`, `customers` | `Repeat Customer Rate %` |
| **Repeat Customer Revenue %** | Revenue from repeat customers / Total revenue × 100 | `orders` | `Repeat Revenue %` |

---

## Profitability KPIs

| KPI | Formula | Source Table(s) | Power BI Measure Name |
|---|---|---|---|
| **Gross Margin** | `SUM(item_revenue) - SUM(quantity × unit_cost)` | `order_items`, `products` | `Gross Margin` |
| **Gross Margin %** | `Gross Margin / SUM(item_revenue) × 100` | `order_items`, `products` | `Gross Margin %` |

---

## Benchmark Reference (Industry Standards for Quick-Commerce)

| KPI | Healthy | Warning | Critical |
|---|---|---|---|
| Stockout Rate | < 8% | 8–15% | > 15% |
| Cancellation Rate | < 5% | 5–10% | > 10% |
| Avg Delivery Time | < 15 min | 15–25 min | > 25 min |
| Delay Rate | < 12% | 12–25% | > 25% |
| Avg Customer Rating | > 4.2 | 3.5–4.2 | < 3.5 |
| Repeat Customer Rate | > 50% | 35–50% | < 35% |
| Gross Margin % | > 20% | 12–20% | < 12% |
