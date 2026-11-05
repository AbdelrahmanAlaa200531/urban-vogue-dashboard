import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(
    page_title="Urban Vogue - Sales & Marketing Dashboard",
    page_icon="📊",
    layout="wide"
)

# Custom CSS Styling
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Urban Vogue - Performance Analytics Dashboard")
st.markdown("---")

# Data Loading Function
@st.cache_data
def load_data(file_path):
    df = pd.read_excel(file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

# File Upload or Default Dataset Loading
uploaded_file = st.sidebar.file_uploader("Upload Excel / CSV Data", type=["xlsx", "csv"])

if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
        df['Date'] = pd.to_datetime(df['Date'])
    else:
        df = pd.read_excel(uploaded_file)
        df['Date'] = pd.to_datetime(df['Date'])
else:
    try:
        df = load_data('Data.xlsx')
    except Exception as e:
        st.error("Please upload Data.xlsx to get started.")
        st.stop()

# Sidebar Filters
st.sidebar.header("🔍 Filters")

min_date = df['Date'].min().date()
max_date = df['Date'].max().date()

start_date, end_date = st.sidebar.date_input(
    "Date Range",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

selected_channels = st.sidebar.multiselect(
    "Channel",
    options=df['Channel'].unique(),
    default=df['Channel'].unique()
)

selected_categories = st.sidebar.multiselect(
    "Category",
    options=df['Category'].unique(),
    default=df['Category'].unique()
)

selected_customer_types = st.sidebar.multiselect(
    "Customer Type",
    options=df['Customer Type'].unique(),
    default=df['Customer Type'].unique()
)

# Filter Dataset based on user selections
filtered_df = df[
    (df['Date'].dt.date >= start_date) &
    (df['Date'].dt.date <= end_date) &
    (df['Channel'].isin(selected_channels)) &
    (df['Category'].isin(selected_categories)) &
    (df['Customer Type'].isin(selected_customer_types))
]

# Key Performance
