import numpy as np
import pandas as pd
import altair as alt
import streamlit as st
from vega_datasets import data

@st.cache
def load_data():

    # Loading ART treatment rate data (saved in pct.csv file)
    
    art_rate = pd.read_csv('data/ART_treatment_pct.csv', index_col = 0)
    periods = art_rate.columns
    
    # Converting treatment rate data into long format

    art_rate.reset_index(inplace=True)
    art_rate = art_rate.rename(columns = {'index':'Country'})
    art_rate = art_rate.melt(id_vars='Country', value_vars = periods, var_name = 'year', value_name = 'rate')
    art_rate['metric'] = 'ART_rate'

    #Replacing <1 and >98 to 0.5 and 98.5 respectively
    
    art_rate['rate'] = art_rate['rate'].replace(['<1'],0.5)
    art_rate['rate'] = art_rate['rate'].replace(['>98'],98.5)
    art_rate = art_rate.replace('...', 0)

    # Ensuring columns are int
    #art_rate['year'] = art_rate['year'].astype('int')
    #art_rate['ART_rate'] = art_rate['ART_rate'].astype('int')

    # Loading ART total treated population data (saved in no.csv file) UPDATE, NOT CURRENTLY LINKING TO CORRECT FILE
    art_total = pd.read_csv('data/ART_treatment_pop.csv', index_col = 0)
    art_total = art_total.replace('...', 0)
    
    return art_rate, art_total

# Loading the ART treatment data
art_rate, art_total  = load_data()

#Check line for df - TO REMOVE FROM APP IN  FINAL VERSION
st.write(art_rate.head(20))
st.write(art_total.head(5))
# st.write(art_tot.head5)

# Creating table of percetange change per year in treated population

pct_change = art_total.pct_change(axis = 1)

st.write(pct_change)


#Adding preliminary title

st.write("Task 2: Linking HIV to ART coverage")

# Adding multi-select country button

countries_all = art_df.index

multiselect_country = st.multiselect("Select Countries:", countries_all)

# Adding year slider 

years_all = art_df.columns

slider_year = st.slider("Select year:", min_value = min(years_all), max_value = max(years_all))

year = slider_year

# Subsetting data for map based on country and time period selection

subset = art_df[year]
subset = subset.loc[multiselect_country]

# Checking df manipulation TO BE REMOVED
st.write(subset)

#subset = subset[subset["Country"].isin(multiselect_country )]

# Background chart 

source = alt.topo_feature(data.world_110m.url, 'countries')

width = 600
height  = 300
project = 'equirectangular'

background = alt.Chart(source
).mark_geoshape(
    fill='#aaa',
    stroke='white'
).properties(
    width=width,
    height=height
).project(project)

chart_base = alt.Chart(source
    ).properties( 
        width=width,
        height=height
    ).project(project
    ).transform_lookup(
        lookup="id",
        from_=alt.LookupData(subset)
    )


chart_art = background + chart_art_rate.resolve_scale(color='indpenden')

st.altair_chart(chart_art, use_container_width=True)
