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

<img src="ReadmeFiles\Hypothesis.png">

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
- Gephi
- BeautifulSoup
- Vader
- Flask
- Ploty Dash
- Sigma JS

# Deliverables

Our project includes a dashboard which plots our sentiment analysis and network analysis.
From our preliminary analysis, we found some correlated DeFi coins and grouped them together. This allows us to predict the prices of coins which have very little data but has high correlation to the group.

### Sentimental Analysis Dashboard

Our Sentiment analysis dashboard allows users to plot the sentiments on a price chart and any underlying selected crypto within the dashboard. There is also an accuracy indicator which is based off a simple algorithm we built to show how accurate a sentiment is with regard to predicting the underlying price. Furthermore, there is an offset button which allows users to offset the sentiment line by 1 month, allowing them to derive further insights.

### Discord Network Dashboard

Our Discord network dashboard represents users who have sent more than 200 messages in various DeFi Channels. Larger nodes are the discord channels of different defi coins. Other nodes are the users who have sent messages in the respective channels. The thickness of edges represents the number of messages sent in their respective channels.
This dashboard can be used to find out who are the key opinion leaders within the different clusters of crypto related discord channels

### Twitter Network Dashboard

Our Twitter network dashboard represents users who have mentioned/hashtagged at least one of the Defi Coins more than 300 times. Larger nodes are the twitter mentions/hashtags of different DeFi coins. Other nodes are the users who mentioned certain DeFi Coins. The thickness of edges represents the number of times the user mentioned the DeFi Coin.
This dashboard can be used to find out who are the key opinion leaders within the different clusters of crypto related twitter mentions or hashtags

### Automated ETL Process
Our dashboard includes a data manager which allows users to run scripts that automatically extract, clean, transform and load text, sentiment and price data into our dashboard. The automated ETL process allows our dashboard to show dynamic and up to date data for business users to perform real time analysis.

# How to Set Up 
**(Dev only not ready for prod)**

*Currently the credentials for the scrape are personal credentials, please do not abuse it* 

Clone our Github Repository or download the ZIP File
`gh repo clone RodentOfUnusualSizee/IS434-Social-Analytics-Crypto`

Step 1 : Run `main_app.py` and `backend-flash.py` inside the dashboard folder 
-	Make sure to `pip install` the required python packages

Step 2 : Run the network dashboards HTML files using live server or wamp
-	If you are to run the HTML files manually they are located in `Dashboard/gephi` and `Dashboard/twitter network gephi`


# Contributors
Group 7 - SuperIdol CryptoCurrency

<table>
    <tr>
        <td align="center"><img src="ReadmeFiles\brandon.jpg" width="150px;" alt=""/><br /><sub><b>Brandon</b></sub></a></td>
        <td align="center"><img src="ReadmeFiles\caleb.jpg" width="150px;" alt=""/><br /><sub><b>Caleb</b></sub></a></td>
        <td align="center"><img src="ReadmeFiles\rou.jpeg" width="150px;" alt=""/><br /><sub><b>Ching Rou</b></sub></a></td>
        <td align="center"><img src="ReadmeFiles\gerald.jpg" width="150px;" alt=""/><br /><sub><b>Gerald</b></sub></a></td>
        <td align="center"><img src="ReadmeFiles\yanwee.jpg" width="150px;" alt=""/><br /><sub><b>Yan Wee</b></sub></a></td>
    </tr>
</table>

