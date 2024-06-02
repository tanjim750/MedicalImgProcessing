import cv2
import numpy as np
import matplotlib.pyplot as plt

from PIL import Image
import io
from django.core.files.base import ContentFile

class EyeFundus:
    def process(self,image):
        img = cv2.imread(image)

        # Extract the green channel
        green_channel = img[:, :, 1]

        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        clahe_img = clahe.apply(green_channel)

        # Apply median filtering to reduce noise
        median_filtered = cv2.medianBlur(clahe_img, 5)

        # Apply adaptive thresholding
        binary_img = cv2.adaptiveThreshold(median_filtered, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                        cv2.THRESH_BINARY_INV, 11, 3)

        # Apply morphological operations to enhance the blood vessels
        kernel = np.ones((2, 2), np.uint8)
        morphed = cv2.morphologyEx(binary_img, cv2.MORPH_OPEN, kernel, iterations=1)
        morphed = cv2.morphologyEx(morphed, cv2.MORPH_CLOSE, kernel, iterations=2)

        # Apply erosion to thin the white lines
        thinned = cv2.erode(morphed, kernel, iterations=1)

        # Convert the processed image to a format suitable for saving
        pil_img = Image.fromarray(thinned)
        buffer = io.BytesIO()
        pil_img.save(buffer, format="PNG")
        image_binary = buffer.getvalue()

        return ContentFile(image_binary, name="processed_image.png")

