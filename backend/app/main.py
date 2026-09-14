from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.routes import detect
from app.core.model import detector_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    detector_service.load_model()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(detect.router, prefix=settings.API_V1_STR, tags=["Detection"])

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "model_id": detector_service.model_id,
        "device": str(detector_service.device),
        "version": settings.VERSION
    }

@app.get("/")
def root():
    return {
        "message": "Welcome to Deepfake Image Detector API. Use POST /api/v1/detect to analyze an image."
    }
