import os
import dash_core_components as dcc
import dash_html_components as html
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

def get_SIR_from_fips(fips):
    print("This is the fips passed", fips)
    df = simulate.simulate_county(fips=fips,duration=100,beta=1/7)
    
    #with open('website/static/website/fips1.json') as json_file:
    #    data = json.load(json_file)
    #df = pd.DataFrame(data)
    df = df.melt('t',var_name='cols',  value_name='vals')
    return df

def create_time_series(df):
    fig2 = px.line(df, x='t', y='vals', color='cols')
    fig2.update_traces(mode='markers+lines')
    
    return fig2

fig = px.choropleth(df, geojson=counties, locations='fips', color='unemp',
                        color_continuous_scale="Viridis",
                        range_color=(0, 12),
                        scope="usa",
                        labels={'unemp':'unemployment rate'}
)




app.layout = html.Div([
    html.Div([html.H1("Demographic Data by Country")], style={'textAlign': "center", "padding-bottom": "30"}),
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
    html.Div([
        dcc.Markdown("""
                **Click Data**

                Click on points in the graph.
            """),
        html.Pre(id='click-data', style=styles['pre']),
        ], className='three columns'),
    html.Div([
        dcc.Graph(id='x-time-series'),
    ]),
    ], 
    className="container", 
)




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
        fips = clickData['points'][0]['location']
    
    data = get_SIR_from_fips(fips)
    return create_time_series(data)



@app.callback(
    Output('click-data', 'children'),
    [
        Input('my-graph', 'clickData'),
    ])
def display_data(clickData):
    Input('my-graph', 'clickData'),
    return json.dumps(clickData, indent=2)  
