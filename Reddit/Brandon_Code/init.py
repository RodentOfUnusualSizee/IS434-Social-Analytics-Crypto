import praw
import pandas as pd

data = []

reddit = praw.Reddit(client_id='qyQ-ZptZzPzRwoEiU-Q8Mg',client_secret='8E1k6yDJmnbnbfCJnmNFHoOarDaWrA', user_agent='IS434-Scrapper')

# get 1000 posts from the makerDAO subreddit
m_posts = reddit.subreddit('makerDAO').hot(limit=10)
for post in m_posts:
    data.append([post.title, post.score, post.id, post.subreddit,
        post.url, post.num_comments, post.selftext, post.created])

# get 1000 posts from the compound subreddit
c_posts = reddit.subreddit('makerDAO').hot(limit=10)
for post in c_posts:
    data.append([post.title, post.score, post.id, post.subreddit,
        post.url, post.num_comments, post.selftext, post.created])

# get 1000 posts from the curve finance subreddit
cf_posts = reddit.subreddit('makerDAO').hot(limit=10)
for post in cf_posts:
    data.append([post.title, post.score, post.id, post.subreddit,
        post.url, post.num_comments, post.selftext, post.created])

posts = pd.DataFrame(data,columns=['title','score','id','subreddit','url','num_comments','body','created'])
print(posts)
