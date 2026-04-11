# Saudi Real Estate Data Pipeline

## 📌 Overview
This project builds an end-to-end data pipeline for analyzing Saudi real estate auction data using multiple datasets and API integration.

## 🏗️ Architecture
The pipeline follows the Medallion Architecture:

- Bronze Layer: Raw CSV data ingestion
- Silver Layer: Data cleaning, transformation, and standardization
- Gold Layer: Analytical data modeling and aggregation

## ⚙️ Technologies Used
- Python (Pandas)
- Data Cleaning & Transformation
- Data Modeling
- Microsoft Fabric (planned deployment)

## 📊 Key Insights
- Top cities by total real estate sales
- Regional distribution of auctions
- Time-series trends of real estate sales

## 🚀 Features
- Multi-file data ingestion
- Data cleaning and normalization (Arabic handling)
- Aggregated analytics tables
- Time-series analysis

## 📁 Project Structure
saudi-real-estate-data-pipeline/
│
├── data/
│   ├── raw/        # ملفات CSV الأصلية (Bronze)
│   ├── processed/  # البيانات بعد التنظيف (Silver)
│
├── notebooks/
│   └── data_pipeline.ipynb
│
│
├── outputs/        # Gold Layer (نتائج التحليل)
│   ├── city_sales.csv
│   ├── region_analysis.csv
│   └── time_trend.csv
│
├── README.md
└── requirements.txt
## 📌 Future Work
- Integrate real-time API data
- Deploy pipeline on Microsoft Fabric
- Build dashboards

## 👤 Author
Ibrahim Abkar
