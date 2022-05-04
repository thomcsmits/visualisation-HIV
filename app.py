## Imports
import altair as alt
import streamlit as st

## Load data
from data_prep import export_hiv, export_treatment_rate, export_treament_pop, export_gdp, export_drug, export_ph_gdp, export_merged_gdp_ph
hiv_df_long = export_hiv()
art_rate = export_treatment_rate()
art_popchange = export_treament_pop()

gdp = export_gdp()
drug = export_drug()
ph_gdp = export_ph_gdp()
merged_gdp_ph = export_merged_gdp_ph()

## Allow using rows more than 5000
alt.data_transformers.disable_max_rows(); 


## Streamlit configurations
st.set_page_config(
    layout="wide",
	initial_sidebar_state = "auto", 
	page_title = "HIV dashboard",
    page_icon = 'img/hiv_icon.png'
)


## Set up country select in sidebar
with st.sidebar: 
    ## Select country
    countries = st.multiselect("Countries", hiv_df_long["Country"].unique())

    ## On worldmap, highlight all or only selected countries
    show_all = st.radio('Do you want to display all countries or only selected?', ('All', 'Selected'))

    ## Retrieve info on which to compare to temporal changes
    topic_selection1 = st.radio('Do you want to see all charts or compare two topics?', ('All', 'Two'))

    if topic_selection1 == 'Two':
        topic_selection2 = st.radio('What topic do you want to see on the left?', ('Cases', 'ART coverage', 'GDP', 'Healthcare funding', 'Drug deaths'))
        topic_selection3 = st.radio('What topic do you want to see on the right?', ('Cases', 'ART coverage', 'GDP', 'Healthcare funding', 'Drug deaths'))


hiv_selection_lower = hiv_df_long[hiv_df_long['Country'].isin(countries)]
art_selection_lower = art_popchange[art_popchange['Country'].isin(countries)]
drug_selection_lower = drug[drug['Country'].isin(countries)]


## Title and year option
st.write('### HIV dashboard')
st.write('#### Explore spatial and temporal HIV cases, ART coverage, funding, and drug abuse.')

year = st.slider('Year', min_value = int(hiv_df_long['Year'].min()), max_value = int(hiv_df_long['Year'].max()), value = 2010, step = 1)
hiv_selection_upper = hiv_df_long[hiv_df_long['Year'] == str(year)]
art_selection_upper = art_rate[art_rate['year'] == year]
gdp_selection_upper = gdp[gdp['Year'] == year]
drug_selection_upper = drug[drug['Year'] == year]
ph_selection_upper = ph_gdp[ph_gdp['Year'] == year]

if show_all == 'Selected':
    hiv_selection_upper = hiv_selection_upper[hiv_selection_upper['Country'].isin(countries)]
    art_selection_upper = art_selection_upper[art_selection_upper['Country'].isin(countries)]
    gdp_selection_upper = gdp_selection_upper[gdp_selection_upper['Country'].isin(countries)]
    ph_selection_upper = ph_selection_upper[ph_selection_upper['Country'].isin(countries)]
    drug_selection_upper = drug_selection_upper[drug_selection_upper['Country'].isin(countries)]

merged_gdp_ph_lower = merged_gdp_ph[merged_gdp_ph['Country'].isin(countries)]
merged_gdp_ph_lower = merged_gdp_ph_lower[merged_gdp_ph_lower['Year'] == year]

## Loading in charts with subsetted data
from charts import return_temporal_map, return_temporal_line, return_art_map, return_art_line, return_gdp_plot, return_ph_gdp_chart, return_funding_bar, return_drug_chart, return_drug_bar
chart_cases_map = return_temporal_map(hiv_selection_upper, hiv_df_long, year)
chart_cases_line = return_temporal_line(hiv_selection_lower)
chart_art_map = return_art_map(art_selection_upper, art_rate, year)
chart_art_line = return_art_line(art_selection_lower)
chart_gdp_map = return_gdp_plot(gdp_selection_upper, gdp, year)
chart_ph_map = return_ph_gdp_chart(ph_selection_upper, ph_gdp, year)
chart_funding_bar = return_funding_bar(merged_gdp_ph_lower)
chart_drug_map = return_drug_chart(drug_selection_upper, drug, year)
chart_drug_bar = return_drug_bar(drug_selection_lower)


def select_correct_chart(topic_selection_choice):
    if topic_selection_choice == 'Cases':
        return chart_cases_map, chart_cases_line
    if topic_selection_choice == 'ART coverage':
        return chart_art_map, chart_art_line
    if topic_selection_choice == 'GDP':
        return chart_gdp_map, chart_funding_bar
    if topic_selection_choice == 'Healthcare funding':
        return chart_ph_map, chart_funding_bar
    if topic_selection_choice == 'Drug deaths':
        return chart_drug_map, chart_drug_bar


if topic_selection1 == 'Two':
    left_map, left_extra = select_correct_chart(topic_selection2)
    right_map, right_extra = select_correct_chart(topic_selection3)

    ## Displaying in streamlit with layout
    comb = (left_map | right_map) 
    st.altair_chart(comb, use_container_width=False)

    c1, c2 = st.columns(2)
    c1.altair_chart(left_extra, use_container_width=False)
    c2.altair_chart(right_extra, use_container_width=False)

else: 
    st.write('### Cases')
    c1, c2 = st.columns(2)
    st.write('### ART coverage')
    c3, c4 = st.columns(2)
    st.write('### GDP and healthcare funding')
    c5, c6 = st.columns(2)
    c7, c8 = st.columns(2)
    st.write('### Drug deaths')
    c9, c10 = st.columns(2)

  
    c1.altair_chart(chart_cases_map, use_container_width=False)
    c2.altair_chart(chart_cases_line, use_container_width=False)

    c3.altair_chart(chart_art_map, use_container_width=False)
    c4.altair_chart(chart_art_line, use_container_width=False)
    
    c5.altair_chart(chart_gdp_map, use_container_width=False)
    c6.altair_chart(chart_ph_map, use_container_width=False)
    c7.altair_chart(chart_funding_bar, use_container_width=False)
    
    c9.altair_chart(chart_drug_map, use_container_width=False)
    c10.altair_chart(chart_drug_bar, use_container_width=False)


