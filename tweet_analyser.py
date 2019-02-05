from stanfordcorenlp import StanfordCoreNLP
from glob import glob
import pandas as pd

from secret import *
from dictionary_manager import DictionaryManager
from tweet_manager import TweetManager, Tweet

#nlp = StanfordCoreNLP(LOCATION_STARFORD_CORE_NLP)

# Load Dictionaries - Create Filter
winter_storm_filenames = glob('./Dictionaries/winter_storm_terms_*.txt')
winter_storm_phrases = DictionaryManager.phrases_from_files(winter_storm_filenames)

winter_storm_words = DictionaryManager.words_from_files(winter_storm_filenames)

#print(winter_storm_phrases)
#print('====')
print(winter_storm_words)

# Input Tweets
tweet_filenames = glob('../snow-tweets/*.csv')
df = pd.read_csv(tweet_filenames[3])

tweets = df[200:300]['text']

tm = TweetManager()

print('\nTWEETS')
relevant_tweets = []
irrelevant_tweets = []
for tweet in tweets:
    clean_tweet = tm.clean_tweet(tweet, winter_storm_words)
    
    relevant_tweet = tm.relevant_tweet(clean_tweet, winter_storm_words)
    if relevant_tweet:
        relevant_tweets.append(clean_tweet)
    else:
        irrelevant_tweets.append(clean_tweet)

print('\nRELEVANT TWEETS.')
for tweet in relevant_tweets:
    print(tweet)
print('\nIRRELEVANT TWEETS.')
for tweet in irrelevant_tweets:
    print(tweet)
#nlp.close() # Do not forget to close! The backend server will consume a lot memery.
