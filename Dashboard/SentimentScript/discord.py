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
            if row[1]['serverName'] in serverNames:
            # cleaning Data
                cleaned = clean_content(content)
            # Storing into time split dict
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
               'Aave Community',
               'r/CrpytoCurrency',
               'Compound',
               'Uniswap']
group2Names = ['Curve Finance']

# ensure data has this date range
from datetime import datetime
startDate = '2021-01-01'
endDate = datetime.today().strftime('%Y-%m-%d')

# group1 = getSentiment(startDate, endDate, group1Names)
# group2 = getSentiment(startDate, endDate, group2Names)
# sushi = getSentiment(startDate, endDate, ['SushiSwap Community'])
# aave = getSentiment(startDate, endDate, ['Aave Community'])
# curve = getSentiment(startDate, endDate, ['Curve Finance'])
# uniswap = getSentiment(startDate, endDate, ['Uniswap'])
# compound = getSentiment(startDate, endDate, ['Compound'])


import json
# for groups
group1 = getSentiment(startDate, endDate, group1Names)
with open("../sentimentalOutput/discord-grp1.json", "w") as write_file:
    json.dump(group1, write_file, indent=4)
group2 = getSentiment(startDate, endDate, group2Names)
with open("../sentimentalOutput/discord-grp2.json", "w") as write_file:
    json.dump(group2, write_file, indent=4)
# For individual Crpto
sushi = getSentiment(startDate, endDate, ['SushiSwap Community'])
with open("../sentimentalOutput/discord-sushi.json", "w") as write_file:
    json.dump(sushi, write_file, indent=4)
aave = getSentiment(startDate, endDate, ['Aave Community'])
with open("../sentimentalOutput/discord-aave.json", "w") as write_file:
    json.dump(aave, write_file, indent=4)
curve = getSentiment(startDate, endDate, ['Curve Finance'])
with open("../sentimentalOutput/discord-curve.json", "w") as write_file:
    json.dump(curve, write_file, indent=4)
uniswap = getSentiment(startDate, endDate, ['Uniswap'])
with open("../sentimentalOutput/discord-uniswap.json", "w") as write_file:
    json.dump(uniswap, write_file, indent=4)
compound = getSentiment(startDate, endDate, ['Compound'])
with open("../sentimentalOutput/discord-compound.json", "w") as write_file:
    json.dump(compound, write_file, indent=4)


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