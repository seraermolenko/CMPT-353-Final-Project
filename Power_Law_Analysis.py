import powerlaw
import numpy as np
import nibabel as nib
import pandas as pd


def main():
    left_parcellation = pd.read_csv("Left_Right_Dataframes/left_parcellation_count.csv")
    right_parcellation = pd.read_csv("Left_Right_Dataframes/right_parcellation_count.csv")
 
    left_data = left_parcellation.drop("Unnamed: 0")
    right_data = right_parcellation.drop("Unnamed: 0")
    print(left_data.head())
    print(right_data.head())











if __name__=='__main__':
   main()