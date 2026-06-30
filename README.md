# Saudi Real Estate Data Pipeline

## Overview

This project analyzes Saudi real estate auction data, taking raw quarterly auction extracts and aggregating them into city-level and time-trend summary tables for analysis.

## Architecture

```mermaid
flowchart TD
    subgraph Bronze["🥉 Bronze — Raw Data"]
        B1[AuctionAgg Q1 2025.csv]
        B2[AuctionAgg Q2 2025.csv]
        B3[AuctionAgg Q3 2025.csv]
        B4[AuctionAgg Q4 2025.csv]
    end

    subgraph Silver["🥈 Silver — Cleaned Data"]
        S1[silver_auction_data.csv]
    end

    subgraph Gold["🥇 Gold — Analytics Tables"]
        G1[city_sales.csv]
        G2[time_trend.csv]
    end

    subgraph Analysis["📊 Analysis"]
        A1[Power BI Dashboards]
    end

    B1 & B2 & B3 & B4 --> |clean.py| S1
    S1 --> |aggregate.py| G1 & G2
    G1 & G2 --> A1
```

## Design intent

The project is structured around a Medallion (Bronze/Silver/Gold) mindset:

- Bronze: raw quarterly auction CSV exports, as received
- Silver: cleaning, standardization, and Arabic-text normalization
- Gold: aggregated analytics tables (city sales, time trends)

## What's in this repo today

- `AuctionAggQuarterElectronic Quarter1-4 2025*.csv` — raw quarterly auction data (Bronze)
- `clean.py` — cleans and normalizes raw CSVs → `silver_auction_data.csv`
- `aggregate.py` — aggregates cleaned data → `city_sales.csv` + `time_trend.csv`
- `city_sales.csv` — aggregated sales by city (Gold)
- `time_trend.csv` — time-series sales trend (Gold)
- `requirements.txt` — Python dependencies

## How to run

```bash
pip install -r requirements.txt
python clean.py       # Bronze → Silver
python aggregate.py   # Silver → Gold
```

## Technologies

- Python (Pandas)
- Planned: Microsoft Fabric for orchestration and deployment

## Key insights

- Top cities by total real estate sales
- Time-series trends of real estate sales

## Future work

- Deploy on Microsoft Fabric
- Build dashboards in Power BI

## Author

Ibrahim Abakar
