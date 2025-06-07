import pandas as pd

# Load the joined CSV
file_path = 'joined_cleaned_data_final/joined_magnificent7_data.csv'
df = pd.read_csv(file_path)

# Convert 'date' column to datetime format
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Add extra time features for Power BI
df['month'] = df['date'].dt.month
df['month_name'] = df['date'].dt.strftime('%B')
df['weekday_name'] = df['date'].dt.strftime('%A')
df['quarter'] = df['date'].dt.quarter

# Optional: preview changes
print(df[['date', 'month', 'month_name', 'weekday_name', 'quarter']].head())

# Save the updated file
output_path = 'joined_cleaned_data_final/joined_magnificent7_data_datetime.csv'
df.to_csv(output_path, index=False)

print("✅ Date column and time features added. File saved to:", output_path)