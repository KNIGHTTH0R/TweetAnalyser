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
import re

# KEYS
KEY_TEXT_ORIGINAL = "KEY_TEXT_ORIGINAL"
KEY_TEXT_FILTERED = "KEY_TEXT_ORIGINAL"
KEY_HASHTAGS_WITH_KEYWORDS = "KEY_HASHTAGS_WITH_KEYWORDS"
KEY_TEXT_KEYWORDS = "KEY_TEXT_KEYWORDS"

# LOCAL GRAMMAR RULES
rgx_rule_one = re.compile(r'TARGET-IN-NNP')

def text_from_tweet(tweet):
    if tweet['truncated']:
       return tweet['extended_tweet']['full_text']

    return tweet['text']

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
        lang = detect(text_from_tweet(tweet))
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
        t_text = text_from_tweet(tweet)
        
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
        tweet_text = text_from_tweet(tweet)
        hashtags = tm.find_hashtags(tweet_text)

        content_filtered_text = tm.clean_tweet(tweet_text)

        keywords_in_text = tm.find_keywords_in_tweet(content_filtered_text, keywords)
        hashtags_with_keywords = tm.find_hashtags_with_keywords(hashtags, keywords)

        if len(keywords_in_text) or len(hashtags_with_keywords):
            filtered_list.append({
                KEY_TEXT_ORIGINAL: tweet_text,
                KEY_TEXT_FILTERED: content_filtered_text,
                KEY_HASHTAGS_WITH_KEYWORDS: hashtags_with_keywords,
                KEY_TEXT_KEYWORDS: keywords_in_text
            })

    return filtered_list

def local_grammar_analysis(tweets, target_word):

    # POS tagging
    st = StanfordCoreNLP(LOCATION_STARFORD_CORE_NLP)
    
    for tweet in tweets_to_analyse:
        if target_word in tweet[KEY_TEXT_KEYWORDS]:
            # Original POS tags
            pos_tagged = st.pos_tag(tweet[KEY_TEXT_FILTERED])
            
            target_index = -1
            for i, tup in enumerate(pos_tagged):
                if tup[0] == target_word:
                    target_index = i
            
            # POS tags string (for Regex)
            pos_string = [tup[1] for tup in pos_tagged]
            pos_string[target_index] = 'TARGET'

            pos_string = '-'.join(pos_string)
            
            print('\n')

            # Regex Search
            rule_one_matches = rgx_rule_one.finditer(pos_string)
            
            if rule_one_matches:
                for match in rule_one_matches:
                    # TO-DO: If gets into this loop, match found, do something with the tweet.
                    print(match[0])
            
            print(tweet[KEY_TEXT_FILTERED])
            print(pos_string)

    st.close() # Do not forget to close! The backend server will consume a lot memery.

# Main Function
if __name__ == "__main__":
    
    # Load winter terms
    WINTER_STORM_DICTIONARIES = './Dictionaries/winter_storm_terms_*.txt'
    winter_storm_terms_filenames = glob(WINTER_STORM_DICTIONARIES)
    dm = DictionaryManager()
    winter_storm_words = dm.words_from_files(winter_storm_terms_filenames)

    filename = glob('./live-tweets/TweetBank/*.json')[0]
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
    tweets_to_analyse = keyword_filtered[5:7]
    local_grammar_analysis(tweets_to_analyse, 'snowfall')

    