import pandas as pd

incidents = pd.read_csv("data/incidents.csv")

risk_map = {
    "LaunchCryptoMiner": 95,
    "PrivilegeEscalationAttempt": 90,
    "CrossAccountAccess": 85,
    "ExposeInstancePublicly": 75,
    "OpenSecurityGroup": 70
}

def calculate_risk(events):

    score = 0

    for event in events.split(","):

        event = event.strip()

        if event in risk_map:
            score = max(score, risk_map[event])

    return score

incidents["risk_score"] = incidents["events"].apply(calculate_risk)

def severity(score):

    if score >= 90:
        return "Critical"

    elif score >= 80:
        return "High"

    elif score >= 70:
        return "Medium"

    else:
        return "Low"

incidents["severity"] = incidents["risk_score"].apply(severity)

incidents.to_csv(
    "data/incidents_scored.csv",
    index=False
)

print(incidents.head())

print("\nSeverity Distribution:\n")
print(
    incidents["severity"].value_counts()
)