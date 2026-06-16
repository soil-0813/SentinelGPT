from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "SentinelGPT",
        "version": "1.0.0"
    }


@router.get("/health/details")
def health_details():
    return {
        "status": "healthy",
        "components": {
            "api": "running",
            "rag": "available",
            "llm": "available",
            "database": "not_connected"
        }
    }