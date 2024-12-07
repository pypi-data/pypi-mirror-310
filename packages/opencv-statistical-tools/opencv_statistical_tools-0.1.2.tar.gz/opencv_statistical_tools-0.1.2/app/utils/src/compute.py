
import cv2
import os

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

def calculate_hsv_hist(image_name, original_image, points=[], label=None, color=(255, 0, 0), thickness=2):
    """
    Draws a bounding box on the specified image from the provided folder.

    Args:
        image_folder (str): Path to the folder containing the images.
        image_name (str): Name of the image to retrieve and modify.
        points (list or ndarray): Four points representing the corners of the bounding box.
        label (str, optional): Label to add to the bounding box. Defaults to None.
        color (tuple, optional): Color of the bounding box in BGR. Defaults to (255, 0, 0).
        thickness (int, optional): Thickness of the bounding box lines. Defaults to 2.

    Returns:
        image: The modified image with the bounding box and label drawn.
    """
    # Construct the full image path
    image_path = f"../Scenes/{image_name}"
    
    # Check if the image exists
    if not os.path.exists(image_path):
        return
    
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        return
    
    noise_histogram = cv2.calcHist([image], [1], None, [256], [0, 256])
    threshold = ground_truth[image_name]

    return original_image, image, threshold