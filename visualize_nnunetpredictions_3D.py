import nibabel as nib
import numpy as np
import os
import matplotlib.pyplot as plt

# Define paths for predictions and inputs
prediction_path = '/Users/nadjagruber/Documents/Stroke_Kardio/predictions_nnunet3d'
input_path = '/Users/nadjagruber/Documents/Stroke_Kardio/ADS_data_selected'
output_nii_path = '/Users/nadjagruber/Documents/Stroke_Kardio/combined_overlay_nii_files'
output_plot_path = '/Users/nadjagruber/Documents/Stroke_Kardio/plots'  # Folder to save plots

# Create output directories if they do not exist
os.makedirs(output_nii_path, exist_ok=True)
os.makedirs(output_plot_path, exist_ok=True)

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

    # Create a red overlay
    overlay = np.zeros((*dwi_normalized.shape, 3), dtype=np.uint8)  # Create a 3D RGB array
    overlay[prediction_data > 0] = [255, 0, 0]  # Set overlay to red where prediction is non-zero

    # Blend the DWI and overlay with transparency
    alpha = 0.5  # Set alpha for transparency (0: fully transparent, 1: fully opaque)
    combined_rgb = np.clip(dwi_normalized[..., np.newaxis] + overlay * alpha, 0, 255).astype(np.uint8)

    # Create a new NIfTI image with the combined RGB data
    combined_img = nib.Nifti1Image(combined_rgb, affine=dwi_img.affine, header=dwi_img.header)

    # Save the combined NIfTI file
    combined_nii_save_path = os.path.join(output_nii_path, f'combined_overlay_{dwi_files[i]}')
    nib.save(combined_img, combined_nii_save_path)

    # Plotting the images
    slice_index = 15  # You can change this to visualize a different slice
    plt.figure(figsize=(10, 5))

    # Plot the DWI image
    plt.subplot(1, 2, 1)
    plt.imshow(dwi_normalized[:, :, slice_index], cmap='gray')
    plt.title('DWI Image')
    plt.axis('off')

    # Plot the overlay
    plt.subplot(1, 2, 2)
    plt.imshow(combined_rgb[:, :, slice_index])
    plt.title('DWI with Segmentation Overlay')
    plt.axis('off')

    # Save the plot
    plt.savefig(os.path.join(output_plot_path, f'combined_overlay_plot_{dwi_files[i][:-7]}.png'))
    plt.close()

    print(f"Saved combined overlay NIfTI for {dwi_files[i]} and {filtered_list[i]} at {combined_nii_save_path}")
