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

current_fips = 1039 #COVIngton county
fl_visible = True
pl_visible = True
p_visible = True

external_stylesheets = 'website/static/website/cssFiles/main.css'

app = DjangoDash('SimpleExample')


with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

#df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
#                   dtype={"fips": str})
df = pd.read_csv("data/counties/simulations/risk_index0.csv",dtype={"fips": str})

"""
fig3 = go.Figure(data=[go.Table(
    header=dict(values=list(df.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[df.rank, df.fips,df['risk']],
               fill_color='lavender',
               align='left'))
])
"""
# fig.show()
def get_map(ix = "r"):
    risk_str = ""
    if ix == "r":
        risk_str = "Risk index"
    elif ix == "ic":
        risk_str = "Peak ICU/ICU beds"
    elif ix == "mi":
        risk_str = "Fatalities/population"
    elif ix == "tf":
        risk_str = "Fatalities"
    fig = px.choropleth_mapbox(df, geojson=counties, locations='fips', color=risk_str,
                            color_continuous_scale = 'Reds',#['#2821FF','#D917E8','#FF4726','#E89817','#FFCB00'],
                            range_color=(df.quantile(0.05)[risk_str], df.quantile(0.95)[risk_str]),
                            mapbox_style="carto-positron",
                            zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                            opacity=0.5,
                            labels={'risk':'County risk'}
                            )
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',)
    return fig

def get_SIR_from_fips(fips,lockdown=None,panic = None, partial_lockdown = None):
    #with open('website/static/website/fips1.json') as json_file:
    #    data = json.load(json_file)
    #df = pd.DataFrame(data)
    df = simulate.simulate_county(fips=fips,duration=500,lockdown = lockdown,panic=panic,partial_lockdown=partial_lockdown)
    #df = df[["t","ICU"]]

    return df
    

def create_time_series(df):
    df = df[["Susceptible","Exposed","Infected","Recovered","Day"]]
    df = df.melt('Day',var_name='Population at interest',  value_name='Individuals')
    fig2 = px.line(df, x='Day', y='Individuals', color='Population at interest')
    fig2.update_traces(mode='lines')
   # fig2.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
   #                   'paper_bgcolor': 'rgba(0, 0, 0, 0)',})
    return fig2

def create_time_series_2(df):
    df = df[["ICU patients","Total hospital beds","ICU beds","Day","Dead"]]
    df = df.melt('Day',var_name='Population at interest',  value_name='Individuals')
    fig2 = px.line(df, x='Day', y='Individuals', color='Population at interest')
    fig2.update_traces(mode='lines')
   # fig2.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
   #                   'paper_bgcolor': 'rgba(0, 0, 0, 0)',})
    return fig2




app.layout = html.Div([

#    html.Div([html.H1("Demographic Data by Country")], id='teeesting', style=webVar.demoStyle),
    html.Div([
        html.Span("Risk metric : ", className="six columns", id='metToDisp'),
        dcc.Dropdown(
            id="value-selected", 
            value='r', 
            options=[
                    {'label': "Combined risk index", 'value': 'r'},
                    {'label': "Intensive care", 'value': 'ic'},
                    {'label': "Mortality index", 'value': 'mi'},
                    {'label': "Total fatalities", 'value': 'tf'}],
            className="six columns", 
            searchable=False)], 
        className="row" ),
    html.Div([
    html.Div([dcc.Graph(id='county-table')], id='county-div'),
    html.Div([dcc.Graph(id="my-graph")],id='graph-div'),
    ]),
    html.Div([dcc.Graph(id='x-time-series')]),
    html.Div([dcc.Graph(id='x-time-series-2')]),

html.Div(
        [
            html.Div([
            html.Button('Panic dynamics', id='fl-button'),
                ],id='button-div'),
            html.Div([dcc.RangeSlider(
        count=1,
        min=0,
        max=500,
        step=1,
        value=[0, 10],id='slider-1',
        marks={
            0: {'label':   'Day 0'},
            50: {'label':  'Day 50'},
            100: {'label': 'Day 100'},
            150: {'label': 'Day 150'},
            200: {'label': 'Day 200'},
            250: {'label': 'Day 250'},
            300: {'label': 'Day 300'},
            350: {'label': 'Day 350'},
            400: {'label': 'Day 400'},
            450: {'label': 'Day 450'},
            500: {'label': 'Day 500'}
        }
        )],id="flsliderdiv-1")
        ]),
html.Div(
        [
            html.Div([
            html.Button('Panic dynamics', id='pl-button'),
                ],id='button-div'),
            html.Div([dcc.RangeSlider(
        count=1,
        min=0,
        max=500,
        step=1,
        value=[0, 10],id='slider-2',
        marks={
            0: {'label':   'Day 0'},
            50: {'label':  'Day 50'},
            100: {'label': 'Day 100'},
            150: {'label': 'Day 150'},
            200: {'label': 'Day 200'},
            250: {'label': 'Day 250'},
            300: {'label': 'Day 300'},
            350: {'label': 'Day 350'},
            400: {'label': 'Day 400'},
            450: {'label': 'Day 450'},
            500: {'label': 'Day 500'}
        }
        )],id="flsliderdiv-2")
        ]),
html.Div(
        [
            html.Div([
            html.Button('Panic dynamics', id='p-button'),
                ],id='button-div'),
            html.Div([dcc.RangeSlider(
        count=1,
        min=0,
        max=500,
        step=1,
        value=[0, 10],id='slider-3',
        marks={
            0: {'label':   'Day 0'},
            50: {'label':  'Day 50'},
            100: {'label': 'Day 100'},
            150: {'label': 'Day 150'},
            200: {'label': 'Day 200'},
            250: {'label': 'Day 250'},
            300: {'label': 'Day 300'},
            350: {'label': 'Day 350'},
            400: {'label': 'Day 400'},
            450: {'label': 'Day 450'},
            500: {'label': 'Day 500'}
        }
        )],id="flsliderdiv-3")
        ]),
    ],
    className="container",
)
@app.callback(
   Output(component_id='my-graph', component_property='figure'),
   [Input(component_id='value-selected', component_property='value')])

def change_risk(ix):
    return get_map(ix)
    

#region Slider callbacks
@app.callback(
   Output(component_id='flsliderdiv-1', component_property='style'),
   [Input(component_id='fl-button', component_property='n_clicks')])

def toggle_fl(value):
    global fl_visible
    
    if fl_visible:
        fl_visible = not fl_visible
        return {'display': 'none'}
    else:
        fl_visible = not fl_visible
        return{'display': 'block'}

@app.callback(
   Output(component_id='flsliderdiv-2', component_property='style'),
   [Input(component_id='pl-button', component_property='n_clicks')])

def toggle_pl(value):
    global pl_visible
    
    if pl_visible:
        pl_visible = not pl_visible
        return {'display': 'none'}
    else:
        pl_visible = not pl_visible
        return{'display': 'block'}

@app.callback(
   Output(component_id='flsliderdiv-3', component_property='style'),
   [Input(component_id='p-button', component_property='n_clicks')])

def toggle_p(value):
    global p_visible
    
    if p_visible:
        p_visible = not p_visible
        return {'display': 'none'}
    else:
        p_visible = not p_visible
        return{'display': 'block'}
#endregion


@app.callback(
    [
        Output('x-time-series', 'figure'),
        Output('county-table', 'figure'),
        Output('x-time-series-2','figure'),
    ],
    [
        Input('my-graph','clickData'),
        Input('slider-1','value'),
        Input('slider-2','value'),
        Input('slider-3','value'),
        Input(component_id='fl-button', component_property='n_clicks'),
        Input(component_id='pl-button', component_property='n_clicks'),
        Input(component_id='p-button', component_property='n_clicks')

    ])
def display_graph(clickData,slider_value_1,slider_value_2,slider_value_3,b1,b2,b3):
    if fl_visible == False:
        slider_value_1 = None
    if pl_visible == False:
        slider_value_2 = None
    if p_visible == False:
        slider_value_3 = None
    global current_fips
    if clickData == None:
        fips = current_fips
    else:
        clickData = dict(clickData)
        fips = int(clickData['points'][0]['location'])
    current_fips = fips
    data = get_SIR_from_fips(fips,lockdown=slider_value_1,partial_lockdown=slider_value_2,panic=slider_value_3)
    #data = get_SIR_from_fips(fips)
    county_table = table_fig(fips)
    return create_time_series(data), county_table, create_time_series_2(data)
