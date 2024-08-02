import powerlaw
import numpy as np
from sklearn.utils import resample

# command line python3 KS_test.py

# using Kolmogorov-Smirnov (KS) statistic
# comparing boot strapped KS p-value tells you how extreme the KS statistic for the original data is relative to the 
# KS statistics obtained from the bootstrap samples

# now that the power law package has ben verified, we can use poer law package to generate power law data,
# use the KS test, and then bootstrap

# The goodness of fit of these distributions must be evaluated before concluding that a power law is a good description 
# of the data. The goodness of fit for each distribution can be considered individually or by comparison to the fit of 
# other distributions (respectively, using bootstrapping and the Kolmogorov-Smirnov test to generate a p-value for an 
# individual fit vs. using loglikelihood ratios to identify which of two fits is better


np.random.seed(0)       # fixing random seed so that the results are repeatble 

# power law 
# generating artifiial data 
a = 2                                                           # alpha value 2
x_min = 1                                                       # x-min value 1 
n = 1000                                                        # generating one thousand observations 
x = np.linspace(0, n, n+1)                                      # array x with 1001 values in it 
s_pareto = (np.random.pareto(a, len(x)) + 1) * x_min            # generatingrandom sample from a pareto distribution 
results_pareto = powerlaw.Fit(s_pareto)

# ALSO, potentially because we have big data set, specify the x-min 
# Anderson-Darling distance
#fit_ad = powerlaw.Fit(results_pareto, xmin_distance='Asquare')
# or by default when you dont specify x-min, power law will do: 
#fit_ks = powerlaw.Fit(results_pareto, xmin_distance='V')


# Goodness of fit using KS test
# the D value (or KS statistic) measures the maximum difference between the cumulative 
# distribution functions (CDFs) of two distributions
# lets us see how well our empirical data follows power law compared ot refrence power law 
# smaller D is good fit, less deviation

D = results_pareto.power_law.KS()       # printed below 


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

# we want small conifdence intervals so that our values are robust and stable 
# using 95% confidence interval 
alpha_conf_interval = np.percentile(alpha_bootstrap, [2.5, 97.5])
xmin_conf_interval = np.percentile(xmin_bootstrap, [2.5, 97.5])

alpha_original = results_pareto.power_law.alpha
x_min_original = results_pareto.power_law.xmin


print("\n\n\n")


print("Original Alpha:",alpha_original)
print("\n")
print("Original X_min:",x_min_original)
print("\n")

# printing original KS test satistic 
print(f"KS test: D = {D}")
print("\n")

print("Alpha confidence interval (95%):", alpha_conf_interval)
print("\n")

print("X_min confidence interval (95%):", xmin_conf_interval)
print("\n")

# calculating p-value for the original KS statistic based on bootstrap distribution
p_value = np.mean(np.array(ks_statistics) >= D)
print("P-value for KS test after bootstrapping:", p_value)

print("\n\n")

