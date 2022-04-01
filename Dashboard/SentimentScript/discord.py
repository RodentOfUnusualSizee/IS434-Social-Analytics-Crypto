from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import pandas as pd
import numpy as np
import re
from nltk.corpus import stopwords

# Data loading
df = pd.read_csv(
    "../textData/discord.csv", encoding="ISO-8859-1")
df = df.fillna(method='ffill')
# Data Cleaning
stop = stopwords.words('english')

def clean_content(contentInput):
    if type(contentInput) == np.float:
        return ""
    contentInput = contentInput.lower()
    # to avoid removing contractions in english
    contentInput = re.sub("'", "", contentInput)
    contentInput = re.sub("@[A-Za-z0-9_]+", "", contentInput)
    contentInput = re.sub("#[A-Za-z0-9_]+", "", contentInput)
    contentInput = re.sub(r'http\S+', '', contentInput)
    contentInput = re.sub('[()!?]', ' ', contentInput)
    contentInput = re.sub('\[.*?\]', ' ', contentInput)
    contentInput = re.sub("[^a-z0-9]", " ", contentInput)
    contentInput = contentInput.strip()
    contentInput = contentInput.split()
    contentInput = [w for w in contentInput if not w in stop]
    contentInput = " ".join(word for word in contentInput)
    return contentInput

# sentimental model
nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()


def getSentiment(startDate, endDate, serverNames):
    monthList = pd.date_range(startDate, endDate,
                              freq='MS').strftime("%m/%Y").tolist()

    timeSplitDataGroup = {}
    timeSplitDataSentimentGroup = {}

    for month in monthList:
        timeSplitDataGroup[month] = []
        timeSplitDataSentimentGroup[month] = []

    for row in df.iterrows():
        # extracting month data from row
        dateData = row[1]['date']
        tmp = dateData.find('/')
        monthData = dateData[tmp+1:]  # removing day e.g '12/'
        if len(monthData) == 6:
            monthData = "0"+monthData

        if monthData in timeSplitDataGroup:  # check if data is in range of date we want to analyli
            content = row[1]['content']
            # cleaning Data
            cleaned = clean_content(content)
            # Storing into time split dict
            if row[1]['serverName'] in serverNames:
                timeSplitDataGroup[monthData].append(cleaned)

    for month in timeSplitDataGroup:
        for content in timeSplitDataGroup[month]:
            output = sid.polarity_scores(content)
            timeSplitDataSentimentGroup[month].append(output)


    # Calculating Net Weighted Sentiment Score
    timeSplitDataNetScoreGroup = {}
    for month in monthList:
        timeSplitDataNetScoreGroup[month] = 0

    for month in timeSplitDataGroup:
        for output in timeSplitDataSentimentGroup[month]:
            compound = output['compound']
            compound = compound / len(timeSplitDataGroup[month])
            timeSplitDataNetScoreGroup[month] += compound

    return timeSplitDataNetScoreGroup

# serverNames
group1Names = ['SushiSwap Community',
               'serverName',
               'Aave Community',
               'r/CrpytoCurrency',
               'Curve Finance',
               'Uniswap']
group2Names = ['Compound']

# ensure data has this date range
startDate = '2021-01-01'
endDate = '2022-02-01'

res = getSentiment(startDate, endDate, group2Names)
print(res)


# ## to chart it
# import matplotlib.pyplot as plt

# xAxis = []
# yAxis = []

# for date in res:
#     xAxis.append(date)
#     yAxis.append(res[date])

# plt.plot(xAxis,yAxis, color='red', marker='o')
# plt.title('Discord Group 1 DEFI CryptoCurrency Sentimental Analysis')
# plt.xlabel('Month')
# plt.xticks(rotation=45)
# plt.ylabel('Net Sentiment')
# # plt.grid(True)
# plt.show()