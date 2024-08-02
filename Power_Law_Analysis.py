import powerlaw
import numpy as np
import pandas as pd
import matplotlib as plt
from sklearn.utils import resample

# function to compute and print p-values
def LogLiklihood(results):
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

    # fitting data to power law with MLE for alpha paramater and KS for x-min
    left_results = powerlaw.Fit(left_data)
    right_results = powerlaw.Fit(right_data)

    # KS test
    D_left = left_results.power_law.KS()   
    D_right = right_results.power_law.KS()   

    # bootstrapping left and right 100 times 
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

    # boot strapping results
    # confidenance interval to 95% percentile 
    alpha_conf_interval_left = np.percentile(alpha_bootstrap_left, [2.5, 97.5])
    xmin_conf_interval_left = np.percentile(xmin_bootstrap_left, [2.5, 97.5])
    alpha_conf_interval_right = np.percentile(alpha_bootstrap_right, [2.5, 97.5])
    xmin_conf_interval_right = np.percentile(xmin_bootstrap_right, [2.5, 97.5])

    print("\n\n")
    # log liklihood test on the left and right data
    print("Left Log-Likihood results")
    LogLiklihood(left_results)
    print("Right Log-Likihood results")
    LogLiklihood(right_results)

    print("\n")
    print("Left data distribution fit results:")
    print("estimated fit alpha: {:.3g}".format(left_results.power_law.alpha - 1)) 
    print("estimated fit x_min: {:.3g}".format(left_results.power_law.xmin))
    print("Left Alpha confidence interval:", alpha_conf_interval_left) 
    print("Left X_min confidence interval:", xmin_conf_interval_left)

    print("\n")
    print("Right data distribution fit results:")
    print("estimated fit alpha: {:.3g}".format(right_results.power_law.alpha - 1)) 
    print("estimated fit x_min: {:.3g}".format(right_results.power_law.xmin))
    print("Right Alpha confidence interval:", alpha_conf_interval_right)
    print("Right X_min confidence interval:", xmin_conf_interval_right)

    # Original KS test satistic 
    print("\n")
    print("KS stastic and its significance for Left Data")
    print("KS test D value:", D_left)

    # calculating p-value for the KS statistic based on bootstrap distribution
    p_value_left = np.mean(np.array(ks_statistics_left) >= D_left)
    print("P-value:", p_value_left)
    
    print("\n")
    print("KS stastic and its significance for Right Data")
    print("KS test D value:", D_right)

    # calculating p-value for the KS statistic based on bootstrap distribution
    p_value_right = np.mean(np.array(ks_statistics_right) >= D_right)
    print("P-value:", p_value_right)

    
    # Plot Left Data 
    # Different figures for plotting 
    fig, ax = plt.subplots(1,2,1) 
    powerlaw.plot_pdf(left_results, ax=ax, color='b', linestyle='-', label='Left Data PDF')
    left_results.power_law.plot_pdf(ax=ax, linestyle='--', color='r', linewidth=2, label='Left Hemisphere Power Law Fit')

    plt.title("Left Hemisphere Fit")
    plt.xlabel('Count')
    plt.ylabel('Probability Density')

    # Plotting Right Data 
    fig2, ax2 = plt.subplots(1,2,2) 
    powerlaw.plot_pdf(right_results, ax=ax2, color='b', linestyle='-', label='Right Data PDF')
    right_results.power_law.plot_pdf(ax=ax2, linestyle='--', color='r', linewidth=2, label='Right Hemisphere Power Law Fit')

    plt.title("Right Hemisphere Fit")
    plt.xlabel('Count')
    plt.ylabel('Probability Density')
    plt.savefig('Power_Law_Analysis.png')

if __name__=='__main__':
   main()

