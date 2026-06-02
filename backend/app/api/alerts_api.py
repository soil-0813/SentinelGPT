from fastapi import APIRouter
from typing import List, Dict

router = APIRouter()

# Temporary mock data
# Later this will come from correlation engine + RAG + LLM

mock_alerts = [
    {
        "alert_id": "ALT-001",
        "title": "Brute Force Attack Detected",
        "severity": "Critical",
        "severity_score": 9.3,
        "timestamp": "2026-06-01T10:15:00Z",

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

    return {
        "count": len(mock_alerts),
        "alerts": mock_alerts
    }


@router.get("/alerts/{alert_id}")
def get_alert(alert_id: str):

    for alert in mock_alerts:

        if alert["alert_id"] == alert_id:
            return alert

    return {
        "error": "Alert not found"
    }