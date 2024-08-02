# Inferential_Tests 

# Description 

This sections speratly demonstrates the KS test, the Log Likelihood test, and both together with bootstrapping. The maximum likelihood test is implicity demonstrated in each file becuase it is used by the Fit function from Power Law package. These 
scripts demonsstrate these testes using generated power law data for illistrative purposes. 

The python3 KS_test.py introduces the Kolmogorov-Smirnov (KS) test and boot strapping. This uses generated power law distributed
data so the output should be our ideal situatio. 

The Log_Likelihood.py introduces the Log Likelihood test and explores the importiance of setting a good x-min paramter. This script 
demonstrates why setting the x-min value to be the lowest value is importiant if our data set was small. However, our anyalsis will be conduded on large data so this method was not chosen in the end. 


# Dependencies

Python 3 is required for these scripts. 
The following Python packages are required to run the validation scripts:

- `numpy`
- `scipy`
- `matplotlib`
- `powerlaw`
- `sklearn.utils`

You can install these dependencies using `pip`:

pip install numpy scipy matplotlib powerlaw sklearn.utils 



# Run the KS_test.py
python3 KS_test.py

# Run the Log_Likelihood.py
python3 Log_Likelihood.py

# Run the KS_Likelihood_Bootstrap.py
python3 KS_Likelihood_Bootstrap.py




