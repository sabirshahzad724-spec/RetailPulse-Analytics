from __future__ import annotations
import pandas as pd

REQUIRED_COLUMNS = [
    "order_id", "order_date", "customer_id", "city", "customer_segment",
    "sales_channel", "product_id", "product_name", "category", "quantity",
    "unit_price", "discount_pct", "order_status", "gross_sales", "net_sales",
    "recognized_revenue"
]

def load_data(path: str) -> pd.DataFrame:
    """Load, type-cast, and enrich order-level data."""
    df = pd.read_csv(path)
    missing_columns = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    for col in ["quantity", "unit_price", "discount_pct", "gross_sales", "net_sales", "recognized_revenue"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["month"] = df["order_date"].dt.to_period("M").astype(str)
    df["year_month_date"] = df["order_date"].dt.to_period("M").dt.to_timestamp()
    return df

def quality_report(df: pd.DataFrame) -> dict:
    """Return transparent quality metrics before analysis."""
    return {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "duplicate_order_ids": int(df["order_id"].duplicated().sum()),
        "missing_cells": int(df.isna().sum().sum()),
        "invalid_dates": int(df["order_date"].isna().sum()),
        "negative_quantity_rows": int((df["quantity"] < 0).sum()),
        "unknown_status_rows": int((~df["order_status"].isin(["Delivered", "Returned", "Cancelled"])).sum()),
    }

def kpis(df: pd.DataFrame) -> dict:
    delivered = df[df["order_status"].eq("Delivered")]
    n = len(df)
    return {
        "recognized_revenue": float(df["recognized_revenue"].sum()),
        "delivered_orders": int(len(delivered)),
        "units_sold": int(delivered["quantity"].sum()),
        "aov": float(df["recognized_revenue"].sum() / len(delivered)) if len(delivered) else 0.0,
        "return_rate": float(df["order_status"].eq("Returned").sum() / n) if n else 0.0,
        "cancellation_rate": float(df["order_status"].eq("Cancelled").sum() / n) if n else 0.0,
        "total_orders": int(n),
        "unique_customers": int(df["customer_id"].nunique()),
    }

def revenue_trend(df: pd.DataFrame) -> pd.DataFrame:
    return (df.groupby("year_month_date", as_index=False)
              .agg(recognized_revenue=("recognized_revenue", "sum"),
                   orders=("order_id", "nunique"))
              .sort_values("year_month_date"))

def ranked_breakdown(df: pd.DataFrame, dimension: str) -> pd.DataFrame:
    if dimension not in df.columns:
        raise ValueError(f"Unknown dimension: {dimension}")
    return (df.groupby(dimension, dropna=False, as_index=False)
              .agg(recognized_revenue=("recognized_revenue", "sum"),
                   orders=("order_id", "nunique"),
                   units=("quantity", "sum"))
              .sort_values("recognized_revenue", ascending=False))

def leakage_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    copy = df.copy()
    copy["outcome"] = copy["order_status"].where(
        copy["order_status"].isin(["Returned", "Cancelled", "Delivered"]), "Other"
    )
    return (copy.groupby("outcome", as_index=False)
            .agg(order_count=("order_id", "nunique"),
                 gross_sales=("gross_sales", "sum"),
                 recognized_revenue=("recognized_revenue", "sum")))

def generate_insights(df: pd.DataFrame) -> list[str]:
    """Explain observable patterns with deterministic, auditable rules."""
    if df.empty:
        return ["No rows match the selected filters. Broaden the filters to see insights."]
    insights = []
    revenue = df["recognized_revenue"].sum()
    if revenue <= 0:
        insights.append("Recognized revenue is zero for this selection; inspect order statuses and filters.")
    else:
        for dim, label in [("category", "category"), ("city", "city"), ("sales_channel", "sales channel")]:
            breakdown = ranked_breakdown(df, dim)
            if len(breakdown):
                top = breakdown.iloc[0]
                share = top["recognized_revenue"] / revenue * 100
                insights.append(f"{top[dim]} is the leading {label}, contributing {share:.1f}% of recognized revenue in this selection.")
        returned = df.loc[df["order_status"].eq("Returned"), "gross_sales"].sum()
        cancelled = df.loc[df["order_status"].eq("Cancelled"), "gross_sales"].sum()
        if returned + cancelled > 0:
            insights.append(f"Returned and cancelled orders represent ₹{returned + cancelled:,.0f} in gross sales to investigate; this is a leakage proxy, not recognized revenue.")
        delivered = df[df["order_status"].eq("Delivered")]
        if not delivered.empty:
            discounted = delivered[delivered["discount_pct"] > 0]["recognized_revenue"].sum()
            full_price = delivered[delivered["discount_pct"] == 0]["recognized_revenue"].sum()
            if discounted > full_price:
                insights.append("Discounted orders contribute more recognized revenue than zero-discount orders; compare margin before increasing promotions.")
            else:
                insights.append("Zero-discount orders contribute at least as much recognized revenue as discounted orders; test whether some discounts can be reduced.")
    return insights[:5]

def scenario_revenue(df: pd.DataFrame, improvement_pct: float) -> float:
    """Estimate upside if recognized revenue improved by a user-entered percentage."""
    return float(df["recognized_revenue"].sum() * (1 + improvement_pct / 100))
