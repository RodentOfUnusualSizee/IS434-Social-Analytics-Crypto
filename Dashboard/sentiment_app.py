from xml.etree.ElementTree import TreeBuilder
from dash import Dash, dcc, Output, Input, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
# for sentiment analysis
from datetime import datetime
from plotly.subplots import make_subplots
import dash_daq as daq
from dash import html
import json
from dash_bootstrap_templates import ThemeSwitchAIO

def calculateAccuracy(priceData,jsonFile):
    monthlyPrice = pd.read_csv(priceData)
    monthlyPrice = monthlyPrice[['Date','Price']]
    monthlyPrice['Date'] = pd.to_datetime(monthlyPrice['Date'])
    monthlyPrice['changePrice'] = monthlyPrice['Price'].pct_change(fill_method ='ffill')
    with open(jsonFile) as json_file:
        data = json.load(json_file)
    date = []
    senti = []
    for key in data:
        date.append(key)
        senti.append(data[key])
    s1={'Date':date,'sentiment':senti}
    s1 = pd.DataFrame(s1)
    
    s1["Date"] = pd.to_datetime(s1['Date'])
    s1['changeSen'] = s1['sentiment'].pct_change(fill_method ='ffill')
    s1['changeSen'] = s1['changeSen'][::-1].shift(periods=1)
    # print(s1)
    new = s1.merge(monthlyPrice, on='Date')
    compare = new[['changeSen','changePrice']]
    compare = compare.dropna()
    compare['changeSen'] = [True if x > 0 else False for x in compare['changeSen']]
    compare['changePrice'] = [True if x > 0 else False for x in compare['changePrice']]
    compare['res'] = compare['changePrice'] == compare['changeSen']
    accuracy = compare['res'].mean()
    return accuracy

app = Dash(__name__, external_stylesheets=[dbc.themes.LUMEN])
# app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

@callback(
    Output(component_id='price-chart', component_property='figure'),
    # Output(component_id='chosen-defi-coin', component_property='children'), 
    # Output(component_id='accuracy', component_property='children'),
    Input(component_id='defi-coin', component_property='value'), ###here
    Input(component_id='my-toggle-switch', component_property='value'),
    # Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)

#chosen_volume
def build_graphs(chosen_defi_coin, match): ###here
    price_string = "priceData/" + chosen_defi_coin.lower() + "_price_data.csv"
    price_df = pd.read_csv(price_string)
    # fig = px.line(df, x="Date", y="Price", template="plotly_dark")

    # here 
    # timeSplitDataNetScore = sentiment_analysis(chosen_defi_coin.lower())
    # timeSplitDataNetScore = pd.read_json('sentimentalOutput/discord.json')
    new_dict= {}
    new_dict2 = {}
    sentiment_string = 'sentimentalOutput/discord-' + chosen_defi_coin.lower() + '.json'

    accuracy = calculateAccuracy(price_string, sentiment_string) #accuracy
    accuracy = "    Accuracy: " + str(round(accuracy*100, 2)) + '%'

    with open(sentiment_string) as json_file:
        timeSplitDataNetScore = json.load(json_file)
        for old_key in timeSplitDataNetScore:
            arr = old_key.split('/')
            new_key = arr[1] + "-" + arr[0]
            new_dict[new_key] = timeSplitDataNetScore[old_key]

            add_month = str(int(arr[0]) + 1)
            if len(add_month) == 1:
                add_month = "0" + add_month
            new_key2 = arr[1] + "-" + add_month
            new_dict2[new_key2] = timeSplitDataNetScore[old_key]

    sentiment_df = pd.DataFrame({'date': new_dict.keys(), 'sentiment': new_dict.values()})
    sentiment_df2 = pd.DataFrame({'date': new_dict2.keys(), 'sentiment': new_dict2.values()})

    def mdy_to_ymd(d):
        return datetime.strptime(d, '%b %d, %Y').strftime('%Y-%m-%d')

    price_df['format_date'] = price_df['Date'].apply(lambda x:  mdy_to_ymd(x))

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=price_df['format_date'], y=price_df['Price'], name='Price'), secondary_y= False)
    # fig.update_xaxes(dtick="M1")

    if match == False:
        fig.add_trace(go.Scatter(x=sentiment_df['date'], y=sentiment_df['sentiment'], name='Sentiment', xperiodalignment='end'), secondary_y= True)

    if match == True:
        fig.add_trace(go.Scatter(x=sentiment_df2['date'], y=sentiment_df2['sentiment'], name='Sentiment', xperiodalignment='start'), secondary_y= True)

    format_title = "Price and Sentiment of " + chosen_defi_coin + accuracy

    fig.update_layout(
        title=format_title,
        xaxis_rangeslider_visible=True,
        title_x=0.5,
        title_font_size=20, # 1.25rem
    )
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Price", secondary_y=False)
    fig.update_yaxes(title_text="Sentiment", secondary_y=True)
    ## here

    # theme
    # if theme == False:
    #     fig.update_layout(template='plotly_dark')
    # if theme == True:
    #     fig.update_layout(template='plotly')
    return fig

# app.layout = 
sentiment_layout = dbc.Container([
    dbc.Row([
<<<<<<< HEAD
    #     dbc.Col(
    #         [
    #             ThemeSwitchAIO(aio_id="theme", themes=[dbc.themes.LUMEN, dbc.themes.LUMEN]),
    #         ]
    #     ),
        dbc.Col(
            dcc.Dropdown
            (
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
                style = {'font-size': '1.25rem', 'font-weight': '500', 'text-align': 'center'}
            )
            , width=dict(size=8, offset=2)
        ),
=======
        dbc.Col(dcc.Dropdown(
            id='defi-coin', ###here
            options=[
                {'label': 'AAVE', 'value': 'AAVE'},
                {'label': 'UNISWAP', 'value': 'UNISWAP'},
                {'label': 'CURVE FINANCE', 'value': 'CURVE FINANCE'},
                {'label': 'MAKER', 'value': 'MAKER'},
                {'label': 'SUSHISWAP', 'value': 'SUSHISWAP'},
                {'label': 'COMPOUND', 'value': 'COMPOUND'},
            ],
            value = 'AAVE'), width=dict(size=8, offset=2)),
>>>>>>> e2e191c45938877223e427cffe95680ada9b770d

        dbc.Col(
            daq.ToggleSwitch(
                id='my-toggle-switch',
                value=False,
                label= {'label': 'Offset Sentiment', 'style': {'font-size': '1.125rem', 'font-weight': '500'}},
                # label position
                labelPosition='bottom',
            ),
        )
            
]),

    dbc.Row([
        dbc.Col(dcc.Graph(id='price-chart')) 
    ]), 
], fluid=True)