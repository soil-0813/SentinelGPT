from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import api_router

app = FastAPI(
    title="SentinelGPT Backend API",
    description="Backend services for SOC Dashboard",
    version="1.0.0",
)

# Configure CORS so the frontend (React/Vite on localhost:3000) can communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the main API router
app.include_router(api_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to SentinelGPT API. Use /docs to view the Swagger UI."}
