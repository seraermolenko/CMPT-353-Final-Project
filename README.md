README.md

**Project Overview**
- Sera's Accomplishment Statement
- Rachel's Accomplishment Statement

**Required Libraries**
- numpy, pandas, matplotlib, powerlaw

**Commands/Arguments**

**Order of Execution**
- Powerlaw Package Validation (.... , python3 exponential_validation.py)

**Files Produced/Expected**

**Code Documentation (4 page report)**

1) Validate the Powerlaw Package
https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0085777#s4

We first wanted to validated our chosen powerlaw package using selected datasets. We chose datasets that we could gurantee followed powerlaw and those that couldn't; for this we chose an exponentially-distributed dataset.

.... this dataset followed powerlaw ...

For the exponential dataset, we chose world population growth from 1951-2020 retrieved from Kaggle (https://www.kaggle.com/datasets/sandhyakrishnan02/world-population-19512020?select=World_population%281951-2020%29.csv). 

For both methods we fit the data to the powerlaw distribution using fit = powerlaw.Fit(dataset). From here we could observe constants alpha and sigma. We then ran R, p = fit.distribution_compare('power_law', 'exponential') to compare our fitted data to these two distributions.

    ... results for powerlaw dataset...

    For the world population dataset, R was less than 0 which means that the exponential distribution was preferred. This was also statistically significant as p = 0.00036369686925081374 which is much less than 0.05.


- The problem you are addressing, particularly how you refined the provided idea
- The data that you used: how it was gathered, cleaned, etc.
- Techniques you used to analyse the data.
- Your results/findings/conclusions.
- Some appropriate visualization of your data/results.
- Limitations: problems you encountered, things you would do if you had more time, things you should have done in retrospect, etc. 


**To-do**
- include 1-2 sample input files
- at end: import as a remote repository to SFU's GitHub server (add prof/TA's as developers)
