import numpy as np
import pandas as pd
from scipy import stats

left_hemisphere = pd.read_csv("left_right_dataframes/left_hemisphere.csv")
right_hemisphere = pd.read_csv("left_right_dataframes/right_hemisphere.csv")
parcellation = pd.read_csv("datasets/five_groups.csv") # some labelled data

#drop index col
left_hemisphere = left_hemisphere.drop(left_hemisphere.columns[0], axis=1)
right_hemisphere = right_hemisphere.drop(right_hemisphere.columns[0], axis=1)

# data is in 180 groups, group into 5 groups.
# multiple variables we'd like to consider; 4 characteristics; leave out corrected_thickness and smoothed_myelin map. just the raw data
left_hemisphere = left_hemisphere.drop(['corrected_thickness', 'smoothed_myelin_map'], axis=1)
right_hemisphere = right_hemisphere.drop(['corrected_thickness', 'smoothed_myelin_map'], axis=1)

print(left_hemisphere)
print(right_hemisphere)