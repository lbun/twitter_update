import twitter
import tweepy
from tweepy import API
from tweepy import Cursor
import numpy as np
from sqlalchemy import create_engine
import pandas as pd
import time
from time import sleep
import os
import requests
from bs4 import BeautifulSoup
import facebook


ck = os.environ.get('CK')
cs = os.environ.get('CS')
atk = os.environ.get('ATK')
ats = os.environ.get('ATS')

token_facebook = os.environ.get('fb')

auth = tweepy.OAuthHandler(ck, cs)
auth.set_access_token(atk, ats)
auth_api = API(auth)

api = tweepy.API(auth, wait_on_rate_limit=True)

# Get the list of friends
list_of_friends_id = api.friends_ids()
# list_of_friends_id[:5]

# To get the name of a friend
x = api.friends()[0]
# x.name

y = api.user_timeline(18949452,count=5)[0]

# print(y.geo,y.id,y.favorite_count,y.retweet_count,y.lang)

# my id
my_id = api.me().id
# len(api.user_timeline(my_id))

# my_id = api.me().id
# y = api.user_timeline(my_id)
# my_tweets_list = [i.id for i in y]

list_of_friends_id = api.friends_ids()

def create_df():
    df = pd.DataFrame(columns=np.arange(12))
    for user in list_of_friends_id:
        list_tweet = api.user_timeline(user,count=3,exclude_replies=True)
        for tweet in list_tweet:
            try:
                hashtags = ' '.join([i for i in tweet._json['text'].split() if i[0]=='#'])
                url=tweet._json['entities']['urls'][0]['url']
                page = requests.get(url)
                soup = BeautifulSoup(page.text, 'html.parser')
                h1 = '#news '+soup.find('h1').text.strip()
                list_values = [tweet.id, #0
                       tweet.geo, #1
                       tweet.favorite_count, #2
                       tweet.retweet_count, #3
                       tweet.lang, #4
                        user,  #5
                       tweet._json['user']['id'],  #6
                       tweet._json['text'],  #7
                       tweet._json['entities']['urls'][0]['url'],   #8
                       hashtags,  #9
                       h1+' '+url+' '+hashtags,       #10
                       tweet.favorite_count*tweet.retweet_count, #11
                      ]
                df.loc[len(df)] = list_values
            except:
                pass

    df[11]=df[2]+df[3]*2   #scoring of the tweets
    df = df[df[4]=='en']
    df[12] = [False if i[:2]=='RT' else True for i in df[7]]
    df = df.sort_values(by=11,ascending=False)
    df = df[df[12]]
    print(df.shape)
    return df

def post_tweet(df):
    counter_tweet = 0
    for i in list(df.index):
        try:
            api.update_status(df.loc[i][10])
            counter_tweet+=1
            print(time.ctime(),counter_tweet)
            time.sleep(180)
        except:
            pass

if __name__=='__main__':
    tweet_counter=0
    while tweet_counter<6:
        df = create_df()
        post_tweet(df)
        if tweet_counter==5:
            tweet_counter=0
