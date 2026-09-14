import os
import io
import requests
from PIL import Image

class DeepfakeDetectorService:
    def __init__(self, model_id="prithivMLmods/Deep-Fake-Detector-v2-Model"):
        self.model_id = os.getenv("HF_MODEL_ID", model_id)
        self.api_url = f"https://router.huggingface.co/hf-inference/models/{self.model_id}"

    def load_model(self):
        token = os.getenv("HF_TOKEN")
        print(f"DeepfakeDetectorService configured for {self.model_id}. Token configured: {bool(token)}")

    def predict(self, orig_pil: Image.Image, generate_heatmap=False):
        token = os.getenv("HF_TOKEN")
        if not token:
            raise RuntimeError(
                "HF_TOKEN environment variable is not configured on Render. "
                "Please add HF_TOKEN in the Render Dashboard -> Environment."
            )

        # Convert PIL image to raw JPEG bytes
        img_byte_arr = io.BytesIO()
        orig_pil.save(img_byte_arr, format="JPEG", quality=95)
        image_bytes = img_byte_arr.getvalue()

        # Explicitly pass Content-Type: image/jpeg so Hugging Face router knows it is binary image data
        headers = {
            "Authorization": f"Bearer {token.strip()}",
            "Content-Type": "image/jpeg"
        }

        response = requests.post(self.api_url, headers=headers, data=image_bytes, timeout=45)

        if response.status_code != 200:
            raise RuntimeError(
                f"Hugging Face API returned status {response.status_code}: {response.text[:300]}"
            )

        results = response.json()

        # Some responses may be a list of dicts [{'label': 'fake', 'score': 0.95}, ...]
        if isinstance(results, dict) and "error" in results:
            raise RuntimeError(f"Hugging Face Model error: {results['error']}")

        fake_prob = 0.0
        real_prob = 0.0

        if isinstance(results, list):
            for item in results:
                lbl = str(item.get("label", "")).lower()
                score = float(item.get("score", 0.0))
                if "fake" in lbl or "synthetic" in lbl or "deepfake" in lbl or lbl == "1":
                    fake_prob = max(fake_prob, score)
                elif "real" in lbl or "authentic" in lbl or lbl == "0":
                    real_prob = max(real_prob, score)

            if fake_prob == 0.0 and real_prob == 0.0 and len(results) > 0:
                top = results[0]
                lbl = str(top.get("label", "")).lower()
                score = float(top.get("score", 0.0))
                if "fake" in lbl:
                    fake_prob = score
                    real_prob = 1.0 - score
                else:
                    real_prob = score
                    fake_prob = 1.0 - score
            else:
                total = fake_prob + real_prob
                if total > 0:
                    fake_prob = fake_prob / total
                    real_prob = real_prob / total

        is_fake = fake_prob >= 0.5
        prediction = "FAKE" if is_fake else "REAL"
        confidence = fake_prob if is_fake else real_prob

        return prediction, confidence, fake_prob, real_prob, None

detector_service = DeepfakeDetectorService()
