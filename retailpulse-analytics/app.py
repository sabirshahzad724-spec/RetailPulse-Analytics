from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st
from src.analytics import load_data, quality_report, kpis, revenue_trend, ranked_breakdown, leakage_breakdown, generate_insights, scenario_revenue

st.set_page_config(page_title="RetailPulse | Retail Intelligence", page_icon="📊", layout="wide")
DATA_PATH = Path(__file__).parent / "data" / "retail_orders.csv"

st.markdown("""
<style>
.block-container {padding-top: 1.5rem; padding-bottom: 2rem;}
div[data-testid="stMetric"] {border: 1px solid rgba(128,128,128,.25); padding: 14px; border-radius: 12px;}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def get_data(path):
    return load_data(str(path))

st.title("📊 RetailPulse")
st.caption("Retail Revenue & Customer Intelligence · Portfolio analytics project")
try:
    raw = get_data(DATA_PATH)
except Exception as exc:
    st.error(f"Could not load the dataset: {exc}")
    st.stop()

with st.sidebar:
    st.header("Explore the data")
    st.caption("All filters update the KPIs, charts, insights, and export.")
    min_date = raw["order_date"].min().date()
    max_date = raw["order_date"].max().date()
    date_range = st.date_input("Order date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    cities = st.multiselect("City", sorted(raw["city"].dropna().unique()))
    categories = st.multiselect("Category", sorted(raw["category"].dropna().unique()))
    segments = st.multiselect("Customer segment", sorted(raw["customer_segment"].dropna().unique()))
    channels = st.multiselect("Sales channel", sorted(raw["sales_channel"].dropna().unique()))
    statuses = st.multiselect("Order status", sorted(raw["order_status"].dropna().unique()), default=sorted(raw["order_status"].dropna().unique()))

df = raw.copy()
if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    df = df[df["order_date"].dt.date.between(date_range[0], date_range[1])]
if cities: df = df[df["city"].isin(cities)]
if categories: df = df[df["category"].isin(categories)]
if segments: df = df[df["customer_segment"].isin(segments)]
if channels: df = df[df["sales_channel"].isin(channels)]
if statuses: df = df[df["order_status"].isin(statuses)]
else: df = df.iloc[0:0]

metrics = kpis(df)
m1,m2,m3,m4 = st.columns(4)
m1.metric("Recognized revenue", f"₹{metrics['recognized_revenue']:,.0f}")
m2.metric("Delivered orders", f"{metrics['delivered_orders']:,}")
m3.metric("Average order value", f"₹{metrics['aov']:,.0f}")
m4.metric("Unique customers", f"{metrics['unique_customers']:,}")
m5,m6,m7,m8 = st.columns(4)
m5.metric("Units in delivered orders", f"{metrics['units_sold']:,}")
m6.metric("Return rate", f"{metrics['return_rate']:.1%}")
m7.metric("Cancellation rate", f"{metrics['cancellation_rate']:.1%}")
m8.metric("Orders in selection", f"{metrics['total_orders']:,}")

if df.empty:
    st.warning("No data matches these filters. Select more values in the sidebar.")
    st.stop()

tab1,tab2,tab3,tab4 = st.tabs(["Overview", "Product & Market", "Operations", "Data Quality"])
with tab1:
    st.subheader("Revenue performance")
    trend = revenue_trend(df)
    fig = px.line(trend, x="year_month_date", y="recognized_revenue", markers=True,
                  labels={"year_month_date":"Month","recognized_revenue":"Recognized revenue (₹)"},
                  title="Monthly recognized revenue")
    st.plotly_chart(fig, use_container_width=True)
    left,right = st.columns(2)
    channel = ranked_breakdown(df, "sales_channel")
    left.plotly_chart(px.bar(channel, x="sales_channel", y="recognized_revenue", title="Revenue by sales channel",
                             labels={"sales_channel":"Channel","recognized_revenue":"Revenue (₹)"}), use_container_width=True)
    segment = ranked_breakdown(df, "customer_segment")
    right.plotly_chart(px.pie(segment, names="customer_segment", values="recognized_revenue", hole=.45,
                              title="Revenue mix by customer segment"), use_container_width=True)
    st.subheader("Decision notes")
    for item in generate_insights(df):
        st.write("• " + item)

with tab2:
    left,right = st.columns(2)
    category = ranked_breakdown(df, "category")
    left.plotly_chart(px.bar(category, x="category", y="recognized_revenue", title="Revenue by category",
                             labels={"category":"Category","recognized_revenue":"Revenue (₹)"}), use_container_width=True)
    product = ranked_breakdown(df, "product_name").head(10)
    right.plotly_chart(px.bar(product, x="recognized_revenue", y="product_name", orientation="h",
                              title="Top 10 products by recognized revenue",
                              labels={"product_name":"Product","recognized_revenue":"Revenue (₹)"}), use_container_width=True)
    city = ranked_breakdown(df, "city")
    st.plotly_chart(px.bar(city, x="city", y="recognized_revenue", title="Revenue by city",
                           labels={"city":"City","recognized_revenue":"Revenue (₹)"}), use_container_width=True)
    st.dataframe(category, use_container_width=True, hide_index=True)

with tab3:
    st.subheader("Order outcomes and revenue leakage proxy")
    leak = leakage_breakdown(df)
    st.plotly_chart(px.bar(leak, x="outcome", y="gross_sales", color="outcome",
                           title="Gross sales by order outcome",
                           labels={"outcome":"Outcome","gross_sales":"Gross sales (₹)"}), use_container_width=True)
    st.dataframe(leak, use_container_width=True, hide_index=True)
    st.caption("Returned/cancelled gross sales are a prioritization proxy; do not interpret them as accounting loss or profit.")
    st.subheader("What-if revenue scenario")
    change = st.slider("Hypothetical change in recognized revenue (%)", min_value=-20, max_value=30, value=5, step=1)
    st.metric("Scenario revenue", f"₹{scenario_revenue(df, change):,.0f}", delta=f"{change:+d}% vs current")
    st.caption("This is a simple sensitivity scenario, not a forecast. It assumes all else stays constant.")

with tab4:
    st.subheader("Dataset quality checks")
    quality = quality_report(raw)
    q1,q2,q3 = st.columns(3)
    q1.metric("Rows", f"{quality['rows']:,}")
    q2.metric("Columns", f"{quality['columns']:,}")
    q3.metric("Duplicate order IDs", f"{quality['duplicate_order_ids']:,}")
    st.json(quality)
    st.write("Missing values by column")
    missing = raw.isna().sum().rename("missing_cells").reset_index().rename(columns={"index":"column"})
    st.dataframe(missing, use_container_width=True, hide_index=True)
    st.write("Preview of filtered data")
    st.dataframe(df.head(100), use_container_width=True, hide_index=True)

st.divider()
st.subheader("Export")
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("Download filtered rows as CSV", data=csv, file_name="retailpulse_filtered_data.csv", mime="text/csv")
st.caption("Built with Python · Pandas · Plotly · Streamlit · MySQL-ready SQL scripts")
