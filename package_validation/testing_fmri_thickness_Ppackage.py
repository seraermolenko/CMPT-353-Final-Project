import powerlaw
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt

# Load the cortical thickness data
thickness_file = ('102109.thickness.164k_fs_LR.dscalar.nii')

try:

    thickness_img = nib.load(thickness_file)
    thickness_data = thickness_img.get_fdata()


    # loading data
    thickness_img = nib.load(thickness_file)  # thickness file 


    # using .get_fdata over get_data
    # https://stackoverflow.com/questions/54705304/what-is-difference-between-get-data-and-get-fdata-in-nibabel-library
    thickness_data = thickness_img.get_fdata()
  

    # The data is organized as a 2D array (vertices of brain region, time points)
    # flattening the data to get a 1D array/linear sequence 
    thickness_values = thickness_data.flatten()

    # Use a subset of the data for testing
    subset_size = 10000
    thickness_values_subset = thickness_values[:subset_size]  


    # mean: measure for central trendancy
    # mean can indicate where the center of mass of the distribution lies amd power-law distributions 
    # are often characterized by a heavy right tail, where extreme values can disproportionately affect the mean
    print("Mean thickness:", np.mean(thickness_values_subset))

    # median: In distributions with heavy tails, the median can be a more robust measure of central tendency compared to the mean
    print("Median thickness:", np.median(thickness_values_subset))

    # shape of data
    # sense of how the data is distributed, heavy-tailed, skwewed, normal/bell shaped
    print("Data shape:", thickness_values_subset.shape)

    # fit power-law distribution
    results = powerlaw.Fit(thickness_values_subset,verbose=True)

    # plotting
    # Plot the data and the fitted power-law distribution
    fig, ax = plt.subplots()                                    # new figure and axes to plot data (matplotlib)

    # ploting the probability density function (PDF) of the empirical data
    # gives comparision btween thoeretical distribution predicited by power law and the actual data
    powerlaw.plot_pdf(thickness_values, ax=ax, color='b', linewidth=2, label='Empirical Data')

    # Plot histogram of data
    plt.hist(thickness_values, bins=50, density=True, alpha=0.75, label='Histogram')

    # plotting the fitted power law distribution using the power law fit object 'results' 
    results.power_law.plot_pdf(ax=ax, linestyle='--', color='r', linewidth=2, label='Power Law Fit')


    # change depending on data 
    xlabel = 'Cortical Thickness'
    ylabel = 'Probability Density'
    title = 'Power-law Fit to Cortical Thickness Data'

    # Customize plot
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()

    # Show plot
    plt.show()


    # alpha and xmin results
    print('\n') 
    print("Alpha :", results.power_law.alpha, '\n')                          # (exponent of the power law)
    print("Xmin ", results.power_law.xmin, '\n')                             # (minimum value for power law):

except FileNotFoundError as e:
    print(f"Error: {e}")