from fastapi import APIRouter
import json
from app.database.db import get_all_incidents

router = APIRouter()

@router.get("/incidents")
def get_incidents():
    incidents = get_all_incidents()
    formatted_incidents = []
    
    for inc in incidents:
        # inc = (incident_id, attack_type, severity, risk_score, incident_data)
        inc_id = inc[0]
        attack_type = inc[1]
        severity = inc[2].lower() if inc[2] else 'medium'
        
        try:
            data = json.loads(inc[4])
        except Exception:
            data = {}
            
        formatted_incidents.append({
            "id": inc_id,
            "title": attack_type,
            "severity": severity,
            "status": "active",
            "affected": len(data.get("timeline", [])),
            "analyst": "Automated Engine",
            "opened": "Just now",
            "mitre": []
        })
        
    return formatted_incidents
