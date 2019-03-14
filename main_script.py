"""
1. Raw tweets collected from Twitter are loaded.
2. Filtering process:
    - Twitter's native keyword filter - DONE on collection.
    - Language filter.
    - Filter out duplicates (duplicate tweets and duplicate retweets).
    - Keyword filter - extract hashtags, then look for relevant keywords in tweets and hashtags.
    - Content filter - remove unnecessary information.
All tweets that pass the filters go into LocalGrammar analysis stage. (Save to separate file?)
3.
"""

from glob import glob
from langdetect import detect
from stanfordcorenlp import StanfordCoreNLP

from tweet_manager import TweetManager
from dictionary_manager import DictionaryManager
from secret import *

import json

def load_tweets(filename):
    """
    Takes a filename.
    Returns a list of raw tweet objects located in that file.
    """

    try:
        with open(filename, 'r') as f:
            data = json.loads(f.read())
    except:
        print('ERROR in load_tweets.')

    return data

def language_filter(tweet_objects):
    """
    Takes a list of raw tweet objects.
    Returns a list of raw tweet objects in English language only.
    """

    filtered_list = []

    for tweet in tweet_objects:    
        lang = detect(tweet['text'])
        if lang == 'en':
            filtered_list.append(tweet)

    return filtered_list

def duplicates_filter(tweet_objects):
    """
    Takes a list of raw tweet objects.
    Returns a list of raw tweet object without duplicate tweets or duplicate retweets.
    """

    cache = []
    filtered_list = []

    for tweet in tweet_objects:
        t_text = tweet['text']
        
        if t_text not in cache:
            filtered_list.append(tweet)
            cache.append(t_text)

    return filtered_list

def keyword_filter(tweet_objects, keywords):
    """
    Takes tweet objects and a list of keywords to look for.
    This function performs hashtag extraction, content filtering and keyword search.
    """
    
    tm = TweetManager()

    filtered_list = []

    for tweet in tweet_objects:
        # Separate text and hashtags
        tweet_text = tweet['text']
        hashtags = tm.find_hashtags(tweet_text)

        content_filtered_text = tm.clean_tweet(tweet_text)

        keywords_in_text = tm.find_keywords_in_tweet(content_filtered_text, keywords)
        keywords_in_hashtags = tm.find_hashtags_with_keywords(hashtags, keywords)

        if len(keywords_in_text) or len(keywords_in_hashtags):
            filtered_list.append({ 
                'text': content_filtered_text,
                'hashtags': keywords_in_hashtags,
                'text_keywords': keywords_in_text
            })

    return filtered_list

# Main Function
if __name__ == "__main__":
    
    # Load winter terms
    WINTER_STORM_DICTIONARIES = './Dictionaries/winter_storm_terms_*.txt'
    winter_storm_terms_filenames = glob(WINTER_STORM_DICTIONARIES)
    dm = DictionaryManager()
    winter_storm_words = dm.words_from_files(winter_storm_terms_filenames)

    filename = glob('./live-tweets/RawTweets/*.json')[0]
    raw_tweets = load_tweets(filename)
    print('Loaded tweets. Size: {}'.format(len(raw_tweets)))

    # Filtering
    en_raw_tweets = language_filter(raw_tweets)
    print('Language filter completed. Size: {}'.format(len(en_raw_tweets)))

    unique_raw_tweets = duplicates_filter(en_raw_tweets)
    print('Duplicates removed. Size: {}'.format(len(unique_raw_tweets)))
    
    keyword_filtered = keyword_filter(unique_raw_tweets, winter_storm_words)
    print('Keyword filtered tweets. Text and Hashtags only. Size: {}'.format(len(keyword_filtered)))

    # Local Grammar Analysis
    tweets_for_lg = keyword_filtered[:20]

    main_word = 'snow'

    # POS tagging
    st = StanfordCoreNLP(LOCATION_STARFORD_CORE_NLP)
    for tweet in tweets_for_lg:
        if main_word in tweet['text_keywords']:
            pos_tagged = st.pos_tag(tweet['text'])

            print(pos_tagged)

            """    
            for i, tup in enumerate(pos_tagged):
                if tup[0] == main_word:
                    print('Found: {} in position {}'.format(tup, i))
            """
    st.close() # Do not forget to close! The backend server will consume a lot memery.
