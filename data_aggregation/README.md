# Data Aggregation

# Description 

loading_1200_data.py
- this loads all 6 dscalar.nii files into dataframes and splits them into left and right hemispheres. The .dlabel file of 180 parcellation groups is joined to each left and right hemisphere. these dataframes are saved in left_right_dataframes and are used in the machine learning portion.

hemisphere_analysis.py
- this groups the left and right dataframes by their parcellation group then counts them, returning the number of vertices per parcellation group for both hemispheres. Results are saved as a datframe in left_right_dataframes folder and used in the inferential stats portion.
