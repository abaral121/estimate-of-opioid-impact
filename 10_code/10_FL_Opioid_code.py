import os
import pandas as pd

os.chdir('/Users/N1/690 local/')
# Import dataset and pick the columns we want
df_check = pd.read_csv("arcos_all_washpost.tsv", nrows=20, sep="\t",
                       usecols=['BUYER_COUNTY', 'TRANSACTION_DATE',
                                'CALC_BASE_WT_IN_GM', 'MME_Conversion_Factor',
                                'BUYER_STATE'])

# Check column names to find column to filter by
for col in df_check.columns:
    print(col)
    pass

# Check how BUYER_STATE values are stored
df_check['BUYER_STATE']

# Filter out for Florida by 1000000 rows, selecting columns we need
iter_csv = pd.read_csv("arcos_all_washpost.tsv",
                       iterator=True, sep="\t", chunksize=1000000,
                       usecols=['BUYER_COUNTY', 'TRANSACTION_DATE',
                                'CALC_BASE_WT_IN_GM', 'MME_Conversion_Factor',
                                'BUYER_STATE'])
FL_data = pd.concat([chunk[chunk['BUYER_STATE'] == "FL"] for chunk in iter_csv])

# Make sure everything came out right
FL_data.head()

# Check # of rows
FL_data.shape

os.chdir('/Users/N1/Op690/estimating-impact-of-opioid-prescription-regulations-team-3/00_source/')
FL_data.to_parquet("FLopiate.parquet", engine='fastparquet')
