import glob
import pandas as pd
import zipfile
import numpy as np
from plotnine import *
import matplotlib as mpl

appended_data = pd.DataFrame()
for filename in glob.glob('../PDSTeam9 Dropbox/00_sourcedata/US_VitalStatistics\*.txt'):
    df_tmp = pd.read_csv(filename,sep = '\t')
    appended_data = appended_data.append(df_tmp)
#split county and State
appended_data[['County','State']] = appended_data.County.str.split(', ',expand = True)
#drop nan data(last few columns)
appended_data_dropna = appended_data.dropna(thresh = 5)

#subset function select only drug poisoning induced deaths.
def subseter (x):
    search2 = "Drug poisonings"
    Y = x["Drug/Alcohol Induced Cause"].str.startswith(search2, na=False)
    return x[Y]

Drug_mortality_allstate = subseter(appended_data_dropna)
Drug_mortality_allstate['Drug/Alcohol Induced Cause Code'].value_counts()

#replace 'Missing' string in 'Deaths' column
Drug_mortality_allstate['Deaths'] = Drug_mortality_allstate['Deaths'].replace('Missing',np.nan)

#convert types in 'Deaths' all to float
Drug_mortality_allstate['Deaths'] = Drug_mortality_allstate['Deaths'].astype('float64',copy = False)

#not required
sort = Drug_mortality_allstate.sort_values(by='Deaths')

#Group data by Year and State
Grouped = Drug_mortality_allstate.groupby(['State','Year'],as_index=False)['Deaths'].sum()

#plot out in one graph
(ggplot(Grouped, aes(x ='Year', y='Deaths',group = 'State',color='State'))+
geom_point(alpha=0.2)+geom_line()
)

#plot out using facet_wrap & save
p=(ggplot(Grouped, aes(x ='Year', y='Deaths',group = 'State',color='State'))+
geom_point(alpha=0.2)+geom_line() +
facet_wrap('State')
)
(ggsave(p,width =10, height = 10))
