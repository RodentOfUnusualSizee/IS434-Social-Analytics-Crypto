import enum
import pandas as pd
import numpy as np

import snscrape.modules.twitter as sntwitter
from datetime import datetime
# keyword scraping
# https://betterprogramming.pub/how-to-scrape-tweets-with-snscrape-90124ed006af
# https://github.com/MartinBeckUT/TwitterScraper/blob/master/snscrape/python-wrapper/snscrape-python-wrapper.py

start_time = datetime.now()
end = start_time.strftime("%Y-%m-%d")
#END is the END of the date range needed for scraping
# START is the START of the date range needed for scraping

# Start should be automatically assigned as the latest date of scraping for the data

def scrape(search_term, start, end = end):
    tweets = []
    print("Started on : {}".format(start_time))
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
        # continue process
        pass
    finally:
        # create dataframe
        tweets_df = pd.DataFrame(tweets, columns=['Date', 'ID', 'Content', 'Username'])
        print("Building CSV....")

        #convert DataFrame to CSV
        tweets_df.to_csv('{}.csv'.format(search_term))

        end_time = datetime.now()
        print("Ended Scraping at: " + str(end_time))
        print("Duration: {}".format(end_time - start_time))


scrape("$aave", "2021-01-01", "2022-03-01")