from fastapi import FastAPI

from app.api.alerts_api import router as alerts_router

app = FastAPI(
    title="SentinelGPT",
    version="1.0.0"
)

app.include_router(
    alerts_router,
    prefix="/api",
    tags=["Alerts"]
)