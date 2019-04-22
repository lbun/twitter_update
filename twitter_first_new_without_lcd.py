import twitter
import tweepy
from tweepy import API
from tweepy import Cursor
import numpy as np
from sqlalchemy import create_engine
import pandas as pd
import time
from time import sleep

# instantiate lcd and specify pins

ck = '06ReKUx7R4bNQAQyWGg1ysiy1'
cs = '6jXPTW5GCqSF32DpVr3EDodhWOgTiAglNAFmMyrS9nkwsxQtoc'
atk = '1119970679313653760-YXSsiawzukr64jaY3CeaaZoaEco4xK'
ats = '0JtmNKFVoZXOa8SjjBLI0uWQ78AyMuKHxxYSmAMgEOcsE'

auth = tweepy.OAuthHandler(ck, cs)
auth.set_access_token(atk, ats)
auth_api = API(auth)

api = tweepy.API(auth, wait_on_rate_limit=True)

# Get the list of friends
list_of_friends_id = api.friends_ids()

# To get the name of a friend
# x = api.friends()[0]
# x.name

# my id
my_id = api.me().id

# Create a dataframe every x minutes
df = pd.DataFrame(columns=np.arange(5))
for user in list_of_friends_id:
    list_tweet = api.user_timeline(user,count=3)
    for tweet in list_tweet:
        df.loc[len(df)] = [tweet.id,tweet.geo,tweet.favorite_count,tweet.retweet_count,tweet.lang]

df[5]=df[2]+df[3]*2
print(df.shape)
df = df.sort_values(by=5,ascending=False)

my_id = api.me().id
y = api.user_timeline(my_id)
my_tweets_list = [i.id for i in y]

print('You have published already ',len(my_tweets_list), ' tweets')
counter = 0
counter_tweet = 0
for tw in list(df[0][:60]):
    counter+=1
    print(counter, end='\r')
    if tw in my_tweets_list:
        print(id,' already published')
    else:
        try:
            counter_tweet+=1
            print('tweet number: ',counter_tweet,end='\r')
            api.retweet(tw)
            time.sleep(60)
        except Exception as e:
            print(e,end='\r')