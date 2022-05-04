## Imports
import numpy as np
import pandas as pd
import altair as alt
import streamlit as st
from vega_datasets import data

## Load data
from data_prep import export_hiv
hiv_df_long = export_hiv()

bins = [-1,0,10000, 50000,100000, 150000, 200000]
labels = ["-1-0","0 - 10000","10000-50000","50000-100000","100000-150000","150000-200000"]
hiv_df_long['cases_bucket'] = pd.cut(hiv_df_long['Cases'], bins=bins, labels=labels)

st.write(hiv_df_long.head())

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
        from_=alt.LookupData(hiv_df_long_year, 'country-code', ['Country','Year','cases_bucket']),
    )

#cases_scale = alt.Scale(domain=[hiv_df_long['Cases'].min(), hiv_df_long['Cases'].max()])

domain = ["No Data", "0 - 10k","10k-50k","50k-100k","100k-150k","150k +" ]
range_ = ['grey', '#aec7e8', '#ffbb78', '#ff9896', 'yellow', 'green']
range2 = alt.Scale(scheme='dark2')

st.write('Testing3', bins)

cases_color = alt.Color(field="Prevalence brackets", scale=alt.Scale(domain=domain,range=range_))
chart_cases = chart_base.mark_geoshape().encode(
    color = cases_color,
    tooltip = ['Country:N', 'cases_bucket:Q']
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