import pandas as pd

# Load original logs
cloud = pd.read_csv("data/cloud_logs.csv")

# Convert timestamp
cloud["timestamp"] = pd.to_datetime(cloud["timestamp"])

# Sort by time
cloud = cloud.sort_values("timestamp")

incidents = []
incident_id = 1

# Suspicious events
suspicious_events = [
    "LaunchCryptoMiner",
    "PrivilegeEscalationAttempt",
    "CrossAccountAccess",
    "ExposeInstancePublicly",
    "OpenSecurityGroup"
]

# Filter suspicious logs
sus = cloud[cloud["event"].isin(suspicious_events)]

# Group by user
for user in sus["user"].unique():

    user_events = sus[sus["user"] == user]

    incidents.append({
        "incident_id": incident_id,
        "user": user,
        "event_count": len(user_events),
        "events": ", ".join(user_events["event"].tolist()),
        "first_seen": user_events["timestamp"].min(),
        "last_seen": user_events["timestamp"].max()
    })

    incident_id += 1

incident_df = pd.DataFrame(incidents)

incident_df.to_csv(
    "data/incidents.csv",
    index=False
)

print(incident_df.head())
print("\nTotal Incidents:", len(incident_df))