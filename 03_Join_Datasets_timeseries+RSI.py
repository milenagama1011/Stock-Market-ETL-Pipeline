import os
import pandas as pd

# Define the folders
data_folder = "cleaned_data_timeseries+RSI+SMA"
output_folder = "joined_cleaned_data_final"
os.makedirs(output_folder, exist_ok=True)

# Define stock tickers
symbols = ['aapl', 'msft', 'googl', 'amzn', 'meta', 'tsla', 'nvda']

# List to collect individual joined dataframes
joined_dfs = []

for symbol in symbols:
    try:
        # Construct full file paths
        price_file = os.path.join(data_folder, f"cleaned_{symbol}_prices.csv")
        rsi_file = os.path.join(data_folder, f"cleaned_{symbol}_rsi.csv")
        sma_file = os.path.join(data_folder, f"cleaned_{symbol}_sma.csv")

        # Load CSVs
        df_price = pd.read_csv(price_file)
        df_rsi = pd.read_csv(rsi_file)
        df_sma = pd.read_csv(sma_file)

        # Ensure date columns are datetime
        df_price['date'] = pd.to_datetime(df_price['date'])
        df_rsi['date'] = pd.to_datetime(df_rsi['date'])
        df_sma['date'] = pd.to_datetime(df_sma['date'])

        # Merge them sequentially
        df_joined = pd.merge(df_price, df_rsi, on=['date', 'symbol'], how='inner')
        df_joined = pd.merge(df_joined, df_sma, on=['date', 'symbol'], how='inner')

        joined_dfs.append(df_joined)
        print(f"✅ Successfully joined data for {symbol.upper()}")

    except Exception as e:
        print(f"❌ Error joining data for {symbol.upper()}: {e}")

# Final concatenation
if joined_dfs:
    final_df = pd.concat(joined_dfs, ignore_index=True)
    output_path = os.path.join(output_folder, "joined_magnificent7_data.csv")
    final_df.to_csv(output_path, index=False)
    print(f"\n✅ Final joined data saved to: {output_path}")
else:
    print("❌ No files joined. Please check file paths and names.")