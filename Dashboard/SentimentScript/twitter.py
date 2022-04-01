import numpy as np
import pandas as pd
import json
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
    df = pd.read_csv('..\TweetData\{}.csv'.format(search_term), sep=',')
    df['year_month'] = df['Date'].apply(lambda x: x[0:x.rfind('-')])

    monthList = list(df['year_month'].unique())
    monthList.reverse() 

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
            timeSplitDataNetScore[month] += compound

    return timeSplitDataNetScore

# INDIVIDUAL
print("Starting Individual Sentiment Score")
aave = sentiment('$aave')
# crv = sentiment('$crv')
comp = sentiment('$comp')
mkr = sentiment('$mkr')
sushi = sentiment('$sushi')
# uni = sentiment('$uni')
# optimise? sentiment runs twice at this rate

# GROUPS
print("Starting Group Sentiment Score")
group1Names = ["$aave","$mkr","$sushi"]
group2Names = ['$comp']

group1 = {}
group2 = {}

for name in group1Names:
    score = sentiment(name)
    for month in score:
        if month in group1:
            group1[month] += score[month]
        else:
            group1[month] = score[month]

for name in group2Names:
    score = sentiment(name)
    for month in score:
        if month in group2:
            group2[month] += score[month]
        else:
            group2[month] = score[month]


print("Starting JSON Dumping")
# assume you have these dicts already
with open("../sentimentalOutput/twitter1.json", "w") as write_file:
    json.dump(group1, write_file, indent=4)
with open("../sentimentalOutput/twitter2.json", "w") as write_file:
    json.dump(group2, write_file, indent=4)
# Individual sentiment 
with open("../sentimentalOutput/twitter-aave.json", "w") as write_file:
    json.dump(aave, write_file, indent=4)
#with open("../sentimentalOutput/twitter-curve.json", "w") as write_file:
    #json.dump(crv, write_file, indent=4)
with open("../sentimentalOutput/twitter-compound.json", "w") as write_file:
    json.dump(comp, write_file, indent=4)
with open("../sentimentalOutput/twitter-mkr.json", "w") as write_file:
    json.dump(mkr, write_file, indent=4)
with open("../sentimentalOutput/twitter-sushi.json", "w") as write_file:
    json.dump(sushi, write_file, indent=4)
# with open("../sentimentalOutput/twitter-uni.json", "w") as write_file:
#     json.dump(uni, write_file, indent=4)


