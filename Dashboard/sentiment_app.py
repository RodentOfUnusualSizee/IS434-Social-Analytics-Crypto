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

def sentiment_analysis(chosen_defi_coin):
    stop = stopwords.words('english')
    def clean_content(contentInput):
        if type(contentInput) == np.float:
            return ""
        contentInput = contentInput.lower()
        contentInput = re.sub("'", "", contentInput) # to avoid removing contractions in english
        contentInput = re.sub("@[A-Za-z0-9_]+","", contentInput)
        contentInput = re.sub("#[A-Za-z0-9_]+","", contentInput)
        contentInput = re.sub(r'http\S+', '', contentInput)
        contentInput = re.sub('[()!?]', ' ', contentInput)
        contentInput = re.sub('\[.*?\]',' ', contentInput)
        contentInput = re.sub("[^a-z0-9]"," ", contentInput)
        contentInput = contentInput.strip()
        contentInput = contentInput.split()
        contentInput = [w for w in contentInput if not w in stop]
        contentInput = " ".join(word for word in contentInput)
        return contentInput

    string = chosen_defi_coin.lower() + ".csv"
    df = pd.read_csv(string)

    df['date'] = df['created'].apply(lambda x: x.split(' ')[0])
    df.sort_values(['date'], inplace=True)

    df['year_month'] = df['date'].apply(lambda x: x[0:x.rfind('-')])

    df = df.fillna(method='ffill')
    # monthList = pd.date_range('2021-01-01','2022-02-01', 
    #             freq='MS').strftime("%m/%Y").tolist()
    monthList = list(df['year_month'].unique())

    timeSplitData={}
    timeSplitDataSentiment = {}

    for month in monthList: 
        timeSplitData[month] = []
        timeSplitDataSentiment[month] = []  

    for row in df.iterrows():
        month = row[1]['year_month']
        content = row[1]['body']
        cleaned = clean_content(content)
        timeSplitData[month].append(cleaned)

    sid = SentimentIntensityAnalyzer()

    for month in monthList: # for month in timeSplitData:
        for content in timeSplitData[month]:
            output = sid.polarity_scores(content)
            timeSplitDataSentiment[month].append(output)
    
    timeSplitDataNetScore = {}
    for month in monthList:
        timeSplitDataNetScore[month] = 0 
        for output in timeSplitDataSentiment[month]:
            compound = output['compound']
            compound = compound / len(timeSplitDataSentiment[month])
            timeSplitDataNetScore[month] +=compound

    return timeSplitDataNetScore

app = Dash(__name__, external_stylesheets=[dbc.themes.LUMEN])
# app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

@callback(
    Output(component_id='price-chart', component_property='figure'),
    # Output(component_id='chosen-defi-coin', component_property='children'), 
    Input(component_id='defi-coin', component_property='value'), ###here
    Input(component_id='my-toggle-switch', component_property='value'),
)

#chosen_volume
def build_graphs(chosen_defi_coin, match): ###here
    string = "priceData/" + chosen_defi_coin.lower() + "_price_data.csv"
    price_df = pd.read_csv(string)
    # fig = px.line(df, x="Date", y="Price", template="plotly_dark")

    # here 
    # timeSplitDataNetScore = sentiment_analysis(chosen_defi_coin.lower())
    # timeSplitDataNetScore = pd.read_json('sentimentalOutput/discord.json')
    new_dict= {}
    new_dict2 = {}
    string = 'sentimentalOutput/discord-' + chosen_defi_coin.lower() + '.json'
    with open(string) as json_file:
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
    fig.update_xaxes(autorange="reversed") 
    # fig.update_xaxes(dtick="M1")

    if match == False:
        fig.add_trace(go.Scatter(x=sentiment_df['date'], y=sentiment_df['sentiment'], name='Sentiment', xperiodalignment='end'), secondary_y= True)

    if match == True:
        fig.add_trace(go.Scatter(x=sentiment_df2['date'], y=sentiment_df2['sentiment'], name='Sentiment', xperiodalignment='start'), secondary_y= True)

    fig.update_layout(
        # add title
        title_text="Price and Sentiment of " + chosen_defi_coin,
        xaxis_rangeslider_visible=True,
        title_x=0.5
    )
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Price", secondary_y=False)
    fig.update_yaxes(title_text="Sentiment", secondary_y=True)
    # fig.update_xaxes(autorange="reversed")
    ## here

    # fig.update_traces(line_color='#FF0000')
    # chosen_defi_coin = chosen_defi_coin + " price data"
    return fig

# app.layout = 
sentiment_layout = dbc.Container([
    # html.H1(id='chosen-defi-coin', style={'textAlign': 'center'}),

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
            value = 'AAVE'), width=dict(size=8, offset=2)),

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