# Saudi Real Estate Data Pipeline

## Overview

This project analyzes Saudi real estate auction data, taking raw quarterly auction extracts and aggregating them into city-level and time-trend summary tables for analysis.

## Design intent

The project is structured around a Medallion (Bronze/Silver/Gold) mindset:

- Bronze: raw quarterly auction CSV exports, as received
- Silver: cleaning, standardization, and Arabic-text normalization
- Gold: aggregated analytics tables (city sales, time trends)

## What's in this repo today

- `AuctionAggQuarterElectronic Quarter1-4 2025*.csv` — raw quarterly auction data (Bronze)
- `city_sales.csv` — aggregated sales by city (Gold)
- `time_trend.csv` — time-series sales trend (Gold)

The cleaning/transformation code and notebooks that produce the Gold tables are still being organized and will be added to this repo.

## Technologies

- Python (Pandas)
- Planned: Microsoft Fabric for orchestration and deployment

## Key insights

- Top cities by total real estate sales
- Time-series trends of real estate sales

## Future work

- Publish the data-cleaning/transformation notebook
- Add a requirements.txt and reproducible pipeline script
- Deploy on Microsoft Fabric
- Build dashboards in Power BI

## Author

Ibrahim Abakar

