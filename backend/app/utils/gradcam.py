import io
import base64
import numpy as np
import torch
from PIL import Image

class GradCAM:
    def __init__(self, model, target_layer):
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None
        self.hook_handles = []
        self._register_hooks()

    def _register_hooks(self):
        def forward_hook(module, input, output):
            self.activations = output

        def backward_hook(module, grad_in, grad_out):
            self.gradients = grad_out[0]

        self.hook_handles.append(self.target_layer.register_forward_hook(forward_hook))
        self.hook_handles.append(self.target_layer.register_full_backward_hook(backward_hook))

    def generate(self, input_tensor):
        self.model.eval()
        self.model.zero_grad()
        
        output = self.model(input_tensor)
        prob = torch.sigmoid(output)
        
        # Backward w.r.t the output logit
        output.backward(retain_graph=True)

        if self.gradients is None or self.activations is None:
            return None

        # Pool gradients across spatial channels
        weights = torch.mean(self.gradients, dim=[2, 3], keepdim=True)
        cam = torch.sum(weights * self.activations, dim=1, keepdim=True)
        cam = torch.relu(cam)

        cam = cam.squeeze().detach().cpu().numpy()
        cam = (cam - np.min(cam)) / (np.max(cam) - np.min(cam) + 1e-8)
        return cam

    def cleanup(self):
        for h in self.hook_handles:
            h.remove()

def overlay_heatmap_to_base64(orig_pil: Image.Image, cam_mask: np.ndarray) -> str:
    """
    Overlays a Grad-CAM heatmap on the original image and returns a base64 encoded PNG data URI.
    """
    # Resize mask to original image dimensions
    w, h = orig_pil.size
    mask_pil = Image.fromarray((cam_mask * 255).astype(np.uint8)).resize((w, h), Image.Resampling.BILINEAR)
    mask_np = np.array(mask_pil) / 255.0

    # Colorize mask with Jet/Turbo-like colormap manually (avoid heavy matplotlib dependency)
    # Simple RGB ramp: blue (low) -> cyan -> yellow -> red (high)
    r = np.clip(1.5 - np.abs(mask_np * 4.0 - 3.0), 0.0, 1.0)
    g = np.clip(1.5 - np.abs(mask_np * 4.0 - 2.0), 0.0, 1.0)
    b = np.clip(1.5 - np.abs(mask_np * 4.0 - 1.0), 0.0, 1.0)
    heatmap = np.stack([r, g, b], axis=-1) * 255.0

    orig_np = np.array(orig_pil, dtype=np.float32)
    alpha = 0.4
    blended = (1.0 - alpha) * orig_np + alpha * heatmap
    blended = np.clip(blended, 0, 255).astype(np.uint8)

    buf = io.BytesIO()
    Image.fromarray(blended).save(buf, format="PNG")
    b64_str = base64.b64encode(buf.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{b64_str}"
