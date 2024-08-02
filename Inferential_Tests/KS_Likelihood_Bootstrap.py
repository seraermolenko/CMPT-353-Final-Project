import powerlaw
import numpy as np
from sklearn.utils import resample

# In this file, I'm combining KS test, log likilhood and bootstrapping 


np.random.seed(0)       # fixing random seed so that the results are repeatble 

# power law 
# generating artifiial data 
alpha = 2                                                       # alpha value 2
x_min = 1                                                       # x-min value 1 
n = 1000                                                       # generating one thousand observations 
x = np.linspace(0, n, n+1)                                      # array x with 10001 values in it, CHANGED TO 1001 FOR SPEED, FEEL FREE TO ALTER BACK
pareto = (np.random.pareto(alpha, len(x)) + 1) * x_min        # generating random sample from a pareto distribution 


# fit power to power law data 
results_pareto = powerlaw.Fit(pareto)

# func to compute and print p-values
def compute_power_law_p_val(results):
    distribution_list = ['lognormal', 'exponential', 'truncated_power_law', 'stretched_exponential', 'lognormal_positive']
    for distribution in distribution_list:
        R, p = results.distribution_compare('power_law', distribution)
        print("\n")
        print("power law vs ", distribution)
        print("R = ", np.round(R, 3))
        print("p =", np.round(p, 3))
    return None

# fitting power to power law data
results_pareto = powerlaw.Fit(pareto)

# Goodness of fit using KS test
D = results_pareto.power_law.KS()

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
    sample = resample(pareto, replace=True)               # bootstrap sample 
    
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

# printing results
print("\n\n\n")

compute_power_law_p_val(results_pareto)

print("\n")
print("Alpha confidence interval:", alpha_conf_interval)
print("X_min confidence interval:", xmin_conf_interval)

print("\n")
print("Pareto distribution fit results:")
print("estimated fit alpha: {:.3g}".format(results_pareto.power_law.alpha - 1)) 
print("estimated fit x_min: {:.3g}".format(results_pareto.power_law.xmin))
print("\n")
print("Original Alpha:",alpha)
print("Original X_min:",x_min)
print("\n")

# printing original KS test satistic 
print("KS test D value:", D)

# calculating p-value for the KS statistic based on bootstrap distribution
p_value = np.mean(np.array(ks_statistics) >= D)
print("P-value:", p_value)

