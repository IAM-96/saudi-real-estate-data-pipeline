"""
Bronze -> Silver: Clean and normalize raw quarterly auction CSVs.

Usage:
    python clean.py

Reads all files matching AuctionAgg*.csv in the current directory,
standardizes column names, normalizes Arabic text, parses dates,
and writes silver_auction_data.csv.
"""

import glob
import re

import pandas as pd


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def normalize_arabic(text):
    """Normalize common Arabic character variants to a canonical form."""
    if not isinstance(text, str):
        return text
    # Alef variants -> plain alef
    text = re.sub(r"[إأآٱ]", "ا", text)
    # Teh marbuta -> heh
    text = text.replace("ة", "ه")
    # Remove tatweel (kashida)
    text = text.replace("ـ", "")
    return text.strip()


def load_raw(pattern="AuctionAgg*.csv"):
    """Load all matching quarterly CSVs and combine into one DataFrame."""
    files = sorted(glob.glob(pattern))
    if not files:
        raise FileNotFoundError(f"No files matched: {pattern}")
    frames = []
    for path in files:
        df = pd.read_csv(path, encoding="utf-8-sig")
        df["source_file"] = path
        frames.append(df)
    combined = pd.concat(frames, ignore_index=True)
    print(f"Loaded {len(combined):,} rows from {len(files)} file(s).")
    return combined


# ---------------------------------------------------------------------------
# Main transform
# ---------------------------------------------------------------------------

def clean(df):
    # 1. Normalize column names
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(r"\s+", "_", regex=True)
    )

    # 2. Rename Arabic / variant headers to English keys
    rename_map = {
        "المدينة": "city",
        "city": "city",
        "التاريخ": "date",
        "date": "date",
        "قيمة_المبيعات": "sales_value",
        "sales_value": "sales_value",
        "نوع_العقار": "property_type",
        "property_type": "property_type",
        "عدد_الصفقات": "transaction_count",
        "transaction_count": "transaction_count",
    }
    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

    # 3. Normalize Arabic text in all string columns
    str_cols = df.select_dtypes(include="object").columns
    for col in str_cols:
        df[col] = df[col].apply(normalize_arabic)

    # 4. Parse dates and derive time dimensions
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df["year"] = df["date"].dt.year
        df["quarter"] = df["date"].dt.quarter
        df["year_quarter"] = df["date"].dt.to_period("Q").astype(str)

    # 5. Cast numeric columns
    for col in ["sales_value", "transaction_count"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # 6. Drop fully-empty rows and duplicates
    df = df.dropna(how="all").drop_duplicates()

    print(f"After cleaning: {len(df):,} rows retained.")
    return df


if __name__ == "__main__":
    raw = load_raw()
    cleaned = clean(raw)
    out = "silver_auction_data.csv"
    cleaned.to_csv(out, index=False, encoding="utf-8-sig")
    print(f"Saved -> {out}")
