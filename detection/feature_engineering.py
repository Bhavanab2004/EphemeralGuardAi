import pandas as pd
import os

# ==========================
# Load CSV Files
# ==========================

cloud_df = pd.read_csv("data/cloud_logs.csv")
iam_df = pd.read_csv("data/iam_logs.csv")
k8s_df = pd.read_csv("data/k8s_logs.csv")

print("Loaded CSV Files Successfully\n")

# ==========================
# Convert Timestamp
# ==========================

cloud_df["timestamp"] = pd.to_datetime(cloud_df["timestamp"])
iam_df["timestamp"] = pd.to_datetime(iam_df["timestamp"])
k8s_df["timestamp"] = pd.to_datetime(k8s_df["timestamp"])

# ==========================
# Extract Hour
# ==========================

cloud_df["hour"] = cloud_df["timestamp"].dt.hour
iam_df["hour"] = iam_df["timestamp"].dt.hour
k8s_df["hour"] = k8s_df["timestamp"].dt.hour

# ==========================
# Off-Hours Feature
# ==========================

def off_hours(hour):
    return 1 if hour < 8 or hour > 20 else 0

cloud_df["off_hours"] = cloud_df["hour"].apply(off_hours)
iam_df["off_hours"] = iam_df["hour"].apply(off_hours)
k8s_df["off_hours"] = k8s_df["hour"].apply(off_hours)

# ==========================
# Event Encoding
# ==========================

cloud_df["event_code"] = cloud_df["event"].astype("category").cat.codes
iam_df["event_code"] = iam_df["event"].astype("category").cat.codes
k8s_df["event_code"] = k8s_df["event"].astype("category").cat.codes

# ==========================
# Burst Detection
# Events occurring in same minute
# ==========================

cloud_df["minute"] = cloud_df["timestamp"].dt.floor("min")
iam_df["minute"] = iam_df["timestamp"].dt.floor("min")
k8s_df["minute"] = k8s_df["timestamp"].dt.floor("min")

cloud_burst = cloud_df.groupby("minute").size()
iam_burst = iam_df.groupby("minute").size()
k8s_burst = k8s_df.groupby("minute").size()

cloud_df["burst_count"] = cloud_df["minute"].map(cloud_burst)
iam_df["burst_count"] = iam_df["minute"].map(iam_burst)
k8s_df["burst_count"] = k8s_df["minute"].map(k8s_burst)

# ==========================
# User Frequency (Cloud)
# ==========================

cloud_user_freq = cloud_df["user"].value_counts()
cloud_df["user_frequency"] = cloud_df["user"].map(cloud_user_freq)

# ==========================
# User Frequency (IAM)
# ==========================

iam_user_freq = iam_df["user"].value_counts()
iam_df["user_frequency"] = iam_df["user"].map(iam_user_freq)

# ==========================
# Namespace Frequency (K8s)
# ==========================

namespace_freq = k8s_df["namespace"].value_counts()
k8s_df["namespace_frequency"] = k8s_df["namespace"].map(namespace_freq)

# ==========================
# Create Feature Datasets
# ==========================

cloud_features = cloud_df[
    [
        "hour",
        "off_hours",
        "event_code",
        "burst_count",
        "user_frequency"
    ]
]

iam_features = iam_df[
    [
        "hour",
        "off_hours",
        "event_code",
        "burst_count",
        "user_frequency"
    ]
]

k8s_features = k8s_df[
    [
        "hour",
        "off_hours",
        "event_code",
        "burst_count",
        "namespace_frequency"
    ]
]

# ==========================
# Save Features
# ==========================

os.makedirs("data", exist_ok=True)

cloud_features.to_csv(
    "data/cloud_features.csv",
    index=False
)

iam_features.to_csv(
    "data/iam_features.csv",
    index=False
)

k8s_features.to_csv(
    "data/k8s_features.csv",
    index=False
)

# ==========================
# Display Results
# ==========================

print("=" * 60)
print("CLOUD FEATURES")
print("=" * 60)
print(cloud_features.head())

print("\nShape:", cloud_features.shape)

print("\n" + "=" * 60)
print("IAM FEATURES")
print("=" * 60)
print(iam_features.head())

print("\nShape:", iam_features.shape)

print("\n" + "=" * 60)
print("KUBERNETES FEATURES")
print("=" * 60)
print(k8s_features.head())

print("\nShape:", k8s_features.shape)

print("\nFeature files created successfully:")
print("data/cloud_features.csv")
print("data/iam_features.csv")
print("data/k8s_features.csv")