# Package validation

# Description 

This sections aims to validate the functionalities and performance of the Power Law Python package. The positive and negative control scripts within this folder are used to ensure that the package works correctly. Additonally, it contains a file fitting 
fMRI scalar data as a tester. 

# Dependencies

Python 3 is required for these scripts. 
The following Python packages are required to run the validation scripts:

- `numpy`
- `scipy`
- `matplotlib`
- `pandas`
- `powerlaw`

You can install these dependencies using `pip`:

pip install numpy scipy matplotlib pandas powerlaw


# Run the negative control script
python3 negative_control.py

# Run the positive control script
python3 positive_control.py


# Run the fmri testing script 
python3 testing_fmri_thickness_Ppackage.py



