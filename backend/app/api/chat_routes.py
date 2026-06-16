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
    reply = "I am analyzing the network traffic. Let me know if you need specific incident details."
    
    if "mitre" in message or "ttp" in message:
        reply = "The MITRE ATT&CK framework mapping indicates suspicious behavior. Prioritizing containment is recommended."
    elif "report" in message or "pdf" in message:
        reply = "I can generate an Incident Report, Threat Intelligence Brief, or Daily SOC Summary. Navigate to the Reports page."
    elif "remediat" in message or "fix" in message:
        reply = "Recommended remediation: Isolate affected endpoints, reset credentials, and patch vulnerable systems."
        
    return {
        "reply": reply
    }
