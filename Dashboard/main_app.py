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

from sentiment_app import sentiment_layout

app = Dash(__name__, external_stylesheets=[dbc.themes.LUMEN])

app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Tabs
                (
                    [dbc.Tab(label="Sentiment", tab_id="tab-sentiment", labelClassName="text-success font-weight-bold", activeLabelClassName="text-danger"),
                    dbc.Tab(label="Network", tab_id="tab-network", labelClassName="text-success font-weight-bold", activeLabelClassName="text-danger")],
                    id="tabs",
                    active_tab="tab-sentiment",
                ), className='mb-3'
        ),
        html.Div(id='content', children=[])
    ]
,fluid=True)

@app.callback(
    Output("content", "children"),
    Input("tabs", "active_tab"),
    suppress_callback_exceptions=True
)

def switch_tab(chosen_tab):
    if chosen_tab == "tab-sentiment":
        return sentiment_layout
    if chosen_tab == "tab-network":
        # return network_layout
        return html.P("Network Analysis has not been implemented yet.")


if __name__=='__main__':
    # app.run_server(debug=True)
    app.run_server(debug=True, host='0.0.0.0', port=80)