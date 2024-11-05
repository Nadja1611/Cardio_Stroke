import os
import shutil
import nibabel as nib
# Paths to your source and destination folders
source_dir = "/Users/nadjagruber/Documents/Stroke_Kardio/DATA_JHT"  # replace with the actual path
destination_dir = "/Users/nadjagruber/Documents/Stroke_Kardio/nnunet_kardio"  # replace with the actual path

# Ensure the destination directory exists
os.makedirs(destination_dir, exist_ok=True)

# Loop through each subject folder
for subject_folder in os.listdir(source_dir):
    if subject_folder.startswith('Sub'):
        subject_path = os.path.join(source_dir, subject_folder)
        if os.path.isdir(subject_path):
            try:
                print(subject_folder)
                # Define paths for DWI and ADC files
                dwi_file = os.path.join(subject_path, f"{subject_folder}_DWI.nii.gz")
                dat_dwi = nib.load(dwi_file).get_fdata()
                print(dat_dwi.shape)
                adc_file = os.path.join(subject_path, f"{subject_folder}_ADC.nii.gz")
                dat_adc = nib.load(adc_file).get_fdata()
                print(dat_adc.shape)                
                # Define new names for the files
                new_dwi_name = f"{subject_folder}_0000.nii.gz"
                new_adc_name = f"{subject_folder}_0001.nii.gz"
                
                # Copy files with new names to the destination folder
                shutil.copy(dwi_file, os.path.join(destination_dir, new_dwi_name))
                shutil.copy(adc_file, os.path.join(destination_dir, new_adc_name))
            except:
                pass    

print("Files copied and renamed successfully!")
