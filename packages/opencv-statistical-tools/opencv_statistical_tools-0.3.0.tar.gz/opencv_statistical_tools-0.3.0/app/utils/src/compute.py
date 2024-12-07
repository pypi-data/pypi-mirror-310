
import cv2
import importlib.resources
from pathlib import Path
import requests
import numpy as np

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

image_urls = {
    "S1_Frontal.jpg": "https://github.com/saifaldin14/ObjectRecognitionImages/blob/main/S1_Frontal.jpg?raw=true",
    "S1_Left.jpg": "https://github.com/saifaldin14/ObjectRecognitionImages/blob/main/S1_Left.jpg?raw=true",
    "S1_Right.jpg": "https://github.com/saifaldin14/ObjectRecognitionImages/blob/main/S1_Right.jpg?raw=true",
    "S2_Frontal.jpg": "https://github.com/saifaldin14/ObjectRecognitionImages/blob/main/S2_Frontal.jpg?raw=true",
    "S2_Left.jpg": "https://github.com/saifaldin14/ObjectRecognitionImages/blob/main/S2_Left.jpg?raw=true",
    "S2_Right.jpg": "https://github.com/saifaldin14/ObjectRecognitionImages/blob/main/S2_Right.jpg?raw=true",
    "S3_Frontal.jpg": "https://github.com/saifaldin14/ObjectRecognitionImages/blob/main/S3_Frontal.jpg?raw=true",
    "S3_Left.jpg": "https://github.com/saifaldin14/ObjectRecognitionImages/blob/main/S3_Left.jpg?raw=true",
    "S3_Right.jpg": "https://github.com/saifaldin14/ObjectRecognitionImages/blob/main/S3_Right.jpg?raw=true",
    "S4_Frontal.jpg": "https://github.com/saifaldin14/ObjectRecognitionImages/blob/main/S4_Frontal.jpg?raw=true",
    "S4_Left.jpg": "https://github.com/saifaldin14/ObjectRecognitionImages/blob/main/S4_Left.jpg?raw=true",
    "S4_Right.jpg": "https://github.com/saifaldin14/ObjectRecognitionImages/blob/main/S4_Right.jpg?raw=true",
    "S5_Frontal.jpg": "https://github.com/saifaldin14/ObjectRecognitionImages/blob/main/S5_Frontal.jpg?raw=true",
    "S5_Left.jpg": "https://github.com/saifaldin14/ObjectRecognitionImages/blob/main/S5_Left.jpg?raw=true",
    "S5_Right.jpg": "https://github.com/saifaldin14/ObjectRecognitionImages/blob/main/S5_Right.jpg?raw=true",
    "S6_Frontal.jpg": "https://github.com/saifaldin14/ObjectRecognitionImages/blob/main/S6_Frontal.jpg?raw=true",
    "S6_Left.jpg": "https://github.com/saifaldin14/ObjectRecognitionImages/blob/main/S6_Left.jpg?raw=true",
    "S6_Right.jpg": "https://github.com/saifaldin14/ObjectRecognitionImages/blob/main/S6_Right.jpg?raw=true",
    "S7_Frontal.jpg": "https://github.com/saifaldin14/ObjectRecognitionImages/blob/main/S7_Frontal.jpg?raw=true",
    "S7_Left.jpg": "https://github.com/saifaldin14/ObjectRecognitionImages/blob/main/S7_Left.jpg?raw=true",
    "S7_Right.jpg": "https://github.com/saifaldin14/ObjectRecognitionImages/blob/main/S7_Right.jpg?raw=true",
    "S8_Frontal.jpg": "https://github.com/saifaldin14/ObjectRecognitionImages/blob/main/S8_Frontal.jpg?raw=true",
    "S8_Left.jpg": "https://github.com/saifaldin14/ObjectRecognitionImages/blob/main/S8_Left.png?raw=true",
    "S8_Right.jpg": "https://github.com/saifaldin14/ObjectRecognitionImages/blob/main/S8_Right.jpg?raw=true",
    "S9_Frontal.jpg": "https://github.com/saifaldin14/ObjectRecognitionImages/blob/main/S9_Frontal.jpg?raw=true",
    "S9_Left.jpg": "https://github.com/saifaldin14/ObjectRecognitionImages/blob/main/S9_Left.jpg?raw=true",
    "S9_Right.jpg": "https://github.com/saifaldin14/ObjectRecognitionImages/blob/main/S9_Right.jpg?raw=true",
    "S10_Frontal.jpg": "https://github.com/saifaldin14/ObjectRecognitionImages/blob/main/S10_Frontal.jpg?raw=true",
    "S10_Left.jpg": "https://github.com/saifaldin14/ObjectRecognitionImages/blob/main/S10_Left.jpg?raw=true",
    "S10_Right.jpg": "https://github.com/saifaldin14/ObjectRecognitionImages/blob/main/S10_Right.jpg?raw=true"
}

def calculate_hsv_hist(image_name, original_image):
    """
    Calculate HSV histogram for an image bundled in the package.
    """
    try:
        # Retrieve the image URL
        image_url = image_urls.get(image_name)
        if not image_url:
            raise ValueError(f"Image {image_name} not found in URL mapping.")

        # Download the image
        response = requests.get(image_url)
        if response.status_code != 200:
            raise ValueError(f"Failed to download image {image_name} from {image_url}. HTTP status code: {response.status_code}")
        
        # Convert the image data to a numpy array
        image_data = np.frombuffer(response.content, np.uint8)

        # Decode the image using OpenCV
        image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError(f"Failed to decode image {image_name} from URL.")

        threshold = ground_truth[image_name]
        return original_image, image, threshold
    except Exception as e:
        print(f"Error: {e}")
        return