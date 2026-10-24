# RetailPulse — Retail Revenue & Customer Intelligence Dashboard

[![Open Live Dashboard](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://retailpulse-analytics-gwrnh2ix8ypspr3mvqvnfq.streamlit.app/)

**An interactive retail analytics project built with Python, Pandas, Plotly, and Streamlit to explore revenue performance, customer behavior, product trends, and operational metrics.**

🔗 **Live Dashboard:** [Launch RetailPulse](https://retailpulse-analytics-gwrnh2ix8ypspr3mvqvnfq.streamlit.app/)  
💻 **GitHub Repository:** [RetailPulse-Analytics](https://github.com/sabirshahzad724-spec/RetailPulse-Analytics)

---

## 📊 Project Overview

RetailPulse is a portfolio project designed to demonstrate how raw retail order data can be transformed into interactive dashboards and actionable business insights.

The dashboard brings together revenue KPIs, product and market performance, order outcomes, and data-quality checks in one interface. Interactive filters and visualizations help users explore the dataset and investigate patterns in retail performance.

## ✨ Key Features

### 1. Revenue & Business Overview
- Key performance indicators, including recognized revenue, delivered orders, average order value, and unique customers.
- Monthly revenue trends.
- Sales channel and customer segment analysis.
- High-level business insights to support decision-making.

### 2. Product & Market Analysis
- Revenue comparison across product categories.
- Top-performing products by revenue.
- City-level revenue comparisons.
- Interactive exploration of product and market performance.

### 3. Operations Analysis
- Order outcome analysis, including delivered, returned, and cancelled orders.
- Analysis of revenue associated with different order outcomes.
- Interactive what-if revenue scenario to explore hypothetical changes in revenue.
- Scenario outputs are illustrative and are not forecasts.

### 4. Data Quality
- Checks for missing values and duplicate order IDs.
- Validation of dates, quantities, and order statuses.
- Data-quality summaries and data previews.

### 5. Interactive Analytics
- Interactive Plotly charts.
- Dashboard filters for exploring subsets of the data.
- Rule-based business insights.
- CSV export functionality.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Data processing and application logic |
| Pandas | Data cleaning, transformation, and analysis |
| Plotly | Interactive data visualizations |
| Streamlit | Dashboard interface and deployment |
| SQL / MySQL | SQL scripts and example business queries |
| Git & GitHub | Version control and project hosting |

## 🖼️ Dashboard Preview

<!-- Add the combined collage at this location in the repository. -->
![RetailPulse Dashboard Preview](retailpulse-analytics/screenshots/RetailPulse_Combined_Collage.png)

*The preview image is stored in the repository's screenshots folder.*

### Individual Dashboard Screenshots

Add your exported dashboard images to `retailpulse-analytics/screenshots/` using these filenames.

| Dashboard | Screenshot |
|---|---|
| Revenue Overview | `RetailPulse_Dashboard_1.png` |
| Product & Market | `RetailPulse_Dashboard_2.png` |
| Operations | `RetailPulse_Dashboard_3.png` |
| Data Quality | `RetailPulse_Dashboard_4.png` |

## 📈 Example Business Questions

RetailPulse can help explore questions such as:

- How does recognized revenue change over time?
- Which product categories and products contribute the most revenue?
- Which cities and sales channels perform best?
- What proportion of orders are returned or cancelled?
- What data-quality issues need attention before analysis?
- How would a hypothetical revenue increase affect the displayed scenario?

## 📂 Project Structure

```text
RetailPulse-Analytics/
├── README.md
└── retailpulse-analytics/
    ├── app.py
    ├── requirements.txt
    ├── README.md
    ├── data/
    ├── reports/
    ├── sql/
    ├── src/
    └── screenshots/
```

*The screenshot folder is where you should add the exported images. The structure above is illustrative; retain the actual files and folders in your repository.*

## 🚀 Run Locally

### Prerequisites
- Python installed on your computer.
- Git (optional, if cloning the repository).
- VS Code or another Python editor.

### 1. Clone the repository

```bash
git clone https://github.com/sabirshahzad724-spec/RetailPulse-Analytics.git
cd RetailPulse-Analytics/retailpulse-analytics
```

### 2. Create and activate a virtual environment

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can run the Python executable inside the virtual environment directly instead.

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Launch the dashboard

```bash
python -m streamlit run app.py
```

Open the local URL displayed in your terminal, usually `http://localhost:8501`.

## 🗄️ SQL Practice

The project includes SQL scripts for practicing business-oriented queries. These can be reviewed and executed in a compatible SQL environment after checking the scripts and preparing any required tables.

**Note:** The dashboard currently reads its dataset from CSV. The presence of SQL scripts does not mean the deployed dashboard is connected to a live MySQL database.

## ⚠️ Project Scope & Limitations

- **Synthetic data:** The dataset is generated for portfolio demonstration and does not represent actual customer transactions or a real company's sales.
- **CSV-based analysis:** The dashboard reads data from CSV files rather than querying a live production database.
- **SQL scripts:** SQL examples are provided separately and are not an active database integration in the dashboard.
- **Rule-based insights:** Automatically displayed insights use predefined logic and should not be described as generative AI.
- **What-if analysis:** Revenue scenarios are hypothetical calculations, not predictive models or guaranteed business outcomes.
- **Business interpretation:** Findings depend on the available synthetic data and should not be generalized to real-world retail businesses without validation.

## 🎯 Skills Demonstrated

- Data cleaning and quality validation
- Exploratory data analysis (EDA)
- KPI development and business metric interpretation
- Data aggregation and transformation with Pandas
- Interactive dashboard development
- Business-focused data visualization
- SQL query practice
- Deploying a Python analytics application

## 👤 Author

**Sabir Ali**  
Aspiring Data Analyst | Python | SQL | Power BI | Excel | Data Visualization

- **GitHub:** [sabirshahzad724-spec](https://github.com/sabirshahzad724-spec)
- **Live Project:** [RetailPulse Dashboard](https://retailpulse-analytics-gwrnh2ix8ypspr3mvqvnfq.streamlit.app/)

---

*Built as a data analytics portfolio project to practice transforming retail data into meaningful business insights.*
