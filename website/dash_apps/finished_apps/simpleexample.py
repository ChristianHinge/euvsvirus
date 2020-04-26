import os
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
from django_plotly_dash import DjangoDash
import json
from urllib.request import urlopen
import plotly.express as px
from src.model import simulate
import website.dash_apps.finished_apps.htmlCssVariables as webVar
from website.dash_apps.finished_apps.county_table import table_fig

current_fips = 1043
external_stylesheets = 'website/static/website/cssFiles/main.css'

app = DjangoDash('SimpleExample')


with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
                   dtype={"fips": str})


df3 = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_usa_states.csv')

fig3 = go.Figure(data=[go.Table(
    header=dict(values=list(df.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[df.rank, df.fips,df.unemp],
               fill_color='lavender',
               align='left'))
])

# fig.show()

fig = px.choropleth_mapbox(df, geojson=counties, locations='fips', color='unemp',
                           color_continuous_scale = ['#2821FF','#D917E8','#FF4726','#E89817','#FFCB00'],
                           range_color=(0, 12),
                           mapbox_style="carto-positron",
                           zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                           opacity=0.5,
                           labels={'unemp':'unemployment rate'}
                          )
fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                      'paper_bgcolor': 'rgba(0, 0, 0, 0)',})

def get_SIR_from_fips(fips,lockdown=None,panic = None, partial_lockdown = None):
    #with open('website/static/website/fips1.json') as json_file:
    #    data = json.load(json_file)
    #df = pd.DataFrame(data)
    df = simulate.simulate_county(fips=fips,duration=500,lockdown = lockdown,panic=panic,partial_lockdown=partial_lockdown)
    #df = df[["t","ICU"]]
    df = df.melt('t',var_name='cols',  value_name='vals')

    return df

def create_time_series(df):
    fig2 = px.line(df, x='t', y='vals', color='cols')
    fig2.update_traces(mode='markers+lines')
   # fig2.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
   #                   'paper_bgcolor': 'rgba(0, 0, 0, 0)',})
    return fig2




app.layout = html.Div([

    html.Div([html.H1("Demographic Data by Country")], id='teeesting', style=webVar.demoStyle),
    html.Div([
        html.Span("Metric to display : ", className="six columns", style=webVar.metricStyle),
        dcc.Dropdown(id="value-selected", value='lifeExp', options=[
                                                       {'label': "Population ", 'value': 'pop'},
                                                       {'label': "GDP Per Capita ", 'value': 'gdpPercap'},
                                                       {'label': "Life Expectancy ", 'value': 'lifeExp'}],
                                              style=webVar.dropStyle,
                                              className="six columns")], className="row"
    ),
    dcc.Graph(figure=fig,id="my-graph", style=webVar.graphStyle),
    html.Div([dcc.Graph(id='x-time-series'),]),
    html.Div([dcc.RangeSlider(
        count=1,
        min=0,
        max=500,
        step=1,
        value=[0, 10],id='slider-1')]),
    html.Div([dcc.RangeSlider(
        count=1,
        min=0,
        max=500,
        step=1,
        value=[0, 10],id='slider-2')]),
    html.Div([dcc.RangeSlider(
        count=1,
        min=0,
        max=500,
        step=1,
        value=[0, 10],id='slider-3')]),
    html.Div([dcc.Graph(id='county-table')]),
    html.Div([dcc.Checklist(
        options=[
            {'label': 'Full lockdown' ,'value':'FP'},
            {'label': 'Partial lockdown', 'value': 'PP'},
            {'label': 'Panic', 'value': 'P'}
        ],
        value=['P'],id='checks')])
    ],
    className="container",
)

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')

# app = DjangoDash.dash(__name__)



@app.callback(
    [
        Output('x-time-series', 'figure'),
        Output('county-table', 'figure'),
    ],
    [
        Input('my-graph','clickData'),
        Input('checks','value'),
        Input('slider-1','value'),
        Input('slider-2','value'),
        Input('slider-3','value')

    ])
def display_graph(clickData,checks,slider_value_1,slider_value_2,slider_value_3):
    global current_fips
    if clickData == None:
        fips = current_fips
    else:
        clickData = dict(clickData)
        fips = int(clickData['points'][0]['location'])
    current_fips = fips
    data = get_SIR_from_fips(fips,lockdown=slider_value_1,partial_lockdown=slider_value_2,panic=slider_value_3)
    county_table = table_fig(fips)
    return create_time_series(data), county_table


"""
@app.callback(
    Output('click-data', 'children'),
    [
        Input('my-graph', 'clickData'),
    ])
def display_data(clickData):
    Input('my-graph', 'clickData'),
    return json.dumps(clickData, indent=2)  
"""
