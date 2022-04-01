from dash import Dash
import dash_bootstrap_components as dbc
from dash import html

from sentiment_app import sentiment_layout

app = Dash(__name__, external_stylesheets=[dbc.themes.LUMEN], suppress_callback_exceptions = True)

app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Nav(
                [
                    dbc.NavLink("Network", href="http://127.0.0.1:5500/Dashboard/gephi/index.html", className="text-danger", style={'font-size': '1.25rem'}), #change
                    dbc.NavLink("Sentiment", href="#", className="text-success bg-light", style={'font-size': '1.25rem'}), 
                ]
            )
        ),
        html.Div(id='content', children=[sentiment_layout]),
        

    ]
,fluid=True)

if __name__=='__main__':
    app.run_server(debug=True)
