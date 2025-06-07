import pandas as pd
import sqlite3
import os
import sys

# Set file paths
joined_csv = "joined_cleaned_data_final/joined_magnificent7_data_final.csv"
overview_csv = "cleaned_data_overview_fundamentals/cleaned_company_overviews.csv"
database_file = "stock_data.db"

# Determine load mode
load_overview_only = "--overview-only" in sys.argv

# Connect to SQLite
conn = sqlite3.connect(database_file)

if load_overview_only:
    # Check path
    if not os.path.exists(overview_csv):
        raise FileNotFoundError(f"Missing file: {overview_csv}")
    
    # Load and write only company overview
    df_overview = pd.read_csv(overview_csv)
    df_overview.to_sql("company_overview", conn, if_exists="replace", index=False)
    print("📊 Loaded company_overview table only.")
    
else:
    # Check both files
    if not os.path.exists(joined_csv):
        raise FileNotFoundError(f"Missing file: {joined_csv}")
    if not os.path.exists(overview_csv):
        raise FileNotFoundError(f"Missing file: {overview_csv}")

    # Load both datasets
    df_joined = pd.read_csv(joined_csv)
    df_overview = pd.read_csv(overview_csv)

    # Write both tables
    df_joined.to_sql("stock_timeseries", conn, if_exists="replace", index=False)
    df_overview.to_sql("company_overview", conn, if_exists="replace", index=False)

    print("✅ Loaded both stock_timeseries and company_overview tables.")

conn.close()