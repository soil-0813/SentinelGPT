import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def build_timeline(story):

    timeline = []

    logs = story["supporting_logs"]

    for log in logs:

        timeline.append({
            "timestamp": log["timestamp"],
            "event_type": log["event_type"],
            "source": log["log_source"]
        })

    timeline.sort(
        key=lambda x: parse_timestamp(x["timestamp"])
    )

    return timeline


def parse_timestamp(ts):

    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%SZ"
    ]

    for fmt in formats:
        try:
            return datetime.strptime(ts, fmt)
        except:
            pass

    return datetime.min