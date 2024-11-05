import os
import nibabel as nib
import numpy as np
from skimage.transform import resize

def resize_nii(input_folder, output_folder, target_shape=(128, 128)):
    """
    Resizes all .nii.gz files in the input folder to the specified shape and saves them in the output folder.
    
    Args:
        input_folder (str): Path to the folder containing .nii.gz files.
        output_folder (str): Path to the folder where resized .nii.gz files will be saved.
        target_shape (tuple): Target in-plane shape (x, y) to resize each slice. Defaults to (128, 128).
    """
    os.makedirs(output_folder, exist_ok=True)

    adc_files = [f for f in sorted(os.listdir(input_folder)) if f.endswith('.nii.gz') and '0001' in f]
    dwi_files = [f for f in sorted(os.listdir(input_folder)) if f.endswith('.nii.gz') and '0000' in f]

    if len(adc_files) != len(dwi_files):
        print("ADC and DWI do not have the same number of files.")
        return

    for adc_filename, dwi_filename in zip(adc_files, dwi_files):
        adc_filepath = os.path.join(input_folder, adc_filename)
        dwi_filepath = os.path.join(input_folder, dwi_filename)
        
        adc_nii = nib.load(adc_filepath)
        dwi_nii = nib.load(dwi_filepath)
        
        adc_data = adc_nii.get_fdata()
        dwi_data = dwi_nii.get_fdata()

        # Compare shape and voxel sizes
        if adc_data.shape != dwi_data.shape:
            print(f"Shape mismatch between ADC ({adc_filename}) and DWI ({dwi_filename}).")
            continue  # Skip resizing if shapes do not match

        adc_voxel_size = adc_nii.header.get_zooms()
        dwi_voxel_size = dwi_nii.header.get_zooms()
        
        if adc_voxel_size != dwi_voxel_size:
            print(f"Voxel size mismatch between ADC ({adc_filename}) and DWI ({dwi_filename}).")
            print(f"ADC voxel size: {adc_voxel_size}, DWI voxel size: {dwi_voxel_size}")
            continue  # Skip resizing if voxel sizes do not match

        # Resize ADC data
        z_adc = adc_data.shape[-1]
        resized_adc_data = resize(adc_data, (target_shape[0], target_shape[1], z_adc))
        resized_adc_nii = nib.Nifti1Image(resized_adc_data, affine=adc_nii.affine)
        adc_output_path = os.path.join(output_folder, adc_filename)
        nib.save(resized_adc_nii, adc_output_path)
        print(f"Resized {adc_filename} and saved to {adc_output_path}")

        # Resize DWI data
        z_dwi = dwi_data.shape[-1]
        resized_dwi_data = resize(dwi_data, (target_shape[0], target_shape[1], z_dwi))
        resized_dwi_nii = nib.Nifti1Image(resized_dwi_data, affine=dwi_nii.affine)
        dwi_output_path = os.path.join(output_folder, dwi_filename)
        nib.save(resized_dwi_nii, dwi_output_path)
        print(f"Resized {dwi_filename} and saved to {dwi_output_path}")

# Example usage:
input_folder = '/Users/nadjagruber/Documents/Stroke_Kardio/nnunet_kardio'
output_folder = '/Users/nadjagruber/Documents/Stroke_Kardio/nnunet_kardio_resized_correct'
resize_nii(input_folder, output_folder)
