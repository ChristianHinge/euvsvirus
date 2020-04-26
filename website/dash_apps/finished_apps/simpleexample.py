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
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                        'paper_bgcolor': 'rgba(0, 0, 0, 0)',})
    return fig

def get_SIR_from_fips(fips,lockdown=None,panic = None, partial_lockdown = None):
    #with open('website/static/website/fips1.json') as json_file:
    #    data = json.load(json_file)
    #df = pd.DataFrame(data)
    df = simulate.simulate_county(fips=fips,duration=500,lockdown = lockdown,panic=panic,partial_lockdown=partial_lockdown)
    #df = df[["t","ICU"]]

    return df
    

def create_time_series(df):
    df = df[["Susceptible","Exposed","Infected","Recovered","Days"]]
    df = df.melt('Days',var_name='Population at interest',  value_name='Individuals')
    fig2 = px.line(df, x='Days', y='Individuals', color='Population at interest')
    fig2.update_traces(mode='markers+lines')
   # fig2.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
   #                   'paper_bgcolor': 'rgba(0, 0, 0, 0)',})
    return fig2

def create_time_series_2(df):
    df = df[["ICU","Hospital beds","ICU beds","Days","Dead"]]
    df = df.melt('Days',var_name='Population at interest',  value_name='Individuals')
    fig2 = px.line(df, x='Days', y='Individuals', color='Population at interest')
    fig2.update_traces(mode='markers+lines')
   # fig2.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
   #                   'paper_bgcolor': 'rgba(0, 0, 0, 0)',})
    return fig2




app.layout = html.Div([

#    html.Div([html.H1("Demographic Data by Country")], id='teeesting', style=webVar.demoStyle),
    html.Div([
        html.Span("Risk metric : ", className="six columns", id='metToDisp'),
        dcc.Dropdown(id="value-selected", value='ic', options=[
                                                       {'label': "Combined risk index", 'value': 'r'},
                                                       {'label': "Intensive care", 'value': 'ic'},
                                                       {'label': "Mortality index", 'value': 'mi'},
                                                       {'label': "Total fatalities", 'value': 'tf'}],
                                              className="six columns")], className="row"
    ),
    dcc.Graph(id="my-graph"),
    html.Div([
        dcc.Graph(id='county-table'),
        html.Div([html.H2(["Some title"],id='titleBetweenPlots'),html.P([""" Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla lacinia pretium dui, at dictum massa elementum at. Nam nec laoreet mi. Aliquam molestie eget mi at dictum. Aliquam mattis mauris metus, at pellentesque elit eleifend id. Integer feugiat purus et sollicitudin fringilla. Vivamus a nunc et diam ullamcorper luctus nec quis diam. Nunc vitae lorem vitae purus tincidunt cursus. Nullam ac viverra leo.

Vestibulum quis volutpat nisi. Duis nec fermentum leo, condimentum cursus felis. Cras nisi elit, suscipit sed risus eu, tristique finibus nunc. Integer ut placerat arcu, eget feugiat mauris. Nam justo nisi, iaculis rhoncus nibh vitae, blandit dictum sapien. Integer commodo odio diam, et lacinia ante condimentum sed. Phasellus lacinia, tortor sit amet feugiat gravida, justo mauris imperdiet ante, sed maximus mauris ligula malesuada ligula.

Vestibulum varius, ante sollicitudin ullamcorper facilisis, quam nisl fermentum nisi, non fringilla eros justo sed nunc. Pellentesque urna massa, finibus sed auctor quis, molestie venenatis nisi. Nam porta ante nec ligula condimentum fringilla. Nulla vulputate odio vel orci fermentum, eu rhoncus felis tristique. Maecenas ac dictum dui, nec rutrum metus. Quisque sed tellus mauris. Curabitur ut dignissim diam. Sed diam massa, aliquam eu consequat id, semper et libero. Pellentesque auctor nec libero at sollicitudin. Etiam pellentesque molestie risus, nec eleifend arcu maximus nec.

In eu mauris a leo aliquam scelerisque. Ut facilisis viverra odio, interdum pulvinar nisl interdum ac. Sed facilisis tellus at purus auctor, ut luctus odio mattis. Sed aliquam massa a augue egestas, porta efficitur ante malesuada. Vestibulum quis finibus dui, vitae convallis arcu. Phasellus tempus euismod diam at auctor. Nullam dapibus, mi et placerat fringilla, nulla lacus imperdiet dui, luctus dignissim dui sem vitae turpis. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; In interdum ipsum dolor, ut sollicitudin risus lacinia in. In aliquet accumsan vehicula. Curabitur laoreet augue ante. """
        ])], id='textBetweenPlots')]),
    html.Div([dcc.Graph(id='x-time-series'),]),
    html.Div([dcc.Graph(id='x-time-series-2'),]),
    html.Div(
        [
            html.Div([
            html.Button('Full lockdown', id='fl-button'),
                ],style={'width': '10%', 'display': 'inline-block','vertical-align': 'middle'}),
            html.Div([dcc.RangeSlider(
        count=1,
        min=0,
        max=500,
        step=1,
        value=[0, 10],id='slider-1',
        marks={
            0: {'label': ''},
            50: {'label': ''},
            100: {'label': ''},
            150: {'label': ''},
            200: {'label': ''},
            250: {'label': ''},
            300: {'label': ''},
            350: {'label': ''},
            400: {'label': ''},
            450: {'label': ''},
            500: {'label': ''}
        }
        )],id="flsliderdiv-1",style={'width': '89%', 'display': 'none','vertical-align': 'middle'})
        ]),
    html.Div(
        [
            html.Div([
            html.Button('Partial lockdown', id='pl-button'),
                ],style={'width': '10%', 'display': 'inline-block','vertical-align': 'middle'}),
            html.Div([dcc.RangeSlider(
        count=1,
        min=0,
        max=500,
        step=1,
        value=[0, 10],id='slider-2',
        marks={
            0: {'label': ''},
            50: {'label': ''},
            100: {'label': ''},
            150: {'label': ''},
            200: {'label': ''},
            250: {'label': ''},
            300: {'label': ''},
            350: {'label': ''},
            400: {'label': ''},
            450: {'label': ''},
            500: {'label': ''}
        }
        )],id="flsliderdiv-2",style={'width': '89%', 'display': 'none','vertical-align': 'middle'})
        ]),
html.Div(
        [
            html.Div([
            html.Button('Panic dynamics', id='p-button'),
                ],style={'width': '10%', 'display': 'inline-block','vertical-align': 'middle'}),
            html.Div([dcc.RangeSlider(
        count=1,
        min=0,
        max=500,
        step=1,
        value=[0, 10],id='slider-3',
        marks={
            0: {'label': ''},
            50: {'label': ''},
            100: {'label': ''},
            150: {'label': ''},
            200: {'label': ''},
            250: {'label': ''},
            300: {'label': ''},
            350: {'label': ''},
            400: {'label': ''},
            450: {'label': ''},
            500: {'label': ''}
        }
        )],id="flsliderdiv-3",style={'width': '89%', 'display': 'none','vertical-align': 'middle'})
        ]),
    ],
    className="container",
)
@app.callback(
   Output(component_id='my-graph', component_property='figure'),
   [Input(component_id='value-selected', component_property='value')])

def change_risk(ix):
    print(ix)
    return get_map()
    

#region Slider callbacks
@app.callback(
   Output(component_id='flsliderdiv-1', component_property='style'),
   [Input(component_id='fl-button', component_property='n_clicks')])

def toggle_fl(value):
    global fl_visible
    
    if fl_visible:
        fl_visible = not fl_visible
        return {'width': '89%', 'display': 'none','vertical-align': 'bottom'}
    else:
        fl_visible = not fl_visible
        return{'width': '89%', 'display': 'inline-block','vertical-align': 'bottom'}

@app.callback(
   Output(component_id='flsliderdiv-2', component_property='style'),
   [Input(component_id='pl-button', component_property='n_clicks')])

def toggle_pl(value):
    global pl_visible
    
    if pl_visible:
        pl_visible = not pl_visible
        return {'width': '89%', 'display': 'none','vertical-align': 'bottom'}
    else:
        pl_visible = not pl_visible
        return{'width': '89%', 'display': 'inline-block','vertical-align': 'bottom'}

@app.callback(
   Output(component_id='flsliderdiv-3', component_property='style'),
   [Input(component_id='p-button', component_property='n_clicks')])

def toggle_p(value):
    global p_visible
    
    if p_visible:
        p_visible = not p_visible
        return {'width': '89%', 'display': 'none','vertical-align': 'bottom'}
    else:
        p_visible = not p_visible
        return{'width': '89%', 'display': 'inline-block','vertical-align': 'bottom'}
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
