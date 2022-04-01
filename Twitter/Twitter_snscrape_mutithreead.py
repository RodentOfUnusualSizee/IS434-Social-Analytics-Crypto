import enum
import pandas as pd
import numpy as np
import os

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

def scrape(inputDetails):
    search_term=inputDetails[0]
    start=inputDetails[1]
    end=inputDetails[2]
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
        tweets_df.to_csv('./test/{}.csv'.format(search_term))

        end_time = datetime.now()
        print("Ended Scraping at: " + str(end_time))
        print("Duration: {}".format(end_time - start_time))


from multiprocess import Process
import time
if __name__ == "__main__":
    inputs= [
        ["$comp", "2021-01-01", "2022-03-01"],
        ["$crv", "2021-01-01", "2022-03-01"],
        ["$mkr", "2021-01-01", "2022-03-01"],
        ["$sushi", "2021-01-01", "2022-03-01"],
        ["$uni", "2021-01-01", "2022-03-01"],
    ]
    allT = []
    threadCount=0
    for indexx in range(0,len(inputs)):
        inputDetails = inputs[indexx]
        t = Process(target=scrape, args=(inputDetails,))
        t.start()
        print("starting process#",threadCount)
        threadCount +=1
        allT.append(t)
        time.sleep(5)


    # # # wait until thread 1 is completely executed
    for tread in allT:
        tread.join()

    print("Done!")
