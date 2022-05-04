## Imports
import numpy as np
import pandas as pd
import altair as alt
import streamlit as st
from vega_datasets import data

## Load data
from data_prep import export_treatment_rate
from data_prep import export_treament_pop
art_rate = export_treatment_rate()
art_popchange = export_treament_pop()

## Check lines  - TO REMOVE
#st.write(art_rate.head())
#st.write(art_popchange.head())

## Bump chart for % change in treated population per year

## Adding country selector

countries = ['South Africa', 'Kenya']

countries_all = art_popchange["Country"].drop_duplicates()

multiselect_country = st.multiselect("Select Country:", countries_all, default = ['SouthAfrica', 'Kenya'])

subset_art_popchange = art_popchange[art_popchange["Country"].isin(multiselect_country )]

chart_treatment_change = alt.Chart(subset_art_popchange).mark_line(point = True).encode(
    x = alt.X("year:O", title="year"),
    y="rank:O",
    color=alt.Color("Country:N")
).transform_window(
    rank="rank()",
    sort=[alt.SortField("ART_pct_change", order="descending")],
    groupby=["year"]
).properties(
    title="Countries ranked overtime by the annual growth in the ART treated population",
    width=800,
    height=1000,
)

st.altair_chart(chart_treatment_change, use_container_width=True)


st.write('This allows for comparison between countries in efforts to role out ART therapy')