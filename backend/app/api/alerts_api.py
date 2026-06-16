from fastapi import APIRouter
from typing import List, Dict

router = APIRouter()

# Perfect match schema for AlertCard.jsx
mock_alerts = [
    {
        "id": "ALT-001",
        "title": "Brute Force Attack Detected",
        "description": "Multiple failed SSH login attempts followed by a successful execution flag.",
        "severity": "critical",  # Lowercase to match your ICONS mapping object
        "source": "Windows Log Engine",
        "ip": "192.168.1.50",
        "mitre": "T1110",
        "timestamp": "2026-06-17T00:00:00Z",
        "status": "open",  # THIS FIXES THE CRASH!
        "severity_score": 9.3,
        
        "attack_reasoning_graph": {
            "nodes": [
                "Failed Login Attempts",
                "Successful Login",
                "PowerShell Execution"
            ],
            "edges": [
                ["Failed Login Attempts", "Successful Login"],
                ["Successful Login", "PowerShell Execution"]
            ]
        },
        "alternative_hypotheses": [
            {
                "name": "Password Spraying",
                "confidence": 12
            },
            {
                "name": "Misconfigured Application",
                "confidence": 6
            }
        ],
        "severity_explanation": {
            "score": 9.3,
            "reasons": [
                {
                    "factor": "30 Failed Logins",
                    "impact": 3.0
                },
                {
                    "factor": "Successful Login",
                    "impact": 3.0
                },
                {
                    "factor": "PowerShell Execution",
                    "impact": 3.3
                }
            ]
        },
        "mitre_mapping": [
            "T1110",
            "T1059"
        ],
        "mitigation": [
            "Block source IP",
            "Reset affected account password",
            "Enable MFA",
            "Review PowerShell activity"
        ]
    }
]


@router.get("/alerts")
def get_alerts():
    # Return the clean, raw list array exactly like your dashboard needs!
    return mock_alerts


@router.get("/alerts/{alert_id}")
def get_alert(alert_id: str):
    for alert in mock_alerts:
        if alert["id"] == alert_id:
            return alert
    return {"error": "Alert not found"}