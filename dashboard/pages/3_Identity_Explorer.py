import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Identity Explorer",
    page_icon="👤",
    layout="wide"
)

st.title("👤 Identity Explorer")
st.subheader("Analyze Users, Permissions & Risk")

# =========================
# Load Data
# =========================

incidents = pd.read_csv("data/incidents_with_narratives.csv")
iam = pd.read_csv("data/iam_logs.csv")

# =========================
# User Selection
# =========================

users = sorted(
    list(
        set(incidents["user"].unique())
    )
)

selected_user = st.selectbox(
    "Select User",
    users
)

# =========================
# User Metrics
# =========================

user_incidents = incidents[
    incidents["user"] == selected_user
]

incident_count = len(user_incidents)

avg_risk = (
    user_incidents["risk_score"].mean()
    if incident_count > 0
    else 0
)

critical_count = len(
    user_incidents[
        user_incidents["severity"] == "Critical"
    ]
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Incidents",
    incident_count
)

col2.metric(
    "Average Risk",
    round(avg_risk, 2)
)

col3.metric(
    "Critical Incidents",
    critical_count
)

st.divider()

# =========================
# Attack Types
# =========================

st.subheader("Attack Types")

attack_counts = (
    user_incidents["attack_type"]
    .value_counts()
)

if len(attack_counts) > 0:

    fig = px.bar(
        x=attack_counts.index,
        y=attack_counts.values,
        labels={
            "x": "Attack Type",
            "y": "Count"
        }
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =========================
# MITRE Techniques
# =========================

st.subheader("MITRE ATT&CK Techniques")

st.dataframe(
    user_incidents[
        [
            "incident_id",
            "mitre",
            "attack_type",
            "severity"
        ]
    ],
    use_container_width=True
)

# =========================
# User Incident History
# =========================

st.subheader("Incident History")

st.dataframe(
    user_incidents[
        [
            "incident_id",
            "risk_score",
            "severity",
            "attack_type"
        ]
    ],
    use_container_width=True
)

# =========================
# IAM Activity
# =========================

st.subheader("IAM Activity")

if "user" in iam.columns:

    iam_user = iam[
        iam["user"] == selected_user
    ]

    st.metric(
        "IAM Events",
        len(iam_user)
    )

    st.dataframe(
        iam_user,
        use_container_width=True
    )

# =========================
# Blast Radius Score
# =========================

st.subheader("Blast Radius Analysis")

blast_radius = min(
    100,
    (incident_count * 10)
    + critical_count * 15
)

if blast_radius >= 80:
    risk_level = "🔴 Critical"

elif blast_radius >= 50:
    risk_level = "🟠 High"

else:
    risk_level = "🟢 Moderate"

col1, col2 = st.columns(2)

col1.metric(
    "Blast Radius Score",
    blast_radius
)

col2.metric(
    "Risk Level",
    risk_level
)

# =========================
# Recommendations
# =========================

st.subheader("Recommended Actions")

if blast_radius >= 80:

    st.error("""
    • Disable active sessions

    • Rotate credentials

    • Review IAM permissions

    • Audit cross-account access

    • Investigate recent activity
    """)

elif blast_radius >= 50:

    st.warning("""
    • Review IAM roles

    • Monitor user activity

    • Restrict unnecessary permissions
    """)

else:

    st.success("""
    • Continue monitoring

    • No immediate action required
    """)