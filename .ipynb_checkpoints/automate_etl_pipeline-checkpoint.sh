#!/bin/bash
cd "$(dirname "$0")"

echo "$(date): Starting full ETL pipeline..." >> automation.log

# 1. Extract data for prices + RSI + SMA
python3 01_AlphaVantage_Extraction.py

# 2. Clean data
python3 02_Data_Cleaning_Preparation.py

# 3. Join data (price + RSI)
python3 03_Join_Datasets_timeseries+RSI.py

# 4. Convert date for Power BI
python3 04_Convert_Date_Format.py

echo "$(date): ✅ Finished full ETL pipeline run." >> automation.og
