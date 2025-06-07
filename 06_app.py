import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import plotly.express as px

# Set up the page
st.set_page_config(page_title="Magnificent 7 Stock Dashboard", layout="wide")

# --- HEADER & DESCRIPTION ---
st.title("Magnificent 7 Stock Dashboard")
st.markdown("""
Welcome to the *Magnificent 7 Stock Dashboard*! This tool helps you explore and monitor key stock performance 
and fundamental insights from the top 7 tech giants. Use the sidebar to select a stock and navigate through 
price trends, RSI/SMA indicators, company fundamentals, and analyst sentiment. You can also compare financial 
metrics across companies.
""")

# --- Load Data from SQLite ---
conn = sqlite3.connect("stock_data.db")
timeseries_df = pd.read_sql("SELECT * FROM stock_timeseries", conn)
overview_df = pd.read_sql("SELECT * FROM company_overview", conn)

# --- SIDEBAR ---
symbols = timeseries_df["symbol"].unique()
selected_symbol = st.sidebar.selectbox("Choose a stock to view", symbols)

# Sidebar Info
with st.sidebar.expander("What does each variable mean?", expanded=False):
    st.markdown("""
    **Stock Metrics:**
    - `Close`: Daily closing price of the stock  
    - `RSI`: Relative Strength Index (momentum indicator)  
    - `SMA`: Simple Moving Average  

    **Company Metrics:**
    - `EPS`: Earnings per Share  
    - `MarketCapitalization`: Total company value  
    - `RevenueTTM`: Trailing 12-month revenue  
    - `DividendYield`: Dividend % per share  

    **Analyst Ratings:**
    - Target price and # of analysts rating buy/hold/sell
    """)

# --- Filter by Selected Symbol ---
filtered_data = timeseries_df[timeseries_df["symbol"] == selected_symbol]
company_info = overview_df[overview_df["Symbol"] == selected_symbol]

# --- COMPANY OVERVIEW TABLES ---

if not company_info.empty:
    # TABLE 1
    overview_data = company_info[[
        "Symbol", "Name", "MarketCapitalization", "DividendYield", "EPS", "RevenueTTM"
    ]].copy()
    overview_data["MarketCapitalization"] = pd.to_numeric(overview_data["MarketCapitalization"], errors="coerce").apply(lambda x: f"${x:,.0f}")
    overview_data["RevenueTTM"] = pd.to_numeric(overview_data["RevenueTTM"], errors="coerce").apply(lambda x: f"${x:,.0f}")
    overview_data["DividendYield"] = pd.to_numeric(overview_data["DividendYield"], errors="coerce").round(4)
    overview_data["EPS"] = pd.to_numeric(overview_data["EPS"], errors="coerce").round(2)

    st.subheader("📌 Company Overview")
    st.dataframe(
        overview_data.T.rename(columns={overview_data.index[0]: "Value"}).reset_index(names="Metric"),
        use_container_width=True, hide_index=True
    )

    # TABLE 2
    rating_data = company_info[[
        "AnalystTargetPrice", "AnalystRatingBuy", "AnalystRatingHold", "AnalystRatingSell", "AnalystRatingStrongSell"
    ]].copy()
    for col in rating_data.columns:
        rating_data[col] = pd.to_numeric(rating_data[col], errors="coerce").round(2)

    st.subheader("📊 Analyst Sentiment (Ratings)")
    st.dataframe(
        rating_data.T.rename(columns={rating_data.index[0]: "Value"}).reset_index(names="Rating Metric"),
        use_container_width=True, hide_index=True
    )
else:
    st.warning("No company overview data found for this symbol.")

# --- DAILY PRICE ---
st.markdown("## 💵 Daily Close Price")
fig_price, ax_price = plt.subplots(figsize=(10, 4))
ax_price.plot(pd.to_datetime(filtered_data["date"]), filtered_data["close"], label="Close Price", color="blue")
ax_price.set_title(f"{selected_symbol} - Daily Close Price")
ax_price.set_xlabel("Date")
ax_price.set_ylabel("Close Price ($)")
ax_price.yaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.0f}"))
ax_price.grid(True)
st.pyplot(fig_price)

# --- RSI/SMA Charts ---
if st.checkbox("📈 Show RSI and SMA Charts"):
    st.markdown("## RSI & SMA Trend")
    fig_rsi_sma, ax_rsi_sma = plt.subplots(figsize=(10, 4))
    ax_rsi_sma.plot(pd.to_datetime(filtered_data["date"]), filtered_data["rsi"], label="RSI", color="orange")
    ax_rsi_sma.plot(pd.to_datetime(filtered_data["date"]), filtered_data["sma"], label="SMA", color="green")
    ax_rsi_sma.set_title(f"{selected_symbol} - RSI and SMA Over Time")
    ax_rsi_sma.set_xlabel("Date")
    ax_rsi_sma.set_ylabel("Value")
    ax_rsi_sma.legend()
    ax_rsi_sma.grid(True)
    st.pyplot(fig_rsi_sma)

# --- COMPARATIVE METRICS ---
st.markdown("## 📊 Comparative Metrics for Magnificent 7")
timeseries_df["date"] = pd.to_datetime(timeseries_df["date"])

# Metric selection
metric_choice = st.selectbox("Choose a financial metric to compare across companies:", ["PERatio", "EPS", "MarketCapitalization"])
overview_df[metric_choice] = pd.to_numeric(overview_df[metric_choice], errors="coerce")

fig_comp_metric = px.bar(
    overview_df, x="Symbol", y=metric_choice,
    color="Symbol", title=f"{metric_choice} Comparison Across Companies"
)
st.plotly_chart(fig_comp_metric, use_container_width=True)

# --- Revenue ---
if st.checkbox("🧾 Show Revenue TTM Comparison"):
    overview_df["RevenueTTM"] = pd.to_numeric(overview_df["RevenueTTM"], errors="coerce")
    fig_revenue = px.bar(
        overview_df, x="Symbol", y="RevenueTTM",
        color="Symbol", title="Revenue (TTM) by Company",
        labels={"RevenueTTM": "Revenue ($)"}
    )
    fig_revenue.update_layout(yaxis_tickprefix="$", yaxis_tickformat=",")
    st.plotly_chart(fig_revenue, use_container_width=True)

# --- LINE CHART COMPARISON ---
st.markdown("## 📉 All Stocks Time Series Comparison")
metric_line = st.radio("Choose metric for line chart comparison:", ["close", "rsi", "sma"])
fig_all = px.line(
    timeseries_df, x="date", y=metric_line, color="symbol",
    title=f"{metric_line.upper()} Comparison Across All Stocks"
)
st.plotly_chart(fig_all, use_container_width=True)

# Close connection
conn.close()
