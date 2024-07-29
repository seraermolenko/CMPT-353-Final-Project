import numpy as np
import powerlaw
import nibabel as nib

# command line python3 aggregating_by_voxel.py


# learned thesere are Cifti files not Nifti files

# Originally suspected the data wouod be 2D, so we could extract the voxels but it turned out to already eb flattned
# now have to figure out the orginal shape of the file in order to get each voexl 

# Load the data (example using nibabel for .nii files)
#file_path = 'datasets/102109.thickness.164k_fs_LR.dscalar.nii'
#nii = nib.load(file_path)
#thickness_data = nii.get_fdata()

#print("Shape of the 2D array:", thickness_data.shape)


file_path2 = 'datasets/rfMRI_REST1_LR_Atlas_hp2000_clean_vn.dscalar.nii'
cifti = nib.cifti2.load(file_path2)

# try figuring out OG data shape withb header info
header = cifti.header
print("Header info:", header)

# figure out attributions 
print("Header Attributes and Methods:", dir(header))

print("Version:", header.version)
print("Number of mapped indices:", header.number_of_mapped_indices)

# Access the index maps
index = 0
for index_map in header.get_index_map(index):
    print("Index Map:", index_map)

# Access the matrix
print("Matrix:", header.matrix)
matrix = header.matrix
# List all attributes and methods
print(dir(matrix))

axes = matrix.get_axis(index)
print("Axis Information:")
for i, axis in enumerate(axes):
    print(f"   Axis {i}: {axis}")


# get the numver of voxols and time points using .shape
#num_voxels, num_time_points = thickness_data.shape


# store results 
results_per_voxel = []   

# curting short becuase xmin take a very long time  

# iterate through each voxel (through each row in 2D array)
# for voxel_index in range(100):
    
#     voxel_time_series = thickness_data[voxel_index,:]       # time series at each data at each voxol, measurement at all the diff tiem points 

#     # Fit a power law distribution to the voxel's time series data
#     results = powerlaw.Fit(voxel_time_series)
    
#     # Store the results
#     voxel_results = {
#         'voxel_index': voxel_index,
#         'alpha': results.power_law.alpha,
#         'xmin': results.power_law.xmin
#     }
#     results_per_voxel.append(voxel_results)


# print results 

for result in results_per_voxel:
    print(f"Voxel {result['voxel_index']}: alpha = {result['alpha']}, xmin = {result['xmin']}")