#!/usr/bin/env python
# coding: utf-8

import os
import time
import requests
import pandas as pd

# Create folder structure (ensure they exist)
os.makedirs('01_time_series_daily', exist_ok=True)
os.makedirs('02_RSI_relative_strength_index', exist_ok=True)
os.makedirs('03_overview_fundamentals', exist_ok=True)
os.makedirs('04_SMA', exist_ok=True)
os.makedirs('cleaned_data_news_sentiment', exist_ok=True)
os.makedirs('cleaned_data_timeseries+RSI', exist_ok=True)
os.makedirs('joined_cleaned_data_timeseries+RSI', exist_ok=True)

# Your API key
api_key = '9N0W9AJ4RQ484I09'

# List of Magnificent 7 tickers
symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NVDA']

### 1. TIME_SERIES_DAILY ###
for symbol in symbols:
    filename = f'01_time_series_daily/daily_prices_{symbol.lower()}.csv'
    if os.path.exists(filename):
        print(f"✅ Skipped existing file: {filename}")
        continue
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "outputsize": "compact",
        "datatype": "json",
        "apikey": api_key
    }
    response = requests.get(url, params=params)
    data = response.json()

    if "Time Series (Daily)" in data:
        df = pd.DataFrame.from_dict(data["Time Series (Daily)"], orient="index")
        df.columns = [col.split(". ")[1] for col in df.columns]
        df.index = pd.to_datetime(df.index)
        df.sort_index(inplace=True)
        df['symbol'] = symbol
        df.to_csv(filename)
        print(f"✅ Saved: {filename}")
    else:
        print(f"❌ Failed for {symbol}: {data}")
    time.sleep(12)

### 2. RSI ###
for symbol in symbols:
    filename = f'02_RSI_relative_strength_index/rsi_{symbol.lower()}_daily.csv'
    if os.path.exists(filename):
        print(f"✅ Skipped existing file: {filename}")
        continue
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "RSI",
        "symbol": symbol,
        "interval": "daily",
        "time_period": 14,
        "series_type": "close",
        "datatype": "json",
        "apikey": api_key
    }
    response = requests.get(url, params=params)
    data = response.json()

    if "Technical Analysis: RSI" in data:
        df = pd.DataFrame.from_dict(data["Technical Analysis: RSI"], orient="index")
        df.columns = ["rsi"]
        df.index = pd.to_datetime(df.index)
        df.sort_index(inplace=True)
        df["symbol"] = symbol
        df.to_csv(filename)
        print(f"✅ Saved: {filename}")
    else:
        print(f"❌ Failed for {symbol}: {data}")
    time.sleep(12)

### 3. SMA ###
for symbol in symbols:
    filename = f'04_SMA/sma_{symbol.lower()}_daily.csv'
    if os.path.exists(filename):
        print(f"✅ Skipped existing file: {filename}")
        continue
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "SMA",
        "symbol": symbol,
        "interval": "daily",
        "time_period": 14,
        "series_type": "close",
        "datatype": "json",
        "apikey": api_key
    }
    response = requests.get(url, params=params)
    data = response.json()

    if "Technical Analysis: SMA" in data:
        df = pd.DataFrame.from_dict(data["Technical Analysis: SMA"], orient="index")
        df.columns = ["sma"]
        df.index = pd.to_datetime(df.index)
        df.sort_index(inplace=True)
        df["symbol"] = symbol
        df.to_csv(filename)
        print(f"✅ Saved: {filename}")
    else:
        print(f"❌ Failed for {symbol}: {data}")
    time.sleep(12)

# === OVERVIEW FUNDAMENTALS ===
overview_file = '03_overview_fundamentals/company_overviews_magnificent7.csv'
if not os.path.exists(overview_file):
    overview_data = []
    for symbol in symbols:
        url = 'https://www.alphavantage.co/query'
        params = {
            'function': 'OVERVIEW',
            'symbol': symbol,
            'apikey': api_key
        }

        response = requests.get(url, params=params)
        data = response.json()

        if data and 'Symbol' in data:
            overview_data.append(data)
            print(f"✅ Fetched overview for {symbol}")
        else:
            print(f"❌ Failed overview for {symbol}")
            print(data)

        time.sleep(12)

    if overview_data:
        df = pd.DataFrame(overview_data)
        df.to_csv(overview_file, index=False)
        print(f"✅ Saved: {overview_file}")
    else:
        print("❌ No overview data collected.")
else:
    print("✅ Overview data file already exists")
    time.sleep(12)