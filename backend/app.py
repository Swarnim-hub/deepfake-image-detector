import io
import time
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import gradio as gr
from app.core.model import detector_service
from app.schemas.detection import DetectionResponse

# 1. Initialize FastAPI
app = FastAPI(title="Deepfake Image Detector API", version="1.0.0")

# Open CORS so your Vercel React frontend can connect freely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model on startup
@app.on_event("startup")
def startup_event():
    detector_service.load_model()

@app.get("/health")
def health():
    return {"status": "healthy", "model_id": detector_service.model_id}

# API route for your React/Vercel frontend
@app.post("/api/v1/detect", response_model=DetectionResponse)
async def detect_image(file: UploadFile = File(...)):
    start_time = time.time()
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        prediction, confidence, fake_prob, real_prob, _ = detector_service.predict(image)
        elapsed_ms = round((time.time() - start_time) * 1000, 2)
        return DetectionResponse(
            prediction=prediction,
            confidence=round(confidence, 4),
            fake_probability=round(fake_prob, 4),
            real_probability=round(real_prob, 4),
            faces_detected=1,
            heatmap_base64=None,
            processing_time_ms=elapsed_ms,
            message="Analysis completed successfully."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 2. Gradio Web Interface (Required for free Hugging Face Space)
def gradio_predict(img):
    if img is None:
        return "Please upload an image."
    prediction, confidence, fake_prob, real_prob, _ = detector_service.predict(img)
    return {
        "Likely Authentic (Real)": real_prob,
        "Deepfake / Synthetic (Fake)": fake_prob
    }

with gr.Blocks(title="Deepfake Image Detector") as demo:
    gr.Markdown("# 🛡️ Deepfake Image Detector")
    gr.Markdown("Upload an image to evaluate if it is an authentic photo or an AI-synthesized deepfake.")
    with gr.Row():
        input_img = gr.Image(type="pil", label="Input Image")
        output_label = gr.Label(num_top_classes=2, label="Prediction")
    btn = gr.Button("Analyze Image", variant="primary")
    btn.click(fn=gradio_predict, inputs=input_img, outputs=output_label)

# 3. Mount Gradio interface to the root of FastAPI
app = gr.mount_gradio_app(app, demo, path="/")
