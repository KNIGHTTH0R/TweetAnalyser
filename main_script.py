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
from dictionary_manager import DictionaryManager
from secret import *

from nltk.tokenize import word_tokenize
import nltk

import ast
import json
import re

# KEYS
KEY_TEXT_ORIGINAL = "KEY_TEXT_ORIGINAL"
KEY_TEXT_FILTERED = "KEY_TEXT_ORIGINAL"
KEY_HASHTAGS_WITH_KEYWORDS = "KEY_HASHTAGS_WITH_KEYWORDS"
KEY_TEXT_KEYWORDS = "KEY_TEXT_KEYWORDS"

# LOCAL GRAMMAR RULES

# signigicant snowfall, heavy snowfall
rule_one = r"""RULEONE: {<JJ>{1}<TARGET>{1}}"""
rule_one_parser = nltk.RegexpParser(rule_one)

def snow_depth_rules(tagged_text):
    rule_depth = r"""DEPTH: {<CD>{1}<TO>?<CD>{1}}"""
    rule_depth_parser = nltk.RegexpParser(rule_depth)

    parsed = rule_depth_parser.parse(tagged_text)
    return parsed

def inches_of_snow_rules(tagged_text):
    rule_inches_of_snow = r"""INCHES_OF_SNOW: {<CD><TO>?<CD><NNS><IN><TARGET>}"""
    rule_inches_of_snow_parser = nltk.RegexpParser(rule_inches_of_snow)

    parsed = rule_inches_of_snow_parser.parse(tagged_text)
    return parsed

def interstate_rules(tagged_text):
    rule_interstate = r"""INTERSTATE: {<PRP>{1}<CD>{1}}"""
    rule_interstate_parser = nltk.RegexpParser(rule_interstate)

    parsed = rule_interstate_parser.parse(tagged_text)
    return parsed

def perhour_rules(tagged_text):
    rule_per_hour = r"""PERHOUR: {<CD><CD><IN><NN><TARGET>}"""
    rule_per_hour_parser = nltk.RegexpParser(rule_per_hour)

    parsed = rule_per_hour_parser.parse(tagged_text)
    return parsed

def print_info(filenames):
    print('=== FILENAMES LIST ===')
    for i, fn in enumerate(filenames):
        print('[{}] {}'.format(i, fn))

def text_from_tweet(tweet):
    try:
        if tweet['truncated']:
            return tweet['extended_tweet']['full_text']

    except KeyError:
        pass

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

def load_tweets_backup(filename):
    """
    This method loads single quoted JSON data.
    Regular JSON expects double quotes.
    """
    
    try:
        with open(filename, 'r') as f:
            data = ast.literal_eval(f.read())
    except:
        print('ERROR in load_tweets_backup.')

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

def pos_tagging(tweets, target_word):
    tagged_tweets = []
    for tweet in tweets:
        if target_word in tweet[KEY_TEXT_KEYWORDS]:
            words = word_tokenize(tweet[KEY_TEXT_FILTERED])
            tagged = nltk.pos_tag(words)

            # Replace target word tag with TARGET
            for i, (word, tag) in enumerate(tagged):
                if word == target_word:
                    tagged[i] = (word, 'TARGET')

            tagged_obj = { 'original': tweet, 'tagged': tagged }
            tagged_tweets.append(tagged_obj)

    return tagged_tweets 

def examine_rule_parsed_tweet(parsed_tweet, tweet_text, label, results):
    new_results = results

    for subtree in parsed_tweet.subtrees():
        if subtree.label() == label:
            if tweet_text in new_results.keys():
                new_results[tweet_text].append(subtree)
            else:
                new_results[tweet_text] = [subtree]

    return new_results

def local_grammar_analysis(tweets, target_word):

    lg_results = {}
    for tweet in tweets:
        if target_word in tweet['original'][KEY_TEXT_KEYWORDS]:
            orig_text = tweet['original'][KEY_TEXT_ORIGINAL]

            parsed = perhour_rules(tweet['tagged'])
            lg_results = examine_rule_parsed_tweet(
                parsed_tweet=parsed,
                tweet_text=orig_text,
                label='PERHOUR',
                results=lg_results)

            parsed = snow_depth_rules(tweet['tagged'])
            lg_results = examine_rule_parsed_tweet(
                parsed_tweet=parsed,
                tweet_text=orig_text,
                label='DEPTH',
                results=lg_results)

            parsed = inches_of_snow_rules(tweet['tagged'])
            lg_results = examine_rule_parsed_tweet(
                parsed_tweet=parsed,
                tweet_text=orig_text,
                label='INCHES_OF_SNOW',
                results=lg_results)

            parsed = interstate_rules(tweet['tagged'])
            lg_results = examine_rule_parsed_tweet(
                parsed_tweet=parsed,
                tweet_text=orig_text,
                label='INTERSTATE',
                results=lg_results)          

    return lg_results

def parse_lg_results():
    pass

def run_program(raw_tweets, keywords, target_list):
    # Filtering
    en_raw_tweets = language_filter(raw_tweets)
    print('Language filter completed. Size: {}'.format(len(en_raw_tweets)))

    unique_raw_tweets = duplicates_filter(en_raw_tweets)
    print('Duplicates removed. Size: {}'.format(len(unique_raw_tweets)))

    keyword_filtered = keyword_filter(unique_raw_tweets, keywords)
    print('Keyword filtered tweets. Text and Hashtags only. Size: {}'.format(len(keyword_filtered)))

    # Local Grammar Analysis
    # Separated Tag and LG Analysis methods.
    # Run LG on tagged tweets.
    lg_results = {}
    tweets_to_analyse = keyword_filtered
    for target_word in target_list:
        tagged_tweet = pos_tagging(tweets_to_analyse, target_word)
        # Find LG in all tweets using current target word.
        lg_result = local_grammar_analysis(tagged_tweet, target_word)
        lg_results[target_word] = lg_result

    print('\n')

    # Analyse LG results
    for key, analysis in lg_results.items():

        print(f'WORD: {key.upper()}')
        for tweet, trees in analysis.items():
            depth = []
            interstate = []
            perhour = []
            inchessnow = []
            
            print(tweet.strip())
            for tree in trees:
                parts = [word for (word, tag) in tree]
                if tree.label() == 'DEPTH':
                    if len(parts) == 2:
                        depth.append(' to '.join(parts))
                    else:
                        depth.append(' '.join(parts))

                elif tree.label() == 'INTERSTATE':
                    interstate.append('-'.join(parts))

                elif tree.label() == 'PERHOUR':
                    perhour.append(' '.join(parts[:4]))

                elif tree.label() == 'INCHES_OF_SNOW':
                    inchessnow.append(' '.join(parts))

            if interstate:
                print('Interstate info: {}'.format(interstate))

            if inchessnow:
                print('Inches of snow: {}'.format(inchessnow))
            elif perhour:
                print('Per hour info: {}'.format(perhour))
            else:
                print('Snow depth info: {}'.format(depth))

            print('\n')

def tag_text(text, keywords, target_word):
    tm = TweetManager()

    hashtags = tm.find_hashtags(text)

    content_filtered_text = tm.clean_tweet(text)

    print(content_filtered_text)

    keywords_in_text = tm.find_keywords_in_tweet(content_filtered_text, keywords)
    hashtags_with_keywords = tm.find_hashtags_with_keywords(hashtags, keywords)

    if len(keywords_in_text) or len(hashtags_with_keywords):
        filtered_tweet = {
            KEY_TEXT_ORIGINAL: text,
            KEY_TEXT_FILTERED: content_filtered_text,
            KEY_HASHTAGS_WITH_KEYWORDS: hashtags_with_keywords,
            KEY_TEXT_KEYWORDS: keywords_in_text
        }
        
    # LG
    if target_word in filtered_tweet[KEY_TEXT_KEYWORDS]:
        words = word_tokenize(filtered_tweet[KEY_TEXT_FILTERED])
        tagged = nltk.pos_tag(words)

        # Replace target word tag with TARGET
        for i, (word, tag) in enumerate(tagged):
            if word == target_word:
                tagged[i] = (word, 'TARGET')

        parsed = snow_depth_rules(tagged)

        print(tagged)

        for subtree in parsed.subtrees():
            if subtree.label() == 'DEPTH':
                print(subtree)

def print_raw_tweets(tweets):
    for tweet in tweets:
        print(tweet['text'])

# Main Function
if __name__ == "__main__":
    
    # Load winter terms
    WINTER_STORM_DICTIONARIES = './Dictionaries/winter_storm_terms_*.txt'
    winter_storm_terms_filenames = glob(WINTER_STORM_DICTIONARIES)
    dm = DictionaryManager()
    winter_storm_words = dm.words_from_files(winter_storm_terms_filenames)

    filenames = glob('./live-tweets/TweetBank/*.json')

    # Info print
    print_info(filenames)
    print('\n')

    raw_tweets = load_tweets_backup(filenames[0]) #_backup #6
    #print_raw_tweets(raw_tweets)
    print('Loaded tweets. Size: {}'.format(len(raw_tweets)))

    # Running main program
    run_program(raw_tweets, winter_storm_words, ['snow', 'snowfall'])

    #test_text = 'RT   NE Ohio...it will basically be a 6" to 10" snowfall with some totals around a foot.  Wind a big factor Saturday night.…'
    #test_text = 'RT   This major storm system dropped another 18-30" of new snow since yesterday bringing the storm total to 33-48" and coun…'
    #test_text = 'Locations near I-55 and east picked up a quick one to three inches of new snowfall Thursday'

    # Northern Illinois - NNP NNP
    #test_text = 'So both NAMs have 6 12 inches of snow across Northern Illinois and GFS is a little more lighter with widespread 4 8 WEBSITE'
    
    #test_text = '3 4 per hour snowfall'
    #tag_text(test_text, winter_storm_words, 'snowfall')
