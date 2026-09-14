import os
import io
from PIL import Image
from huggingface_hub import InferenceClient

class DeepfakeDetectorService:
    def __init__(self, model_id="prithivMLmods/Deep-Fake-Detector-v2-Model"):
        self.model_id = os.getenv("HF_MODEL_ID", model_id)
        self.token = os.getenv("HF_TOKEN", None)
        self.client = None

    def load_model(self):
        token = os.getenv("HF_TOKEN", self.token)
        print(f"Initializing Hugging Face InferenceClient for {self.model_id} (token present: {bool(token)})...")
        self.client = InferenceClient(token=token)

    def predict(self, orig_pil: Image.Image, generate_heatmap=False):
        if self.client is None:
            self.load_model()

        # Check if HF_TOKEN is missing
        current_token = os.getenv("HF_TOKEN", self.token)
        if not current_token:
            raise RuntimeError(
                "HF_TOKEN environment variable is missing on Render. "
                "Please generate a free Hugging Face Read Token at https://huggingface.co/settings/tokens "
                "and add 'HF_TOKEN' to your Environment Variables on the Render dashboard."
            )

        # Convert PIL to bytes
        img_byte_arr = io.BytesIO()
        orig_pil.save(img_byte_arr, format="JPEG")
        image_bytes = img_byte_arr.getvalue()

        # Call Hugging Face Serverless Inference API
        results = self.client.image_classification(
            image=image_bytes,
            model=self.model_id
        )

        fake_prob = 0.0
        real_prob = 0.0

        for item in results:
            lbl = item.label.lower()
            score = float(item.score)
            if "fake" in lbl or "synthetic" in lbl or "deepfake" in lbl or lbl == "1":
                fake_prob = max(fake_prob, score)
            elif "real" in lbl or "authentic" in lbl or lbl == "0":
                real_prob = max(real_prob, score)

        if fake_prob == 0.0 and real_prob == 0.0 and len(results) > 0:
            top_item = results[0]
            lbl = top_item.label.lower()
            score = float(top_item.score)
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
