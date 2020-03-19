import pandas as pd
import numpy as np
from sklearn import linear_model

df = pd.read_csv('C:/Users/Jiajie Zhang/IDS_mid_project/Intermediate_data/Census_raw.csv',skiprows = 1)

Census  =df.drop(columns = ['Id','Id2','April 1, 2010 - Census','April 1, 2010 - Estimates Base'])
#reset column names
Census.columns = ['Geography','2010','2011','2012','2013','2014','2015','2016','2017','2018']

# extropolate Population to 2003-2010
Year = np.arange(2010,2019).reshape(-1,1)
Pred_Year = np.arange(2003,2010).reshape(-1,1)
#Pred = np.array([]).reshape(Pred_Year.shape)
Pred = np.array([]).reshape(-1,7)
for i in range(Census.shape[0]):
    lr = linear_model.LinearRegression()
    lr.fit(X= Year,y=Census.iloc[i,1:])
    y_pred = lr.predict(Pred_Year)
    Pred = np.vstack((Pred,y_pred))
#convert prediction result to df
columns = ['2003','2004','2005','2006','2007','2008','2009']
Pred_df =pd.DataFrame(Pred,columns = columns)

#merge and reorder columns
Merged_Census = Census.merge(Pred_df,left_index =True,right_index = True)
Merged_Census = Merged_Census[['Geography','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018']]
Merged_Census = Merged_Census.set_index('Geography')

#save 
Merged_Census.to_csv('C:/Users/Jiajie Zhang/IDS_mid_project/Intermediate_data/Census_Full.csv')
