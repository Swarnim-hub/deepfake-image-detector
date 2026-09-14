import os
import torch
from PIL import Image
from transformers import AutoImageProcessor, AutoModelForImageClassification

class DeepfakeDetectorService:
    def __init__(self, model_id="prithivMLmods/Deep-Fake-Detector-v2-Model"):
        self.model_id = os.getenv("HF_MODEL_ID", model_id)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.processor = None
        self.model = None

    def load_model(self):
        print(f"Loading pre-trained Hugging Face model '{self.model_id}' on {self.device}...")
        try:
            self.processor = AutoImageProcessor.from_pretrained(self.model_id)
            self.model = AutoModelForImageClassification.from_pretrained(self.model_id)
            self.model.to(self.device)
            self.model.eval()
            print("Model successfully loaded from Hugging Face Hub!")
        except Exception as e:
            print(f"Error loading model from Hugging Face Hub: {e}")
            raise e

    def predict(self, orig_pil: Image.Image, generate_heatmap=False):
        if self.model is None or self.processor is None:
            raise RuntimeError("Model is not initialized. Call load_model() first.")

        # Preprocess input image using the official model processor
        inputs = self.processor(images=orig_pil, return_tensors="pt")
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self.model(**inputs)
            probs = torch.nn.functional.softmax(outputs.logits, dim=-1)[0]

        labels = self.model.config.id2label
        
        # Determine fake vs real probability
        fake_prob = 0.0
        real_prob = 0.0

        for idx, prob_val in enumerate(probs):
            lbl = labels[idx].lower()
            val = float(prob_val.cpu().item())
            if "fake" in lbl or "synthetic" in lbl or "deepfake" in lbl or lbl == "1":
                fake_prob = val
            elif "real" in lbl or "authentic" in lbl or lbl == "0":
                real_prob = val

        # If labels don't explicitly match, use primary class
        if fake_prob == 0.0 and real_prob == 0.0:
            top_class = int(torch.argmax(probs).cpu().item())
            top_prob = float(probs[top_class].cpu().item())
            lbl = labels[top_class].lower()
            if "fake" in lbl:
                fake_prob = top_prob
                real_prob = 1.0 - top_prob
            else:
                real_prob = top_prob
                fake_prob = 1.0 - top_prob
        else:
            # Normalize if needed
            total = fake_prob + real_prob
            if total > 0:
                fake_prob = fake_prob / total
                real_prob = real_prob / total

        is_fake = fake_prob >= 0.5
        prediction = "FAKE" if is_fake else "REAL"
        confidence = fake_prob if is_fake else real_prob

        return prediction, confidence, fake_prob, real_prob, None

detector_service = DeepfakeDetectorService()
