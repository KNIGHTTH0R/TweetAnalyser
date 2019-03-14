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

from tweet_manager import TweetManager

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

def keyword_filter(tweet_objects):
    tm = TweetManager()

    for tweet in tweet_objects:
        tweet_text = tweet['text']

        hashtags = tm.find_hashtags(tweet_text)
        

    pass

def content_filter(tweet_objects):
    pass

# Main Function
if __name__ == "__main__":

    filename = glob('./live-tweets/RawTweets/*.json')[0]
    raw_tweets = load_tweets(filename)
    print('Loaded tweets. Size: {}'.format(len(raw_tweets)))

    en_raw_tweets = language_filter(raw_tweets)
    print('Language filter completed. Size: {}'.format(len(en_raw_tweets)))

    unique_raw_tweets = duplicates_filter(en_raw_tweets)
    print('Duplicates removed. Size: {}'.format(len(unique_raw_tweets)))

