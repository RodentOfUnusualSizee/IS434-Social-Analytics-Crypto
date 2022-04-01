from distutils.command.build import build
from dash import Dash, html, dcc, Output, Input, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
# for sentiment analysis
import numpy as np
import re
from nltk.corpus import stopwords
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from datetime import datetime
from plotly.subplots import make_subplots
import dash_daq as daq
from dash import html
import json

network_layout = html.Div([
    # dcc.Location(id='gephi/index.html')
    dcc.Location(id='index.html', refresh=False)
    dcc.Link(href='index.html')
    html.Div(id='page-content')
])

@callback(Output('page-content', 'children'))
def display_page(pathname):
    return html.Div([
        html.H3('Network Analysis'),
    ])