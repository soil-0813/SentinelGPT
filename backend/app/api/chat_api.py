from fastapi import APIRouter
from pydantic import BaseModel

from app.rag.retriever import retrieve_context
from app.llm_engine.local_llm import generate_response

router = APIRouter()


class ChatRequest(BaseModel):
    query: str


@router.post("/chat")
async def soc_chat(request: ChatRequest):

    context = retrieve_context(request.query)

    answer = generate_response(
        query=request.query,
        context=context
    )

    return {
        "query": request.query,
        "context": context,
        "answer": answer
    }