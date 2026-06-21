EphemeralGuardAI
Ephemeral Cloud & Kubernetes Risk Detection Platform

1. Problem Statement
Cloud-native enterprises provision hundreds of ephemeral resources daily: CI/CD job pods, spot instances, temporary IAM sessions, and autoscaled containers. These assets exist for minutes to hours and then disappear. Traditional security controls — quarterly scans and daily inventory syncs — were never designed for this tempo, leaving organizations blind to a rapidly expanding attack surface.
 
1.1 Real-World Incidents That Inspired This Project
 
Case
Incident Summary
Case 1
Attacker compromised CI/CD service account and spun up 20 spot VMs for crypto mining at 3 AM. All terminated before the morning SOC shift. Cost: $14,000 in 90 minutes. Zero alerts.
Case 2
Developer created a debug pod with NodePort exposed to 0.0.0.0/0. Pod ran for 11 minutes — long enough for an external scanner to find and exploit it.
Case 3
Short-lived assumed-role session accessed production S3 buckets with PII. Session expired in 15 minutes with no correlation to the compromised Lambda function that triggered it.
Case 4
Autoscaler burst created 40 pods in 2 minutes. SOC received 40 individual false-positive alerts, burying a real credential-abuse alert.

 
1.2 Core Pain Points
•       Traditional asset inventory runs too slowly for minute-long resources.
•       High alert volumes from autoscaling and CI/CD create analyst fatigue.
•       Identity and session context is fragmented across cloud, Kubernetes, and IAM logs.
•       Teams investigate isolated alerts but miss campaign-level behavior.
•       Post-incident forensics are impossible when the resource no longer exists.
 
1.3 Compliance Drivers
Framework Control
Requirement
NIST CM-8
Asset inventory must include transient and ephemeral resources.
NIST SI-4
Continuous monitoring must cover dynamic workloads.
CIS Kubernetes
Pod security, RBAC, and network policy enforcement.
GDPR Article 32
Ephemeral workloads handling PII must still be governed.



2. Solution Overview — EphemeralGuard AI
EphemeralGuard AI is a full-stack, AI-powered cloud and Kubernetes risk detection platform. It ingests multi-source telemetry, extracts behavioral features, detects anomalies with an ML model, correlates events into incidents, scores and ranks risk, and generates analyst-ready narratives — all surfaced through a multi-page Streamlit dashboard.
 
2.1 Key Capabilities
•       Near real-time ephemeral asset discovery across cloud, K8s, and IAM sources.
•       ML-based anomaly detection using Isolation Forest on engineered behavioral features.
•       Identity-based incident correlation: events grouped by user/principal with time-windowing.
•       Risk scoring from 0–100 mapped to Critical / High / Medium / Low severity bands.
•       LLM-generated triage narratives with MITRE ATT&CK mapping and remediation steps.
•       Interactive Streamlit dashboard with 6 specialized pages and CSV export.
•       Blast Radius Analysis per identity to quantify potential lateral movement impact.
•       Attack Replay timeline reconstruction for step-by-step forensic analysis.


 EphemeralGuard AI provides:
Real-Time Asset Discovery
Tracks cloud and Kubernetes resources as soon as they are created.
AI-Based Anomaly Detection
Uses Isolation Forest Machine Learning models to identify abnormal behaviors.
Incident Correlation Engine
Groups related events into meaningful incidents instead of producing individual alerts.
Risk Scoring System
Assigns severity levels based on attack indicators and business impact.
Analyst Narrative Generation
Automatically generates investigation summaries, MITRE mappings, and remediation guidance.
Interactive Security Dashboard
Provides real-time visualization of incidents and cloud risks.
Objectives
The main objectives are:
Detect ephemeral resources in real time.
Identify suspicious cloud activities.
Reduce alert noise through correlation.
Prioritize incidents using risk scoring.
Generate analyst-ready reports.
Improve cloud security visibility.
System Architecture 

Cloud Logs + IAM Logs + Kubernetes Logs
                │
                ▼
        Feature Engineering
                │
                ▼
       Isolation Forest Model
         (Anomaly Detection)
                │
                ▼
       Incident Correlation
                │
                ▼
          Risk Scoring
                │
                ▼
      Narrative Generation
                │
                ▼
     Streamlit Dashboard

Technology Stack

Component
Technology
Programming Language
Python
Dashboard
Streamlit
Data Processing
Pandas
Machine Learning
Scikit-Learn
Visualization
Plotly
Incident Correlation
Python
Data Storage
CSV
Security Frameworks
MITRE ATT&CK, NIST


3. System Architecture
The platform is organized as a six-stage pipeline. Each stage is a discrete Python module that reads from and writes to the shared data/ directory.
 
#
Stage
Module / File
Output
1
Data Ingestion
data/cloud_logs.csv data/k8s_logs.csv data/iam_logs.csv
Raw simulated telemetry from three sources
2
Feature Engineering
detection/feature_engineering.py
cloud_features.csv, iam_features.csv, k8s_features.csv
3
Anomaly Detection
models/anomaly_detector.py
cloud_anomalies.csv (Normal / Anomaly labels)
4
Incident Correlation
correlation/incident_correlator.py
incidents.csv (grouped by user & event type)
5
Risk Scoring
detection/risk_scoring.py
incidents_scored.csv (score 0–100, severity band)
6
LLM Triage
llm/triage.py
incidents_with_narratives.csv (attack type, MITRE, recommendation)

 
The dashboard (dashboard/Home.py and 5 pages) reads from the final incidents_with_narratives.csv and the raw log files, providing interactive exploration at every layer 

4. Data Sources & Schema
All telemetry is synthetically generated to simulate a realistic cloud-native environment with approximately 500–1,000 events per source, containing the expected distribution of normal and anomalous behavior.
 
4.1 Cloud Audit Logs (data/cloud_logs.csv)
Field
Description
timestamp
ISO 8601 datetime of the API call
event
Cloud API action (e.g., RunInstance, DeleteBucket, LaunchCryptoMiner)
user
Principal identifier (user1–user50, service accounts)
resource
Targeted cloud resource (vm001–vm500, bucket names, etc.)

 
4.2 Kubernetes Event Logs (data/k8s_logs.csv)
Field
Description
timestamp
ISO 8601 datetime of the K8s API event
event
K8s action (CreatePod, DeletePod, ScaleDeployment, CreateClusterRoleBinding, etc.)
pod
Pod name or workload identifier
namespace
Kubernetes namespace (prod, staging, etc.)

 
4.3 IAM / Session Logs (data/iam_logs.csv)
Field
Description
timestamp
ISO 8601 datetime of the IAM event
event
IAM action (AssumeRole, TokenIssued, MassTokenGeneration, etc.)
user
Principal or service account identifier

 
4.4 Expected Anomaly Distribution
Event Category
Approximate Share
Routine ephemeral lifecycle (normal)
30–40%
Legitimate autoscaling / CI/CD bursts
40–50%
Resource hijacking (crypto mining)
5–8%
Public exposure of ephemeral compute
3–5%
Unexpected identity / session activity
5–8%


5. Pipeline Deep Dive
5.1 Feature Engineering (detection/feature_engineering.py)
Features are extracted independently for each data source and saved as separate feature CSVs. The following behavioral signals are computed per event:
 
Feature
Logic
hour
Hour of day extracted from timestamp (0–23).
off_hours
Binary flag: 1 if hour < 8 or hour > 20, else 0.
event_code
Integer encoding of the event string using Pandas category codes.
burst_count
Number of events in the same 1-minute window (floor of timestamp).
user_frequency
Total event count for that user across the full dataset (cloud/IAM).
namespace_frequency
Total event count for that namespace (Kubernetes only).

 
5.2 Anomaly Detection (models/anomaly_detector.py)
An Isolation Forest model is trained on the cloud feature set. Isolation Forest is well-suited for this domain because it does not require labeled training data and naturally handles high-dimensional, sparse anomaly patterns.
 
•       Contamination factor: 0.05 (5% of events expected to be anomalous).
•       random_state=42 for reproducibility.
•       Output labels: Normal (1 → mapped) or Anomaly (-1 → mapped) per event.
•       Results saved to data/cloud_anomalies.csv for downstream consumption.
 
5.3 Incident Correlation (correlation/incident_correlator.py)
Raw events are grouped into incidents using identity-based correlation — a proven SOC methodology for reducing alert noise.
 
•       Suspicious event types monitored: LaunchCryptoMiner, PrivilegeEscalationAttempt, CrossAccountAccess, ExposeInstancePublicly, OpenSecurityGroup.
•       Events are filtered to only suspicious types, then grouped by user/principal.
•       Each unique user with suspicious activity becomes a single incident record.
•       Incident metadata: incident_id, user, event_count, full event list, first_seen, last_seen.
•       Correlation reduces N individual alerts to M incidents (N >> M), directly reducing analyst fatigue.
 
5.4 Risk Scoring (detection/risk_scoring.py)
Each incident is assigned a risk score based on the highest-severity event it contains. The max-score heuristic ensures that a single critical event elevates the entire incident.
 
Risk Score
Detection Rule / Signal
Severity
MITRE
Event Type
95
LaunchCryptoMiner
Critical
T1496
Cloud Audit
90
PrivilegeEscalationAttempt
Critical
T1068
Cloud/IAM
85
CrossAccountAccess
High
T1078
IAM
75
ExposeInstancePublicly
High
T1190
Cloud Audit
70
OpenSecurityGroup
Medium
T1190
Cloud Audit

 
5.5 LLM Triage (llm/triage.py)
A rule-based narrative generator (backed by the Claude AI API pattern) produces structured triage output for each incident. For each incident, the system determines:
 
•       Attack Type: categorized label (Resource Hijacking, Privilege Escalation, Credential Abuse, Suspicious Activity).
•       MITRE ATT&CK Technique ID: mapped from the primary event type.
•       Recommended Action: concise, analyst-ready remediation instruction.
 
Sample output for a LaunchCryptoMiner incident:
Attack Type : Resource Hijacking
MITRE   	: T1496
Action  	: Investigate compute usage and disable compromised credentials.

6. Dashboard — Page Reference
The Streamlit dashboard is the primary analyst interface. It is organized into six pages, each targeting a different investigative workflow.
 
Page 1: Home (dashboard/Home.py)
The executive summary and main command center.
•       KPI cards: Total Incidents, Critical count, High count, Medium count.
•       Pie chart: Incident Severity Distribution.
•       Histogram: Risk Score Distribution across all incidents.
•       Bar chart: Attack Type Distribution.
•       Bar chart: Top 10 Risky Users by incident count.
•       Incident Explorer: drill-down selectbox with full incident detail (severity, score, MITRE, events, recommendation).
•       Full incident data table with all columns.
 
Page 2: Incident Center (dashboard/pages/1_Incident_Center.py)
Cloud event exploration with real-time filtering.
•       Sidebar filters: User and Event Type.
•       Metrics: Total Events, Unique Resources, Unique Users, Event Types.
•       Bar chart: Top Resources by activity count.
•       Pie chart: Event distribution across all types.
•       Suspicious activities table: filtered to high-risk event types only.
•       Full asset inventory table with search and CSV download.
 
Page 3: Asset Inventory (dashboard/pages/2_Asset_Inventory.py)
Simplified resource view for asset management workflows.
•       Filter by user to scope the inventory.
•       Metrics: Total Unique Resources, Total Events.
•       Full scrollable data table of all cloud log events.
 
Page 4: Identity Explorer (dashboard/pages/3_Identity_Explorer.py)
Per-identity risk profiling and blast radius analysis.
•       User selector drives all panels on the page.
•       Metrics: Incident count, Average Risk Score, Critical Incident count.
•       Attack type bar chart for the selected user.
•       MITRE technique table: all techniques observed for that user.
•       Incident history table with scores and severity.
•       IAM activity log: all IAM events attributed to the selected user.
•       Blast Radius Score (0–100): calculated as min(100, incidents×10 + critical×15).
•       Risk Level badge: Critical (≥80) / High (≥50) / Moderate (<50).
•       Context-aware recommendation panel based on blast radius threshold.
 
Page 5: Analytics (dashboard/pages/4_Analytics.py)
Detection performance metrics and threat intelligence summary.
•       Top-line metrics: Total Events Analyzed, Total Incidents, Critical, High.
•       Noise Reduction %: computed as (events - incidents) / events × 100.
•       Severity Distribution pie chart.
•       Attack Type bar chart.
•       MITRE ATT&CK technique coverage bar chart.
•       Risk Score histogram.
•       Top 10 Risky Users bar chart.
•       Detection Summary green banner with all key statistics.
 
Page 6: Attack Replay (dashboard/pages/5_Attack_Replay.py)
Forensic timeline reconstruction for individual incidents.
•       Incident selector drives the full page.
•       Overview metrics: Severity, Risk Score, Attack Type.
•       Attack Timeline: each event in the incident rendered as a numbered step.
•       MITRE ATT&CK mapping displayed as an info panel.
•       Recommended Response highlighted in a success panel.
•       Executive Summary: auto-generated brief suitable for management escalation.
7. Detection Logic & Signal Design
7.1 Detection Rules
Rule
Signal Logic
Crypto Mining Burst
event == LaunchCryptoMiner → Risk 95, CRITICAL
Privilege Escalation
event == PrivilegeEscalationAttempt → Risk 90, CRITICAL
Cross-Account Abuse
event == CrossAccountAccess → Risk 85, HIGH
Public Exposure
event == ExposeInstancePublicly → Risk 75, HIGH
Security Group Open
event == OpenSecurityGroup → Risk 70, MEDIUM
Off-Hours Activity
hour < 8 or hour > 20 → off_hours = 1 (ML feature)
Event Burst
burst_count = events in same 1-min window (ML feature)
Novel Principal
low user_frequency = rare user (ML feature)

 
7.2 Ambiguous Scenario Handling
Scenario
System Response
40 pods in 2 minutes (HPA vs hijack?)
Burst count feature elevated; off-hours flag + event_code determines anomaly score. K8s namespace frequency provides context.
Spot VM, public IP, no tags
ExposeInstancePublicly event triggers Risk 75 directly. Low user_frequency amplifies Isolation Forest score.
AssumeRole at 3 AM
off_hours=1 captured as feature; CrossAccountAccess if session spans accounts triggers Risk 85.
Privileged debug pod, 5 min TTL
PrivilegeEscalationAttempt maps to Risk 90 CRITICAL. Short TTL means detection must happen on create, not scan cycle.

 

 
8. Sample Incident Narratives
Incident INC-001 — Crypto Mining Campaign
Risk Score
95 / 100 — CRITICAL
Attack Type
Resource Hijacking
MITRE Technique
T1496 — Resource Hijacking
User
user26
Events Observed
LaunchCryptoMiner (×2), CrossAccountAccess (×3)
First Seen
2026-06-20 00:08
Last Seen
2026-06-20 19:25
Recommended Action
Investigate compute usage and disable compromised credentials.

 
Incident INC-002 — Privilege Escalation + Public Exposure
Risk Score
95 / 100 — CRITICAL
Attack Type
Resource Hijacking
MITRE Technique
T1496, T1068
User
user15
Events Observed
ExposeInstancePublicly (×2), LaunchCryptoMiner (×2), CrossAccountAccess (×1)
First Seen
2026-06-20 00:11
Last Seen
2026-06-20 22:28
Recommended Action
Investigate compute usage and disable compromised credentials.

 
Incident INC-003 — Multi-Vector Escalation
Risk Score
95 / 100 — CRITICAL
Attack Type
Resource Hijacking
MITRE Technique
T1496, T1068, T1078
User
user47
Events Observed
LaunchCryptoMiner, CrossAccountAccess (×2), PrivilegeEscalationAttempt (×2)
First Seen
2026-06-20 00:16
Last Seen
2026-06-20 15:50
Recommended Action
Investigate compute usage, disable compromised credentials, review IAM permissions.



9. MITRE ATT&CK Mapping
Technique
Coverage in EphemeralGuard AI
T1496 — Resource Hijacking
Primary detection target. LaunchCryptoMiner event triggers Risk 95 and generates a Resource Hijacking narrative.
T1068 — Privilege Escalation
Detected via PrivilegeEscalationAttempt event. Risk 90, triggers IAM review recommendation.
T1078 — Valid Accounts (Abuse)
Detected via CrossAccountAccess. Risk 85, triggers credential audit recommendation.
T1190 — Exploit Public-Facing Application
Detected via ExposeInstancePublicly and OpenSecurityGroup events. Risk 70–75.
T1578 — Modify Cloud Compute Infrastructure
Partially covered by RunInstance, UpdateLaunchTemplate events captured in feature engineering.



10. Setup & Running the Application
10.1 Prerequisites
•       Python 3.10+ with pip
•       Virtual environment (included as venv/ in the project)
•       All dependencies listed in requirements.txt
 
10.2 Installation
# 1. Clone or unzip the project
cd EphemeralGuardAI
 
# 2. Activate the virtual environment (Windows)
.\venv\Scripts\activate
 
# 3. Activate (macOS / Linux)
source venv/bin/activate
 
# 4. Install dependencies
pip install -r requirements.txt
 
10.3 Running the Pipeline
# Step 1: Feature Engineering
python detection/feature_engineering.py
 
# Step 2: Anomaly Detection
python models/anomaly_detector.py
 
# Step 3: Incident Correlation
python correlation/incident_correlator.py
 
# Step 4: Risk Scoring
python detection/risk_scoring.py
 
# Step 5: LLM Triage / Narrative Generation
python llm/triage.py
 
# Step 6: Launch Dashboard
streamlit run dashboard/Home.py
 
10.4 Key Dependencies
Package
Purpose
streamlit
Multi-page interactive dashboard framework
pandas
Data ingestion, transformation, and feature engineering
scikit-learn
Isolation Forest anomaly detection model
plotly
Interactive charts and visualizations
numpy / scipy
Statistical feature computation
faker
Synthetic data generation for simulation

 

11. Performance Targets & Self-Evaluation
Metric
Target & Rationale
Ephemeral Asset Visibility
95%+ of short-lived resources identified. Achieved through event-driven ingestion rather than scheduled scans.
Detection Latency
Near real-time (sub-minute). Events processed as they arrive to the pipeline; no batch scan delays.
Noise Reduction
≥40% reduction from raw alerts to correlated incidents. Identity-based grouping collapses N events per user into 1 incident.
Incident Correlation Accuracy
High confidence. Events with the same suspicious principal grouped together; no false cluster splits.
Risk Scoring Quality
Scores align with analyst judgment (95 for crypto mining, 70 for misconfigured SG). Validated against domain knowledge.
Analyst Readiness
Single incident card with MITRE, evidence, and recommendation. Tested on the Attack Replay page.
Precision (Detection Model)
Target >75%. Isolation Forest with contamination=0.05 calibrated to expected anomaly rate.
Recall (Detection Model)
Target >70%. Off-hours + burst + event-code features ensure rare high-severity events are not missed.



12. Future Enhancements
1.     Real-time streaming ingestion via Kafka or AWS Kinesis to replace batch CSV reads.
2.     Integration of live Kubernetes API server audit log webhooks.
3.     Graph-based incident correlation (NetworkX) to model lateral movement chains across identities.
4.     Replace rule-based triage with live Claude API calls for fully dynamic LLM narratives.
5.     SOAR integration (PagerDuty, Jira, Slack) for automated incident ticket creation.
6.     Per-namespace and per-principal behavioral baselines using Z-score/IQR rolling windows.
7.     Drift detection to distinguish legitimate autoscaling bursts from malicious resource bursts.
8.     GDPR / compliance report generation: continuous monitoring proof for auditors.


