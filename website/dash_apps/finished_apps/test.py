# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 13:45:26 2020

@author: chris
"""
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

df = pd.read_csv("data/counties/simulations/risk_index0.csv",dtype={"fips": str})

ix = "r"
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

