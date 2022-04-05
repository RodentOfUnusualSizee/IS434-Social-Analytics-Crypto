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
import plotly.express as px
import numpy as np
import ast
from os import walk

def calculateAccuracy(priceData,jsonFile):
    monthlyPrice = pd.read_csv(priceData)
    if monthlyPrice['Price'].dtypes == 'object':
        newPrice = []
        for row in monthlyPrice.iterrows():
            price = row[1][2]
            if ',' in price:
                price = price.split(',')
                price = ''.join(price)
                price = float(price)
                newPrice.append(price)
            else:
                price = float(price)
                newPrice.append(price)
        monthlyPrice['Price'] = newPrice
    monthlyPrice = monthlyPrice[['Date','Price']]
    monthlyPrice['Date'] = pd.to_datetime(monthlyPrice['Date']).dt.to_period('M')
    monthlyPrice = monthlyPrice.groupby(pd.Grouper(key='Date', axis=0)).max().reset_index()

    with open(jsonFile) as json_file:
        data = json.load(json_file)
    date = []
    senti = []
    for key in data:
        date.append(key)
        senti.append(data[key])
    s1={'Date':date,'sentiment':senti}
    s1 = pd.DataFrame(s1)
    s1["Date"] = pd.to_datetime(s1['Date']).dt.to_period('M')
    new = s1.merge(monthlyPrice, on='Date')
    new['changePrice'] = new['Price'].pct_change(fill_method ='ffill')
    new['changeSen'] = new['sentiment'].pct_change(fill_method ='ffill')
    new['changeSen'] = new['changeSen'].shift(periods=1)
    compare = new[['changeSen','changePrice']]
    compare = compare.dropna()
    compare['changeSen'] = [True if x > 0 else False for x in compare['changeSen']]
    compare['changePrice'] = [True if x > 0 else False for x in compare['changePrice']]
    compare['res'] = compare['changePrice'] == compare['changeSen']
    accuracy = compare['res'].mean()
    return accuracy

def mdy_to_ymd(d):
    return datetime.strptime(d, '%b %d, %Y').strftime('%Y-%m-%d')

def plot_grp1_price():
        aave = pd.read_csv('priceData/aave_price_data.csv')
        compound = pd.read_csv('priceData/compound_price_data.csv')
        sushi = pd.read_csv('priceData/sushiswap_price_data.csv')
        uniswap = pd.read_csv('priceData/uniswap_price_data.csv')

        date = aave['Date']
        aave = aave['Price']
        compound = compound['Price']
        sushi = sushi['Price']
        uniswap = uniswap['Price']
        newdate = []

        for i in date:
            newdate.append(mdy_to_ymd(i))
        d = {'date':newdate,'aave':aave,'compound':compound,'sushi':sushi,'uniswap':uniswap}

        df = pd.DataFrame(data=d)

        subfig = make_subplots(specs=[[{"secondary_y": True}]])

        fig = px.line(df, x="date",y=['aave','compound'], render_mode="webgl")
        fig2 = px.line(df, x="date",y=['sushi','uniswap'], render_mode="webgl")

        fig2.update_traces(yaxis="y2")

        fig.update_layout(
            title_text = "Price and Sentiment of Aave, Compound, Sushi, and Uniswap",
            xaxis_rangeslider_visible= True,
            title_x= 0.5,
            title_font_size= 20,
        )

        subfig.add_traces(fig.data + fig2.data)
        subfig.layout.xaxis.title="Time"
        subfig.layout.yaxis.title="AAVE, COMPOUND"
        subfig.layout.yaxis2.title="SUSHI, UNISWAP"
        subfig.update_xaxes(dtick="M1")
        return subfig

def plot_sentiment(price_fig, sentiment, offset, chosen_defi_coin):
    arr = sentiment.lower().split(' ')
    filename = "sentimentalOutput/" + "-".join(arr) + ".json"
    with open(filename) as json_file:
        data = json.load(json_file)

    dict1 = {}
    dict2 = {}
    for i in data:
        arr = i.split("/")
        new_key = arr[1] + "-" + arr[0]
        dict1[new_key] = data[i]

        x = int(arr[0])
        if x == 12:
            # new_x = 1
            # new_key = str(int(arr[1]) + 1) + "-" + str(new_x)
            pass
        else:
            new_x = x + 1
            new_key = arr[1] + "-" + str(new_x)

        if len(new_key) == 6:
            arr = new_key.split('-')
            new_key = arr[0] + "-0" + arr[1] 
        dict2[new_key] = data[i]
    
    # for GPP1 price
    if chosen_defi_coin in ['GRP1', 'GRP2']:
        for new_key in dict1:
            dict1[new_key] = dict1[new_key] * 200
        for new_key in dict2:
            dict2[new_key] = dict2[new_key] * 200

    df = pd.DataFrame({'date': dict1.keys(), 'sentiment': dict1.values()})
    offset_df = pd.DataFrame({'date': dict2.keys(), 'sentiment': dict2.values()})

    if offset == False:
        sentiment_fig = px.line(df, x='date', y='sentiment')
    if offset == True:
        sentiment_fig = px.line(offset_df, x='date', y='sentiment')
    sentiment_fig.update_traces(yaxis="y2")
    fig = price_fig.add_traces(sentiment_fig.data)
    return fig

GRP1 = ['AAVE', 'UNISWAP', 'COMPOUND', 'SUSHI']
GRP2 = ['CURVE']

def plot_price(chosen_defi_coin):
    if chosen_defi_coin.lower() == "grp1":
        fig = plot_grp1_price()
        return fig
    if chosen_defi_coin.lower() == "grp2":
        chosen_defi_coin = "curve"
    filename = "priceData/" + chosen_defi_coin.lower() + "_price_data.csv"
    df = pd.read_csv(filename)
    df['format_date'] = df['Date'].apply(lambda x:  mdy_to_ymd(x))
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    price_fig = px.line(df, x="format_date", y="Price")
    price_fig.update_xaxes(dtick="M1")

    fig.add_traces(price_fig.data)

    return fig
    

app = Dash(__name__, external_stylesheets=[dbc.themes.LUMEN])
# app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

@callback(
    Output(component_id='price-chart', component_property='figure'),
    Input(component_id='defi-coin', component_property='value'), ###here
    Input(component_id='my-toggle-switch', component_property='value'),
    Input(component_id='sentiment', component_property='value')
    # Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)

#chosen_volume
def build_graphs(chosen_defi_coin, offset, sentiment): 

    fig = plot_price(chosen_defi_coin)

    if sentiment != None: #
        fig = plot_sentiment(fig, sentiment, offset, chosen_defi_coin)

        if chosen_defi_coin not in ['GRP1', 'GRP2']:
            priceFile = "priceData/" + chosen_defi_coin.lower() + "_price_data.csv"
            arr = sentiment.lower().split(' ')
            sentimentFile = "sentimentalOutput/" + "-".join(arr) + ".json"
            accuracy = calculateAccuracy(priceFile, sentimentFile) #accuracy
            accuracy = "    Accuracy: " + str(round(accuracy*100, 2)) + '%'

            fig.update_layout(
                title_text = "Price and Sentiment of " + chosen_defi_coin + accuracy,
                xaxis_rangeslider_visible= True,
                title_x= 0.5,
                title_font_size= 20,
            )

            fig.layout.xaxis.title="Time"
            fig.layout.yaxis.title="Price"
            fig.layout.yaxis2.title="Sentiment"

    else:
        fig.update_layout(
            title_text = "Price of " + chosen_defi_coin,
            xaxis_rangeslider_visible= True,
            title_x= 0.5,
            title_font_size= 20,
        )
        fig.layout.xaxis.title="Time"
        fig.layout.yaxis.title="Price"

    fig.for_each_trace(lambda t: t.update(line=dict(color=t.marker.color)))

    return fig

f = []
for (dirpath, dirnames, filenames) in walk('sentimentalOutput'):
    f.extend(filenames)
    break
tmp = ""

for i in f:
    arr = i.split('-')
    coin = arr[1].split('.')[0]
    option = arr[0].capitalize() + " " + coin.upper()
    tmp += option + ","
tmp = tmp[:-2].split(',')

f = []
for (dirpath, dirnames, filenames) in walk('priceData'):
    f.extend(filenames)
    break
hold = []
for i in f:
    arr = i.split('_')
    x = arr[0]
    x = arr[0].upper()
    hold.append({'label': x, 'value' : x})
hold.append({'label': 'GRP1 (AAVE, UNISWAP, SUSHI, COMPOUND)', 'value': 'GRP1'})

sentiment_layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            dcc.Dropdown
            (
                id='sentiment', 
                options= tmp,
                value = 'Discord GRP1',
                style = {'font-size': '1.25rem', 'font-weight': '500', 'text-align': 'center'}
            )
        ),
        dbc.Col(
            dcc.Dropdown
            (
                id='defi-coin', 
                options= hold,
                value = 'AAVE',
                style = {'font-size': '1.25rem', 'font-weight': '500', 'text-align': 'center'}
            )
        ),

        dbc.Col(
            daq.ToggleSwitch(
                id='my-toggle-switch',
                value=False,
                label= {'label': 'Offset Sentiment', 'style': {'font-size': '12px', 'font-weight': '500'}},
                labelPosition='bottom',
            ), width=dict(size=1)

        )
            
]),

    dbc.Row([
        dbc.Col(dcc.Graph(id='price-chart')) 
    ])
], fluid=True)