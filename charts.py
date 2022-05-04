## Imports
import numpy as np
import pandas as pd
import altair as alt
import streamlit as st
from vega_datasets import data


## Set up basic world map as template backgorund
source = alt.topo_feature(data.world_110m.url, 'countries')

width = 400
height  = 200
project = 'equirectangular'

map_background = alt.Chart(source
).mark_geoshape(
    fill = '#aaa',
    stroke = 'white'
).properties(
    width = width,
    height = height
).project(project)


def return_temporal_map(data_subset, data_full):
    if (data_subset.shape[0] == 0):
        return map_background.properties(title=f'HIV cases worldwide')

    chart_base_map = alt.Chart(source
        ).properties( 
            width = width,
            height = height
        ).project(project
        ).transform_lookup(
            lookup = 'id',
            from_ = alt.LookupData(data_subset, 'country-code', ['Country','Year','Cases']),
        )
     
    chart_base_map = alt.Chart(source
        ).properties( 
            width = width,
            height = height
        ).project(project
        ).transform_lookup(
            lookup = 'id',
            from_ = alt.LookupData(data_subset, 'country-code', ['Country','Year','Cases']),
        )

    cases_scale = alt.Scale(domain=[data_full['Cases'].min(), data_full['Cases'].max()]) #we want the domain to stay the same regardless of subset
    cases_color = alt.Color(field = 'Cases', type = 'quantitative', scale = cases_scale)
    chart_cases = chart_base_map.mark_geoshape().encode(
        color = cases_color,
        tooltip = ['Country:N', 'Cases:Q']
        ).properties(
        title=f'HIV cases worldwide'
    )

    chart_cases_map = alt.vconcat(map_background + chart_cases
    ).resolve_scale(
        color = 'independent'
    )

    return chart_cases_map


def return_temporal_line(data_subset):
    chart_base_map_line = alt.Chart(data_subset).mark_line().encode(
        x = alt.X('Year:Q', axis = alt.Axis(tickMinStep=1)),
        y = alt.Y('Cases:Q', title = "Cases"), 
        color = 'Country:N'
    ).properties(
        width = width,
        height = height,
        title = 'Compare temporal HIV cases for countries'
    )

    brush_map_line = alt.selection_interval( encodings=['x'])

    brush_map_line_upper = chart_base_map_line.encode(
        alt.X('Year:Q', axis=alt.Axis(tickMinStep=1), scale = alt.Scale(domain=brush_map_line))
    )

    brush_map_line_lower = chart_base_map_line.properties(
        height = height * 0.2
    ).add_selection(brush_map_line)

    brush_map_line_lower2 = brush_map_line_upper & brush_map_line_lower

    return brush_map_line_lower2



def return_art_map(data_subset):
    if (data_subset.shape[0] == 0):
        return map_background.properties(title=f'Proportion of HIV patients receiving ART therapy')

    chart_base = alt.Chart(source
        ).properties( 
            width = width,
            height = height
        ).project(project
        ).transform_lookup(
            lookup = 'id',
            from_ = alt.LookupData(data_subset, 'country-code', ['Country','year','rate']),
        )

    rate_scale = alt.Scale(domain=[data_subset['rate'].min(), data_subset['rate'].max()])
    rate_color = alt.Color(field = 'rate', type = 'quantitative', scale = rate_scale)
    chart_rate = chart_base.mark_geoshape().encode(
        color = rate_color,
        tooltip = ['Country:N', 'rate:Q']
        ).properties(
        title = f'Proportion of HIV patients receiving ART therapy'
    )

    chart_art_map = alt.vconcat(map_background + chart_rate
    ).resolve_scale(
        color = 'independent'
    )

    return chart_art_map



def return_art_line(data_subset):
    chart_treatment_change = alt.Chart(data_subset).mark_line(point = True).encode(
        x = alt.X('year:O', title='year'),
        y = 'rank:O',
        color=alt.Color('Country:N')
    ).transform_window(
        rank = 'rank()',
        sort = [alt.SortField('ART_pct_change', order = 'descending')],
        groupby = ['year']
    ).properties(
        title = 'Countries ranked overtime by the annual growth in the ART treated population',
        width = width * 1.2,
        height = height * 1.8,
    )

    return chart_treatment_change
