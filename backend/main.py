from fastapi import FastAPI

from app.api.alerts_api import router as alerts_router
from app.api.chat_api import router as chat_router
from app.api.health_api import router as health_router
from app.api.report_api import router as reports_router

app = FastAPI(
    title="SentinelGPT",
    version="1.0.0"
)

app.include_router(alerts_router, prefix="/api", tags=["Alerts"])
app.include_router(chat_router, prefix="/api", tags=["Chat"])
app.include_router(health_router, prefix="/api", tags=["Health"])
app.include_router(reports_router, prefix="/api", tags=["Reports"])


@app.get("/")
def root():
    return {
        "message": "SentinelGPT API Running"
    }