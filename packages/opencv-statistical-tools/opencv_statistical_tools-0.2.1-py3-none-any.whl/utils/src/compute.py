
import cv2
import importlib.resources
from pathlib import Path

ground_truth = {
    "S1_Frontal.jpg": ["O10"],
    "S1_Left.jpg": ["O10"],
    "S1_Right.jpg": ["O10"],
    "S2_Frontal.jpg": ["O10", "O3"],
    "S2_Left.jpg": ["O10", "O3"],
    "S2_Right.jpg": ["O10", "O3"],
    "S3_Frontal.jpg": ["O10", "O3", "O2"],
    "S3_Left.jpg": ["O10", "O3", "O2"],
    "S3_Right.jpg": ["O10", "O3", "O2"],
    "S4_Frontal.jpg": ["O10", "O3", "O2", "O1"],
    "S4_Left.jpg": ["O10", "O3", "O2", "O1"],
    "S4_Right.jpg": ["O10", "O3", "O2", "O1"],
    "S5_Frontal.jpg": ["O10", "O3", "O2", "O1", "O7"],
    "S5_Left.jpg": ["O10", "O3", "O2", "O1", "O7"],
    "S5_Right.jpg": ["O10", "O3", "O2", "O1", "O7"],
    "S6_Frontal.jpg": ["O10", "O3", "O2", "O1", "O7", "O6"],
    "S6_Left.jpg": ["O10", "O3", "O2", "O1", "O7", "O6"],
    "S6_Right.jpg": ["O10", "O3", "O2", "O1", "O7", "O6"],
    "S7_Frontal.jpg": ["O10", "O3", "O2", "O1", "O7", "O6", "O8"],
    "S7_Left.jpg": ["O10", "O3", "O2", "O1", "O7", "O6", "O8"],
    "S7_Right.jpg": ["O10", "O3", "O2", "O1", "O7", "O6", "O8"],
    "S8_Frontal.jpg": ["O10", "O3", "O2", "O1", "O7", "O6", "O8", "O5"],
    "S8_Left.jpg": ["O10", "O3", "O2", "O1", "O7", "O6", "O8", "O5"],
    "S8_Right.jpg": ["O10", "O3", "O2", "O1", "O7", "O6", "O8", "O5"],
    "S9_Frontal.jpg": ["O10", "O3", "O2", "O1", "O7", "O6", "O8", "O5", "O4"],
    "S9_Left.jpg": ["O10", "O3", "O2", "O1", "O7", "O6", "O8", "O5", "O4"],
    "S9_Right.jpg": ["O10", "O3", "O2", "O1", "O7", "O6", "O8", "O5", "O4"],
    "S10_Frontal.jpg": ["O10", "O3", "O2", "O1", "O7", "O6", "O8", "O5", "O4", "O9"],
    "S10_Left.jpg": ["O10", "O3", "O2", "O1", "O7", "O6", "O8", "O5", "O4", "O9"],
    "S10_Right.jpg": ["O10", "O3", "O2", "O1", "O7", "O6", "O8", "O5", "O4", "O9"]
}

def calculate_hsv_hist(image_name, original_image):
    """
    Calculate HSV histogram for an image bundled in the package.
    """
    try:
        # Access the image from the package
        with importlib.resources.path('app.Scenes', image_name) as image_path:
            image_path = str(image_path)  # Convert Path to string for OpenCV
            print(f"Image path: {image_path}")

            # Load the image
            image = cv2.imread(image_path)
            if image is None:
                print(f"Error: Image {image_name} could not be loaded.")
                return

            # Perform histogram calculation
            noise_histogram = cv2.calcHist([image], [1], None, [256], [0, 256])
            threshold = ground_truth[image_name]
            print(f"Threshold: {threshold}")

            return original_image, image, threshold
    except Exception as e:
        print(f"Error: {e}")
        return