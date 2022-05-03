## Imports
import numpy as np
import pandas as pd
import altair as alt
import streamlit as st
from vega_datasets import data

## Load data
from data_prep import export_hiv
hiv_df_long = export_hiv()

## Allow using rows more than 5000
alt.data_transformers.disable_max_rows(); 

st.write('## HIV cases worldwide per year')

year = st.slider('Year', min_value = int(hiv_df_long['Year'].min()), max_value = int(hiv_df_long['Year'].max()), value = 2010, step = 1)
hiv_df_long_year = hiv_df_long[hiv_df_long['Year'] == str(year)]


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
        from_=alt.LookupData(hiv_df_long_year, 'country-code', ['Country','Year','Cases']),
    )


cases_scale = alt.Scale(domain=[hiv_df_long['Cases'].min(), hiv_df_long['Cases'].max()])
cases_color = alt.Color(field="Cases", type="quantitative", scale=cases_scale)
chart_cases = chart_base.mark_geoshape().encode(
    color = cases_color,
    tooltip = ['Country:N', 'Cases:Q']
    #).transform_filter(
    #selector
    ).properties(
    title=f'HIV cases worldwide'
)


chart2 = alt.vconcat(background + chart_cases
).resolve_scale(
    color='independent'
)


st.altair_chart(chart2, use_container_width=True)