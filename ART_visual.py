import numpy as np
import pandas as pd
import altair as alt
import streamlit as st
from vega_datasets import data

@st.cache
def load_data():

    # Loading ART treatment rate data

    art_data = pd.read_csv('data/ART_treatment_pct.csv', index_col = 0)
    periods = art_data.columns
    art_data.reset_index(inplace=True)
    art_data = art_data.rename(columns = {'index':'Country'})
    
    # Converting data into long format

    art_df = art_data.melt(id_vars='Country', value_vars = periods, var_name = 'year', value_name = 'ART_rate')
    art_df['metric'] = 'ART_rate'

    #Replacing <1 and >98 to 1 and 98 respectively
    
    art_df['year'] = art_df['year'].replace(['<1'],0.9)
    art_df['year'] = art_df['year'].replace(['>98'],98.1)
    art_df['year'] = art_df['year'].replace(['...'],0)

    return art_df

# Loading the ART treatment data
art_df= load_data()

#Check line for df - TO REMOVE FROM APP IN  FINAL VERSION
st.write(art_df.head(5))


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
