import numpy as np
import pandas as pd
import re
from nltk.corpus import stopwords
# nltk.download('vader_lexicon') if needed
from nltk.sentiment.vader import SentimentIntensityAnalyzer



def clean_content(contentInput):
    stop = stopwords.words('english')
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

def sentiment(search_term):
    # tweet_path = 'Tweets\{}.csv'.format(search_term)
    # price_path = 'Price Data\{}.csv'.format(search_term)

    df = pd.read_csv('{}.csv'.format(search_term), sep=',')
    print(df.head())

    df['year_month'] = df['Date'].apply(lambda x: x[0:x.rfind('-')])
    list(df['year_month'].unique()) 

    monthList = list(df['year_month'].unique())
    monthList.reverse()  # dynamically change the date range here

    timeSplitData={}
    timeSplitDataSentiment = {}

    for month in monthList: 
        timeSplitData[month] = []
        timeSplitDataSentiment[month] = []

    for row in df.iterrows():
    #extracting month data from row
        monthData = row[1]['year_month']
        content = row[1]['Content']
        #cleaning Data
        cleaned = clean_content(content)
        #Storing into time split dict
        timeSplitData[monthData].append(cleaned)
    
    ######## SENTIMENT SCORING  ##########

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
    
    print(timeSplitDataNetScore)



sentiment()