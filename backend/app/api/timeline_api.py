from fastapi import APIRouter
import json

from app.database.db import get_all_incidents

router = APIRouter()


@router.get("/timeline")
def get_timeline():

    incidents = get_all_incidents()

    timeline_events = []

    for incident in incidents:

        try:
            data = json.loads(incident[4])

            for event in data.get("timeline", []):

                timeline_events.append({
                    "id": len(timeline_events) + 1,
                    "title": event.get("event_type", "Security Event"),
                    "severity": incident[2].lower(),
                    "time": event.get("timestamp", ""),
                    "desc": f"Source: {event.get('source', 'unknown')}",
                    "ip": data.get("source_ip", ""),
                    "mitre": "T1110"
                })

        except Exception:
            continue

    return timeline_events