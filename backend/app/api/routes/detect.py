import time
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.core.preprocessing import process_uploaded_image
from app.core.model import detector_service
from app.schemas.detection import DetectionResponse

router = APIRouter()

ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp", "image/jpg"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

@router.post("/detect", response_model=DetectionResponse)
async def detect_image(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file.content_type}. Please upload a JPEG, PNG, or WebP image."
        )

    start_time = time.time()
    try:
        contents = await file.read()
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File too large. Maximum size is 10 MB.")

        orig_pil = process_uploaded_image(contents)
        
        prediction, confidence, fake_prob, real_prob, _ = detector_service.predict(orig_pil)

        elapsed_ms = round((time.time() - start_time) * 1000, 2)

        return DetectionResponse(
            prediction=prediction,
            confidence=round(confidence, 4),
            fake_probability=round(fake_prob, 4),
            real_probability=round(real_prob, 4),
            faces_detected=1,
            heatmap_base64=None,
            processing_time_ms=elapsed_ms,
            message="Analysis completed successfully via Hugging Face model."
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")
