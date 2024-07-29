import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys


left_hemisphere = pd.read_csv("left_right_dataframes/left_hemisphere.csv")
right_hemisphere = pd.read_csv("left_right_dataframes/right_hemisphere.csv")

#drop index col
left_hemisphere = left_hemisphere.drop(left_hemisphere.columns[0], axis=1)
right_hemisphere = right_hemisphere.drop(right_hemisphere.columns[0], axis=1)

# print(left_hemisphere)
# print(right_hemisphere)

# group by parcellation group, count number of occurences of vertices per parcellation group
agg_left = left_hemisphere.groupby('parcellation_group').count().reset_index()
agg_right = right_hemisphere.groupby('parcellation_group').count().reset_index()
agg_left = agg_left[['parcellation_group', 'corrected_thickness']].rename(columns={"corrected_thickness": "count"})
agg_right = agg_right[['parcellation_group', 'corrected_thickness']].rename(columns={"corrected_thickness": "count"})

# get number of vertices per parcellation group
print(agg_left)
print(agg_right)

# Plot # vertices per parcellation group
# Left Hemisphere
plt.plot(agg_left['parcellation_group'], agg_left['count'])
plt.title('Left Hemisphere Vertice Count per Cortical Area')
plt.xlabel('Parcellation Group #')
plt.ylabel('Number of Vertices')

# save dataframe and figure
agg_left.to_csv("left_right_dataframes/left_parcellation_count.csv")
plt.savefig("outputs/parcellation_count/left_parcellation_count")
plt.clf()


# Right Hemisphere
plt.plot(agg_right['parcellation_group'], agg_right['count'])
plt.title('Right Hemisphere Vertice Count per Cortical Area')
plt.xlabel('Parcellation Group #')
plt.ylabel('Number of Vertices')

# save dataframe and figure
agg_left.to_csv("left_right_dataframes/right_parcellation_count.csv")
plt.savefig("outputs/parcellation_count/right_parcellation_count")
