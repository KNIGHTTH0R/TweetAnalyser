from glob import glob
import pandas as pd

from utils import *
from secret import *
from dictionary_manager import DictionaryManager
from tweet_manager import TweetManager, SnowTweet

from config.config import *

# 0. Notes - Tweet Info
# "screen_name" - twitter username
# "retweeted_status" - if attribute exists - it's a retweet.
# RT (original username) tweets_start.iloc[[i]]['retweeted_status'].values[0]['user']['screen_name']

# 1. Load Dictionary of Snow words.
winter_storm_filenames = glob(RELEVANT_TERMS_DICTIONARIES)
dm = DictionaryManager()
winter_storm_words = dm.words_from_files(winter_storm_filenames)

# 2. Load collected Tweets.
tweets_filename = glob(TWEETS_FILE)
df_tweets = pd.read_json(tweets_filename[0], orient='records')

tweets_start = df_tweets[:40]
print('Starting with :: {} :: Tweets'.format(len(tweets_start)))


# TEST
#tweets_test = df_tweets[:2][['text','retweeted_status']]
#print(tweets_test)
# TEST

tm = TweetManager()

# 3. First Phase Analysis
# Gets Tweets and Hashtags and looks for features in them.
analysed_tweets_fp = tm.tweets_analysis_phase_one(tweets=tweets_start['text'], dictionary=winter_storm_words)

accepted_tweets = []
accepted_tweets_text = []
rejected_tweets = []
for i, tweet in enumerate(analysed_tweets_fp):
        st = SnowTweet(original_tweet=tweet['tweet'], hashtags=tweet['hashtags'])
        if tweet['accepted']:
                if tweets_start.iloc[[i]]['retweeted_status'].any():
                        st.retweet_from = tweets_start.iloc[[i]]['retweeted_status'].values[0]['user']['screen_name']
                accepted_tweets.append(st)
                accepted_tweets_text.append(tweet['tweet'])
        else:
                rejected_tweets.append(st)

print('\nAfter First Phase analysis (FP) :: {} :: Tweets left'.format(len(accepted_tweets)))

if PRINT_REJECTED_PHASE_ONE:
        print('\nTWEETS REJECTED IN PHASE ONE.')
        print('{')
        for tweet in rejected_tweets:
                print(tweet.original_tweet)
        print('}')

# Collocation Analysis on word - snowfall
left_list = dm.words_from_files([PATH_LEFT_LIST])
right_list = dm.words_from_files([PATH_RIGHT_LIST])

if PRINT_COLLOCATES:
        print('\n{')
        print('COLLOCATES IN TWEETS. CENTER WORD - {}.'.format(COLLOCATES_WORD))
        collocates_analysis = collocates(accepted_tweets_text, COLLOCATES_WORD, 5)
        print('LEFT: {}'.format(collocates_analysis['left']))
        print('RIGHT: {}'.format(collocates_analysis['right']))
        print('}')

# 4. Local Grammar
if PRINT_LOCAL_GRAMMAR:
        lg_tweets = []
        non_lg_tweets = []
        print('\nLOCAL GRAMMAR')
        for st in accepted_tweets:
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
                        if st.retweet_from:
                                print('RT from: {}'.format(st.retweet_from))
                        else:
                                print('ORIGINAL TWEET.')
                        print()
                else:
                        non_lg_tweets.append(st)

        print('\nLG detected in :: {} :: Tweets'.format(len(lg_tweets)))

if PRINT_NON_LG_TWEETS:
        print('\nNON LG TWEETS.')
        for tweet in non_lg_tweets:
                print(tweet.original_tweet)
