from pydantic import BaseModel
from typing import Optional

class DetectionResponse(BaseModel):
    prediction: str            # "REAL" or "FAKE"
    confidence: float          # 0.0 to 1.0 (confidence of the predicted class)
    fake_probability: float    # 0.0 to 1.0 (raw probability of being fake)
    real_probability: float    # 0.0 to 1.0 (raw probability of being real)
    faces_detected: int
    heatmap_base64: Optional[str] = None
    processing_time_ms: float
    message: Optional[str] = None
