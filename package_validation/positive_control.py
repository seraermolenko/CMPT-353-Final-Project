import powerlaw
import os
import numpy as np
import matplotlib.pyplot as plt

# command line: python3 positive_control.py


try:
    # load Moby file
    moby_file=open('datasets/moby_data.txt')
    nums = []

    for line in moby_file: 
        nums.append(int(line.rstrip()))

    moby_file.close()
    
    moby_data = np.array(nums)            # list of numbera into numpy array

    #incase its slow
    subset = 10000
    moby_subset = moby_data[:subset]

    # fitting power law distribution 
    results = powerlaw.Fit(moby_subset, verbose=True)       # keeping verbose for more info 

    # x values 
    x = range(len(moby_data))

    # new figure for plotting 
    fig, ax = plt.subplots() 

    #ax.loglog(x, moby_data)    #plot for regular, loglog for the loglog scale 

    # plotting porbability density function 
    powerlaw.plot_pdf(moby_subset, ax=ax, color='b', linewidth=2, label='Empirical Data')

    # plot histogram of data
    #plt.hist(moby_subset, bins=50, density=True, alpha=0.75, label='Histogram')

    # change depending on data 
    xlabel = ' Words'
    ylabel = 'frequency of the words'
    title = 'Power-law Fit to Moby-Dick Distribution'

    # Customize plot
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()

    # Show plot
    #plt.show()
    plt.savefig('outputs/Positive_Control_PDF.png')

    # alpha and xmin results
    #print('\n') 
    #print("Alpha :", results.power_law.alpha, '\n')                          # (exponent of the power law)
    #print("Xmin ", results.power_law.xmin, '\n')                             # (minimum value for power law):



    # COMPARING 

    # plotting the fitted power law distribution using the power law fit object 'results' 
    # visualizes the differences in fit between power law and exponential distribution
    # The goodness of these distribution fits can be compared with distribution_compare.
    results.power_law.plot_pdf(ax=ax, linestyle='--', color='r', linewidth=2, label='Power Law Fit')

    first_distribution = 'power_law'
    second_distribution = 'exponential'

    R, p = results.distribution_compare(first_distribution, second_distribution, normalized_ratio = True)  

    # look into what null hypothesis is, and p value 
    # positve control and negative control 

    # R is the loglikelihood ratio between the two candidate distributions
    # Note: This number will be positive if the data is more likely in the first distribution, 
    #       and negative if the data is more likely in the second distribution
    # Note: Likelihood of a model given data measures how probable it is that the data would be observed under that model. 
    #       Higher likelihood means the model better explains the data
    # The significance value for that direction is p
    print("\n")
    print(f"R: {R}, p: {p}, \n")

    # add p value print 

    if(R > 0):
        print(f"The data is more likely to be {first_distribution}\n")            
    elif(R == 0):
        print(f"The data is equally likley under both {first_distribution} and {second_distribution}\n")
    else:
        print(f"The data is more likley to be {second_distribution}\n")



    # SIMULATING POWER LAW

    alpha = 5.0  # Exponent of the power law, small alpha is heavy tailed 
    xmin = 2.5    # Minimum value from which the power-law behavior starts

    # generating simulated data 
    theoretical_distribution = powerlaw.Power_Law(xmin=xmin, parameters=[alpha])
    simulated_data = theoretical_distribution.generate_random(10000)
    
    # such simulated data can then be fit again, to validate the accuracy of fitting software such as powerlaw:
    # fitting simulated data 
    fit = powerlaw.Fit(simulated_data)

    # calculating best minimal value for power law fit
    fitted_xmin = fit.power_law.xmin
    fitted_alpha = fit.power_law.alpha

    # printing out the estimated parameters
    print(f"Estimated xmin: {fitted_xmin}")
    print(f"Estimated alpha: {fitted_alpha}")


# there are package plots PDF that aere better 


except FileNotFoundError as e:
    print(f"Error: {e}")