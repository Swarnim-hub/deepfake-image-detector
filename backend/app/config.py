import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Deepfake Image Detector API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    MODEL_PATH: str = os.getenv("MODEL_PATH", "models/best_model.pth")
    DEVICE: str = "cpu"
    MAX_UPLOAD_SIZE_MB: int = 10

settings = Settings()
