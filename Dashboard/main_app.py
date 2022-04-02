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
                    dbc.NavLink("Sentimental Analysis", href="#", className="nav-link active  text-success bg-light font-weight-bold", style={'font-size': '1.25rem'}), 
                    dbc.NavLink("Discord Network Analysis", href="http://127.0.0.1:5500/Dashboard/gephi/index.html", className="text-danger", style={'font-size': '1.25rem'}), #change
                    dbc.NavLink("Twitter Network Analysis", href="http://127.0.0.1:5500/Dashboard/twitter%20network%20gephi/index.html", className="text-danger", style={'font-size': '1.25rem'}), #change
                    dbc.NavLink("Data Manager", href="http://127.0.0.1:5500/Dashboard/dataETL.html", className="text-danger", style={'font-size': '1.25rem'}), #change
                ]
            )
        ),
        # dbc.Row([
        #     dbc.Col(
        #         html.Center('Sentiment'), width=dict(size=6)
        #     ),
        #     dbc.Col(
        #         html.Center('Price'), width=dict(size=6)
        #     )
        # ]),
        html.Div(id='content', children=[sentiment_layout]),
        

    ]
,fluid=True)

if __name__=='__main__':
    app.run_server(debug=True)
