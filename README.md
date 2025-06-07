# Magnificent 7 Stock Dashboard

This project automates the extraction, transformation, storage, and visualization of stock market data from the **Magnificent 7** (AAPL, MSFT, GOOGL, AMZN, META, TSLA, NVDA). It uses Alpha Vantage’s API, Python-based data processing, SQLite for storage, and Streamlit for interactive dashboards.

---

## Features

- **Automated ETL Pipeline**: Fetches data via Alpha Vantage API and processes it into a local SQLite database.
- **Cleaned, Joined Data**: Prepared datasets on price, RSI, and fundamentals.
- **Interactive Dashboard**:
  - Stock selector dropdown
  - Company overviews and sentiment tables
  - Close price, RSI, and SMA line graphs
  - Comparative plots for all 7 stocks
  - Revenue tracking trends
- **Monthly cron job automation** for full refreshes

---

## Technologies

- `Python`
- `Streamlit`
- `pandas`, `matplotlib`, `plotly`
- `SQLite`
- `Alpha Vantage API`
- Shell scripting & cron jobs

---

## How to Run

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/stock-market-etl-dashboard.git
   cd stock-market-etl-dashboard

---

## Project Structure
├── 01_AlphaVantage_Extraction.py
├── 02_Data_Cleaning_Preparation.py
├── 03_Join_Datasets_timeseries+RSI.py
├── 04_Convert_Date_Format.py
├── 05_Load_to_SQLite.py
├── 06_app.py
├── automate_etl_pipeline.sh
├── automate_overview_only.sh
├── final_cron_jobs.txt
├── stock_data.db
├── requirements.txt
└── README.md
