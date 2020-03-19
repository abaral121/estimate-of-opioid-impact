import pandas as pd
import os

# Change to directory for ease of loading files
os.chdir('/Users/N1/Op690/estimating-impact-of-opioid-prescription-regulations-team-3/00_source/')
pd.set_option('display.max_columns', None)


###############################################################################
# FL_Opiate cleaning
###############################################################################

# FL_Opiate load with only the columns we need
FL_Opiate = pd.read_parquet("FLopiate.parquet", engine='fastparquet', columns=['BUYER_COUNTY', 'TRANSACTION_DATE',
                                                                               'CALC_BASE_WT_IN_GM',
                                                                               'MME_Conversion_Factor', 'BUYER_STATE'])

# Drop Duplicates - there are no duplicates
# FL_Opiate.shape
# FL_Opiate = FL_Opiate.drop_duplicates()
# FL_Opiate.shape

# Extract State from BUYER_COUNTY -- no longer needed when we changed the file
# FL_Mort['State'] = FL_Mort['County'].str.extract('([A-Z]{2}$)', expand=True)
# FL_Mort.head(5)

# Extract year from the TRANSACTION_DATE string
FL_Opiate['TRANSACTION_DATE'] = FL_Opiate['TRANSACTION_DATE'].astype('str')
FL_Opiate['Year'] = FL_Opiate['TRANSACTION_DATE'].str.extract('([0-9]{4}$)', expand=True)
FL_Opiate.drop(['TRANSACTION_DATE'], axis=1, inplace=True)
FL_Opiate.head(5)

# Rename so we can merge easily later
FL_Opiate.rename(columns={'BUYER_STATE': 'State'}, inplace=True)
FL_Opiate.rename(columns={'BUYER_COUNTY': 'County'}, inplace=True)
FL_Opiate.head()

# Conversion to float for upcoming math // both these convert to float
FL_Opiate['MME_Conversion_Factor'] = FL_Opiate['MME_Conversion_Factor'].astype(float)
FL_Opiate['CALC_BASE_WT_IN_GM'] = pd.to_numeric(FL_Opiate['CALC_BASE_WT_IN_GM'])

# Checking Type
FL_Opiate['MME_Conversion_Factor'].dtype
FL_Opiate['CALC_BASE_WT_IN_GM'].dtype

# Get MME and drop columns that are no longer needed
FL_Opiate['MME'] = FL_Opiate.CALC_BASE_WT_IN_GM * FL_Opiate.MME_Conversion_Factor
FL_Opiate.drop(['CALC_BASE_WT_IN_GM', 'MME_Conversion_Factor'], axis=1, inplace=True)
FL_Opiate.head()

# Drop missing County values (not needed)
FL_Opiate[FL_Opiate['County'] == None]
FL_Opiate = FL_Opiate[FL_Opiate['County'] != None]

# Save to Parquet file
FL_Opiate.to_parquet("FLopiate cleaned.parquet", engine='fastparquet')


###############################################################################
# FL_Mort cleaning
###############################################################################

# Load and Drop useless columns
FL_Mort = pd.read_csv("FL_mortality_2003_2015.csv", usecols=['Year', 'County', 'Deaths', 'State'])

FL_Mort.head(5)

# Change from lower case to upper case so that the merged values in 'County' will match
FL_Mort['County'] = FL_Mort['County'].str.upper()
FL_Mort['County'] = FL_Mort['County'].str.rstrip(' COUNTY')

# Make a replace dictionary fix the different naming
Replace_list = ['WAL', 'LE', 'ST.JOHNS', 'ST. LUCIE',
                'BA', 'CLA', 'LEV', 'MARI', 'MARTI', 'NASSA', 'PAS']
Replace_fixed = ['WALTON', 'LEE', 'SAINT JOHNS', 'SAINT LUCIE',
                 'BAY', 'CLAY', 'LEVY', 'MARION', 'MARTIN', 'NASSAU', 'PASCO']
Replace_dict = dict(zip(Replace_list, Replace_fixed))

# Replace Counties with proper names
FL_Mort['County'].replace(Replace_dict, inplace=True)

# Drop Years beyond 2012 from Mort
FL_Mort['Year'] = FL_Mort['Year'].astype(int)
FL_Mort = FL_Mort[FL_Mort['Year'] < 2013]

FL_Mort.shape

FL_Mort.to_csv("20_FL_Mort cleaned.csv")
