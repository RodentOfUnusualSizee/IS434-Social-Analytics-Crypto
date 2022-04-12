import enum
import pandas as pd
import numpy as np
from dateutil import parser

import snscrape.modules.twitter as sntwitter
from datetime import datetime
# keyword scraping
# https://betterprogramming.pub/how-to-scrape-tweets-with-snscrape-90124ed006af
# https://github.com/MartinBeckUT/TwitterScraper/blob/master/snscrape/python-wrapper/snscrape-python-wrapper.py

start_time = datetime.now()
end = start_time.strftime("%Y-%m-%d")
#END is the END of the date range needed for scraping - later date
# START is the START of the date range needed for scraping - earlier date
# Start should be automatically assigned as the latest date of scraping for the data

def scrape(search_term, start = "test", end = end):
    # if start not specified, assume starting from latest date in 
    # also assume that there is already data present
    path = "..\TweetData\${}.csv".format(search_term)
    old = pd.read_csv(path, encoding="ISO-8859-1")
    last_date = old['Date'][0]
    strTime = parser.parse(last_date)
    startDate = strTime.strftime("%Y-%m-%d")
    if start == "test":  # if start not specified, start = latest date on file
        start = startDate

    tweets = []
    print("Started on : {}".format(start_time))
    print("START DATE: {}".format(start))
    timeframeString = " since:" + start +" until:" + end

    try:
        for i,tweet in enumerate(sntwitter.TwitterSearchScraper(search_term + timeframeString).get_items()):
            # tweet is literally a link to said tweet
            content = tweet.content
            # Remove line breaks 
            content = content.replace('\n', ' ').replace('\r', ' ')
            tweets.append([tweet.date, tweet.id, content, tweet.user.username])
            if i % 10000 == 0:
                print("Progress : {}, Time : {} ".format(i, datetime.now() - start_time))
    except KeyboardInterrupt:
        print("Stopping Scraping....")
        print("Continuing the process....")
        # continue process
    finally:
        # create dataframe
        tweets_df = pd.DataFrame(tweets, columns=['Date', 'ID', 'Content', 'Username'])
        print("Building CSV....")

        #convert DataFrame to CSV
        new = pd.concat([tweets_df, old])
        new.to_csv('..\TweetData\${}.csv'.format(search_term))  # replace old csv sheet with updated one

        end_time = datetime.now()
        print("Ended Scraping at: " + str(end_time))
        print("Duration: {}".format(end_time - start_time))

list = ["aave", "crv", "comp", "mkr", "sushi", "uni"]
for coin in list:
    scrape(coin)