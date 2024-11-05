import os
import shutil


# Set the paths for the source and target directories
source_directory = '/Users/nadjagruber/Documents/Stroke_Kardio/ADS_data_nii'
target_directory = '/Users/nadjagruber/Documents/Stroke_Kardio/DATA_JHT'

# Ensure the target directory exists
os.makedirs(target_directory, exist_ok=True)

# Iterate through each folder in the source directory
for folder_name in os.listdir(source_directory):
    folder_path = os.path.join(source_directory, folder_name)
    
    # Check if it's a directory
    if os.path.isdir(folder_path):
        # Count the number of files in the folder
        file_count = len([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])
        
        # If there are exactly 3 files, copy the folder to the target directory
        if file_count == 3:
            shutil.copytree(folder_path, os.path.join(target_directory, folder_name))
            print(f"Copied: {folder_name}")
