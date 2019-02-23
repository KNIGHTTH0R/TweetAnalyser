from glob import glob
import pandas as pd

from utils import *
from secret import *
from dictionary_manager import DictionaryManager
from tweet_manager import TweetManager, SnowTweet

# 0. Notes - Tweet Info
# "screen_name" - twitter username
# "retweeted_status" - if attribute exists - it's a retweet.

# 1. Load Dictionary of Snow words.
winter_storm_filenames = glob('./Dictionaries/winter_storm_terms_*.txt')
dm = DictionaryManager()
winter_storm_words = dm.words_from_files(winter_storm_filenames)

# 2. Load collected Tweets.
tweets_filename = glob('./live-tweets/*.json')
df_tweets = pd.read_json(tweets_filename[0], orient='records')

tweets_text = df_tweets[:40]['text']

# TEST
tweets_test = df_tweets[:2][['text','retweeted_status']]
print(tweets_test)
# TEST

tm = TweetManager()

# 3. First Phase Analysis
# Gets Tweets and Hashtags and looks for features in them.
analysed_tweets_fp = tm.tweets_analysis_phase_one(tweets=tweets_text, dictionary=winter_storm_words)
print('Analysed Tweets (FP) :: Len :: {}'.format(len(analysed_tweets_fp)))

snow_tweets = []
snow_tweets_text = []
print('\nTWEETS REJECTED IN PHASE ONE.')
print('{')
for tweet in analysed_tweets_fp:
        if tweet['accepted']:
                st = SnowTweet(original_tweet=tweet['tweet'], hashtags=tweet['hashtags'])
                snow_tweets.append(st)
                snow_tweets_text.append(tweet['tweet'])
        else:
                print('{}\n'.format(tweet['tweet']))
print('}')

print('\nSnow Tweets :: Len :: {}'.format(len(snow_tweets)))

# Collocation Analysis on word - snowfall
left_list = dm.words_from_files(['./Dictionaries/snowfall_lg1l.txt'])
right_list = dm.words_from_files(['./Dictionaries/snowfall_lg1r.txt'])

print('\n{')
print('COLLOCATES (OF LIVE TWEETS). CENTER WORD - snowfall.')
collocates_analysis = collocates(snow_tweets_text, 'snowfall', 5)
print('LEFT: {}'.format(collocates_analysis['left']))
print('RIGHT: {}'.format(collocates_analysis['right']))
print('}')

# 4. Local Grammar

lg_tweets = []
non_lg_tweets = []
print('\nLOCAL GRAMMAR')
for st in snow_tweets:
        lg = st.local_grammar('snowfall',left_list,right_list)

        if lg['left'] or lg['right']:
                st.extract_links()
                lg_tweets.append(st)
                print(st.original_tweet)
                print('LG: [{} {} {}]'.format(lg['left'], 'snowfall', lg['right']))

                if st.hashtags:
                        print(st.hashtags)
                if st.links:
                        print(st.links)
                print()
        else:
                non_lg_tweets.append(st)

print('\nLG Tweets :: Len :: {}'.format(len(lg_tweets)))

print('\nNON LG TWEETS.')
for tweet in non_lg_tweets:
        print(tweet.original_tweet)
