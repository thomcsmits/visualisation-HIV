## Imports
import numpy as np
import pandas as pd
import altair as alt
import streamlit as st

## Read in raw data and clean

hiv_df = pd.read_csv('data/hiv_temporal.csv', index_col = 0)
years = [str(i) for i in range(1990, 2021)]
hiv_df = hiv_df[years]


hiv_df = hiv_df.apply(lambda x: x.str.replace('<', '').str.replace(' ', ''))
hiv_df = hiv_df.replace('...', 0)
hiv_df = hiv_df.apply(lambda x: pd.to_numeric(x))

hiv_df = hiv_df.reset_index()

hiv_df_long = pd.melt(hiv_df, id_vars = "Country", value_vars = hiv_df.columns[1:], var_name = "Year", value_name = "Cases")
print(hiv_df_long.head())
