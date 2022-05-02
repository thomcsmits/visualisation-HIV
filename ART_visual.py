import numpy as np
import pandas as pd
import altair as alt
import streamlit as st
from vega_datasets import data

@st.cache
def load_data():

    art_df = pd.read_csv('data/ART_treatment.csv', index_col = 0)
    years = [str(i) for i in range(2010, 2020)]
    art_df = art_df[years]
    st.write("testing loaddata")
    
    return art_df

# Loading data
art_df= load_data()
st.write(art_df.head())
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

st.altair_chart(background, use_container_width=True)