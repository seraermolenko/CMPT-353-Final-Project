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


    # # Get the index map
    # index_maps = hdr.get_index_maps()

    # # Display information about the index map
    # print("Index Maps:", index_maps)

    # # If the index map contains multiple maps, you can iterate through them
    # for im in index_maps:
    #     print(im)
    #     print("Type:", type(im))
    #     print("Data:", im.data)
    #     print("Brain Models:", im.brain_models)
    #     print("Index:", im.index)

    #print('Data space: ', hdr.get_data_shape())

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
    
    # mean_left_series.to_csv("left_right_dataframes/" + output_name + "_" + dictionary[0][0] + ".csv")
    # print("Left hemisphere dataframe " + output_name + "_" + dictionary[0][0] + ".csv saved in left_right_dataframes/")

    # mean_right_series.to_csv("left_right_dataframes/" + output_name + "_" + dictionary[1][0] + ".csv")
    # print("Right hemisphere dataframe " + output_name + "_" + dictionary[1][0] + ".csv saved in left_right_dataframes/")
    # print("\n\n")

    # return left and right series
    return mean_left_series, mean_right_series

# add parcellation (brain groups) to data
def parcellation_data():
    parcellation = nib.load("datasets\Q1-Q6_RelatedValidation210.CorticalAreas_dil_Final_Final_Areas_Group_Colors.32k_fs_LR.dlabel.nii")
    parcellation_array = parcellation.get_fdata() # to numpy array

    # get dataframes
    parcel_df = pd.DataFrame(parcellation_array) #, columns=['Cerebral Cortex Thickness'])
    #print(parcel_df)

    # split into left and right hemispheres, use same hardcoded values as brain data files
    # parcel_left_df = pd.DataFrame(parcellation_array[:29695])
    # parcel_right_df = pd.DataFrame(parcellation_array[29695:])

    parcel_left_df = parcel_df.iloc[:, 0:29695+1].reset_index()
    parcel_right_df = parcel_df.iloc[:, 29695+1:].reset_index()

    mean_left_df = parcel_left_df.mean()
    mean_right_df = parcel_right_df.mean()
    

    # Average across all 1200 applicants
    # now they're series, 1D
    mean_left_series = mean_left_df.iloc[1: ]
    mean_right_series = mean_right_df.iloc[1: ]



    return mean_left_series, mean_right_series # .iloc[1: ] # drop weird index at the front

# python3 loading_1200_data.py

if __name__=='__main__':
    filetype = ['corrThickness', 'curvature', 'myelinMap', 'smoothedMyelinMap', 'sulc', 'thickness']
    filenames = ['S1200.corrThickness_MSMAll.32k_fs_LR.dscalar.nii', 'S1200.curvature_MSMAll.32k_fs_LR.dscalar.nii', 'S1200.MyelinMap_BC_MSMAll.32k_fs_LR.dscalar.nii', 'S1200.SmoothedMyelinMap_BC_MSMAll.32k_fs_LR.dscalar.nii', 'S1200.sulc_MSMAll.32k_fs_LR.dscalar.nii', 'S1200.thickness_MSMAll.32k_fs_LR.dscalar.nii']
    # initialize dataframes
    left_hemisphere = pd.DataFrame()
    right_hemisphere = pd.DataFrame()
    for i in range(len(filenames)):
        print("Running " + filetype[i] + " file...")
        left_row, right_row = main('datasets/' + filenames[i], filetype[i])

        # get series to dataframe, transpose to row: https://stackoverflow.com/questions/46796943/converting-a-row-of-a-pandas-dataframe-into-a-dataframe-itself-instead-of-a-ser
        left_df_col = left_row.to_frame().T
        right_df_col = right_row.to_frame().T

        left_hemisphere = pd.concat([left_hemisphere, left_df_col], ignore_index=True)
        right_hemisphere = pd.concat([right_hemisphere, right_df_col], ignore_index=True)

    # append parcellation data as series
    parcel_left, parcel_right = parcellation_data()
    # reference for appending series to dataframe: https://stackoverflow.com/questions/33094056/is-it-possible-to-append-series-to-rows-of-dataframe-without-making-a-list-first

    parcel_left_df = parcel_left.to_frame().T # dataframe to series
    parcel_right_df = parcel_right.to_frame().T

    # append to the front, reference: https://pandas.pydata.org/docs/reference/api/pandas.concat.html
    left_hemisphere = pd.concat([parcel_left_df, left_hemisphere], ignore_index=True)
    right_hemisphere = pd.concat([parcel_right_df, right_hemisphere], ignore_index=True)

    # print(parcel_left_df)
    # print(parcel_right_df)
    # print("and hemispheres")

    # transpose to (60000 rows, 7 cols)
    left_hemisphere = left_hemisphere.T
    right_hemisphere = right_hemisphere.T
    # adding col names reference: https://www.geeksforgeeks.org/add-column-names-to-dataframe-in-pandas/
    left_hemisphere.columns = ['parcellation_group', 'corrected_thickness', 'curvature', 'myelin_map', 'smoothed_myelin_map', 'sulcal_depth', 'thickness']
    right_hemisphere.columns = ['parcellation_group', 'corrected_thickness', 'curvature', 'myelin_map', 'smoothed_myelin_map', 'sulcal_depth', 'thickness']
    
    # convert grouping to int
    left_hemisphere['parcellation_group'] = left_hemisphere['parcellation_group'].astype(int)
    right_hemisphere['parcellation_group'] = right_hemisphere['parcellation_group'].astype(int)

    # # 180 groupings total for parcellation; subtract 180 from left to match
    left_hemisphere['parcellation_group'] = left_hemisphere['parcellation_group'] - 180
    print(left_hemisphere)
    print(right_hemisphere)

    left_hemisphere.to_csv("left_right_dataframes/left_hemisphere.csv")

    right_hemisphere.to_csv("left_right_dataframes/right_hemisphere.csv")


