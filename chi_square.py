import numpy as np
import pandas as pd
from scipy import stats

# Question: Is the number of vertices per core parcellation category independent?
# five categories: auditory, somatosemsory, visual, task positive, task negative.
# left vs. right hemisphere: 
# 
left_count = pd.read_csv("left_right_dataframes/left_hemisphere.csv").shape[0]
right_count = pd.read_csv("left_right_dataframes/right_hemisphere.csv").shape[0]

left_hemisphere = pd.read_csv("left_right_dataframes/left_parcellation_count.csv")
right_hemisphere = pd.read_csv("left_right_dataframes/right_parcellation_count.csv")
parcellation = pd.read_csv("datasets/five_groups.csv")

#drop index col
left_hemisphere = left_hemisphere.drop(left_hemisphere.columns[0], axis=1)
right_hemisphere = right_hemisphere.drop(right_hemisphere.columns[0], axis=1)

# add 5 main group labels
left_group = pd.merge(left_hemisphere, parcellation, left_on='group_num', right_on=' group_num', how='inner').groupby('parcellation').sum('count').reset_index()
right_group = pd.merge(right_hemisphere, parcellation, left_on='group_num', right_on=' group_num', how='inner').groupby('parcellation').sum('count').reset_index()

# sum of all vertices per 5 main groups

# auditory, somatosensory, task negative, task positive, visual
left_num = [left_count] # 29696
right_num = [right_count] # 29716
print("Contingency table of left and right hemisphere:")
contingency = [ left_num + left_group['count'].tolist(), right_num + right_group['count'].tolist()]
print(contingency)

statistic, pvalue, dof, expected_freq = stats.chi2_contingency(contingency)
print("Chi-squared test p-value: " + str(pvalue)) # null hypothesis : categories are independent/proportions ar the same. Does the left/right hemisphere affect the number of vertices?
#print("Chi-squared test expected frequency: " + str(expected_freq))