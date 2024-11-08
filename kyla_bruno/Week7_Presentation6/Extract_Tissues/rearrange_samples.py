import os
import shutil
from pathlib import Path

def merge_folders(source_dir, destination_dir):
    # Create the destination directory if it doesn't exist
    Path(destination_dir).mkdir(parents=True, exist_ok=True)

    # Iterate through each subfolder in the source directory
    for subfolder in os.listdir(source_dir):
        subfolder_path = os.path.join(source_dir, subfolder)
        
        # Only process if it's a directory
        if os.path.isdir(subfolder_path):
            # Extract the unique image ID and stain type (before and after the first underscore)
            parts = subfolder.split('_')
            if len(parts) < 2:
                continue
            image_id = parts[0]
            stain_type = parts[1].split(' -')[0]  # Extract stain type before " - Series 0"

            # Create a new folder name with the unique image ID followed by "_tissues"
            new_folder_name = f"{image_id}_tissues"
            new_folder_path = os.path.join(destination_dir, new_folder_name)
            
            # Create the new merged directory if it doesn't exist
            Path(new_folder_path).mkdir(parents=True, exist_ok=True)

            # Iterate over .tif files in the subfolder
            for file_name in os.listdir(subfolder_path):
                if file_name.endswith(".tif"):
                    # Extract the t# from the original file name (before the .tif extension)
                    t_number = file_name.split('_')[-1].replace('.tif', '')

                    # New file name format: "<image_id>_<stain_type>_<t_number>.tif"
                    new_file_name = f"{image_id}_{stain_type}_{t_number}.tif"
                    old_file_path = os.path.join(subfolder_path, file_name)
                    new_file_path = os.path.join(new_folder_path, new_file_name)

                    # Copy and rename the .tif file
                    shutil.copy2(old_file_path, new_file_path)

    print(f"Folders merged and files renamed in '{destination_dir}'.")

# Set the source and destination directories
source_dir = os.path.join(os.getcwd(), 'Tissues')
destination_dir = os.path.join(os.getcwd(), 'Sheffield_Samples')

# Run the merge function
merge_folders(source_dir, destination_dir)
