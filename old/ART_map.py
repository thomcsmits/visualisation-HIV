## Imports
import numpy as np
import pandas as pd
import altair as alt
import streamlit as st
from vega_datasets import data

## Load data
from data_prep import export_treatment_rate
art_rate = export_treatment_rate()

## Check line
st.write(art_rate.head())

## Allow using rows more than 5000
alt.data_transformers.disable_max_rows(); 

st.write('## HIV cases worldwide per year')

year = st.slider('year', min_value = int(art_rate['year'].min()), max_value = int(art_rate['year'].max()), value = 2010, step = 1)
hiv_df_long_year = art_rate[art_rate['year'] == str(year)]


## Set up basic world map as template backgorund
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

# selector = alt.selection_single(
#     fields = ['Country']
#     )

chart_base = alt.Chart(source
    ).properties( 
        width=width,
        height=height
    ).project(project
    # ).add_selection(selector
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(art_rate, 'country-code', ['Country','year','rate']),
    )


rate_scale = alt.Scale(domain=[art_rate['rate'].min(), art_rate['rate'].max()])
rate_color = alt.Color(field="Proportion of HIV patients (%)", type="quantitative", scale=rate_scale)
chart_rate = chart_base.mark_geoshape().encode(
    color = rate_color,
    tooltip = ['Country:N', 'rate:Q']
    #).transform_filter(
    #selector
    ).properties(
    title=f'Proportion of HIV patients receiving ART therapy'
)


chart2 = alt.vconcat(background + chart_rate
).resolve_scale(
    color='independent'
)


st.altair_chart(chart2, use_container_width=True)