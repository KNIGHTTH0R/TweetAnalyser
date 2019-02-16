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

print('\nTWEETS')
snow_tweets =[]
for tweet in analysed_tweets_fp:
    if tweet['accepted']:
        st = SnowTweet(original_tweet=tweet['tweet'],
                       hashtags=tweet['hashtags'])
        snow_tweets.append(st)
        
        print('\n')
        print_tweet_status(tweet=tweet['tweet'],
                            hashtags=tweet['hashtags'],
                            clean_tweet=tweet['clean_tweet'],
                            features_in_tweet=tweet['features_in_tweet'],
                            features_in_hashtags=tweet['features_in_hashtags'])

left_list = dm.words_from_files(['./Dictionaries/snowfall_lg1l.txt'])
right_list = dm.words_from_files(['./Dictionaries/snowfall_lg1r.txt'])

collocates_analysis = collocates(tweets, 'snowfall', 5)
print('LEFT: {}'.format(collocates_analysis['left']))

"""
print('\nLOCAL GRAMMAR')
for st in snow_tweets:
        st.local_grammar('snowfall',left_list,right_list)
"""
#pos_tagged = nlp.pos_tag(st.get_tweet())
#nlp = StanfordCoreNLP(LOCATION_STARFORD_CORE_NLP)
#nlp.close() # Do not forget to close! The backend server will consume a lot memery.
