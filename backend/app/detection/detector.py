import uuid
from datetime import datetime
from typing import List, Dict


# -----------------------------
# MITRE Mapping
# -----------------------------

MITRE_MAP = {
    "failed_login": "T1110",
    "port_scan": "T1046",
    "malware": "T1204",
    "phishing": "T1566",
    "credential_attack": "T1003",
    "lateral_movement": "T1021",
    "ransomware": "T1486",
    "file_encryption": "T1486",
}


# -----------------------------
# Alert Generator
# -----------------------------

def create_alert(
    title: str,
    description: str,
    severity: str,
    source_ip: str,
    mitre: str
):
    return {
        "id": f"ALT-{uuid.uuid4().hex[:8].upper()}",
        "title": title,
        "description": description,
        "severity": severity,
        "source": "SentinelGPT Detection Engine",
        "ip": source_ip,
        "mitre": mitre,
        "timestamp": datetime.utcnow().isoformat(),
        "status": "open"
    }


# -----------------------------
# Core Detection Logic
# -----------------------------

def detect_attacks(featured_logs: List[Dict]) -> List[Dict]:

    alerts = []

    for log in featured_logs:

        features = log.get("log_features", {})

        source_ip = features.get("source_ip", "")

        # ---------------------------------
        # Failed Login
        # ---------------------------------

        if features.get("is_failed_login"):

            alerts.append(
                create_alert(
                    title="Failed Login Detected",
                    description="Multiple failed login activity observed.",
                    severity="medium",
                    source_ip=source_ip,
                    mitre=MITRE_MAP["failed_login"]
                )
            )

        # ---------------------------------
        # Port Scan
        # ---------------------------------

        if features.get("is_port_scan"):

            alerts.append(
                create_alert(
                    title="Port Scan Detected",
                    description="Reconnaissance activity detected.",
                    severity="medium",
                    source_ip=source_ip,
                    mitre=MITRE_MAP["port_scan"]
                )
            )

        # ---------------------------------
        # Malware
        # ---------------------------------

        if features.get("is_malware"):

            alerts.append(
                create_alert(
                    title="Malware Activity Detected",
                    description="Known malware indicators found.",
                    severity="high",
                    source_ip=source_ip,
                    mitre=MITRE_MAP["malware"]
                )
            )

        # ---------------------------------
        # Phishing
        # ---------------------------------

        if features.get("is_phishing"):

            alerts.append(
                create_alert(
                    title="Phishing Attempt Detected",
                    description="Potential phishing activity identified.",
                    severity="high",
                    source_ip=source_ip,
                    mitre=MITRE_MAP["phishing"]
                )
            )

        # ---------------------------------
        # Credential Attack
        # ---------------------------------

        if features.get("is_credential_attack"):

            alerts.append(
                create_alert(
                    title="Credential Attack Detected",
                    description="Credential theft behavior identified.",
                    severity="critical",
                    source_ip=source_ip,
                    mitre=MITRE_MAP["credential_attack"]
                )
            )

        # ---------------------------------
        # Lateral Movement
        # ---------------------------------

        if features.get("is_lateral_movement"):

            alerts.append(
                create_alert(
                    title="Lateral Movement Detected",
                    description="Internal movement between hosts observed.",
                    severity="critical",
                    source_ip=source_ip,
                    mitre=MITRE_MAP["lateral_movement"]
                )
            )

        # ---------------------------------
        # Ransomware
        # ---------------------------------

        if features.get("is_ransomware"):

            alerts.append(
                create_alert(
                    title="Ransomware Activity Detected",
                    description="Indicators of ransomware execution found.",
                    severity="critical",
                    source_ip=source_ip,
                    mitre=MITRE_MAP["ransomware"]
                )
            )

        # ---------------------------------
        # File Encryption
        # ---------------------------------

        if features.get("is_file_encryption"):

            alerts.append(
                create_alert(
                    title="Mass File Encryption Detected",
                    description="Large-scale encryption activity observed.",
                    severity="critical",
                    source_ip=source_ip,
                    mitre=MITRE_MAP["file_encryption"]
                )
            )

    return alerts


# -----------------------------
# Incident Builder
# -----------------------------

def build_incidents(alerts: List[Dict]):

    incidents = []

    for alert in alerts:

        incidents.append(
            {
                "id": alert["id"].replace("ALT", "INC"),
                "title": alert["title"],
                "severity": alert["severity"],
                "status": "active",
                "affected": 1,
                "analyst": "SentinelGPT Engine",
                "opened": alert["timestamp"],
                "mitre": [alert["mitre"]],
                "source_ip": alert["ip"]
            }
        )

    return incidents