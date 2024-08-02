import powerlaw
import numpy as np
import nibabel as nib
import pandas as pd


def main():
    left_parcellation = pd.read.csv("Left_Right_Dataframes/left_parcellation_count.csv")
    right_parcellation = pd.read.csv("Left_Right_Dataframes/right_parcellation_count.csv")

    left_parcellation.show()
    right_parcellation.show()











if __name__=='__main__':
   main()