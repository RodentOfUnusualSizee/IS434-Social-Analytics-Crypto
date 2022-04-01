import dash
from dash.dependencies import Input, Output
import dash_daq as daq
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash import Dash, dcc, html, Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objects as go

app = dash.Dash(__name__)

app.layout = html.Div([
    daq.ToggleSwitch(
        id='my-toggle-switch',
        value=False
    ),
    html.Div(id='my-toggle-switch-output')
])

@app.callback(
    Output('graph', 'figure'),
    Input('my-toggle-switch', 'value'),
)
def build_graphs(match):
    df = pd.read_csv("curve_price_data.csv")
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    if match==True:
        fig = px.line(df, x="Date", y="Price")
        # fig.add_trace(go.Scatter(x=df['Date'], y=df['Price'], xperiodalignment='end'))
    else:
        # plot dark theme
        fig = px.line(df, x="Date", y="Price", template='plotly_dark')
        # fig.add_trace(go.Scatter(x=df['Date'], y=df['Price'], xperiodalignment='start'))
    return fig

app.layout = html.Div([
    daq.ToggleSwitch(
        id='my-toggle-switch',
        value=False
    ),
    dcc.Graph(id="graph"),
])

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=80)