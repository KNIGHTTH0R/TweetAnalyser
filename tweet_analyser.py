from stanfordcorenlp import StanfordCoreNLP
from glob import glob
import pandas as pd

from utils import *
from secret import *
from dictionary_manager import DictionaryManager
from tweet_manager import TweetManager, SnowTweet

# TO-DO: Clean up the script. Rethink classes.

# Load Dictionaries - Create Filter
winter_storm_filenames = glob('./Dictionaries/winter_storm_terms_*.txt')
winter_storm_phrases = DictionaryManager.phrases_from_files(winter_storm_filenames)

winter_storm_words = DictionaryManager.words_from_files(winter_storm_filenames)

#print(winter_storm_phrases)
#print('====')
print('DICTIONARY OF WORDS:')
print(winter_storm_words)

# Input Tweets
tweet_filenames = glob('../snow-tweets/*.csv')
df_orig_tweets = pd.read_csv(tweet_filenames[2]) #0 #3 #2

tweets = df_orig_tweets[:20]['text']

tm = TweetManager()

# fp - first phase
analysed_tweets_fp = tm.tweets_analysis_phase_one(tweets=tweets, dictionary=winter_storm_words)
print('Size: {}'.format(len(analysed_tweets_fp)))

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

print('\nSNOW TWEETS')
#nlp = StanfordCoreNLP(LOCATION_STARFORD_CORE_NLP)
inches_range = []
for st in snow_tweets:
        #print('============')
        tweet_text = st.get_tweet()
        print(tweet_text)
        if tm.find_tweet(tweet_text):
                inches_range.append(tweet_text)
        
        #pos_tagged = nlp.pos_tag(st.get_tweet())

        # TO-DO: Define Regex for Local Grammar (LG) that I'm looking for.
        # Search tagged sentence for that LG using NLTK.

        #print(pos_tagged)

#nlp.close() # Do not forget to close! The backend server will consume a lot memery.

print('\nINCHES RANGE TWEETS: {}'.format(len(inches_range)))
for tweet in inches_range:
        print(tweet)