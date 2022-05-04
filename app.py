## Imports
import altair as alt
import streamlit as st

## Load data
from data_prep import export_hiv
hiv_df_long = export_hiv()

from data_prep import export_treatment_rate
art_rate = export_treatment_rate()

from data_prep import export_treament_pop
art_popchange = export_treament_pop()

## Allow using rows more than 5000
alt.data_transformers.disable_max_rows(); 


## Streamlit configurations
st.set_page_config(
    layout="wide",
	initial_sidebar_state = "auto", 
	page_title = "HIV_dashboard",
)


## Set up country select in sidebar
with st.sidebar: 
    countries = st.multiselect("Countries", hiv_df_long["Country"].unique())

hiv_selection_lower = hiv_df_long[hiv_df_long['Country'].isin(countries)]
art_selection_lower = art_popchange[art_popchange['Country'].isin(countries)]

## Title and year option
st.write('### HIV dashboard')
st.write('#### Explore spatial and temporal HIV cases, ART and PrEP coverage, and social factors.')

year = st.slider('Year', min_value = int(hiv_df_long['Year'].min()), max_value = int(hiv_df_long['Year'].max()), value = 2010, step = 1)
hiv_selection_upper = hiv_df_long[hiv_df_long['Year'] == str(year)]
art_selection_upper = art_rate[art_rate['year'] == year]

show_all = st.radio('Do you want to display all countries or only selected?', ('All', 'Selected'))

if show_all == 'Selected':
    hiv_selection_upper = hiv_selection_upper[hiv_selection_upper['Country'].isin(countries)]
    art_selection_upper = art_selection_upper[art_selection_upper['Country'].isin(countries)]


## Loading in charts with subsetted data
from charts import return_temporal_map, return_temporal_line, return_art_map, return_art_line
chart_cases_map = return_temporal_map(hiv_selection_upper, hiv_df_long)
chart_cases_line = return_temporal_line(hiv_selection_lower)
chart_art_map = return_art_map(art_selection_upper)
chart_art_line = return_art_line(art_selection_lower)


## Displaying in streamlit with layout
comb = (chart_cases_map | chart_art_map) 
st.altair_chart(comb, use_container_width=False)

c1, c2 = st.columns(2)
c1.altair_chart(chart_cases_line, use_container_width=False)
c2.altair_chart(chart_art_line, use_container_width=False)

