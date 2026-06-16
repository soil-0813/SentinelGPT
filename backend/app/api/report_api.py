from fastapi import APIRouter
from typing import List, Dict

router = APIRouter()

# Schema perfectly mapped to match Reports.jsx fields
mock_reports = [
    {
        "id": "REP-2026-001",
        "title": "Brute Force Attack Remediation",
        "type": "incident",  # Must be 'incident', 'threat', or 'summary'
        "severity": "critical",  # Lowercase to match SEVERITY_COLOR keys
        "analyst": "Aritra B.",
        "created": "2026-06-17T00:43:00Z",
        "summary": "Automated log correlation detected an active Brute Force attack against Windows authentication endpoints stemming from source IP 192.168.1.50.",
        "sections": {
            "Executive_Summary": "At approximately 10:00 AM UTC, multiple authentication failures were detected on system clusters, followed by an anomalous successful login flag.",
            "Technical_Analysis": "Log analysis indicates a classic brute-force pattern targeting local administrator profiles via network logins. Firewall tracking verified an anomalous outbound communication baseline shift post-compromise.",
            "Remediation_Steps": "1. Temporarily isolate target host nodes.\n2. Revoke and cycle credential tokens for compromised entities.\n3. Explicitly block external requests originating from IP footprint 192.168.1.50."
        }
    },
    {
        "id": "REP-2026-002",
        "title": "Threat Intelligence Feed Sync",
        "type": "threat",
        "severity": "high",
        "analyst": "SOC Automation Engine",
        "created": "2026-06-17T01:10:00Z",
        "summary": "Regular synchronization with external threat telemetry nodes identified multi-vector malicious indicators active across the routing matrix.",
        "sections": {
            "Threat_Landscape": "Malicious network entities running active scanners have been mapped interacting with public gateway endpoints.",
            "Action_Items": "Enforced updated egress blacklists at internal edge routing nodes across active subnets."
        }
    }
]


@router.get("/reports")
def get_reports():
    # Return raw list directly so frontend maps it cleanly
    return mock_reports


@router.post("/reports/generate")
def generate_report(payload: dict):
    # Fallback to prevent crash when clicking 'New Report' button
    return mock_reports[0]