from distutils.command.build import build
from dash import Dash, html, dcc, Output, Input, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
# for sentiment analysis
import numpy as np
import re
from datetime import datetime
from plotly.subplots import make_subplots
import dash_daq as daq
from dash import html
import json



app = Dash(__name__, external_stylesheets=[dbc.themes.LUMEN])
# app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])


@callback(
    Output(component_id='price-chart', component_property='figure'),
    Output(component_id='chosen-defi-coin', component_property='children'),
    Input(component_id='defi-coin', component_property='value'),  # here
    Input(component_id='my-toggle-switch', component_property='value'),
)
# chosen_volume
def build_graphs(chosen_defi_coin, match):  # here
    string = chosen_defi_coin.lower() + "_price_data.csv"
    price_df = pd.read_csv(string)
    # fig = px.line(df, x="Date", y="Price", template="plotly_dark")

    # here
    # timeSplitDataNetScore = sentiment_analysis(chosen_defi_coin.lower())
    # timeSplitDataNetScore = pd.read_json('sentimentalOutput/discord.json')
    new_dict = {}
    string = 'sentimentalOutput/discord-' + chosen_defi_coin.lower() + '.json'
    with open(string) as json_file:
        timeSplitDataNetScore = json.load(json_file)
        for old_key in timeSplitDataNetScore:
            arr = old_key.split('/')
            new_key = arr[1] + "-" + arr[0]
            new_dict[new_key] = timeSplitDataNetScore[old_key]

    sentiment_df = pd.DataFrame(
        {'date': new_dict.keys(), 'sentiment': new_dict.values()})

    def mdy_to_ymd(d):
        return datetime.strptime(d, '%b %d, %Y').strftime('%Y-%m-%d')

    price_df['format_date'] = price_df['Date'].apply(lambda x:  mdy_to_ymd(x))

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(
        x=price_df['format_date'], y=price_df['Price'], name='Price'), secondary_y=False)
    fig.update_xaxes(autorange="reversed")
    # fig.update_xaxes(dtick="M1")

    if match == False:
        chosen_defi_coin = "End"
        fig.add_trace(go.Scatter(x=sentiment_df['date'], y=sentiment_df['sentiment'],
                      name='Sentiment', xperiodalignment='end'), secondary_y=True)

    if match == True:
        chosen_defi_coin = "Start"
        fig.add_trace(go.Scatter(x=sentiment_df['date'], y=sentiment_df['sentiment'],
                      name='Sentiment', xperiodalignment='start'), secondary_y=True)

    fig.update_layout(
        xaxis_rangeslider_visible=True,
        title_text="Curve Data Price against Sentiment",
        title_x=0.5
    )
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Price", secondary_y=False)
    fig.update_yaxes(title_text="Sentiment", secondary_y=True)
    # here

    # fig.update_traces(line_color='#FF0000')
    chosen_defi_coin = chosen_defi_coin + " price data"
    fig.update_yaxes(autorange="reversed")
    return fig, chosen_defi_coin


app.layout = dbc.Container([
    html.H1(id='chosen-defi-coin', style={'textAlign': 'center'}),
    dbc.Link("back", href=f"url"),
    html.Button(dcc.Link("back", href=f"url"), className='three columns'),
    dbc.Row([
        dbc.Col(dcc.Dropdown(
            id='defi-coin',  # here
            options=[
                {'label': 'AAVE', 'value': 'AAVE'},
                {'label': 'UNISWAP', 'value': 'UNISWAP'},
                {'label': 'CURVE', 'value': 'CURVE'},
                {'label': 'MAKER', 'value': 'MAKER'},
                {'label': 'SUSHI', 'value': 'SUSHI'},
                {'label': 'COMPOUND', 'value': 'COMPOUND'},
            ],
            value='AAVE'), width=dict(size=8, offset=2)),

        dbc.Col(
            daq.ToggleSwitch(
                id='my-toggle-switch',
                value=False
            ),
        )

    ]),

    dbc.Row([
        dbc.Col(dcc.Graph(id='price-chart'))
    ]),
], fluid=True)


if __name__ == '__main__':
    # app.run_server(debug=True)
    app.run_server(debug=True, host='0.0.0.0', port=80)
