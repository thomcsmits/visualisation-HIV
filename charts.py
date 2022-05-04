## Imports
import altair as alt
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


def return_temporal_map(data_subset, data_full, selected_year):
    if (data_subset.shape[0] == 0):
        return map_background.properties(title=f'HIV cases worldwide in {selected_year}')

    chart_base_map = alt.Chart(source
        ).properties( 
            width = width,
            height = height
        ).project(project
        ).transform_lookup(
            lookup = 'id',
            from_ = alt.LookupData(data_subset, 'country-code', ['Country','Year','Cases']),
        )

    cases_scale = alt.Scale(domain=[data_full['Cases'].min(), data_full['Cases'].max()], type = 'log') #we want the domain to stay the same regardless of subset
    cases_color = alt.Color(field = 'Cases', type = 'quantitative', scale = cases_scale)
    chart_cases = chart_base_map.mark_geoshape().encode(
        color = cases_color,
        tooltip = ['Country:N', 'Cases:Q']
        ).properties(
        title=f'HIV cases worldwide in {selected_year}'
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



def return_art_map(data_subset, selected_year):
    if (data_subset.shape[0] == 0):
        return map_background.properties(title=f'Proportion of HIV patients receiving ART therapy in {selected_year}')

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
        title = f'Proportion of HIV patients receiving ART therapy in {selected_year}'
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
    ).resolve_scale(
        color = 'independent'
    )

    return chart_treatment_change


def return_gdp_plot(data_subset, data_full, selected_year):
    if (data_subset.shape[0] == 0):
        return map_background.properties(title=f'Global GDP distribution in {selected_year}')

    chart_base = alt.Chart(source
        ).properties( 
            width=width,
            height=height
        ).project(project
        ).transform_lookup(
            lookup = "id",
            from_= alt.LookupData(data_subset, "country-code", ['Country', 'Year', 'GDP_in_dollars']),
        )

    # fix the color schema so that it will not change upon user selection
    rate_scale = alt.Scale(domain=[data_full['GDP_in_dollars'].min(), data_full['GDP_in_dollars'].max()], scheme = "orangered")
    rate_color = alt.Color(field="GDP_in_dollars", type="quantitative", scale=rate_scale)
    chart_gdp = chart_base.mark_geoshape().encode(
        color = rate_color,
        tooltip=["GDP_in_dollars:N", "Country:O", "Year:O"]
        ).properties(
        title=f'Global GDP distribution in {selected_year}'
        )
    
    chart_gdp_map = alt.vconcat(map_background + chart_gdp
    ).resolve_scale(
        color = 'independent'
    )

    return chart_gdp_map


## GDP % Spent on Healthcare Data World Map
def return_ph_gdp_chart(data_subset, data_full, selected_year):
    if (data_subset.shape[0] == 0):
        return map_background.properties(title=f'% of GDP spent on healthcare per country in {selected_year}')

    chart_base = alt.Chart(source
        ).properties( 
            width=width,
            height=height
        ).project(project
        ).transform_lookup(
            lookup = "id",
            from_= alt.LookupData(data_subset, "country-code", ['Country', 'Year', 'GDP_percent_towards_health']),
        )

    # fix the color schema so that it will not change upon user selection
    rate_scale = alt.Scale(domain=[data_full['GDP_percent_towards_health'].min(), data_full['GDP_percent_towards_health'].max()], scheme = "greenblue")
    rate_color = alt.Color(field='GDP_percent_towards_health', type="quantitative", scale=rate_scale)
    chart_ph_gdp = chart_base.mark_geoshape().encode(
        color = rate_color,
        tooltip=["GDP_percent_towards_health:N", "Country:O"]
        ).properties(
        title=f'% of GDP spent on healthcare per country in {selected_year}'
        )

    chart_ph_gdp_map = alt.vconcat(map_background + chart_ph_gdp
    ).resolve_scale(
        color = 'independent'
    )

    return chart_ph_gdp_map


## Funding merged bar chart
def return_funding_bar(data_subset):
    chart_funding_bar = alt.Chart(data_subset).mark_bar().encode(
        x='Country:O',
        y='USD_per_million:Q',
        color=alt.Color('Cost:N', scale = alt.Scale(scheme = "greenblue")), 
        tooltip=["Country", "Year"], 
        column = 'Year:N'
    ).properties(
    width = width,
    height = height
    )

    return chart_funding_bar




## Drug related Death Map
def return_drug_chart(data_subset, data_full, selected_year):
    if (data_subset.shape[0] == 0):
        return map_background.properties(title=f'Global death rate due to drug abuse in {selected_year}')

    chart_base = alt.Chart(source
    ).properties( 
        width=width,
        height=height
    ).project(project
    ).transform_lookup(
        lookup = "id",
        from_= alt.LookupData(data_subset, "country-code", ['Country', 'Year', 'Drug_Deaths']),
    )

    rate_scale = alt.Scale(domain=[data_full['Drug_Deaths'].min(), data_full['Drug_Deaths'].max()], scheme = "purplered")
    rate_color = alt.Color(field='Drug_Deaths', type="quantitative", scale=rate_scale)
    chart_drug_death = chart_base.mark_geoshape().encode(
        color = rate_color,
        tooltip=["Drug_Deaths:N", "Country:O"]
        ).properties(
        title=f'Global death rate due to drug abuse in {selected_year}'
        )
    
    chart_drug_map = alt.vconcat(map_background + chart_drug_death
    ).resolve_scale(
        color = 'independent'
    )

    return chart_drug_map




def return_drug_bar(data_subset):
    drug_bar =  alt.Chart(data_subset).mark_bar().encode(
                x=alt.X('Country', title = "Country", sort = 'y'),
                y=alt.Y('Drug_Deaths', title = "Death Count"),
                color=alt.Color('sum(Drug_Deaths):Q', legend=None, scale=alt.Scale(scheme='purplered')),
                tooltip=["Country", "sum(Drug_Deaths):Q"]
            ).properties(
                title="Total deaths due to drugs between 1990-2020",
                width=width,
                height=height * 1.5
            ).transform_window(
            rank='rank(Drug_Deaths)',
            sort=[alt.SortField('Drug_Deaths', order='descending')]
            )

    return drug_bar

