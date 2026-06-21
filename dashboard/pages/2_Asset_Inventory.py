import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("📦 Asset Inventory")

cloud = pd.read_csv("data/cloud_logs.csv")

# Filters
users = ["All"] + sorted(cloud["user"].unique().tolist())

selected_user = st.selectbox(
    "Filter by User",
    users
)

if selected_user != "All":
    cloud = cloud[
        cloud["user"] == selected_user
    ]

st.metric(
    "Total Resources",
    cloud["resource"].nunique()
)

st.metric(
    "Total Events",
    len(cloud)
)

st.dataframe(
    cloud,
    use_container_width=True
)