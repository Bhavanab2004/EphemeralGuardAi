import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Security Analytics")
st.subheader("Detection Performance & Threat Insights")

# ====================================
# Load Data
# ====================================

incidents = pd.read_csv("data/incidents_with_narratives.csv")

cloud = pd.read_csv("data/cloud_logs.csv")

# ====================================
# Metrics
# ====================================

total_events = len(cloud)
total_incidents = len(incidents)

critical = len(
    incidents[
        incidents["severity"] == "Critical"
    ]
)

high = len(
    incidents[
        incidents["severity"] == "High"
    ]
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Events",
    total_events
)

col2.metric(
    "Incidents",
    total_incidents
)

col3.metric(
    "Critical",
    critical
)

col4.metric(
    "High",
    high
)

st.divider()

# ====================================
# Noise Reduction
# ====================================

st.subheader("Noise Reduction")

noise_reduction = round(
    ((total_events - total_incidents)
    / total_events) * 100,
    2
)

st.metric(
    "Noise Reduction %",
    f"{noise_reduction}%"
)

# ====================================
# Severity Distribution
# ====================================

col1, col2 = st.columns(2)

with col1:

    severity_counts = (
        incidents["severity"]
        .value_counts()
    )

    fig = px.pie(
        values=severity_counts.values,
        names=severity_counts.index,
        title="Severity Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    attack_counts = (
        incidents["attack_type"]
        .value_counts()
    )

    fig2 = px.bar(
        x=attack_counts.index,
        y=attack_counts.values,
        title="Attack Types"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# ====================================
# MITRE Mapping
# ====================================

st.subheader("MITRE ATT&CK Coverage")

mitre_counts = (
    incidents["mitre"]
    .value_counts()
)

fig3 = px.bar(
    x=mitre_counts.index,
    y=mitre_counts.values,
    title="MITRE Techniques"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ====================================
# Risk Score Analysis
# ====================================

st.subheader("Risk Score Distribution")

fig4 = px.histogram(
    incidents,
    x="risk_score",
    nbins=20
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# ====================================
# Top Risky Users
# ====================================

st.subheader("Top Risky Users")

top_users = (
    incidents["user"]
    .value_counts()
    .head(10)
)

fig5 = px.bar(
    x=top_users.index,
    y=top_users.values,
    labels={
        "x":"User",
        "y":"Incidents"
    }
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

# ====================================
# Detection Summary
# ====================================

st.subheader("Detection Summary")

st.success(f"""
Total Events Analysed: {total_events}

Total Incidents Correlated: {total_incidents}

Noise Reduction Achieved: {noise_reduction}%

Critical Threats Identified: {critical}

MITRE Techniques Covered: {incidents['mitre'].nunique()}
""")