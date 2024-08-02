import numpy as np
import pandas as pd
from scipy import stats

# load left/right hemisphere results into contingency table
crosstab = pd.read_csv('machine_learning\sample_crosstab.csv').set_index('Unnamed: 0').T
left = crosstab.iloc[:, :5].to_numpy()
right = crosstab.iloc[:, 5:10].to_numpy()


# zeroes skewing results, remove them
# all zeroes in the exact same spots, reference: https://stackoverflow.com/questions/5927180/how-do-i-remove-all-zero-elements-from-a-numpy-array
left = left[left != 0]
right = right[right != 0]

# join along rows, 2 rows of left and right
contingency2 = [left, right] #np.concatenate([left, right], axis=0)

statistic, pvalue, dof, expected_freq = stats.chi2_contingency(contingency2)
print("Chi-squared test p-value: " + str(pvalue)) # null hypothesis : categories are independent/proportions ar the same. Does the left/right hemisphere affect?
#print("Chi-squared test expected frequency: " + str(expected_freq))
