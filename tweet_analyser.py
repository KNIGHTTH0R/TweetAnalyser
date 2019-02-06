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
print('DICTIONARY OF WORDS:')
print(winter_storm_words)

# Input Tweets
tweet_filenames = glob('../snow-tweets/*.csv')
df = pd.read_csv(tweet_filenames[3])

tweets = df[:20]['text']

tm = TweetManager()

print('\nTWEETS')
for tweet in tweets:
    clean_tweet = tm.clean_tweet(tweet, winter_storm_words)
    found_hashtags = tm.find_hashtags(tweet)
    parsed_hashtags = tm.hashtags_to_words(found_hashtags)
    found_words_in_tweet = tm.find_dictionary_words(clean_tweet, winter_storm_words)
    found_words_in_hashtags = tm.find_dictionary_words_in_hashtags(parsed_hashtags, winter_storm_words)

    print('Original Tweet :: {}'.format(tweet))
    print('Hashtags :: {}'.format(found_hashtags))
    print('Clean Tweet :: {}'.format(clean_tweet))
    print('Found Dictionary Words (in tweet) :: {}'.format(found_words_in_tweet))
    print('Found Dictionary Words (in hashtags) :: {}'.format(found_words_in_hashtags))

    if len(found_words_in_hashtags) > 0 or len(found_words_in_tweet) > 0:
        print('TWEET ACCEPTED.')
    else:
        print('TWEET REJECTED.')
    print('\n')

#nlp.close() # Do not forget to close! The backend server will consume a lot memery.
