## Imports
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