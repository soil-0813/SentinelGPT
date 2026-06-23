from fastapi import APIRouter
import json

from app.database.db import get_all_incidents

router = APIRouter()


@router.get("/alerts")
def get_alerts():

    incidents = get_all_incidents()

    alerts = []

    for inc in incidents:

        try:
            incident_id = inc[0]
            attack_type = inc[1]
            severity = inc[2].lower()
            risk_score = inc[3]

            incident_data = json.loads(inc[4])

            source_ip = incident_data.get(
                "source_ip",
                "Unknown"
            )

            timeline = incident_data.get(
                "timeline",
                []
            )

            timestamp = (
                timeline[0]["timestamp"]
                if timeline
                else "2026-01-01T00:00:00Z"
            )

            reasoning = incident_data.get(
                "reasoning",
                []
            )

            description = (
                reasoning[0]
                if reasoning
                else attack_type
            )

            mitre_mapping = {
                "Brute Force Attack": "T1110",
                "Port Scan": "T1046",
                "Malware Infection": "T1204",
                "Ransomware Attack": "T1486",
                "Phishing Attack": "T1566",
                "Credential Attack": "T1110",
                "Lateral Movement": "T1021"
            }

            alerts.append({

                "id": incident_id,

                "title": attack_type,

                "description": description,

                "severity": severity,

                "source": "SentinelGPT Correlation Engine",

                "ip": source_ip,

                "mitre": mitre_mapping.get(
                    attack_type,
                    "T0000"
                ),

                "timestamp": timestamp,

                "status": "open",

                "severity_score": risk_score

            })

        except Exception as e:

            print(
                f"Error converting incident "
                f"to alert: {e}"
            )

    return alerts


@router.get("/alerts/{alert_id}")
def get_alert(alert_id: str):

    alerts = get_alerts()

    for alert in alerts:

        if alert["id"] == alert_id:
            return alert

    return {
        "error": "Alert not found"
    }