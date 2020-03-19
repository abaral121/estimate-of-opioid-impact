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
#checkout if all states are included
#Opioid_Mort['State'].value_counts()
Opioid_Mort = Opioid_Mort.drop(columns = 'Unnamed: 0')

## There are two rows with county = NaN, dorp it.
Opioid_Mort = Opioid_Mort.drop(Opioid_Mort.loc[Opioid_Mort['County'].isnull()].index)
#read in Census data
Census_full = pd.read_csv('./21_Census_Full_County_Level.csv')

# subset needed states
mask = Census_full['State'].isin(States)
Census_sel = Census_full.loc[mask]
#validate
Census_sel['State'].value_counts()
Census_sel = Census_sel.drop(columns = 'Unnamed: 0')
#collapse Opioid_Mort to state_year level
#Opioid_Mort_state_year = Opioid_Mort.groupby(['State','Year'], as_index=False)['MME'].sum()

# Merge Opioid_Mort with Census
Opioid_Mort_Census = pd.merge(Opioid_Mort,Census_sel,on =['Year','State','County'],how = 'left')
##test['County'].unique()
##test = pd.merge(Opioid_Mort,Census_sel,on =['Year','State','County'],how = 'outer')

# We'vedone combining all data needed for FL Opioid & Deaths Did, next cal value per-cap for deaths and MME

# Calculate Deaths per 100,000 people & MME per capita
Opioid_Mort_Census['MME_Per_Capita'] = Opioid_Mort_Census['MME']/Opioid_Mort_Census['Population']
Opioid_Mort_Census['Deaths_Per_100000'] = Opioid_Mort_Census['Deaths']/Opioid_Mort_Census['Population']*100000
Opioid_Mort_Census.to_csv('FL_Did_Opioid_Mort_Census.csv')
Opioid_Mort_Census['Is_Target_State'] = Opioid_Mort_Census['State'] == States[0]
# subtract comparison States and average over population
#Study_Opioid_Mort_Census = Opioid_Mort_Census.loc[Opioid_Mort_Census['State']==States[0]]
#Compare_Opioid_Mort_Census = Opioid_Mort_Census.loc[Opioid_Mort_Census['State']!=States[0]]
Opioid_Mort_Census['Year'].isnull().sum()

#Compare_grouped = Compare_Opioid_Mort_Census.groupby(['Year'],as_index = False,)['Deaths','MME','Population'].sum()
#Compare_grouped['MME_Per_Capita'] = Compare_grouped['MME']/Compare_grouped['Population']
#Compare_grouped['Deaths_Per_100000'] = Compare_grouped['Deaths']/Compare_grouped['Population']*100000
#Compare_grouped['State'] = 'Compare_State'

#stack two dataframes
#Opioid_Mort_Census = pd.concat([Study_Opioid_Mort_Census,Compare_grouped],sort = False)
#line_a = Opioid_Mort_Census.loc[(Opioid_Mort_Census['Year']<=(policy_year-1)) & (Opioid_Mort_Census['Is_Target_State']==True)]
#len(sorted(line_a['MME_Per_Capita'],reverse = True))
#line_a['MME_Per_Capita'].isnull().sum()
p = (ggplot(Opioid_Mort_Census,aes( x = 'Year', y ='MME_Per_Capita')) +
#geom_line(Opioid_Mort_Census.loc[Opioid_Mort_Census['after_policy_year']==True], aes( x = 'Year', y ='Pred_Deaths_per_Pop'), color = "red") +
geom_smooth(Opioid_Mort_Census.loc[(Opioid_Mort_Census['Year']>=policy_year) & (Opioid_Mort_Census['Is_Target_State']==False)], aes( x = 'Year', y = 'MME_Per_Capita', color = 'Is_Target_State'), method = 'lm') +
geom_smooth(Opioid_Mort_Census.loc[(Opioid_Mort_Census['Year']<=(policy_year-1)) & (Opioid_Mort_Census['Is_Target_State']==False)], aes( x = 'Year', y ='MME_Per_Capita',color = 'Is_Target_State'), method = 'lm') +
geom_smooth(Opioid_Mort_Census.loc[(Opioid_Mort_Census['Year']>=policy_year) & (Opioid_Mort_Census['Is_Target_State']==True)], aes( x = 'Year', y = 'MME_Per_Capita',color = 'Is_Target_State'), method = 'lm') +
geom_smooth(Opioid_Mort_Census.loc[(Opioid_Mort_Census['Year']<=(policy_year-1)) & (Opioid_Mort_Census['Is_Target_State']==True)], aes( x = 'Year', y ='MME_Per_Capita',color = 'Is_Target_State'), method = 'lm') +
#geom_point(Opioid_Mort_Census.loc[(Opioid_Mort_Census['Year']>=policy_year) & (Opioid_Mort_Census['Is_Target_State']==False)], aes( x = 'Year', y = 'MME_Per_Capita'), color = "black") +
#geom_point(Opioid_Mort_Census.loc[(Opioid_Mort_Census['Year']<=(policy_year-1)) & (Opioid_Mort_Census['Is_Target_State']==False)], aes( x = 'Year', y ='MME_Per_Capita'),color = "black") +
#geom_point(Opioid_Mort_Census.loc[(Opioid_Mort_Census['Year']>=policy_year) & (Opioid_Mort_Census['Is_Target_State']==True)], aes( x = 'Year', y = 'MME_Per_Capita'), color = "blue") +
#geom_point(Opioid_Mort_Census.loc[(Opioid_Mort_Census['Year']<=(policy_year-1)) & (Opioid_Mort_Census['Is_Target_State']==True)], aes( x = 'Year', y ='MME_Per_Capita'),color = "blue") +

geom_vline(xintercept = policy_year,colour="#BB0000") +
ggtitle('FL Drug Shipment Diff-in-Diff Analysis')
#ylim(0,1)
)
(ggsave(filename = '../30_results/FL_Drug_DiD_Analysis',plot = p,width =12, height = 8))


## add propotional change later
