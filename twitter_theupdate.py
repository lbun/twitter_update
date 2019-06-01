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


ck = os.environ.get('CK')
cs = os.environ.get('CS')
atk = os.environ.get('ATK')
ats = os.environ.get('ATS')

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

def theupdate_at_work():
    while True:
        df = pd.DataFrame(columns=np.arange(11))
        for user in list_of_friends_id[:5]:
            list_tweet = api.user_timeline(user,count=3,exclude_replies=True)
            for tweet in list_tweet:
                try:
                    hashtags = ' '.join([i for i in tweet._json['text'].split() if i[0]=='#'])
                    url=tweet._json['entities']['urls'][0]['url']
                    page = requests.get(url)
                    soup = BeautifulSoup(page.text, 'html.parser')
                    h1 = '#news '+soup.find('h1').text.strip()
                    df.loc[len(df)] = [tweet.id, #0
                                       tweet.geo, #1
                                       tweet.favorite_count, #2
                                       tweet.retweet_count, #3
                                       tweet.lang, #4
                                        user,  #5
                                       tweet._json['user']['id'],  #6
                                       tweet._json['text'],  #7
                                       tweet._json['entities']['urls'][0]['url'],   #8
                                       hashtags,  #9
                                       h1+' '+url+' '+hashtags]        #10
                except:
                    pass
        df[11]=df[2]+df[3]*2   #scoring of the tweets
        df = df[df[4]=='en']
        df[12] = [False if i[:2]=='RT' else True for i in df[7]]
        df = df.sort_values(by=11,ascending=False)
        df = df[df[12]]
        counter = 0
        counter_tweet = 0
        counter_errors = 0
        for tw in list(df[10]):
            # counter+=1
            # print('Global counter: ',counter, end='\r')
            if counter_tweet==5:
                break
            else:
                try:
                    api.update_status(tw)
                    counter_tweet+=1
                    #print('tweet number: ',counter_tweet,end='\r')
                    for second in range(180):
                        time.sleep(1)
                        #print('timer: ',179-second,end='\r')
                except:
                    pass

if __name__=='__main__':
    theupdate_at_work()
