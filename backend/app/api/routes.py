from fastapi import APIRouter

from .alerts_api import router as alerts_router
from .health_api import router as health_router
from .report_api import router as report_router
from .incident_routes import router as incident_router
from .chat_routes import router as chat_router
from .dashboard_api import router as dashboard_router
from .timeline_api import router as timeline_router
from .threat_intel_api import router as threat_intel_router

api_router = APIRouter()

api_router.include_router(alerts_router, tags=["alerts"])
api_router.include_router(health_router, tags=["health"])
api_router.include_router(report_router, tags=["reports"])
api_router.include_router(incident_router, tags=["incidents"])
api_router.include_router(chat_router, tags=["chat"])
api_router.include_router(
    dashboard_router,
    tags=["dashboard"]
)
api_router.include_router(
    timeline_router,
    tags=["timeline"]
)
api_router.include_router(
    threat_intel_router,
    tags=["threat-intel"]
)