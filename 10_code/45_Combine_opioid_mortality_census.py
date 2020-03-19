import pandas as pd
import numpy as np
import glob
import os
from plotnine import *
pd.set_option('display.max_columns', None)
#define states, the first is study state, the latters are comparison states
States = ['FL','GA','IL','IN','OH','PA']
policy_year = 2010
os.chdir('C:/Users/Jiajie Zhang/estimating-impact-of-opioid-prescription-regulations-team-3/20_intermediate_files')
os.getcwd()

#read in opioid data
Opioid_Mort = pd.DataFrame()
for filename in glob.glob('./*cleaned_and_merged.csv'):
    print(filename)
    df_tmp = pd.read_csv(filename)
    Opioid_Mort = Opioid_Mort.append(df_tmp)
