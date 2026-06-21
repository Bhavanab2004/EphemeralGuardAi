import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Attack Replay",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Attack Replay")
st.subheader("Reconstruct Ephemeral Attack Timelines")

# ==================================
# Load Data
# ==================================

incidents = pd.read_csv(
    "data/incidents_with_narratives.csv"
)

# ==================================
# Incident Selector
# ==================================

incident_id = st.selectbox(
    "Select Incident",
    incidents["incident_id"]
)

incident = incidents[
    incidents["incident_id"] == incident_id
].iloc[0]

# ==================================
# Incident Overview
# ==================================

col1, col2, col3 = st.columns(3)

col1.metric(
    "Severity",
    incident["severity"]
)

col2.metric(
    "Risk Score",
    incident["risk_score"]
)

col3.metric(
    "Attack Type",
    incident["attack_type"]
)

st.divider()

# ==================================
# Timeline
# ==================================

st.subheader("Attack Timeline")

events = [
    e.strip()
    for e in incident["events"].split(",")
]

for i, event in enumerate(events):

    st.markdown(
        f"""
### Step {i+1}

🔹 {event}

⬇
"""
    )

st.divider()

# ==================================
# MITRE
# ==================================

st.subheader("MITRE ATT&CK Mapping")

st.info(incident["mitre"])

# ==================================
# Recommendation
# ==================================

st.subheader("Recommended Response")

st.success(
    incident["recommendation"]
)

# ==================================
# Executive Summary
# ==================================

st.subheader("Executive Summary")

summary = f"""
User {incident['user']} triggered
{incident['event_count']} suspicious events.

Attack Type:
{incident['attack_type']}

Risk Score:
{incident['risk_score']}

Severity:
{incident['severity']}
"""

st.warning(summary)