# Define source folders and destination folder
source_folders = ['processed_data/sheffield_h&e', 'processed_data/sheffield_melan', 'processed_data/sheffield_sox10']
destination_folder = 'matching_test_data'

# Create dictionary to hold lists of images by patient
image_groups = {}

# Loop through each folder
for folder in source_folders:
    for filename in os.listdir(folder):
        if os.path.isfile(os.path.join(folder, filename)):
            patient = filename[:8]
            if patient not in image_groups:
                image_groups[patient] = []
            image_groups[patient].append(os.path.join(folder, filename))

# Create new folders and copy images
for patient, images in image_groups.items():
    new_folder_path = os.path.join(destination_folder, patient)
    os.makedirs(new_folder_path, exist_ok=True)
    
    # Copy each image into new folders
    for image in images:
        shutil.copy2(image, new_folder_path)
