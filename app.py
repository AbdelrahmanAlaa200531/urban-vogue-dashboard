import os
import pandas as pd
import plotly.express as px
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Urban Vogue - Performance Analytics",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Urban Vogue - Performance Analytics Dashboard")
st.markdown("---")


# Automatic File Detection
@st.cache_data
def load_data():
  possible_files = ["Data.xlsx", "data.xlsx", "Data.xlsx.xlsx", "data.csv"]
  for fname in possible_files:
    if os.path.exists(fname):
      if fname.endswith(".csv"):
        df = pd.read_csv(fname)
      else:
        df = pd.read_excel(fname)
      df["Date"] = pd.to_datetime(df["Date"])
      return df
  return None


# Load Data Automatically or via Optional File Upload
uploaded_file = st.sidebar.file_uploader(
    "Upload Alternative File (Optional)", type=["xlsx", "csv"]
)

if uploaded_file is not None:
  if uploaded_file.name.endswith(".csv"):
    df = pd.read_csv(uploaded_file)
  else:
    df = pd.read_excel(uploaded_file)
  df["Date"] = pd.to_datetime(df["Date"])
else:
  df = load_data()

if df is None:
  st.warning(
      "⚠️ Data file not found in repository. Please make sure Data.xlsx is uploaded."
  )
  st.stop()

# Sidebar Filters
st.sidebar.header("🔍 Filters")

min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

start_date, end_date = st.sidebar.date_input(
    "Date Range",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date,
)

selected_channels = st.sidebar.multiselect(
    "Channel", options=df["Channel"].unique(), default=df["Channel"].unique()
)

selected_categories = st.sidebar.multiselect(
    "Category", options=df["Category"].unique(), default=df["Category"].unique()
)

selected_customer_types = st.sidebar.multiselect(
    "Customer Type",
    options=df["Customer Type"].unique(),
    default=df["Customer Type"].unique(),
)

# Filter Dataset
filtered_df = df[
    (df["Date"].dt.date >= start_date)
    & (df["Date"].dt.date <= end_date)
    & (df["Channel"].isin(selected_channels))
    & (df["Category"].isin(selected_categories))
    & (df["Customer Type"].isin(selected_customer_types))
]

# Key Performance Indicators (KPIs)
total_revenue = filtered_df["Revenue"].sum()
total_profit = filtered_df["Profit"].sum()
total_spend = filtered_df["Ad Spend"].sum()
total_conversions = filtered_df["Conversions"].sum()
roas = (total_revenue / total_spend) if total_spend > 0 else 0
cpa = (total_spend / total_conversions) if total_conversions > 0 else 0

# KPIs Grid
k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("Total Revenue", f"${total_revenue:,.2f}")
k2.metric("Total Profit", f"${total_profit:,.2f}")
k3.metric("Ad Spend", f"${total_spend:,.2f}")
k4.metric("ROAS", f"{roas:.2f}x")
k5.metric("Total Conversions", f"{total_conversions:,}")
k6.metric("CPA", f"${cpa:.2f}")

st.markdown("---")

# Navigation Tabs
tab1, tab2, tab3 = st.tabs([
    "📦 Sales & Collections",
    "📣 Marketing Effectiveness",
    "👥 Customer Loyalty Trends",
])

# ----------------- TAB 1: Sales & Collections -----------------
with tab1:
  st.subheader("Sales Analysis by Category & Service")
  c1, c2 = st.columns(2)

  with c1:
    cat_sales = (
        filtered_df.groupby("Category")[["Revenue", "Profit"]]
        .sum()
        .reset_index()
    )
    fig_cat = px.bar(
        cat_sales,
        x="Category",
        y=["Revenue", "Profit"],
        barmode="group",
        title="Revenue & Profit by Category",
        labels={"value": "USD ($)", "Category": "Category"},
        color_discrete_sequence=["#2b5c8f", "#25a18e"],
    )
    st.plotly_chart(fig_cat, use_container_width=True)

  with c2:
    time_sales = (
        filtered_df.groupby("Time of Day")["Revenue"].sum().reset_index()
    )
    fig_time = px.pie(
        time_sales,
        values="Revenue",
        names="Time of Day",
        title="Revenue Distribution by Time of Day",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    st.plotly_chart(fig_time, use_container_width=True)

  st.subheader("Daily Sales & Profit Trends")
  daily_trend = (
      filtered_df.groupby("Date")[["Revenue", "Profit"]].sum().reset_index()
  )
  fig_trend = px.line(
      daily_trend,
      x="Date",
      y=["Revenue", "Profit"],
      title="Daily Revenue & Profit Over Time",
      labels={"value": "USD ($)", "Date": "Date"},
      color_discrete_sequence=["#1f77b4", "#2ca02c"],
  )
  st.plotly_chart(fig_trend, use_container_width=True)

# ----------------- TAB 2: Marketing Effectiveness -----------------
with tab2:
  st.subheader("Marketing Channel Performance")

  channel_perf = (
      filtered_df.groupby("Channel")
      .agg({
          "Ad Spend": "sum",
          "Revenue": "sum",
          "Profit": "sum",
          "Conversions": "sum",
      })
      .reset_index()
  )
  channel_perf["ROAS"] = channel_perf["Revenue"] / channel_perf["Ad Spend"]
  channel_perf["CPA"] = channel_perf["Ad Spend"] / channel_perf["Conversions"]

  m1, m2 = st.columns(2)

  with m1:
    fig_chan = px.bar(
        channel_perf,
        x="Channel",
        y=["Ad Spend", "Revenue"],
        barmode="group",
        title="Ad Spend vs Revenue by Channel",
        color_discrete_sequence=["#e63946", "#457b9d"],
    )
    st.plotly_chart(fig_chan, use_container_width=True)

  with m2:
    fig_roas = px.bar(
        channel_perf,
        x="Channel",
        y="ROAS",
        title="Return on Ad Spend (ROAS) by Channel",
        text_auto=".2f",
        color="ROAS",
        color_continuous_scale="Greens",
    )
    st.plotly_chart(fig_roas, use_container_width=True)

  st.subheader("Campaign Performance Breakdown")
  st.dataframe(
      channel_perf.style.format({
          "Ad Spend": "${:,.2f}",
          "Revenue": "${:,.2f}",
          "Profit": "${:,.2f}",
          "Conversions": "{:,}",
          "ROAS": "{:.2f}x",
          "CPA": "${:.2f}",
      }),
      use_container_width=True,
  )

# ----------------- TAB 3: Customer Loyalty Trends -----------------
with tab3:
  st.subheader("Customer Loyalty Analysis (New vs Returning)")

  cust_summary = filtered_df.groupby("Customer Type").agg({
      "Revenue": ["sum", "mean"],
      "Profit": ["sum", "mean"],
      "Conversions": "sum",
      "Customer Type": "count",
  })
  cust_summary.columns = [
      "Total Revenue",
      "Avg Revenue",
      "Total Profit",
      "Avg Profit",
      "Conversions",
      "Orders Count",
  ]
  cust_summary = cust_summary.reset_index()

  l1, l2 = st.columns(2)

  with l1:
    fig_cust_pie = px.pie(
        cust_summary,
        values="Total Revenue",
        names="Customer Type",
        title="Revenue Share: New vs Returning Customers",
        hole=0.4,
        color_discrete_sequence=["#ff9f1c", "#2ec4b6"],
    )
    st.plotly_chart(fig_cust_pie, use_container_width=True)

  with l2:
    fig_cust_bar = px.bar(
        cust_summary,
        x="Customer Type",
        y=["Avg Revenue", "Avg Profit"],
        barmode="group",
        title="Average Order Revenue & Profit per Customer Type",
        labels={"value": "USD ($)"},
        color_discrete_sequence=["#3a86ff", "#8338ec"],
    )
    st.plotly_chart(fig_cust_bar, use_container_width=True)

  st.subheader("Customer Type Distribution Across Channels")
  chan_cust = (
      filtered_df.groupby(["Channel", "Customer Type"])["Revenue"]
      .sum()
      .reset_index()
  )
  fig_chan_cust = px.bar(
      chan_cust,
      x="Channel",
      y="Revenue",
      color="Customer Type",
      barmode="stack",
      title="Revenue by Channel & Customer Type",
      color_discrete_sequence=["#ff9f1c", "#2ec4b6"],
  )
  st.plotly_chart(fig_chan_cust, use_container_width=True)
