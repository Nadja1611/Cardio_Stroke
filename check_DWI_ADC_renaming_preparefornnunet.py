import os
import nibabel as nib
import shutil

# Define the input and output directories
input_dir = '/Users/nadjagruber/Documents/Stroke_Kardio/ADS_data_nii/'
output_dir = '/Users/nadjagruber/Documents/Stroke_Kardio/ADS_data_selected/'

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

for sub in os.listdir(input_dir):
    # Skip irrelevant files like '.DS_Store' or Excel files
    if sub != '.DS_Store' and '.xlsx' not in sub:
        output_folder = os.path.join(input_dir, sub)
        files = os.listdir(output_folder)

        # Check for sufficient files
        if len(files) < 2:
            print(f"Insufficient files in folder {output_folder}")
            continue

        # Check if both files are NIfTI files
        if all(file.endswith(('.nii', '.nii.gz')) for file in files):
            print(f"Both files are NIfTI files in {output_folder}")
        else:
            print(f"Both files are not NIfTI files in {output_folder}")
            continue  # Skip to the next folder if both files are not NIfTI files

        # Check for too many files
        if len(files) > 2:
            print(f"Too many files in folder {output_folder}")

        # Create the subject-specific output folder
        subject_output_folder = os.path.join(output_dir, sub)
        #os.makedirs(subject_output_folder, exist_ok=True)

        # Initialize flags to check if both ADC and DWI files are found
        adc_found, dwi_found = False, False

        for file in files:
            if 'ADC.nii.gz' in file:
                # Load and print details of ADC file
                adc_path = os.path.join(output_folder, file)
                adc = nib.load(adc_path)
                print(f"ADC File: {file}")
                print("ADC Voxel Dimensions:", adc.header.get_zooms())
                print("ADC Shape:", adc.get_fdata().shape)

                # Copy ADC file to output directory with new name "0001.nii.gz"
                new_adc_path = os.path.join(output_dir, file[:-11] + '_0001.nii.gz')
                adc_found = True

            if 'DWI.nii.gz' in file:
                # Load and print details of DWI file
                dwi_path = os.path.join(output_folder, file)
                dwi = nib.load(dwi_path)
                print(f"DWI File: {file}")
                print("DWI Voxel Dimensions:", dwi.header.get_zooms())
                print("DWI Shape:", dwi.get_fdata().shape)

                # Copy DWI file to output directory with new name "0000.nii.gz"
                new_dwi_path = os.path.join(output_dir, file[:-11] + '_0000.nii.gz')
                dwi_found = True

        # Check if both ADC and DWI files were found and copied
        if adc_found and dwi_found and adc.get_fdata().shape == dwi.get_fdata().shape and dwi.header.get_zooms() == adc.header.get_zooms():
            print(f"Both ADC and DWI files from {output_folder} copied and renamed in {subject_output_folder}")
            shutil.copy(adc_path, new_adc_path)
            shutil.copy(dwi_path, new_dwi_path)
        else:
            print('for ' + file + ' something does not fit')   

