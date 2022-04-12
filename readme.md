# Correlation of DeFi Coin Prices and Social Media Sentiment

## IS434 Social Analytics Project - Group 7 SuperIdol CryptoCurrency

# Table of Contents
1. [Project Overview](#project-overview)
2. [Data Collection](#data-collection)
3. [Tools Used](#tools-used)
4. [Deliverables](#deliverables)
5. [How to Set Up](#how-to-set-up)
6. [Contributors](#contributors)

# Project Overview
Decentralised Finance (DeFi) is a form of cryptocurrency that provides decentralised financial products and services, such as borrowing, lending and derivatives. 

We believe that opinions on social media platforms influence investment decisions, and due to the strong network effect of social media, more people will make investment decisions based on social media opinions. This will lead to a change in the price of DeFi coins.

Based on this hypothesis, we set out to answer 3 questions:
1. Is there a relationship between Social Media Conversations and the price of DeFi coins?
2. How can we predict the impact of Social Media Conversations on the value of DeFi coins?
3. Who are the key drivers of crypto-related conversation on Social Media?

# Data Collection

We gathered data from the following sources:
- **Discord** : Conversations and User Data
- **Reddit** : Posts and Comments
- **Twitter** : Tweets
- **CoinGecko/Investing.com** : Price Data

# Tools Used
- Discord Developer API
- Python Reddit API Wrapper
- Pushshift.io
- SnScrape
- CoingeckoAPI
- Selenium

# Deliverables

Our project includes a dashboard which plots our sentimental analysis and network analysis.
From our preliminary analysis, we have found some correlated cryptos and had group them together. The idea behind is so that we can still predict cryptos prices that have very little sentimental data but is corelated to the group of correlated cryptos.

## Sentimental Analysis Dashboard

Our sentimental analysis dashboard allows users to plot the sentiments on a price chart and any underlying selected crypto within the dashboard. There is also an accuracy indicator which is a simple algorithm that we build to show how accurate a sentiment is in regard to predicting the underlying price. Furthermore, there is an offset button that allows users to offset the sentimental line by 1 month to visually see if there are any insights.

## Discord Network Dashboard

Our discord network dashboard represents users who have sent more than 200 messages in various Defi Channels. Larger nodes are the discord channels of different defi coins. Other nodes are the users who are sent messages the respective channels. The thickness of edges represents the number of messages sent in their respective channels.
This dashboard can be used to find out who is the key opinion leaders within the different clusters of crypto’s related discord channels

## Twitter Network Dashboard

Our twitter network dashboard represents users who have mentioned/hash tagged at least one of the Defi Coins more than 300 times. Larger nodes are the twitter mentions/hashtags of different defi coins. Other nodes are the users who mentioned certain Defi Coins. The thickness of edges represents the number of times the user mentioned the Defi Coin.
This dashboard can be used to find out who is the key opinion leaders within the different clusters of crypto’s related twitter mentions or hashtags

## Automated ETL Process
Our dashboard also includes a data manager that allows users to run scripts that automatically extract, clean, transform and load text, sentiment and price data into our dashboard. The automated ETL process allows our dashboard to show dynamic and up to date data for our business users to perform real time analysis.

# How to Set Up 
**(Dev only not ready for prod)**

*Currently the credentials for the scrape are personal credentials, please do not abuse it* 

Step 1 : Run main_app.py and backend-flash.py inside the dashboard folder 
-	Make sure to pip install the required python packages

Step 2 : Run the network dashboards HTML files using live server or wamp
-	If you are to run the HTML files manually they are located in Dashboard/gephi and Dashboard/twitter network gephi


# Contributors
Group 7 - SuperIdol CryptoCurrency

<table style="border:0.5px solid;">
    <tr>
        <td align="center"><img src="" width="150px;" alt=""/><br /><sub><b>Brandon</b></sub></a></td>
        <td align="center"><img src="" width="150px;" alt=""/><br /><sub><b>Caleb</b></sub></a></td>
        <td align="center"><img src="" width="150px;" alt=""/><br /><sub><b>Rou</b></sub></a></td>
        <td align="center"><img src="" width="150px;" alt=""/><br /><sub><b>Gerald</b></sub></a></td>
        <td align="center"><img src="" width="150px;" alt=""/><br /><sub><b>Yan Wee</b></sub></a></td>
    </tr>
</table>
