import praw
import pandas as pd
import requests
import json
import datetime as dt


def getPushshiftData(query, after, before):
    # Build URL
    url = 'https://api.pushshift.io/reddit/search/submission/?q=' + \
        str(query)+'&size=1000&after='+str(after) + \
        '&before='+str(before)
    # Print URL to show user
    print(url)
    # Request URL
    r = requests.get(url)
    # Load JSON data from webpage into data variable
    data = json.loads(r.text)
    # return the data element which contains all the submissions data
    return data['data']

# This function will be used to extract the key data points from each JSON result
def collectSubData(subm):
    # subData was created at the start to hold all the data which is then added to our global subStats dictionary
    title = subm['title']
    url = subm['url']
    # flairs are not always present so we wrap in try/except
    try:
        flair = subm['link_flair_text']
    except KeyError:
        flair = "NaN"
    author = subm['author']
    sub_id = subm['id']
    score = subm['score']
    created = dt.datetime.fromtimestamp(
        subm['created_utc'])  # 1520561700.0
    numComms = subm['num_comments']
    permalink = subm['permalink']
    try:
        body = subm['selftext']
    except KeyError:
        body = "NaN"

    subDict = {
        'title': title,
        'url': url,
        'author': author,
        'score': score,
        'created': created,
        'numComms': numComms,
        'permalink': permalink,
        'flair': flair,
        'body': body
    }
    # Create a dictionary entry of current submission data and store all data related to it
    subStats[sub_id] = subDict


month = 1

monthDict = {
    1: [1, 31],
    2: [1, 28],
    3: [1, 31],
    4: [1, 30],
    5: [1, 31],
    6: [1, 30],
    7: [1, 31],
    8: [1, 31],
    9: [1, 30],
    10: [1, 31],
    11: [1, 30],
    12: [1, 31]
}


query = "MakerDAO"
#query="Curve Finance"

for i in range(month, 13):

    subCount = 0
    subStats = {}

    stDate = monthDict[i][0]
    endDate = monthDict[i][1]

    after = int(dt.datetime(2021, i, stDate, 0, 0).timestamp())
    before = int(dt.datetime(2021, i, endDate, 0, 0).timestamp())

    print(after)
    print(before)

    print(f'running query: {i} Month')

    data = getPushshiftData(query, after, before)

    # The length of data is the number submissions (data[0], data[1] etc), once it hits zero (after and before vars are the same) end
    while len(data) > 0:
        for submission in data:
            collectSubData(submission)
            subCount += 1
        # Calls getPushshiftData() with the created date of the last submission
        print(len(data))
        print(str(dt.datetime.fromtimestamp(data[-1]['created_utc'])))
        # update after variable to last created date of submission
        after = data[-1]['created_utc']
        # data has changed due to the new after variable provided by above code
        data = getPushshiftData(query, after, before)

    print(str(len(subStats)) + " submissions have added to list")

    posts_df = pd.DataFrame.from_dict(subStats, orient='index')
    
    posts_df.to_csv('../datav2/'+ query + "_query_" + str(i) + '.csv',
                    header=True, index=False, columns=list(posts_df.axes[1]))

# reddit = praw.Reddit(client_id='qyQ-ZptZzPzRwoEiU-Q8Mg',client_secret='8E1k6yDJmnbnbfCJnmNFHoOarDaWrA', user_agent='IS434-Scrapper')

# # get 1000 posts from the makerDAO subreddit
# m_posts = reddit.subreddit('makerDAO').hot(limit=10)
# for post in m_posts:
#     data.append([post.title, post.score, post.id, post.subreddit,
#         post.url, post.num_comments, post.selftext, post.created])


# posts = pd.DataFrame(data,columns=['title','score','id','subreddit','url','num_comments','body','created'])
# print(posts)
