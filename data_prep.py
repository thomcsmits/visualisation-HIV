## Imports
import numpy as np
import pandas as pd
import altair as alt
import streamlit as st

## Read in raw data and clean
hiv_df = pd.read_csv('data/hiv_temporal.csv', index_col = 0)
years = [str(i) for i in range(1990, 2021)]
hiv_df = hiv_df[years]

hiv_df = hiv_df.apply(lambda x: x.str.replace('<', '').str.replace(' ', ''))
hiv_df = hiv_df.replace('...', 0)
hiv_df = hiv_df.apply(lambda x: pd.to_numeric(x))

hiv_df = hiv_df.reset_index()


## add country codes
country_df = pd.read_csv('https://raw.githubusercontent.com/hms-dbmi/bmi706-2022/main/cancer_data/country_codes.csv', dtype = {'conuntry-code': str})

## not all countries are written the same. Dict for conversion:
country_mapping = {
    "Democratic People's Republic of Korea" : "Korea (Democratic People's Republic of)",
    'Democratic Republic of the Congo' : 'Congo, Democratic Republic of the',
    'Republic of Korea' : 'Korea, Republic of',
    'Republic of Moldova' : 'Moldova, Republic of',
    'United Kingdom' : 'United Kingdom of Great Britain and Northern Ireland',
    'United Republic of Tanzania' : 'Tanzania, United Republic of',
    'United States' : 'United States of America'}
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




## Hannah adding from here:

## Read in raw treatment data (rate and population)

art_rate = pd.read_csv('ART_treatment_pct.csv', index_col = 0)
art_pop = pd.read_csv('ART_treatment_pop.csv', index_col = 0)


periods = art_rate.columns

## Clean rate data    
## Convert treatment rate data into long format

art_rate.reset_index(inplace=True)
art_rate = art_rate.rename(columns = {'index':'Country'})
art_rate = art_rate.melt(id_vars='Country', value_vars = periods, var_name = 'year', value_name = 'rate')

## Add metric column
art_rate['metric'] = 'ART_rate'

## Replacing <1 and >98 to 0.5 and 98.5 respectively
    
art_rate['rate'] = art_rate['rate'].replace(['<1'],0.5)
art_rate['rate'] = art_rate['rate'].replace(['>98'],98.5)
art_rate['rate'] = art_rate['rate'].replace('...', 0)


## Convert to int
art_rate = art_rate.astype({'year':'int'})
art_rate = art_rate.astype({'rate':'int'})

## Clean population data

art_pop = art_pop.replace('...', 0)

## Calculate percentage change in treated population per year

art_popchange = art_pop.pct_change(axis = 1)
art_popchange = art_popchange.drop(labels = '2010', axis = 1)

# Convert to long dataformat 
art_popchange.reset_index(inplace=True)
art_popchange = art_popchange.rename(columns = {'index':'Country'})
periods = art_popchange.columns
art_popchange = art_popchange.melt(id_vars='Country', value_vars = periods, var_name = 'year', value_name = 'ART_pct_change')
art_popchange

# Exporting treatment df
def export_treatment_rate(): 
    return art_rate

def export_treament_pop():
    return art_popchange