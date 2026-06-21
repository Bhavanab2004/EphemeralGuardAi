import pandas as pd

incidents = pd.read_csv("data/incidents_scored.csv")

def generate_summary(row):

    events = row["events"]

    if "LaunchCryptoMiner" in events:
        attack = "Resource Hijacking"

        mitre = "T1496"

        recommendation = (
            "Investigate compute usage and disable compromised credentials."
        )

    elif "PrivilegeEscalationAttempt" in events:
        attack = "Privilege Escalation"

        mitre = "T1068"

        recommendation = (
            "Review IAM permissions and enforce least privilege."
        )

    elif "CrossAccountAccess" in events:
        attack = "Credential Abuse"

        mitre = "T1078"

        recommendation = (
            "Audit cross-account roles and rotate credentials."
        )

    else:
        attack = "Suspicious Activity"

        mitre = "Unknown"

        recommendation = (
            "Review incident manually."
        )

    return pd.Series([
        attack,
        mitre,
        recommendation
    ])

incidents[
    [
        "attack_type",
        "mitre",
        "recommendation"
    ]
] = incidents.apply(
    generate_summary,
    axis=1
)

incidents.to_csv(
    "data/incidents_with_narratives.csv",
    index=False
)

print(
    incidents[
        [
            "incident_id",
            "attack_type",
            "mitre"
        ]
    ].head()
)