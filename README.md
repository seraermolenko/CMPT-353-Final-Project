README.md

**Required Libraries**

- `numpy` 1.24.2
- `pandas`
- `matplotlib` 
- `powerlaw` 
- `nibabel` 
- `scipy` 
- `sklearn.utils`

You can install these dependencies using `pip`:

pip install numpy pandas matplotlib powerlaw nibabel scipy sklearn.utils 


**Commands, Order of Execution and Produced Files**
1. Powerlaw Package Validation
   - python package_validation\positive_control.py
       -  produces package_validation\Positive_Control_PDF.png
   -  python package_validation\negative_control.py
        - produces package_validation\Negative_Control_PDF.png
   - python package_validation/testing_fmri_thickness_Ppackage.py
        - prints out power law test results on raw data. For testing fMRI package on unaggregated scalar data.
2. Data Cleaning and Aggregation
    - python data_aggregation/loading_1200_data.py
        - produces 6 histograms of left & right hemispheres of each brain characteristic in ‘outputs/histograms’ folder
        - produces 6 loglog() plots of left & right hemispheres of each brain characteristic in ‘outputs/loglog’ folder
        - produces two dataframes left_hemisphere.csv and right_hemisphere.csv in ‘left_right_dataframes’ folder
    - python data_aggregation/hemisphere_analysis.py
        - produces 2 plots of vertices per parcellation grouping for left and right hemispheres (left_parcellation_count.png and    right_parcellation_count.png) in ‘outputs/parcellation_count’ folder
        - produces two aggregated dataframes left_parcellation_count.csv and right_parcellation_count.csv in ‘left_right_dataframes’ folder
3. Power Law Analysis
   - python Power_Law_Analysis.py
5. Inferrential Stats
    - python Inferential_Tests\KS_test.py
    - python Inferential_Tests\Log_Likelihood.py
    - python Inferential_Tests\KS_Likelihood_Bootstrap.py
6. Machine Learning
    - python machine_learning\clustering.py
        - produces two plots of clustered labelled data: left_hemisphere_clustering.png right_hemisphere_clustering.png in 'outputs\ml_results' folder
        - prints the crosstab() results of left and right hemispheres, un-aligned. One program run's data was manually aligned and created as machine_learning\sample_crosstab.csv
    - python chi_square.py
        - prints p-value

**To-do**
- at end: import as a remote repository to SFU's GitHub server (add prof/TA's as developers)
