from distutils.command.build import build
from dash import Dash, html, dcc, Output, Input, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px

app = Dash(__name__, external_stylesheets=[dbc.themes.LUMEN])
# app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

aave_df = pd.read_csv("aave_price_data.csv")
uniswap_df = pd.read_csv("uniswap_price_data.csv")


@callback(
    Output(component_id='price-chart', component_property='figure'),
    Output(component_id='chosen-defi-coin', component_property='children'), 
    Input(component_id='defi-coin', component_property='value') ###here
)

#chosen_volume
def build_graphs(chosen_defi_coin): ###here
    string = chosen_defi_coin.lower() + "_price_data.csv"
    df = pd.read_csv(string)
    fig = px.line(df, x="Date", y="Price")
    # fig = px.line(df, x="Date", y="Price", template="plotly_dark")

    fig.update_layout(
        xaxis_rangeslider_visible=True,
    )

    fig.update_xaxes(autorange="reversed")

    # fig.update_traces(line_color='#FF0000')
    chosen_defi_coin = chosen_defi_coin + " price data"

    return fig, chosen_defi_coin

app.layout = dbc.Container([
    html.H1(id='chosen-defi-coin', style={'textAlign': 'center'}),

    dbc.Row([
        dbc.Col(dcc.Dropdown(
            id='defi-coin', ###here
            options=[
                {'label': 'AAVE', 'value': 'AAVE'},
                {'label': 'UNISWAP', 'value': 'UNISWAP'},
                {'label': 'CURVE', 'value': 'CURVE'},
                {'label': 'MAKER', 'value': 'MAKER'},
                {'label': 'SUSHI', 'value': 'SUSHI'},
                {'label': 'COMPOUND', 'value': 'COMPOUND'},
            ],
            value = 'AAVE',
    ), width=dict(size=8, offset=2))]),

    dbc.Row([
        dbc.Col(dcc.Graph(id='price-chart')) 
    ]), 
], fluid=True)


if __name__=='__main__':
    app.run_server(debug=True)