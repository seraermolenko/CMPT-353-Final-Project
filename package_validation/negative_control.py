import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import powerlaw

# python3 negative_control.py

# get world population by year from 1951-2020
# source: https://www.kaggle.com/datasets/sandhyakrishnan02/world-population-19512020?select=World_population%281951-2020%29.csv
population = pd.read_csv("package_validation/World_population(1951-2020).csv")

# Convert to per billion
population['World Population'] = pd.to_numeric(population['World Population'].str.replace(',', ''))/1000000000
#print(population)

# plot exponential graph
plt.plot(population['Year'], population['World Population'])
#plt.yscale('log')
plt.title('World Population from 1951-2020')
plt.xlabel('Year')
plt.ylabel('Population (billions)')
#plt.show()
plt.savefig('package_validation\\Negative_Control_PDF.png')

# only keep Year, World Population
world_pop = population.iloc[:, 0:2] 
print(world_pop)

# Powerlaw comparison
fit = powerlaw.Fit(world_pop['World Population'])
print("power_law.alpha: " + str(fit.power_law.alpha))
print("power_law.sigma: " + str(fit.power_law.sigma))

R, p = fit.distribution_compare('power_law', 'exponential')
print("R for power_law vs. exponential distributions: " + str(R))
print("p-value for power_law vs. exponential distributions: " + str(p))

# R is negative therefore the second function, exponential, is preferred for the dataset.
# the p value = 0.00036369686925081374 which is extremely small which means that the second dataset is extremely preferred