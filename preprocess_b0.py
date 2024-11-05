import os
import pandas as pd
import pydicom
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt

# Load the Excel file
excel_path = '/Users/nadjagruber/Documents/Stroke_Kardio/ADS_data_nii/patient_index_mapping.xlsx'  # Replace with the path to your Excel file
df = pd.read_excel(excel_path)

# Define the folder where you want to save the NIfTI files
save_folder = '/Users/nadjagruber/Documents/Stroke_Kardio/ADS_data_nii/'  # Replace with the actual save folder path
img = []
path = '/Users/nadjagruber/Documents/Stroke_Kardio/b0'
files = os.listdir(path)

for f in files[:]:
    if f != '.DS_Store':
        print(f)
        dcm_dir = os.path.join(path, f)
        for dcm in os.listdir(dcm_dir):
            dat = pydicom.dcmread(os.path.join(dcm_dir, dcm))
            
            print(dat.SequenceName)
            if 'ep_b0' in dat.SequenceName:
                img.append(dat)

                # Extract the mosaic image data
                mosaic_data = dat.pixel_array

                # Get the number of slices in the mosaic
                try:
                    num_slices = dat[0x0019, 0x100A].value  # (0019,100A) is the tag for the number of images in the mosaic

                    # Determine the size of each slice
                    image_size = dat.Rows  # Assuming Rows and Columns are equal for individual slices
                    slice_size = mosaic_data.shape[1]//7

                    # Reshape the mosaic into individual slices
                    slices = []
                    for i in range(num_slices):
                        row = (i // (mosaic_data.shape[1] // slice_size))
                        col = (i % (mosaic_data.shape[1] // slice_size))
                        
                        # Extract the slice from the mosaic
                        slice_img = mosaic_data[
                            row * slice_size:(row + 1) * slice_size,
                            col * slice_size:(col + 1) * slice_size
                        ]
                        
                        # Rotate the slice by 90 degrees (counterclockwise)
                        rotated_slice = np.rot90(np.rot90(np.rot90(slice_img)))
                        
                        slices.append(rotated_slice)

    

                    # Reverse the order of the slices
                    slices_reversed = slices[::-1]

                    # Stack reversed slices into a 3D volume
                    volume_3d = np.stack(slices_reversed[:int(num_slices)], axis=-1)  # Stack along the third dimension


                    # Create a NIfTI image
                    affine = np.eye(4)  # Identity matrix for affine; modify if needed
                    nii_img = nib.Nifti1Image(volume_3d, affine)

                    # Find the incognito name (number) based on the original path from the Excel file
                    matching_row = df[df['Patient_Folder'].str.contains(f)]  # Assuming column 1 is named 'Path'
                    if not matching_row.empty:
                        incognito_name = str(matching_row.iloc[0, 1])  # Assuming incognito name is in the second column
                        save_folder_new = os.path.join(save_folder,'Subject0' + incognito_name)
                        # Save the NIfTI image to the new folder with the incognito name
                        output_path = os.path.join(save_folder_new, 'Subject0' + f"{incognito_name}_b0.nii.gz")
                        nib.save(nii_img, output_path)
                        print(f"Saved NIfTI image as {output_path}")
                except Exception as e:
                    print(f"Error processing file {f}: {e}")
