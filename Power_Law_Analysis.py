import powerlaw
import numpy as np
import nibabel as nib
import pandas as pd

# function to compute and print p-values
def compute_power_law_p_val(results):
    distribution_list = ['lognormal', 'exponential', 'truncated_power_law', 'stretched_exponential', 'lognormal_positive']
    for distribution in distribution_list:
        R, p = results.distribution_compare('power_law', distribution)
        print("\n")
        print("power law vs ", distribution)
        print("R = ", np.round(R, 3))
        print("p =", np.round(p, 3))
    return None

def main():
    left_parcellation = pd.read_csv("Left_Right_Dataframes/left_parcellation_count.csv")
    right_parcellation = pd.read_csv("Left_Right_Dataframes/right_parcellation_count.csv")
 
    left_data = left_parcellation.drop("Unnamed: 0")
    right_data = right_parcellation.drop("Unnamed: 0")
    print(left_data.head())
    print(right_data.head())













if __name__=='__main__':
   main()