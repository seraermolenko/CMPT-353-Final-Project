import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA

# used weather_clusters.py from Exercise 8 as a reference
# python machine_learning/clustering.py

def display_clusters(X, y, plot_title, filename):
    # predict parcellation labels clustering labelled data!

    # reference to Exercise 8
    pca_model = make_pipeline(
        MinMaxScaler(),
        PCA(n_components=2) # create a 2D plot to show results
    )
    # find best characteristics (normalized) to show clustering with
    Xl_pca = pca_model.fit_transform(X)
    Xl_pca_df = pd.DataFrame(Xl_pca)
    #print(Xl_pca_df)
    model = make_pipeline(
        MinMaxScaler(),
        KMeans(n_clusters=5) # 5 labels
    )

    model.fit(X)
    clusters = model.predict(X)
    #print(clusters)
    #plt.scatter(X2[:, 0], X2[:, 1], c=clusters)
    plt.scatter(Xl_pca_df.iloc[:, 0], Xl_pca_df.iloc[:, 1], c=clusters)
    plt.title(plot_title)
    plt.savefig("outputs/ml_results/" + filename)
    plt.clf()

    # counts per category
    counts = pd.crosstab(y, clusters)
    print("Counts of vertices per parcellation:")
    return counts

left_hemisphere = pd.read_csv("left_right_dataframes\left_hemisphere.csv")
right_hemisphere = pd.read_csv("left_right_dataframes\\right_hemisphere.csv")
parcellation = pd.read_csv("datasets\\five_groups.csv") # some labelled data

#drop index col
left_hemisphere = left_hemisphere.drop(left_hemisphere.columns[0], axis=1)
right_hemisphere = right_hemisphere.drop(right_hemisphere.columns[0], axis=1)

# data is in 180 groups, group into 5 groups.
# multiple variables we'd like to consider; 4 characteristics; leave out corrected_thickness and smoothed_myelin map. just the raw data
left_hemisphere = left_hemisphere.drop(['corrected_thickness', 'smoothed_myelin_map'], axis=1)
right_hemisphere = right_hemisphere.drop(['corrected_thickness', 'smoothed_myelin_map'], axis=1)


# 5 clusters for 5 main groupings

# read labelled data: parcellations
# add 5 main group labels
left_labelled = pd.merge(left_hemisphere, parcellation, left_on='group_num', right_on=' group_num', how='inner').reset_index()
right_labelled = pd.merge(right_hemisphere, parcellation, left_on='group_num', right_on=' group_num', how='inner').reset_index()

left_labelled = left_labelled[['parcellation', 'group_num', 'curvature', 'myelin_map', 'sulcal_depth', 'thickness']]
right_labelled = right_labelled[['parcellation', 'group_num', 'curvature', 'myelin_map', 'sulcal_depth', 'thickness']]

# get groups, remove duplicates: https://www.w3schools.com/python/pandas/ref_df_drop_duplicates.asp
left_groups = left_labelled['group_num'].drop_duplicates()
right_groups = right_labelled['group_num'].drop_duplicates()

# remove all groupings not in left_labelled and right_labelled to get all unlabelled data.
left_unlabelled = left_hemisphere[~left_hemisphere['group_num'].isin(left_groups)]
right_unlabelled = right_hemisphere[~right_hemisphere['group_num'].isin(right_groups)]

# now get unlabelled data to fit model to: all vertices that aren't in this subset

# cluster left and right independently then compare 
# all vertices that are in one of the five main groups: labelled data
# train one model and run on both hemispheres.

X_left_label = left_labelled.drop(['parcellation'], axis=1)
y_left_label = left_labelled['parcellation']

X_right_label = right_labelled.drop(['parcellation'], axis=1)
y_right_label = right_labelled['parcellation']

# train model and run independently on left and right hemisphere data
left_counts = display_clusters(X_left_label, y_left_label, "Labelled Data: Left Hemisphere Clustering", "left_hemisphere_clustering")
right_counts = display_clusters(X_right_label, y_right_label, "Labelled Data: Right Hemisphere Clustering", "right_hemisphere_clustering")

print("Left counts: ")
print(left_counts.T)

print("Right counts: ")
print(right_counts.T)
