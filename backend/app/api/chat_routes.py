from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[dict]] = []

@router.post("/chat")
def soc_chat(request: ChatRequest):

    message = request.message.lower()

    response = {
        "title": "AI Incident Explainer",
        "risk": "LOW",
        "summary": "",
        "actions": []
    }


    if "brute" in message or "login" in message:

        response["risk"] = "HIGH"

        response["summary"] = """
This incident indicates a possible credential attack.

The attacker attempted repeated authentication failures,
which may indicate password guessing or account compromise attempts.

SentinelGPT correlation:
- Authentication anomaly detected
- Multiple failures from same source
- Possible unauthorized access attempt
"""

        response["actions"] = [
            "Block suspicious source IP",
            "Reset affected credentials",
            "Review authentication logs",
            "Enable MFA for affected accounts"
        ]


    elif "mitre" in message or "ttp" in message:

        response["risk"] = "MEDIUM"

        response["summary"] = """
The observed behaviour matches adversary techniques
from the MITRE ATT&CK framework.

Further investigation is required to confirm attacker intent.
"""

        response["actions"] = [
            "Review mapped techniques",
            "Check related alerts",
            "Investigate affected hosts"
        ]


    elif "ioc" in message or "ip" in message:

        response["risk"] = "MEDIUM"

        response["summary"] = """
SentinelGPT is correlating the indicator against
available threat intelligence context.

The indicator should be validated before containment.
"""

        response["actions"] = [
            "Check IOC reputation",
            "Search historical activity",
            "Monitor affected systems"
        ]


    elif "report" in message:

        response["risk"] = "INFO"

        response["summary"] = """
Incident reporting workflow is available.
The system can prepare analyst-level summaries.
"""

        response["actions"] = [
            "Open Reports module",
            "Review incident evidence",
            "Export analyst summary"
        ]


    else:

        response["summary"] = """
I am analysing this security event.

Provide more context such as:
- attack type
- source IP
- affected system
- alert message

I will correlate the event and suggest response actions.
"""

        response["actions"] = [
            "Provide incident details",
            "Check active alerts",
            "Review timeline"
        ]


    return {
        "reply": response
    }