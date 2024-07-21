import powerlaw
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
from sklearn.utils import resample

# In this file, I'm combining KS test, log likilhood and bootstrapping 


np.random.seed(0)       # fixing random seed so that the results are repeatble 

# power law 
# generating artifiial data 
a = 2                                                           # alpha value 2
x_min = 1                                                       # x-min value 1 
n = 1000                                                        # generating one thousand observations 
x = np.linspace(0, n, n+1)                                      # array x with 1001 values in it 
s_pareto = (np.random.pareto(a, len(x)) + 1) * x_min            # generatign random sample from a pareto distribution 


# fit power to power law data 
results_pareto = powerlaw.Fit(s_pareto)

# func to compute and print p-values
def compute_power_law_p_val(results):
    distribution_list = ['lognormal', 'exponential', 'truncated_power_law', 'stretched_exponential', 'lognormal_positive']
    for distribution in distribution_list:
        R, p = results.distribution_compare('power_law', distribution)
        print(f"Power law vs {distribution}: R = {np.round(R, 3)}, p = {np.round(p, 3)}")
    return None

# fitting power to power law data
results_pareto = powerlaw.Fit(s_pareto)

# results
print("Pareto distribution fit results:")
print("alpha = " + str(results_pareto.power_law.alpha))  # estimated tail index
print("x_min= " + str(results_pareto.power_law.xmin))  # estimated x min value

compute_power_law_p_val(results_pareto)


# Goodness of fit using KS test

D = results_pareto.power_law.KS()
print(f"KS test: D = {D}")


# boot strapping 
bootstrap_num = 100

# bootstrap results
alpha_bootstrap = []
xmin_bootstrap = []
ks_statistics = []

# bootstrapping 
# P value will tell us if the D value is significant
# https://scikit-learn.org/stable/modules/generated/sklearn.utils.resample.html

for _ in range(bootstrap_num):
    sample = resample(s_pareto, replace=True)               # bootstrap sample 
    
    results = powerlaw.Fit(sample)
    
    alpha_bootstrap.append(results.power_law.alpha)
    xmin_bootstrap.append(results.power_law.xmin)

    # KS test 
    D = results.power_law.KS()
    ks_statistics.append(D)

# we want small ocnifdence intervals so that our values are robust and stable 
# using 95% confidence interval 
alpha_conf_interval = np.percentile(alpha_bootstrap, [2.5, 97.5])
xmin_conf_interval = np.percentile(xmin_bootstrap, [2.5, 97.5])

print("Alpha confidence interval:", alpha_conf_interval)
print("X_min confidence interval:", xmin_conf_interval)

# printing original KS test satistic 
print(f"KS test: D = {D}")

# calculating p-value for the original KS statistic based on bootstrap distribution
p_value = np.mean(np.array(ks_statistics) >= D)
print(f"P-value: {p_value}")

