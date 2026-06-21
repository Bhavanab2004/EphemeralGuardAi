import pandas as pd
from sklearn.ensemble import IsolationForest

# =========================
# Load Feature Files
# =========================

cloud_features = pd.read_csv("data/cloud_features.csv")
iam_features = pd.read_csv("data/iam_features.csv")
k8s_features = pd.read_csv("data/k8s_features.csv")

# =========================
# Train Isolation Forest
# =========================

cloud_model = IsolationForest(
    contamination=0.05,
    random_state=42
)

cloud_model.fit(cloud_features)

# =========================
# Predict Anomalies
# =========================

cloud_features["anomaly"] = cloud_model.predict(cloud_features)

# Convert
# 1 = normal
# -1 = anomaly

cloud_features["anomaly"] = cloud_features["anomaly"].map(
    {1: "Normal", -1: "Anomaly"}
)

# =========================
# Save Results
# =========================

cloud_features.to_csv(
    "data/cloud_anomalies.csv",
    index=False
)

print("\nResults Saved")

print("\nAnomaly Count:")
print(cloud_features["anomaly"].value_counts())

print("\nSample Anomalies:")
print(
    cloud_features[
        cloud_features["anomaly"] == "Anomaly"
    ].head()
)