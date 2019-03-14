from stanfordcorenlp import StanfordCoreNLP
from glob import glob
import pandas as pd

from utils import *
from secret import *
from dictionary_manager import DictionaryManager
from tweet_manager import TweetManager, SnowTweet

# Load Dictionaries - Create Filter
winter_storm_filenames = glob('./Dictionaries/winter_storm_terms_*.txt')

dm = DictionaryManager()
winter_storm_words = dm.words_from_files(winter_storm_filenames)

print('DICTIONARY OF WORDS:')
print(winter_storm_words)

# Input Tweets
tweet_filenames = glob('../snow-tweets/*.csv')
df_orig_tweets = pd.read_csv(tweet_filenames[2]) #0 #3 #2 #4

tweets = df_orig_tweets[:300]['text']

tm = TweetManager()

# fp - first phase
analysed_tweets_fp = tm.tweets_analysis_phase_one(tweets=tweets, dictionary=winter_storm_words)

#print('\nTWEETS')
snow_tweets =[]
for tweet in analysed_tweets_fp:
    if tweet['accepted']:
        st = SnowTweet(original_tweet=tweet['tweet'],
                       hashtags=tweet['hashtags'])
        snow_tweets.append(st)

left_list = dm.words_from_files(['./Dictionaries/snowfall_lg1l.txt'])
right_list = dm.words_from_files(['./Dictionaries/snowfall_lg1r.txt'])

print('\nCOLLOCATES (USE TRAINING DATA SETS)')
collocates_analysis = collocates(tweets, 'snowfall', 5)
print('LEFT: {}'.format(collocates_analysis['left']))
print('RIGHT: {}'.format(collocates_analysis['right']))

"""
print('\nLOCAL GRAMMAR')
for st in snow_tweets:
        lg = st.local_grammar('snowfall',left_list,right_list)

        if lg['left'] or lg['right']:
                print('LG: {} {} {}'.format(lg['left'], 'snowfall', lg['right']))
                print(st.original_tweet)
                print('\n')
"""