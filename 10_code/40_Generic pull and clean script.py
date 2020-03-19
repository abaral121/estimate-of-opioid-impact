import pandas as pd
import numpy as np

### Inputs for pulling information ###
state = 'IN'

### Functions ###
def subseter (x):
    search1 = state
    search2 = "Drug poisonings"

    state_select = x["County"].str.endswith(search1, na=False)
    x = x[state_select]
    drug_select = x["Drug/Alcohol Induced Cause"].str.startswith(search2, na=False)
    return x[drug_select]

### Loading data in ###
iter_csv = pd.read_csv("C:/Users/abhis/Documents/Duke University/IDS 690 Practical Data Science/arcos_all_washpost.tsv",
iterator=True, chunksize=500000, sep = '\t', usecols=['BUYER_COUNTY', 'TRANSACTION_DATE', 'CALC_BASE_WT_IN_GM', 'MME_Conversion_Factor', 'BUYER_STATE'])

Opioid = pd.concat(   [chunk[chunk['BUYER_STATE']  == state] for chunk in iter_csv]   )

Mortality = pd.read_csv("C:/Users/abhis/Documents/Duke University/IDS 690 Practical Data Science/Mortality_Full.csv")
Mortality = subseter(Mortality)

Population = pd.read_csv("C:/Users/abhis/Documents/Duke University/IDS 690 Practical Data Science/16_Merged_population_Death_Data.csv")
Population = Population[Population['State'] == state]

### Load data sets in, if you want to skip previous steps ###
#Opioid = pd.read_csv("C:/Users/abhis/Desktop/IL_Opiate cleaned.csv")
#Mortality = pd.read_csv("C:/Users/abhis/Documents/Duke University/IDS 690 Practical Data Science/WA_Mortality_Full.csv")

### Looking at shapes ###
Opioid.shape
Mortality.shape

### Selecting columns ###
#Opioid = Opioid[['BUYER_COUNTY','DRUG_NAME', 'QUANTITY', 'TRANSACTION_DATE',
#                       'CALC_BASE_WT_IN_GM', 'DOSAGE_UNIT', 'Ingredient_Name',
#                       'MME_Conversion_Factor','dos_str', 'Revised_Company_Name'
#                       ,'BUYER_STATE']]

###  Extract year from the TRANSACTION_DATE string ###
Opioid['TRANSACTION_DATE'] = Opioid['TRANSACTION_DATE'].astype('str')
Opioid['Year'] = Opioid['TRANSACTION_DATE'].str.extract('([0-9]{4}$)', expand=True)

# Rename so we can merge later
Opioid.rename(columns = {'BUYER_STATE':'State'}, inplace = True)
Opioid.rename(columns = {'BUYER_COUNTY':'County'}, inplace = True)

### Creating MME no. ###
Opioid['MME'] = Opioid.CALC_BASE_WT_IN_GM * Opioid.MME_Conversion_Factor
Opioid = Opioid.copy()

### Recasting vars ###
Opioid['State'] = Opioid['State'].astype(str)
Opioid['Year'] = Opioid['Year'].astype(str)
Opioid['County'] = Opioid['County'].astype(str)

Mortality['County'] = Mortality['County'].astype(str)
Mortality['Year'] = Mortality['Year'].astype(int)
Mortality['Year'] = Mortality['Year'].astype(str)
#Mortality['Year'] = Mortality['Year'].str.rstrip('.0')
Mortality[['County','State']] = Mortality.County.str.split(', ',expand = True)
Mortality['State'] = Mortality['State'].astype(str)
Mortality['Deaths'] = Mortality['Deaths'].astype(float).astype(int)

### Data cleaning ###
Mortality['County'] = Mortality['County'].str.rstrip(' County')
Mortality['County'] = Mortality['County'].str.upper()

Mortality['Year'].unique()

### Aggregating Opioid data & Mortality do for mortality ###
Opioid = Opioid.groupby(['County', 'Year', 'State']).sum().reset_index()
Opioid = Opioid.drop(columns = ['CALC_BASE_WT_IN_GM', 'DOSAGE_UNIT', 'MME_Conversion_Factor', 'dos_str'],  errors = 'ignore')
Opioid.drop_duplicates()

Mortality = Mortality.groupby(['County', 'Year', 'State']).sum().reset_index()
Mortality = Mortality.drop(columns = ['Unnamed: 0', 'County Code', 'Year Code'], errors = 'ignore')
Mortality = Mortality.drop_duplicates()

### Copy and paste into excel and identify the misnamed Mortality Counties, use vlookup ###
sorted(Opioid['County'].unique())
sorted(Mortality['County'].unique())






### Replaceing misnamed counties ###

### Indianna ###
#d = {'ALLE':'ALLEN','DEARBOR':'DEARBORN', 'ELKHAR':'ELKHART', 'GRA':'GRANT', 'HAMIL':'HAMILTON', 'HENR':'HENRY',
#'JACKS':'JACKSON', 'JOHNS':'JOHNSON', 'KOSCIUSK':'KOSCIUSKO', 'MADIS':'MADISON', 'MARI':'MARION', 'MONTGOMER':'MONTGOMERY',
#'MORGA':'MORGAN', 'SC':'SCOTT', 'SHELB':'SHELBY', 'ST.JOSEPH':'ST JOSEPH','VIG':'VIGO'}

### Illinois ###
#d = {'BUREA':'BUREAU', 'CHAMPAIG':'CHAMPAIGN', 'FRANKLI':'FRANKLIN', 'GRUND':'GRUNDY', 'JEFFERS':'JEFFERSON',
#'LASALLE':'LA SALLE', 'MADIS':'MADISON', 'MARI':'MARION', 'MCHENR':'MCHENRY', 'MCLEA':'MCLEAN', 'SANGAM':'SANGAMON',
#'ST.CLAIR':'SAINT CLAIR', 'VERMILI':'VERMILION', 'WILLIAMS':'WILLIAMSON', 'WINNEBAG':'WINNEBAGO'}

### Georgia ###
#d = {'CAMDE':'CAMDEN', 'CLA':'CLAY', 'DOUGHER':'DOUGHERTY', 'FUL':'FULTON', 'GORD':'GORDON', 'GWINNE':'GWINNETT',
#'HARALS':'HARALSON', 'HENR':'HENRY', 'JACKS':'JACKSON', 'MADIS':'MADISON', 'MURRA':'MURRAY', 'NEW':'NEWTON',
#'WAL':'WALTON'}

### Pensalvnia ###
#d = {'ALLEGHE':'ALLEGHENY', 'CARB':'CARBON', 'DAUPHI':'DAUPHIN', 'FRANKLI':'FRANKLIN','JEFFERS':'JEFFERSON',
#'LEBA':'LEBANON', 'MC KEA':'MCKEAN', 'MIFFLI':'MIFFLIN', 'MONTGOMER':'MONTGOMERY', 'NORTHAMP':'NORTHAMPTON',
#'SOMERSE':'SOMERSET', 'VENANG':'VENANGO', 'WASHING':'WASHINGTON'}

### Ohio ###
#d = {'ALLE':'ALLEN', 'BELM':'BELMONT', 'BROW':'BROWN', 'CHAMPAIG':'CHAMPAIGN', 'CLERM':'CLERMONT', 'CLI':'CLINTON',
#'FRANKLI':'FRANKLIN', 'GUERNSE':'GUERNSEY', 'HAMIL':'HAMILTON', 'HARDI':'HARDIN', 'HUR':'HURON', 'JACKS':'JACKSON',
#'JEFFERS':'JEFFERSON', 'LORAI':'LORAIN', 'MADIS':'MADISON', 'MARI':'MARION', 'MONTGOMER':'MONTGOMERY', 'PICKAWA':'PICKAWAY',
#'SANDUSK':'SANDUSKY', 'SCI':'SCIOTO', 'SHELB':'SHELBY', 'SUMMI':'SUMMIT', 'UNI':'UNION', 'WARRE':'WARREN', 'WASHING':'WASHINGTON'}

### Texas ###
#d = {'ANDERS':'ANDERSON', 'CAMER':'CAMERON', 'COLLI':'COLLINS', 'DE':'DE WITT', 'EL PAS':'EL PASO', 'GALVES':'GALVESTON',
#'GRAYS':'GRAYSON', 'HARDI':'HARDIN', 'HIDALG':'HILDAGO', 'JEFFERS':'JEFFERSON', 'JOHNS':'JOHNSON', 'KAUFMA':'KAUFMAN',
#'LIBER':'LIBERTY', 'MCLENNA':'MCLENNAN', 'MONTGOMER':'MONTGOMERY', 'SAN PATRICI':'SAN PATRICIO', 'TARRA':'TARRANT',
#'TOM GREE':'TOM GREEN', 'VAN ZAND':'VAN ZANDT', 'WILLIAMS':'WILLIAMSON'}

### Florida ###
#d = {'ALACHUA':'ALACHUA', 'CLA':'CLAY', 'HERNAND':'HERNANDO', 'LE':'LEON', 'LEV':'LEVY', 'MARI':'MARION', 'NASSA':'NASSAU',
#'PASC':'PASCO', 'ST.JOHNS':'SAINT JOHNS', 'ST.LUCIE':'SAINT LUCIE', 'WAL':'WALTON'}

Mortality["County"] = Mortality["County"].replace(d)

### REMOVE ANY COUNTIES THAT YOU CANNOT FIND A REPLACEMENT !!! ###
Mortality["County"].unique()
Opioid['County'].unique()

### Filter out stuff ###
Opioid = Opioid.query('County != "nan"')
#Mortality = Mortality.query('County != "MAC"')

Mortality["County"].unique()
Opioid['County'].unique()

### Merging Mortality and Opioid ###
Combine =  pd.merge(Opioid, Mortality, how = 'left', on = ['County', 'Year', 'State'], validate = '1:1')
Combine =  pd.merge(Combine, Population, how = 'left', on = ['Year', 'State'], validate = '1:1')

### Write out, puts in state name into path ###
out = ("C:/Users/abhis/Documents/Duke University/IDS 690 Practical Data Science/{}_cleaned_and_merged_full.csv").format(state)
Combine.to_csv(out)


Mortality['Deaths'].dtype
Combine_t['Deaths'].astype(float).unique()
