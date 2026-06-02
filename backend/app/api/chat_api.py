from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    query: str

@router.post("/chat")
async def soc_chat(request: ChatRequest):
    return {
        "query": request.query,
        "answer": "SentinelGPT chat endpoint is working."
    }