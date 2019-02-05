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

print(winter_storm_phrases)
print('====')
print(winter_storm_words)

# Input Tweets
tweet_filenames = glob('../snow-tweets/*.csv')
df = pd.read_csv(tweet_filenames[0])

print('\nTWEETS')
tweet_set = df[1:100]['text']

for tweet in tweet_set:
    found = TweetManager.find_tweet(tweet)
    if found:
        print('YES: {}, F: {}'.format(tweet, found[0].group(0)))
    #else:
    #    print('NO: {}'.format(tweet))
    print('========')

    """
    parsed_tweet = TweetManager.parse_tweet(tweet, winter_storm_words)
    relevant_tweet = TweetManager.relevant_tweet(parsed_tweet, winter_storm_words)
    if relevant_tweet:
        print('YES: {}'.format(tweet))
        print('Parsed: {}'.format(parsed_tweet))
    else:
        print('NO: {}'.format(tweet))
        print('Parsed: {}'.format(parsed_tweet))

    print('====')
    """
#nlp.close() # Do not forget to close! The backend server will consume a lot memery.
