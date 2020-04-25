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

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('SimpleExample', external_stylesheets=external_stylesheets)


with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
                   dtype={"fips": str})


styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

df3 = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_usa_states.csv')

fig3 = go.Figure(data=[go.Table(
    header=dict(values=list(df.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[df.Rank, df.State, df.Postal, df.Population],
               fill_color='lavender',
               align='left'))
])

fig.show()

fig = px.choropleth_mapbox(df, geojson=counties, locations='fips', color='unemp',
                           color_continuous_scale="Viridis",
                           range_color=(0, 12),
                           mapbox_style="carto-positron",
                           zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                           opacity=0.5,
                           labels={'unemp':'unemployment rate'}
                          )
fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                      'paper_bgcolor': 'rgba(0, 0, 0, 0)',})

def get_SIR_from_fips(fips):
    print("This is the fips passed", fips)

    df = simulate.simulate_county(fips=fips,duration=500)
    df = df.melt('t',var_name='cols',  value_name='vals')

    return df

def create_time_series(df):
    fig2 = px.line(df, x='t', y='vals', color='cols')
    fig2.update_traces(mode='markers+lines')
    fig2.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                      'paper_bgcolor': 'rgba(0, 0, 0, 0)',})
    return fig2



fig.update_layout({
    'plot_bgcolor':'rgb(0,0,0,0)',
    'paper_bgcolor':'rgb(0,0,0,0)',
})


app.layout = html.Div([

    html.Div([html.H1("Demographic Data by Country")], id='teeesting', style={'textAlign': "center", "padding-bottom": "30"}),
    html.Div([
        html.Span("Metric to display : ", className="six columns", style={"text-align": "right", "width": "40%", "padding-top": 10}),
        dcc.Dropdown(id="value-selected", value='lifeExp', options=[
                                                       {'label': "Population ", 'value': 'pop'},
                                                       {'label': "GDP Per Capita ", 'value': 'gdpPercap'},
                                                       {'label': "Life Expectancy ", 'value': 'lifeExp'}],
                                              style={"display": "block", "margin-left": "auto", "margin-right": "auto",
                                                     "width": "70%"},
                                              className="six columns")], className="row"
    ),
    dcc.Graph(figure=fig,id="my-graph"),
    html.Div([dcc.Graph(id='x-time-series'),]),
    ], 
    className="container",
)

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')

app = dash.Dash(__name__)

@app.callback(
    Output('x-time-series', 'figure'),
    [
        Input('my-graph','clickData')
    ])
def display_graph(clickData):
    if clickData == None:
        fips = 1043
    else:
        clickData = dict(clickData)
        fips = int(clickData['points'][0]['location'])
    
    data = get_SIR_from_fips(fips)
    return create_time_series(data)


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
