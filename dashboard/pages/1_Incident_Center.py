import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Asset Inventory",
    page_icon="📦",
    layout="wide"
)

st.title("📦 Ephemeral Asset Inventory")
st.subheader("Cloud & Kubernetes Resource Visibility")

# =========================
# Load Data
# =========================

cloud = pd.read_csv("data/cloud_logs.csv")

# =========================
# Sidebar Filters
# =========================

st.sidebar.header("Filters")

users = ["All"] + sorted(cloud["user"].unique().tolist())
events = ["All"] + sorted(cloud["event"].unique().tolist())

selected_user = st.sidebar.selectbox(
    "User",
    users
)

selected_event = st.sidebar.selectbox(
    "Event",
    events
)

filtered = cloud.copy()

if selected_user != "All":
    filtered = filtered[
        filtered["user"] == selected_user
    ]

if selected_event != "All":
    filtered = filtered[
        filtered["event"] == selected_event
    ]

# =========================
# Metrics
# =========================

st.markdown("## Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Events",
    len(filtered)
)

col2.metric(
    "Unique Resources",
    filtered["resource"].nunique()
)

col3.metric(
    "Unique Users",
    filtered["user"].nunique()
)

col4.metric(
    "Event Types",
    filtered["event"].nunique()
)

st.divider()

# =========================
# Resource Activity
# =========================

col1, col2 = st.columns(2)

with col1:

    st.subheader("Top Resources")

    resource_counts = (
        filtered["resource"]
        .value_counts()
        .head(10)
    )

    fig1 = px.bar(
        x=resource_counts.index,
        y=resource_counts.values,
        labels={
            "x": "Resource",
            "y": "Activity Count"
        }
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

with col2:

    st.subheader("Event Distribution")

    event_counts = (
        filtered["event"]
        .value_counts()
    )

    fig2 = px.pie(
        values=event_counts.values,
        names=event_counts.index
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# =========================
# Risky Events
# =========================

st.subheader("⚠ Suspicious Cloud Activities")

suspicious_events = [
    "LaunchCryptoMiner",
    "PrivilegeEscalationAttempt",
    "CrossAccountAccess",
    "ExposeInstancePublicly",
    "OpenSecurityGroup"
]

suspicious_df = filtered[
    filtered["event"].isin(suspicious_events)
]

st.dataframe(
    suspicious_df,
    use_container_width=True
)

# =========================
# Asset Inventory Table
# =========================

st.subheader("📋 Complete Asset Inventory")

search = st.text_input(
    "Search Resource"
)

inventory = filtered.copy()

if search:
    inventory = inventory[
        inventory["resource"]
        .str.contains(
            search,
            case=False,
            na=False
        )
    ]

st.dataframe(
    inventory,
    use_container_width=True
)

# =========================
# Download CSV
# =========================

csv = inventory.to_csv(index=False)

st.download_button(
    "⬇ Download Inventory",
    csv,
    "asset_inventory.csv",
    "text/csv"
)