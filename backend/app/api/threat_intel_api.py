from fastapi import APIRouter
from app.database.db import get_all_incidents
import json

router = APIRouter()

@router.get("/threat-intel")
def get_threat_intel():

    incidents = get_all_incidents()

    intel = []

    for inc in incidents:

        attack_type = inc[1]
        severity = str(inc[2]).lower()

        try:
            data = json.loads(inc[4])
        except:
            data = {}

        timeline = data.get("timeline", [])

        source_ip = "Unknown"

        source_ip="Unknown"
        if "source_ip" in data:
            source_ip = data["source_ip"]
        elif timeline:
            source_ip = timeline[0].get("ip", "Unknown")

        intel.append({
            "title": source_ip,
            "sub": f"{attack_type} detected by correlation engine",
            "severity": severity
        })

    return intel