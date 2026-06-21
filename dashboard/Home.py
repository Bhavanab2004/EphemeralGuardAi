import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================
# Page Config
# =====================================

st.set_page_config(
    page_title="EphemeralGuard AI",
    page_icon="🛡️",
    layout="wide"
)

# =====================================
# Load Data
# =====================================

df = pd.read_csv("data/incidents_with_narratives.csv")

# =====================================
# Header
# =====================================

st.title("🛡️ EphemeralGuard AI")
st.subheader("Ephemeral Cloud & Kubernetes Risk Detection Platform")

st.markdown("---")

# =====================================
# KPI Cards
# =====================================

critical_count = len(df[df["severity"] == "Critical"])
high_count = len(df[df["severity"] == "High"])
medium_count = len(df[df["severity"] == "Medium"])

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Incidents", len(df))
col2.metric("Critical", critical_count)
col3.metric("High", high_count)
col4.metric("Medium", medium_count)

st.markdown("---")

# =====================================
# Charts Row
# =====================================

col1, col2 = st.columns(2)

with col1:

    severity_counts = df["severity"].value_counts()

    fig = px.pie(
        values=severity_counts.values,
        names=severity_counts.index,
        title="Incident Severity Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    fig2 = px.histogram(
        df,
        x="risk_score",
        nbins=20,
        title="Risk Score Distribution"
    )

    st.plotly_chart(fig2, use_container_width=True)

# =====================================
# Attack Types
# =====================================

st.subheader("Attack Type Distribution")

attack_counts = df["attack_type"].value_counts()

fig3 = px.bar(
    x=attack_counts.index,
    y=attack_counts.values,
    labels={
        "x": "Attack Type",
        "y": "Count"
    }
)

st.plotly_chart(fig3, use_container_width=True)

# =====================================
# Top Risky Users
# =====================================

st.subheader("Top Risky Users")

top_users = df["user"].value_counts().head(10)

fig4 = px.bar(
    x=top_users.index,
    y=top_users.values,
    labels={
        "x": "User",
        "y": "Incidents"
    }
)

st.plotly_chart(fig4, use_container_width=True)

# =====================================
# Incident Explorer
# =====================================

st.subheader("Incident Explorer")

incident_id = st.selectbox(
    "Select Incident",
    sorted(df["incident_id"].unique())
)

incident = df[df["incident_id"] == incident_id].iloc[0]

col1, col2 = st.columns(2)

with col1:

    st.info(f"User: {incident['user']}")

    st.write("### Severity")
    st.write(incident["severity"])

    st.write("### Risk Score")
    st.write(incident["risk_score"])

    st.write("### Attack Type")
    st.write(incident["attack_type"])

with col2:

    st.write("### MITRE ATT&CK")
    st.write(incident["mitre"])

    st.write("### Event Count")
    st.write(incident["event_count"])

    st.write("### First Seen")
    st.write(incident["first_seen"])

    st.write("### Last Seen")
    st.write(incident["last_seen"])

st.write("### Events")

st.code(incident["events"])

st.write("### Recommendation")

st.success(incident["recommendation"])

st.markdown("---")

# =====================================
# Full Incident Table
# =====================================

st.subheader("All Incidents")

st.dataframe(df, use_container_width=True)