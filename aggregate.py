"""
Silver -> Gold: Aggregate cleaned auction data into analytics tables.

Usage:
    python aggregate.py

Reads silver_auction_data.csv (produced by clean.py) and writes:
  city_sales.csv    -- total sales value and transaction count by city
  time_trend.csv    -- quarterly sales trend with QoQ growth rate
"""

import pandas as pd


# ---------------------------------------------------------------------------
# Load
# ---------------------------------------------------------------------------

def load_silver(path="silver_auction_data.csv"):
    df = pd.read_csv(path, encoding="utf-8-sig", parse_dates=["date"])
    print(f"Loaded {len(df):,} cleaned rows from {path}")
    return df


# ---------------------------------------------------------------------------
# Gold table 1: city_sales
# ---------------------------------------------------------------------------

def build_city_sales(df):
    """
    Aggregate total sales value and transaction count per city.
    Returns rows sorted by total_sales_value descending.
    """
    required = {"city", "sales_value"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns for city_sales: {missing}")

    agg = (
        df.groupby("city", as_index=False)
        .agg(
            total_sales_value=("sales_value", "sum"),
            total_transactions=("transaction_count", "sum") if "transaction_count" in df.columns else ("sales_value", "count"),
            avg_sale_value=("sales_value", "mean"),
        )
        .sort_values("total_sales_value", ascending=False)
        .reset_index(drop=True)
    )
    agg["rank"] = agg.index + 1
    agg["total_sales_value"] = agg["total_sales_value"].round(2)
    agg["avg_sale_value"] = agg["avg_sale_value"].round(2)
    return agg


# ---------------------------------------------------------------------------
# Gold table 2: time_trend
# ---------------------------------------------------------------------------

def build_time_trend(df):
    """
    Aggregate quarterly sales totals and compute quarter-over-quarter growth.
    """
    if "year_quarter" not in df.columns:
        raise ValueError("Column 'year_quarter' not found. Run clean.py first.")

    agg = (
        df.groupby("year_quarter", as_index=False)
        .agg(
            total_sales_value=("sales_value", "sum"),
            total_transactions=("transaction_count", "sum") if "transaction_count" in df.columns else ("sales_value", "count"),
        )
        .sort_values("year_quarter")
        .reset_index(drop=True)
    )

    # Quarter-over-quarter growth %
    agg["sales_qoq_pct"] = (
        agg["total_sales_value"].pct_change().mul(100).round(2)
    )
    agg["total_sales_value"] = agg["total_sales_value"].round(2)
    return agg


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    df = load_silver()

    city_sales = build_city_sales(df)
    city_sales.to_csv("city_sales.csv", index=False, encoding="utf-8-sig")
    print(f"Saved city_sales.csv  ({len(city_sales)} cities)")

    time_trend = build_time_trend(df)
    time_trend.to_csv("time_trend.csv", index=False, encoding="utf-8-sig")
    print(f"Saved time_trend.csv  ({len(time_trend)} quarters)")

    print("\nTop 5 cities by sales:")
    print(city_sales[["rank", "city", "total_sales_value"]].head().to_string(index=False))
