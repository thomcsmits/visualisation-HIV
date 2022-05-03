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