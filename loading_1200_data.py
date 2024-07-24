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

    # get dataframes
    df = pd.DataFrame(file_data) #, columns=['Cerebral Cortex Thickness'])
    hdr = file_img.header # header

    # Access the matrix
    matrix = hdr.matrix

    # reference for getting brain model axis: https://neurostars.org/t/how-to-read-a-cifti-file-header-with-nibabel/21341/2
    cifti_axes_list = [hdr.get_axis(i) for i in range(file_img.ndim)] # (ScalarAxis, BrainModelAxis)

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
    #print(dictionary)

    # split df by column index into left and right cortexes

    index1 = dictionary[0][2] # 29695 columns
    index2 = dictionary[1][2] # 29716 columns

    left_cortex = dictionary[0]
    left_df = df.iloc[:, 0:index1].reset_index()
    right_cortex = dictionary[1]
    right_df = df.iloc[:, index1:].reset_index()

    mean_left_df = left_df.mean()
    mean_right_df = right_df.mean()
    

    # Average across all 1200 applicants
    # now they're series, 1D
    mean_left_series = mean_left_df.iloc[1: ]
    mean_right_series = mean_right_df.iloc[1: ]

    
    # weird first value, drop it
    mean_left_series.iloc[1:]
    mean_right_series.iloc[1:]

    # drop index row
    # print(mean_left_series)
    # print(mean_right_series)

    # Reference for two plots side by side
    # https://stackoverflow.com/questions/42818361/how-to-make-two-plots-side-by-side
    # Histogram
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.hist(mean_left_series, bins = 100)
    plt.title("Left Hemisphere")

    plt.subplot(1, 2, 2)
    plt.hist(mean_right_series, bins = 100)
    plt.title("Right Hemisphere")
    plt.suptitle('Histogram of ' + output_name)
    plt.savefig("outputs/histograms/" + output_name + "_left_right")    
    print("Histogram " + output_name + "_left_right.png saved in outputs/histograms")

    plt.close()

    # Loglog plot
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.loglog(mean_left_series)
    plt.title("Left Hemisphere")

    plt.subplot(1, 2, 2)
    plt.loglog(mean_right_series)
    plt.title("Right Hemisphere")
    plt.suptitle('Loglog Plot of ' + output_name)
    plt.savefig("outputs/loglog/" + output_name + "_left_right")
    print("Loglog plot " + output_name + "_left_right.png saved in outputs/loglog")

    mean_left_series.to_csv("left_right_dataframes/" + output_name + "_" + dictionary[0][0] + ".csv")
    print("Left hemisphere dataframe " + output_name + "_" + dictionary[0][0] + ".csv saved in left_right_dataframes/")

    mean_right_series.to_csv("left_right_dataframes/" + output_name + "_" + dictionary[1][0] + ".csv")
    print("Right hemisphere dataframe " + output_name + "_" + dictionary[1][0] + ".csv saved in left_right_dataframes/")
    print("\n\n")

if __name__=='__main__':
    filetype = ['corrThickness', 'curvature', 'myelinMap', 'smoothedMyelinMap', 'sulc', 'thickness']
    filenames = ['S1200.corrThickness_MSMAll.32k_fs_LR.dscalar.nii', 'S1200.curvature_MSMAll.32k_fs_LR.dscalar.nii', 'S1200.MyelinMap_BC_MSMAll.32k_fs_LR.dscalar.nii', 'S1200.SmoothedMyelinMap_BC_MSMAll.32k_fs_LR.dscalar.nii', 'S1200.sulc_MSMAll.32k_fs_LR.dscalar.nii', 'S1200.thickness_MSMAll.32k_fs_LR.dscalar.nii']
    for i in range(len(filenames)):
        print("Running " + filetype[i] + " file...")
        main('datasets/' + filenames[i], filetype[i])
