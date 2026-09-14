import io
from PIL import Image

def process_uploaded_image(file_bytes: bytes) -> Image.Image:
    """
    Decodes raw image bytes into an RGB PIL Image.
    """
    return Image.open(io.BytesIO(file_bytes)).convert("RGB")
