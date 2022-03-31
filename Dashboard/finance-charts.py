from distutils.command.build import build
from dash import Dash, html, dcc, Output, Input, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import numpy as np
import re
from nltk.corpus import stopwords
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from plotly.subplots import make_subplots

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

stop = stopwords.words('english')


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
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(px.line(price_df, x="Date", y="Price"))
    # fig = px.line(df, x="Date", y="Price", template="plotly_dark")

    fig.update_layout(
        xaxis = dict(
            tickmode = "array",
            tickvals = ['Mar 01, 2022', 'Feb 05, 2022', 'Jan 06, 2022', 'Dec 01, 2021',
                        'Nov 01, 2021', 'Oct 02, 2021', 'Sep 02, 2021', 'Aug 03, 2021',
                        'Jul 04, 2021', 'Jun 04, 2021'],
            ticktext = ['Mar 2022', 'Feb 2022', 'Jan 2022', 'Dec 2021',
                        'Nov 2021', 'Oct 2021', 'Sep 2021', 'Aug 2021',
                        'July 2021', 'June 2021']
        ), xaxis_rangeslider_visible=True
    )
    
    fig.update_yaxes(autorange="reversed")

    ### sentiment analysis  start ###
    string = chosen_defi_coin.lower() + ".csv"
    sentiment_df = pd.read_csv(string)
    sentiment_df['date'] = sentiment_df['created'].apply(lambda x: x.split(' ')[0])
    sentiment_df.sort_values(['date'], inplace=True)
    sentiment_df = sentiment_df.fillna(method='ffill')
    sentiment_df['year_month'] = sentiment_df['date'].apply(lambda x: x[0:x.rfind('-')])

    monthList = list(sentiment_df['year_month'].unique())
    timeSplitData={}
    timeSplitDataSentiment = {}

    for month in monthList: 
        timeSplitData[month] = []
        timeSplitDataSentiment[month] = []  

    def split(x):
        monthData = x['year_month']
        content = x['body']
        cleaned = clean_content(content)
        timeSplitData[monthData].append(cleaned)

    sentiment_df.apply(lambda x: split(x), axis=1) 
    sid = SentimentIntensityAnalyzer()
    for month in timeSplitData:
        for content in timeSplitData[month]:
            output = sid.polarity_scores(content)
            timeSplitDataSentiment[month].append(output)  

    timeSplitDataNetScore = {}
    for month in monthList:
        timeSplitDataNetScore[month] = 0 
        
    for month in timeSplitDataSentiment:
        for output in timeSplitDataSentiment[month]:
            compound = output['compound']
            compound = compound / len(timeSplitDataSentiment[month])
            timeSplitDataNetScore[month] +=compound 
    
    date_dict ={
    '2021-01': 'Jan 2021',
    '2021-02': 'Feb 2021',
    '2021-03': 'Mar 2021',
    '2021-04': 'Apr 2021',
    '2021-05': 'May 2021',
    '2021-06': 'Jun 2021',
    '2021-07': 'Jul 2021',
    '2021-08': 'Aug 2021',
    '2021-09': 'Sep 2021',
    '2021-10': 'Oct 2021',
    '2021-11': 'Nov 2021',
    '2021-12': 'Dec 2021',
    }

    final = {}
    for old_key in timeSplitDataNetScore.keys():
        new_key = date_dict[old_key]
        final[new_key] = timeSplitDataNetScore[old_key]

    fig.add_trace(
    go.Scatter(x=list(final.keys()), y=list(final.values()), name="Sentiment"),
    secondary_y=True,
    )
    ### sentiment analysis end ###  

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
            value = 'MAKER',
    ), width=dict(size=8, offset=2))]),

    dbc.Row([
        dbc.Col(dcc.Graph(id='price-chart')) 
    ]), 
], fluid=True)


if __name__=='__main__':
    app.run_server(debug=True)