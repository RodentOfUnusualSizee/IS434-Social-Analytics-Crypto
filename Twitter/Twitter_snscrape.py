import enum
import snscrape.modules.twitter as sntwitter
import pandas as pd

from datetime import datetime
# keyword scraping
# https://betterprogramming.pub/how-to-scrape-tweets-with-snscrape-90124ed006af
# https://github.com/MartinBeckUT/TwitterScraper/blob/master/snscrape/python-wrapper/snscrape-python-wrapper.py

tweets = []

'''
Defi List:
makerDAO - $MKR
compound - $COMP
curve finance - $CRV
aave - $AAVE
uniswap - $UNI
sushiswap - $SUSHI
'''
search_term = "BTC"

# DONE : All done

start_time = datetime.now()
print("Started Scraping at: " + str(start_time))
try:
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(search_term + ' since:2021-09-01 until:2022-03-12').get_items()):
        # tweet is literally a link to said tweet
        content = tweet.content
        # Remove line breaks 
        content = content.replace('\n', ' ').replace('\r', ' ')
        tweets.append([tweet.date, tweet.id, content, tweet.user.username])
        if i % 10000 == 0:
            print("Progress : {}, Time : {} ".format(i, datetime.now() - start_time))
except KeyboardInterrupt:
    print("Stopping Scraping....")
    pass

finally:
    # convert to pandas DataFrame
    tweets_df = pd.DataFrame(tweets, columns=['Date', 'ID', 'Content', 'Username'])

    print("Building CSV....")

    #convert DataFrame to CSV
    tweets_df.to_csv('BTCTweets.csv', sep=',', index=False)

    end_time = datetime.now()

    print("Ended Scraping at: " + str(end_time))
    print("Duration: {}".format(end_time - start_time))
