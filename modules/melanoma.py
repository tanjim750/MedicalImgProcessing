import cv2
import numpy as np
import matplotlib.pyplot as plt

from PIL import Image
import io
from django.core.files.base import ContentFile

class Melanoma:
    def process(self,image):
        img = cv2.imread(image)

        if img is None:
            raise IOError("Image not found")
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        clahe_img = clahe.apply(gray)

        # Apply median filtering to reduce noise
        median_filtered = cv2.medianBlur(clahe_img, 5)

        # Apply Otsu's thresholding to segment the lesion
        _, binary_img = cv2.threshold(median_filtered, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # Apply morphological operations to enhance the lesion extraction
        kernel = np.ones((3, 3), np.uint8)
        morphed = cv2.morphologyEx(binary_img, cv2.MORPH_CLOSE, kernel, iterations=2)
        morphed = cv2.morphologyEx(morphed, cv2.MORPH_OPEN, kernel, iterations=2)

        # Further refine the lesion by removing small noise
        contours, _ = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            if cv2.contourArea(cnt) < 100:
                cv2.drawContours(morphed, [cnt], 0, (0, 0, 0), -1)

        # Convert the processed image to a format suitable for saving
        pil_img = Image.fromarray(morphed)
        buffer = io.BytesIO()
        pil_img.save(buffer, format="PNG")
        image_binary = buffer.getvalue()

        return ContentFile(image_binary, name="processed_image.png")
