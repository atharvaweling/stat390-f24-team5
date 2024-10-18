import cv2
import os
import numpy as np
from comparison_algorithm_functions import compare_contours 

# helper function
def resize_image(image1, image2):
    height1, width1 = image1.shape[:2]
    height2, width2 = image2.shape[:2]
    
    if height1 != height2 or width1 != width2:
        # Resize image2 to match image1's dimensions
        image2_resized = cv2.resize(image2, (width1, height1))
        return image1, image2_resized
    else:
        return image1, image2


# apply to a single patients images
def process_patient_images(patient_folder, white_threshold=220, similarity_threshold=90):
    image_files = [f for f in os.listdir(patient_folder) if f.endswith('.tif')]
    
    similarity_results = []
    
    for i in range(len(image_files)):
        for j in range(i+1, len(image_files)): # adjust later on!!
            image1_path = os.path.join(patient_folder, image_files[i])
            image2_path = os.path.join(patient_folder, image_files[j])
            
            image1 = cv2.imread(image1_path)
            image2 = cv2.imread(image2_path)
            
            # results
            similarity_score = compare_contours(image1, image2, white_threshold)
            similarity_results.append((image_files[i], image_files[j], similarity_score))
            
            # Show image pairs
            if similarity_score < similarity_threshold:
                print(f"Displaying similar images: {image_files[i]} and {image_files[j]}")
                
                image1_resized, image2_resized = resize_image(image1, image2)
                combined_image = np.hstack([image1_resized, image2_resized])

                cv2.imshow(f"Comparison: {image_files[i]} and {image_files[j]}", combined_image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
    
    return similarity_results


# apply to entire folder of patients with multiple stains
def process_all_patients(base_directory, white_threshold=220, similarity_threshold= 95):  # can adjust similarity score cutoff
    patient_folders = [os.path.join(base_directory, d) for d in os.listdir(base_directory) if os.path.isdir(os.path.join(base_directory, d))]
    
    all_similarity_results = {}
    
    for patient_folder in patient_folders:
        patient_id = os.path.basename(patient_folder)
        print(f"Processing patient folder: {patient_id}")
        
        similarity_results = process_patient_images(patient_folder, white_threshold, similarity_threshold)
        all_similarity_results[patient_id] = similarity_results
    
    return all_similarity_results


# RUN ALL TOGETHER
base_directory = "Sheffield_Samples/has_multiple"
all_results = process_all_patients(base_directory, white_threshold=220, similarity_threshold=90)

# store results
with open("similarity_results.txt", "w") as result_file:
    for patient_id, results in all_results.items():
        result_file.write(f"Results for {patient_id}:\n")
        for image1, image2, score in results:
            result_file.write(f"{image1} vs {image2}: Similarity score = {score:.2f}\n")
