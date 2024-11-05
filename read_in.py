import nibabel as nib
import numpy as np
import os

# Define paths for predictions and inputs
prediction_path = '/Users/nadjagruber/Documents/Stroke_Kardio/predictions_nnunet3d'
input_path = '/Users/nadjagruber/Documents/Stroke_Kardio/ADS_data_selected'
output_nii_path = '/Users/nadjagruber/Documents/Stroke_Kardio/combined_nii_files'

# Create output directory if it does not exist
os.makedirs(output_nii_path, exist_ok=True)

# Get list of prediction files and filter only NIfTI files
list_pred = sorted(os.listdir(prediction_path))
filtered_list = [s for s in list_pred if 'nii.gz' in s]

# Get list of input files (DWI) and filter by convention "_0000.nii.gz"
list_inp = sorted(os.listdir(input_path))
inp_list = [s for s in list_inp if '0000' in s]

# Sort both lists to ensure matching order
filtered_list = sorted(filtered_list, key=lambda s: s.split('.')[0])
inp_list = sorted(inp_list, key=lambda s: s.split('_')[0])

# Match DWI files to predictions
dwi_files = []
for pred_file in filtered_list:
    matching_dwi_file = pred_file.split('.')[0] + '_0000.nii.gz'
    if matching_dwi_file in inp_list:
        dwi_files.append(matching_dwi_file)

# Loop over matched DWI and prediction files
for i in range(len(dwi_files)):
    # Load DWI and prediction data
    dwi_img = nib.load(os.path.join(input_path, dwi_files[i]))
    dwi_data = dwi_img.get_fdata()

    prediction_img = nib.load(os.path.join(prediction_path, filtered_list[i]))
    prediction_data = prediction_img.get_fdata()

    # Ensure DWI and prediction have the same shape
    if dwi_data.shape != prediction_data.shape:
        print(f"Shape mismatch for {dwi_files[i]} and {filtered_list[i]}")
        continue

    # Normalize DWI to a suitable range (0-255) for grayscale background
    dwi_normalized = (dwi_data - np.min(dwi_data)) / (np.max(dwi_data) - np.min(dwi_data)) * 255
    dwi_normalized = dwi_normalized.astype(np.uint8)

    # Create the red overlay as a single-channel mask
    overlay = np.zeros_like(dwi_normalized, dtype=np.uint8)
    overlay[prediction_data > 0] = 255  # Max intensity for areas of interest

    # Create a combined image where the overlay is applied
    combined_data = np.maximum(dwi_normalized, overlay)  # Use max to combine

    # Create a new NIfTI image with the same affine and header as the DWI
    combined_img = nib.Nifti1Image(combined_data, affine=dwi_img.affine, header=dwi_img.header)

    # Save the combined NIfTI file
    combined_nii_save_path = os.path.join(output_nii_path, f'combined_overlay_{dwi_files[i]}')
    nib.save(combined_img, combined_nii_save_path)
    
    print(f"Saved combined overlay NIfTI for {dwi_files[i]} and {filtered_list[i]} at {combined_nii_save_path}")
