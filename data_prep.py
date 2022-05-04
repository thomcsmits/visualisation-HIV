## Imports
import numpy as np
import pandas as pd
from code_mappings import *

## Read in raw data and clean
hiv_df = pd.read_csv('data/hiv_temporal.csv', index_col = 0)
years = [str(i) for i in range(1990, 2021)]
hiv_df = hiv_df[years]

hiv_df = hiv_df.apply(lambda x: x.str.replace('<', '').str.replace(' ', ''))
hiv_df = hiv_df.replace('...', -1)
hiv_df = hiv_df.apply(lambda x: pd.to_numeric(x))

hiv_df = hiv_df.reset_index()


## add country codes
country_df = pd.read_csv('https://raw.githubusercontent.com/hms-dbmi/bmi706-2022/main/cancer_data/country_codes.csv', dtype = {'conuntry-code': str})

## Not all countries are written the same way. country_mapping is an imported dictionary.
for index, row in hiv_df.iterrows():
  if row['Country'] in country_mapping.keys():
    hiv_df.iloc[index, 0] = country_mapping[row['Country']]

hiv_df = hiv_df[hiv_df['Country'] != 'Global']


## long format
hiv_df_long = pd.melt(hiv_df, id_vars = "Country", value_vars = hiv_df.columns[1:], var_name = "Year", value_name = "Cases")

hiv_df_long = hiv_df_long.merge(
    country_df[['Country', 'country-code']],
    how = 'left',
    on = 'Country',
)

hiv_df_long['country-code'] = hiv_df_long['country-code'].astype(int)

def export_hiv(): 
    return hiv_df_long


## Read in raw treatment data (rate and population)
art_rate = pd.read_csv('data/ART_treatment_pct.csv', index_col = 0)
art_pop = pd.read_csv('data/ART_treatment_pop.csv', index_col = 0)

## Clean rate data    
## Convert treatment rate data into long format
art_rate.reset_index(inplace=True)
art_rate = art_rate.rename(columns = {'index':'Country'})

## Not all countries are written the same way. art_mapping is an imported dictionary.
for index, row in art_rate.iterrows():
  if row['Country'] in art_mapping.keys():
    art_rate.iloc[index, 0] = art_mapping[row['Country']]

art_rate = art_rate[art_rate['Country'] != 'Global']

art_rate = art_rate.melt(id_vars='Country', value_vars = art_rate.columns, var_name = 'year', value_name = 'rate')

## Replacing <1 and >98 to 0.5 and 98.5 respectively
art_rate['rate'] = art_rate['rate'].replace(['<1'],0.5)
art_rate['rate'] = art_rate['rate'].replace(['>98'],98.5)
art_rate['rate'] = art_rate['rate'].replace('...', 0)

## Convert to int
art_rate = art_rate.astype({'year':'int'})
art_rate = art_rate.astype({'rate':'int'})

art_rate = art_rate.merge(
    country_df[['Country', 'country-code']],
    how = 'left',
    on = 'Country',
)

## Clean population data
art_pop = art_pop.replace('...', 0)

## Calculate percentage change in treated population per year
art_popchange = art_pop.pct_change(axis = 1)
art_popchange = art_popchange.drop(labels = '2010', axis = 1)

# Convert to long dataformat 
art_popchange.reset_index(inplace=True)
art_popchange = art_popchange.rename(columns = {'index':'Country'})

for index, row in art_popchange.iterrows():
  if row['Country'] in art_mapping.keys():
    art_popchange.iloc[index, 0] = art_mapping[row['Country']]

art_popchange = art_popchange[art_popchange['Country'] != 'Global']
art_popchange = art_popchange.melt(id_vars='Country', value_vars = art_popchange.columns, var_name = 'year', value_name = 'ART_pct_change')

# Exporting treatment df
def export_treatment_rate(): 
    return art_rate

def export_treament_pop():
    return art_popchange
    


## World GDP

## read in GDP data
gdp = pd.read_csv('data/gdp-per-capita-worldbank.csv')
gdp = gdp.drop(['Code'], axis=1)
gdp = gdp.rename(columns={"Entity": "Country"}) # Rename column to 'Country'
gdp = gdp.rename(columns={"GDP per capita, PPP (constant 2017 international $)": "GDP_in_dollars"}) # Rename column to 'Country'

## Not all countries are written the same way. country_gdp is an imported dictionary.
for index, row in gdp.iterrows():
    if row['Country'] in country_mapping_gdp.keys():
        gdp.iloc[index, 0] = country_mapping_gdp[row['Country']]

## remove country data that does not match temporal data
exclusion = np.setxor1d(gdp['Country'].unique(), hiv_df_long['Country'].unique())
gdp = gdp[~gdp['Country'].isin(exclusion)]

## Add country codes and convert to int
gdp = gdp.merge(
    country_df[['Country', 'country-code']],
    how = 'left',
    on = 'Country')

gdp['country-code'] = gdp['country-code'].astype(int)

## reindex and drop extra index column
gdp = gdp.reset_index()
gdp = gdp.drop(['index'], axis=1)

## Deaths due to drug abuse

## read in drug and substance disorders data
drug = pd.read_csv('data/deaths-substance-disorders.csv')
drug = drug.drop(['Code'], axis=1)
drug = drug.rename(columns={"Entity": "Country"}) # Rename column to 'Country'

## rename countries based on gdp-dict
for index, row in drug.iterrows():
    if row['Country'] in country_mapping_gdp.keys():
        drug.iloc[index, 0] = country_mapping_gdp[row['Country']]

## sum over the different drug causitive agents
drug['Drug_Deaths'] = drug.iloc[:,3:9].sum(axis=1)
drug = drug.drop(drug.iloc[:,2:8] , axis=1)

## Add country codes and convert to int
drug = drug.merge(
    country_df[['Country', 'country-code']],
    how = 'left',
    on = 'Country')

## remove country data that does not match temporal data
exclusion = np.setxor1d(drug['Country'].unique(), hiv_df_long['Country'].unique())
drug = drug[~drug['Country'].isin(exclusion)]

## reindex and drop extra index column
drug = drug.reset_index()
drug = drug.drop(['index'], axis=1)

## Public Health Expense as a % of GDP

## read in public healthcare expenses for GDP data
ph_gdp = pd.read_csv('data/public-healthcare-spending-share-gdp.csv')
ph_gdp = ph_gdp.drop(['Code'], axis=1)
ph_gdp = ph_gdp.rename(columns={"Entity": "Country"})
ph_gdp = ph_gdp.rename(columns={"Domestic general government health expenditure (% of GDP)": "GDP_percent_towards_health"})

## rename countries based on gdp-dict
for index, row in ph_gdp.iterrows():
    if row['Country'] in country_mapping_gdp.keys():
        ph_gdp.iloc[index, 0] = country_mapping_gdp[row['Country']]

## Add country codes
ph_gdp = ph_gdp.merge(
    country_df[['Country', 'country-code']],
    how = 'left',
    on = 'Country')

## remove country data that does not match temporal data
exclusion = np.setxor1d(ph_gdp['Country'].unique(), hiv_df_long['Country'].unique())
ph_gdp = ph_gdp[~ph_gdp['Country'].isin(exclusion)]

## reindex and drop extra index column
ph_gdp = ph_gdp.reset_index()
ph_gdp = ph_gdp.drop(['index'], axis=1)

## Export all 3 datasets (GDP, Drug Deaths, Public Health) as functions
def export_gdp(): 
    return gdp

def export_drug():
    return drug

def export_ph_gdp():
    return ph_gdp