import os
import nibabel as nib
import numpy as np
from skimage.transform import resize

def resize_nii(input_folder,target_shape=(128, 128)):
    """
    Resizes all .nii.gz files in the input folder to the specified shape and saves them in the output folder.
    
    Args:
        input_folder (str): Path to the folder containing .nii.gz files.
        output_folder (str): Path to the folder where resized .nii.gz files will be saved.
        target_shape (tuple): Target in-plane shape (x, y) to resize each slice. Defaults to (128, 128).
    """
    
    for filename in os.listdir(input_folder):
        if filename.endswith('.nii.gz'):
            filepath = os.path.join(input_folder, filename)
            nii = nib.load(filepath)
            data = nii.get_fdata()
            if len(data.shape)>3:
                print('error')
            print(data.shape)
            if len((data.shape))==3:
                print('stop')
                print(nii)
            # Calculate resize factors
            
                z = data.shape[-1]
            # Resize data
                resized_data = resize(data, (128,128, z))  # order=1 for bilinear interpolation
            
            # Save the resized 
                resized_nii = nib.Nifti1Image(resized_data, affine=nii.affine)

# Example usage:
input_folder = '/Users/nadjagruber/Documents/Stroke_Kardio/test'
resize_nii(input_folder)
