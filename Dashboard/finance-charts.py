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
    Output(component_id='chosen-defi-coin', component_property='children'), 
    Input(component_id='defi-coin', component_property='value') ###here
)

#chosen_volume
def build_graphs(chosen_defi_coin): ###here
    string = chosen_defi_coin.lower() + "_price_data.csv"
    price_df = pd.read_csv(string)
    # fig = px.line(df, x="Date", y="Price", template="plotly_dark")

    fig.update_layout(
        xaxis_rangeslider_visible=True,
    )

    fig.update_xaxes(autorange="reversed")

    # add sentiment
    fig.add_trace(sentiment_analysis(chosen_defi_coin))

    ## here 
    timeSplitDataNetScore = sentiment_analysis(chosen_defi_coin.lower())
    sentiment_df = pd.DataFrame({'date': timeSplitDataNetScore.keys(), 'sentiment': timeSplitDataNetScore.values()})

    def mdy_to_ymd(d):
        return datetime.strptime(d, '%b %d, %Y').strftime('%Y-%m-%d')

    price_df['format_date'] = price_df['Date'].apply(lambda x:  mdy_to_ymd(x))

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=price_df['format_date'], y=price_df['Price'], name='Price'), secondary_y= False)
    fig.update_xaxes(autorange="reversed") 
    # fig.update_xaxes(dtick="M1")

    fig.add_trace(go.Scatter(x=sentiment_df['date'], y=sentiment_df['sentiment'], name='Sentiment'), secondary_y= True)

    fig.update_layout(
        title_text="Curve Data Price against Sentiment",
        title_x=0.5
    )
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Price", secondary_y=False)
    fig.update_yaxes(title_text="Sentiment", secondary_y=True)
    ## here

    # fig.update_traces(line_color='#FF0000')
    chosen_defi_coin = chosen_defi_coin + " price data"
    fig.update_yaxes(autorange="reversed")
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