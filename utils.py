import re

# REGEX
rgx_link = re.compile(r'https?://[\w\d.-/]+')
rgx_punctuation = re.compile(r'[^\w\d\s#]')
rgx_whitespace = re.compile(r'\s+')

rgx_hashtag = re.compile(r'\B#\w*[a-zA-Z]+\w*')

# For Local Grammar
rgx_inches_range = re.compile(r'\d{1,2}[\"\'\`]?\s?(-|to)\s?\d{1,2}[\"\'\`]?\s?(inches)?')
rgx_interstate = re.compile(r'[iI]-[0-9]+')

def print_tweet_status(tweet, hashtags, clean_tweet, features_in_tweet,
                       features_in_hashtags):
    print('Original tweet :: {}'.format(tweet))
    print('Clean tweet :: {}'.format(clean_tweet))
    print('Hashtags :: {}'.format(hashtags))
    print('Features in tweet :: {}'.format(features_in_tweet))
    print('Features in hashtags :: {}'.format(features_in_hashtags))
