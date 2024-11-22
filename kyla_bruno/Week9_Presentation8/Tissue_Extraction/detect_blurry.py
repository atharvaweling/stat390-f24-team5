import os
import cv2

# Set the root directory containing subfolders of images
root_dir = "./"  # Update with your directory path

# Define the variance threshold for blur detection
threshold = 50  # Adjust this value as needed

def is_blurry(image_path, threshold):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        return False  # Skip non-image files
    variance = cv2.Laplacian(image, cv2.CV_64F).var()
    return variance < threshold

for subdir, _, files in os.walk(root_dir):
    for file in files:
        file_path = os.path.join(subdir, file)
        if is_blurry(file_path, threshold):
            os.remove(file_path)
            print(f"Deleted blurry image: {file_path}")
