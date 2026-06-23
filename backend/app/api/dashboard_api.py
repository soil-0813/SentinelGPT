from fastapi import APIRouter
from app.database.db import get_all_incidents
import json
from collections import Counter

router = APIRouter()


@router.get("/dashboard/stats")
def dashboard_stats():

    incidents = get_all_incidents()

    total_incidents = len(incidents)

    active_threats = len(incidents)

    critical_alerts = 0

    severity_count = Counter()

    activity_count = Counter()


    for incident in incidents:

        severity = str(incident[2]).lower()

        severity_count[severity] += 1


        if severity in ["critical", "high"]:
            critical_alerts += 1


        # incident_data column
        try:
            data = json.loads(incident[4])

            print(data.keys())
            print(data)

            timestamp = (data.get("timestamp") or data.get("opened") or data.get("created") or data.get("created_at") or data.get("time"))

            if timestamp :
                hour = timestamp[11:13]
                activity_count[hour] += 1

        except:
            pass



    severity_data = [
        {
            "name": key,
            "value": value
        }
        for key, value in severity_count.items()
    ]


    activity_data = []

    for index, incident in enumerate(incidents):
        hour = str(index).zfill(2)
        activity_count[hour] += 1

    for i in range(24):
        hour = f"{i:02d}"

        activity_data.append({
            "h": f"{i:02d}",
            "events": activity_count.get(f"{i:02d}", 0)
            })


    return {

        "total_incidents": total_incidents,

        "active_threats": active_threats,

        "resolved_today": 0,

        "critical_alerts": critical_alerts,


        # NEW
        "severity": severity_data,

        "activity": activity_data
    }