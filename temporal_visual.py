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


## Set up basic world map as template backgorund
source = alt.topo_feature(data.world_110m.url, 'countries')

width = 600
height  = 300
project = 'equirectangular'

map_background = alt.Chart(source
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


## Chart 1: World map with cases and temporal slider
st.write('## HIV cases worldwide per year')

year = st.slider('Year', min_value = int(hiv_df_long['Year'].min()), max_value = int(hiv_df_long['Year'].max()), value = 2010, step = 1)
hiv_df_long_year = hiv_df_long[hiv_df_long['Year'] == str(year)]

chart_base_map = alt.Chart(source
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
chart_cases = chart_base_map.mark_geoshape().encode(
    color = cases_color,
    tooltip = ['Country:N', 'Cases:Q']
    #).transform_filter(
    #selector
    ).properties(
    title=f'HIV cases worldwide'
)

chart_cases_map = alt.vconcat(map_background + chart_cases
).resolve_scale(
    color='independent'
)

st.altair_chart(chart_cases_map, use_container_width=True)

## Chart 2: linechart for selected countries
countries = st.multiselect("Countries", hiv_df_long["Country"].unique())
hiv_df_long_country = hiv_df_long[hiv_df_long['Country'].isin(countries)]


chart_base_map_line = alt.Chart(hiv_df_long_country).mark_line().encode(
    x = alt.X('Year:Q', axis=alt.Axis(tickMinStep=1)),
    y = alt.Y('Cases:Q', title="Cases"), 
    color = 'Country:N'
).properties(
    width=500,
    height=400,
    title = "Compare temporal HIV cases for countries"
)

brush_map_line = alt.selection_interval( encodings=['x'])

brush_map_line_upper = chart_base_map_line.encode(
    alt.X('Year:Q', axis=alt.Axis(tickMinStep=1), scale = alt.Scale(domain=brush_map_line))
)

brush_map_line_lower = chart_base_map_line.properties(
    height = 60
).add_selection(brush_map_line)

brush_map_line_lower2 = brush_map_line_upper & brush_map_line_lower



st.altair_chart(brush_map_line_lower2, use_container_width=True)
