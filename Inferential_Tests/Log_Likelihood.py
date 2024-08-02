import powerlaw
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt

# ideas in this code were learned form https://towardsdatascience.com/detecting-power-laws-in-real-world-data-with-python-b464190fade6


# function explained at the bottom 
def compute_power_law_p_val(results):

    distribution_list = ['lognormal', 'exponential', 'truncated_power_law', 'stretched_exponential', 'lognormal_positive']

    for distribution in distribution_list:
        R, p = results.distribution_compare('power_law', distribution)
        print("\n")
        print("power law vs ", distribution)
        print("R = ", np.round(R, 3))
        print("p =", np.round(p, 3))
 

    # this p value quantifies the significance level of the likleyhood ratio
    # R is the likley hood ratio, posititve is power law is better fit 
    # likley hood ration of 0 means there is no difference 

    # power law vs lognormal: R = -776.987, P = 0.0
    # power law vs exponential: R = -737.24, p = 0.0
    # power law vs truncated_power_law: R = -419.958, P = 0.0
    # power law vs stretched_exponential: R = -737.289, P = 0.0
    # power law vs lognormal_positive: R = -776.987, p = 0.0
    return None


np.random.seed(0)       # fixing random seed so that the results are repeatble 


# power law 
# generating artifiial data 
a = 2                                                           # alpha value 2
x_min = 1                                                       # x-min value 1 
n = 1000                                                        # generating one thousand observations 
x = np.linspace(0, n, n+1)                                      # array x with 1001 values in it 
s_pareto = (np.random.pareto(a, len(x)) + 1) * x_min            # generatign random sample from a pareto distribution 


# log-normal distribution
# can appear more guasian like or appear more like pwoer law depending on the value of sigma 
# makes it hard for real world data, becasue it might be power low or it might be fat-tailed log normal distribuiton 
m = 10                                                                      # mean = 10 
s = 1                                                                       # sigma = 1
s_lognormal = np.random.lognormal(m, s, len(x)) * s * np.sqrt(2*np.pi)      # generating random sample from lognormal distribution 

# power law package handles this because when we do our fit it generates paramater estimates for both a power law and log normal distributions 

# fit power to power law data 
results_pareto = powerlaw.Fit(s_pareto)

# printing results
print("\n\n")
print("----------------------------------------")
print("\n")
print("Log Likihood using Power Law distributed data, small data set")
print("\n")

print("Power-law parameters for the generated data:")
print("alpha: ",results_pareto.power_law.alpha)                     # estimated tail index
print("x_min: ",results_pareto.power_law.xmin)                      # estimated x min value s
compute_power_law_p_val(results_pareto)                             # use Log-likihood              

 
print("\n")
print("note that the python packages alpha libary is = to the standard alpha library +1")
print("so we have to subtract 1 from the value generated form the power law fit to make the comparison to the true alpha vlaue") 

# alpha = 2.9331912195958676                
# x_min = 1.2703447024073973

alpha_true = results_pareto.power_law.alpha - 1
print("true alpha: ", alpha_true)

print("\n\n")
print("----------------------------------------")
print("\n")
print("Log Likihood using Lognormaly distributed data, small data set")
print("\n")

# fit power to log normal data
results_lognormal = powerlaw.Fit(s_lognormal)

# printing results 
print("\n\n")
print("Log-normal parameters for the generated data:")
print("alpha: ", results_lognormal.power_law.alpha)
print("x_min: ", results_lognormal.power_law.xmin)
compute_power_law_p_val(results_lognormal)

# Calculating best minimal value for power law fit
# alpha = 2.5508694755027337
# x_min = 76574.4701482522

# so the issue here is that we are getting a good quality score/p value on a lognormla distribution (it is not power law)
# Why is the lognormla distribution described so well by power law? 
# Because the x min vlaue is far into the tail 
# Solution: manually fix the x-min value to force the libary to fit all of the data not just the tail which best-fits power law 


print("\n\n")
print("----------------------------------------")
print("\n")
print("Log Likihood using Lognormaly distributed data, small data set with maunual lowest x-min")
print("\n")
# fixing xmin so that fit must include all data
results = powerlaw.Fit(s_lognormal, xmin=np.min(s_lognormal))              # manually settong the x-min argument to the smallest value in the data set (uses all values)


print("alpha: ", results.power_law.alpha)
print("x_min: ", results.power_law.xmin)

# alpha = 1.3087955873576855
# x_min = 2201.318351239509

# can generate estimates of the log normal distribution paramters
print("mu: ", results.lognormal.mu)
print("sigma: ", results.lognormal.sigma)

# mu = 10.933481999687547
# sigma = 0.9834599169175509

print("You can compare the mu and sigma estimates to the ground truth of the distribution and see that the fit does a good job.")
print("however in practice, we dont know what the true values are so we wouldnt be able to tell which is a better fit by compring paramater values.")
print("\n")
print("If we new the true paramters of our empirical distribution, we could simply access the paramters of each fitted distribution to compare!")
print("The solution?")
print("We compute likley hood-ratio between the power law fit and a list of other distributions to give us a sense of which distributions best explains the data ")

print("\n") 
print("The function at the top of this script is the Log Likihood implentation")
