import numpy as np
import pandas as pd
import nibabel as nib
from nibabel import cifti2
import matplotlib.pyplot as plt
import sys



def main(file, output_name):
    # cerebral cortext thickness
    
    # 1. extract corr_thickness/curvature into dataframe
    file_img = nib.load(file)
    file_data = file_img.get_fdata() # to numpy array
    print(file_data.shape)
    # get dataframes
    df = pd.DataFrame(file_data) #, columns=['Cerebral Cortex Thickness'])
    print(df)

    hdr = file_img.header
    print("Header Information:")
    print(hdr)
    # Access the matrix
    matrix = hdr.matrix
    print("\nMatrix Information:")
    print(matrix)
    # reference for getting brain model axis: https://neurostars.org/t/how-to-read-a-cifti-file-header-with-nibabel/21341/2
    cifti_axes_list = [hdr.get_axis(i) for i in range(file_img.ndim)] # (ScalarAxis, BrainModelAxis)

    # print(cifti_axes_list[0]) # scalaraxis
    # print(cifti_axes_list[1]) # brainmodelaxis

    # isolate brain model
    brainmodel_axis = cifti_axes_list[1].iter_structures()

    # iter_structures(): (CIFTI-2 brain structure name, slice to select the data associated with the brain structure from the tensor, brain model covering that specific brain structure

    # CIFTI_STRUCTURE_CORTEX_LEFT and CIFTI_STRUCTURE_CORTEX_RIGHT. separate into separate dataframes
    # extract information
    dictionary = {}
    for i, brain_model in enumerate(brainmodel_axis):
        (name, slice, brainmodel) = brain_model
        dictionary[i] = [name, slice, len(brainmodel.vertex), brainmodel]
        # extract size of cortex mask, process separately
    print(dictionary)

    # split df by column index into left and right cortexes

    index1 = dictionary[0][2] # 29695 columns
    index2 = dictionary[1][2] # 29716 columns

    left_cortex = dictionary[0]
    left_df = df.iloc[:, 0:index1].reset_index()
    right_cortex = dictionary[1]
    right_df = df.iloc[:, index1:].reset_index()


    

    # Average across all 1200 applicants
    # mean_left_df = left_df.mean()
    # mean_right_df = right_df.mean()
    # now they're series, 1D
    # drop first column, 0: https://www.statology.org/pandas-drop-first-column/
    left_df = left_df.iloc[ : , 1:]
    right_df = right_df.iloc[ : , 1:]
    # # drop index row
    # print(mean_left_series)
    # print(mean_right_series)
    
    print(left_df) # left cortex
    print(right_df) # right cortex

    plt.figure(figsize=(10, 5))

    # print(np.log(left_df))
    # print(np.log(right_df))

    # Reference for two plots side by side
    # https://stackoverflow.com/questions/42818361/how-to-make-two-plots-side-by-side
    plt.subplot(1, 2, 1)
    plt.hist(left_df, bins = 1000)
    #plt.loglog(left_df)
    plt.title("Left Hemisphere")

    plt.subplot(1, 2, 2)
    plt.hist(right_df, bins = 1000)
    #plt.loglog(right_df)
    plt.title("Right Hemisphere")

    #plt.show()
    plt.savefig("outputs/loglog" + output_name + "_left_right")
    
    # Don't save to csv!! too large
    left_df.to_csv("left_right_dataframes/" + output_name + "_" + dictionary[0][0] + ".csv")
    right_df.to_csv("left_right_dataframes/" + output_name + "_" + dictionary[1][0] + ".csv")


# corrThickness data: python3 loading_1200_data.py 1

# curvature data: python3 loading_1200_data.py 2
# 
# smoothed myelin map data: python3 loading_1200_data.py 3

# sulc data: python3 loading_1200_data.py 4

# thickness data: python3 loading_1200_data.py 5

if __name__=='__main__':
    files = ['corrThickness', 'curvature', 'myelinMap', 'smoothedMyelinMap', 'sulc', 'thicness']
    if (sys.argv[1] == '1'):
        # corr_thickness
        print("Running corrThickness file...")
        main('datasets/S1200.corrThickness_MSMAll.32k_fs_LR.dscalar.nii', files[0])
    elif (sys.argv[1] == '2'):
        # curvature
        print("Running curvature file...")
        main('datasets/S1200.corrThickness_MSMAll.32k_fs_LR.dscalar.nii', files[1])
    elif (sys.argv[1] == '3'):
        print("Running myelin map file...")
        main('datasets/S1200.MyelinMap_BC_MSMAll.32k_fs_LR.dscalar.nii', files[2])
    
    elif (sys.argv[1] == '4'):
        print("Running smoothed myelin map file...")
        main('datasets/S1200.SmoothedMyelinMap_BC_MSMAll.32k_fs_LR.dscalar.nii', files[2])

    elif (sys.argv[1] == '5'):
        print("Running sulc file...")
        main('datasets/S1200.sulc_MSMAll.32k_fs_LR.dscalar.nii', files[3])

    elif (sys.argv[1] == '6'):
        print("Running thickness file...")
        main('datasets/S1200.thickness_MSMAll.32k_fs_LR.dscalar.nii', files[4])
    
    
