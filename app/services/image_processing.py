import base64
import io
from PIL import Image
import cv2
import numpy as np

def preprocess_image(image_data: bytes) -> str:
    """
    Pre-processes an image for OCR.
    - Converts to grayscale
    - Resizes for better processing (optional, can be adjusted)
    - Returns base64 encoded image
    """
    # Convert bytes to a numpy array
    nparr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img is None:
        raise ValueError("Could not decode image data.")

    # Convert to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Resize (optional, adjust dimensions as needed)
    # For example, resize to a consistent width while maintaining aspect ratio
    # target_width = 1000
    # (h, w) = gray_img.shape[:2]
    # r = target_width / float(w)
    # dim = (target_width, int(h * r))
    # resized_img = cv2.resize(gray_img, dim, interpolation=cv2.INTER_AREA)

    # Convert back to PIL Image to save to bytes
    pil_img = Image.fromarray(gray_img)
    buffered = io.BytesIO()
    pil_img.save(buffered, format="JPEG") # Save as JPEG for base64 encoding
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def is_valid_image(image_data: bytes) -> bool:
    """
    Checks if the provided bytes represent a valid image.
    """
    try:
        Image.open(io.BytesIO(image_data)).verify()
        return True
    except Exception:
        return False
