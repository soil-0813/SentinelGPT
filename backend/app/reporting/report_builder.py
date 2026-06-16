from typing import Dict, Any
from .attack_summary import generate_attack_summary
import datetime
import uuid

def build_incident_report(incident_data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": incident_data.get("incident_id", str(uuid.uuid4())[:8]),
        "title": f"Incident Report: {incident_data.get('attack_type', 'Suspicious Activity')}",
        "type": "incident",
        "severity": incident_data.get("severity", "medium").lower(),
        "created": datetime.datetime.utcnow().isoformat() + "Z",
        "analyst": "SentinelGPT Auto-Report",
        "summary": generate_attack_summary(incident_data),
        "sections": {
            "executive_summary": "An automated incident report was generated based on correlated security events.",
            "timeline": "\n".join([f"[{e.get('timestamp')}] {e.get('event_type')}" for e in incident_data.get('timeline', [])]),
            "iocs": incident_data.get("source_ip", "None identified"),
            "mitre_techniques": "Refer to dashboard for specific mappings",
            "remediation": "Review affected endpoints and isolate if necessary."
        }
    }

def build_threat_report(threat_data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": "THR-" + threat_data.get("id", str(uuid.uuid4())[:8]),
        "title": f"Threat Report: {threat_data.get('name', 'General Threat')}",
        "type": "threat",
        "severity": "high",
        "created": datetime.datetime.utcnow().isoformat() + "Z",
        "analyst": "Threat Intel Feed",
        "summary": threat_data.get("description", "A new threat has been identified."),
        "sections": {
            "executive_summary": "Threat intelligence report based on latest feed data.",
            "iocs": "N/A",
            "mitre_techniques": "N/A",
            "remediation": "Update defenses with latest indicators."
        }
    }
