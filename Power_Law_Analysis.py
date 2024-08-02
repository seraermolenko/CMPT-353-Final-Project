import powerlaw
import numpy as np
import nibabel as nib
import pandas as pd
from sklearn.utils import resample

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
 
    left_data = left_parcellation["count"]
    right_data = right_parcellation["count"]
    print(left_data)
    print(right_data)


    # fitting data to power law with MLE for alpha paramater and KS for x-min
    left_results = powerlaw.Fit(left_data)
    right_results = powerlaw.Fit(right_data)

    # KS test
    D_Left = left_results.power_law.KS()   
    D_right = right_results.power_law.KS()   

    # bootstrapping 
    bootstrap_num = 100

    # bootstrap left results
    alpha_bootstrap_left = []
    xmin_bootstrap_left = []
    ks_statistics_left = []

    for _ in range(bootstrap_num):
        sample = resample(left_data, replace=True)               # bootstrap sample 
        
        left_boot_results = powerlaw.Fit(sample)
        
        alpha_bootstrap_left.append(left_boot_results.power_law.alpha)
        xmin_bootstrap_left.append(left_boot_results.power_law.xmin)

        # KS test 
        D_left_boot = left_boot_results.power_law.KS()
        ks_statistics_left.append(D_left_boot)

    # bootstrap right results
        alpha_bootstrap_right = []
        xmin_bootstrap_right = []
        ks_statistics_right = []

        for _ in range(bootstrap_num):
            sample = resample(right_data, replace=True)               # bootstrap sample 
            
            right_boot_results = powerlaw.Fit(sample)
            
            alpha_bootstrap_right.append(right_boot_results.power_law.alpha)
            xmin_bootstrap_right.append(right_boot_results.power_law.xmin)

            # KS test 
            D_right_boot = right_boot_results.power_law.KS()
            ks_statistics_right.append(D_right_boot)



















if __name__=='__main__':
   main()