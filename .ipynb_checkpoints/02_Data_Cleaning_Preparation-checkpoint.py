#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import os

# List of the Magnificent 7 tickers
symbols = ['aapl', 'msft', 'googl', 'amzn', 'meta', 'tsla', 'nvda']

# === CLEAN DAILY PRICE FILES ===
for symbol in symbols:
    try:
        file_path = f'01_time_series_daily/daily_prices_{symbol}.csv'
        df = pd.read_csv(file_path)

        if 'Unnamed: 0' in df.columns:
            df.rename(columns={'Unnamed: 0': 'date'}, inplace=True)

        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        cols = ['open', 'high', 'low', 'close', 'volume']
        df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')
        df.replace([np.inf, -np.inf], np.nan, inplace=True)
        df.dropna(inplace=True)
        df['symbol'] = symbol.upper()

        df.to_csv(f'cleaned_{symbol}_prices.csv', index=False)
        print(f"✅ Cleaned price data saved: cleaned_{symbol}_prices.csv")

    except Exception as e:
        print(f"❌ Error cleaning price for {symbol.upper()}: {e}")

# === CLEAN RSI FILES ===
for symbol in symbols:
    try:
        file_path = f'02_RSI_relative_strength_index/rsi_{symbol}_daily.csv'
        df = pd.read_csv(file_path)

        if 'Unnamed: 0' in df.columns:
            df.rename(columns={'Unnamed: 0': 'date'}, inplace=True)

        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['rsi'] = pd.to_numeric(df['rsi'], errors='coerce')
        df.replace([np.inf, -np.inf], np.nan, inplace=True)
        df.dropna(inplace=True)
        df['symbol'] = symbol.upper()
        df.sort_values('date', inplace=True)

        df.to_csv(f'cleaned_{symbol}_rsi.csv', index=False)
        print(f"✅ Cleaned RSI saved: cleaned_{symbol}_rsi.csv")

    except Exception as e:
        print(f"❌ Error cleaning RSI for {symbol.upper()}: {e}")

# === CLEAN FUNDAMENTAL OVERVIEW FILE ===
try:
    df = pd.read_csv('03_overview_fundamentals/company_overviews_magnificent7.csv')

    # Define final selected columns
    cols_to_keep = [
        'Symbol', 'Name', 'MarketCapitalization', 'PERatio', 'PEGRatio',
        'DividendYield', 'EPS', 'RevenueTTM', 'ProfitMargin', 'ReturnOnEquityTTM',
        'Beta', 'AnalystTargetPrice', 'AnalystRatingBuy', 'AnalystRatingHold', 'AnalystRatingSell',
        'AnalystRatingStrongSell'
    ]

    # Keep only selected columns (drop the rest)
    df = df[cols_to_keep]

    # Convert appropriate columns to numeric
    cols_to_convert = [col for col in cols_to_keep if col not in ['Symbol', 'Name']]
    for col in cols_to_convert:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Drop rows with missing critical info
    df.dropna(subset=['Symbol', 'Name', 'MarketCapitalization'], inplace=True)

    # Save cleaned file
    df.to_csv('cleaned_company_overviews.csv', index=False)
    print("✅ Cleaned overview data saved.")

except Exception as e:
    print(f"❌ Error cleaning company overviews: {e}")

# === CLEAN SMA FILES ===
for symbol in symbols:
    try:
        file_path = f'04_SMA/sma_{symbol}_daily.csv'
        cleaned_path = f'cleaned_{symbol}_sma.csv'

        if os.path.exists(cleaned_path):
            print(f"🗂️ Skipped SMA for {symbol.upper()} (already exists)")
            continue

        df = pd.read_csv(file_path)

        # Reset index and rename Unnamed column to 'date'
        if 'Unnamed: 0' in df.columns:
            df.rename(columns={'Unnamed: 0': 'date'}, inplace=True)

        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['sma'] = pd.to_numeric(df['sma'], errors='coerce')
        df.dropna(inplace=True)
        df['symbol'] = symbol.upper()

        # Keep only dates between Jan 3, 2025 and May 29, 2025
        df = df[(df['date'] >= '2025-01-03') & (df['date'] <= '2025-05-29')]

        df.to_csv(cleaned_path, index=False)
        print(f"✅ Cleaned SMA for {symbol.upper()}")

    except Exception as e:
        print(f"❌ Error cleaning SMA for {symbol.upper()}: {e}")