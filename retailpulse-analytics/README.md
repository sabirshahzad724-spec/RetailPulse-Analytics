# RetailPulse — Retail Revenue & Customer Intelligence

**Portfolio project | SQL + Python + Streamlit | Synthetic retail data**

RetailPulse turns raw order-level retail data into a practical decision-support dashboard. It helps a business answer:
- Which products and categories drive recognized revenue?
- Which cities, customer segments, and sales channels perform best?
- How much revenue is lost to returns/cancellations?
- Are discounts associated with stronger sales?
- What should a manager investigate next?

> Data note: `data/retail_orders.csv` is a synthetic dataset created for this portfolio project. It does not represent a real company or real customers.

## Features
- Data-quality checks: missing values, duplicate order IDs, date parsing, and numeric validation.
- KPI layer: recognized revenue, delivered orders, units sold, average order value, return rate, cancellation rate.
- Interactive filters: date range, city, category, segment, channel, and order status.
- Trend analysis by month and category / product / city / channel breakdowns.
- Revenue leakage view for returns and cancellations.
- Discount analysis and a simple scenario calculator.
- Rule-based insight generator that explains notable patterns without requiring a paid AI API.
- SQL schema and interview-style business queries for MySQL.
- CSV export of the currently filtered dataset.

## Quick start
Use Python 3.10+.

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# If PowerShell blocks activation, use:
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m streamlit run app.py
```

On macOS/Linux:
```bash
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL shown by Streamlit (usually `http://localhost:8501`).

## Project structure
```text
retailpulse-analytics/
├── app.py
├── data/retail_orders.csv
├── sql/schema.sql
├── sql/business_questions.sql
├── src/analytics.py
├── reports/README.md
├── requirements.txt
└── .gitignore
```

## KPI definitions
- **Recognized revenue:** `recognized_revenue` summed; only delivered orders count in this dataset.
- **Delivered orders:** count of rows with status `Delivered`.
- **Average order value (AOV):** recognized revenue / delivered order count.
- **Return rate:** returned orders / all orders.
- **Cancellation rate:** cancelled orders / all orders.
- **Revenue leakage proxy:** gross sales for returned + cancelled orders. This is a directional operational measure, not an accounting figure.

## How to discuss this in an interview
1. Explain why revenue is based on delivered orders instead of all placed orders.
2. Describe how the filters keep every chart and KPI consistent.
3. Show how the quality report catches duplicate IDs, missing values, and invalid dates.
4. Explain that the insight engine is transparent rule-based logic, not a generative AI model.
5. Discuss how the SQL file could be adapted to a production database and why synthetic data is used here.

## Resume bullet (use only after running and reviewing it)
**RetailPulse — Retail Revenue & Customer Intelligence Dashboard**  
Built an interactive retail analytics dashboard using Python, Pandas, Plotly, and Streamlit to monitor revenue, order outcomes, product/category performance, customer segments, and channel trends; implemented data-quality checks, SQL business queries, CSV export, and rule-based decision insights.

## Suggested next improvements
- Load data from MySQL instead of CSV.
- Add automated tests and a scheduled refresh.
- Build a Power BI version using the same KPI definitions.
- Add customer cohort / repeat-purchase analysis once customer-level purchase history is modeled carefully.
