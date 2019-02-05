import re
from dictionary_manager import DictionaryManager

# Regex
# TO-DO: Create regex for xx inches of snow
# Regex for location

rgx_link = re.compile(r'https?://[\w\d.-/]+')
rgx_punctuation = re.compile(r'[^\w\d\s#]')
rgx_whitespace = re.compile(r'\s+')

# Fails on: 6-12 inches
rgx_inches = re.compile(r'(\d{1-2}["”]*\s?(-|to)\s?)?\d{1,2}\w*("|”|inches)')
rgx_interstate = re.compile(r'[iI]-[0-9]+')

class TweetManager():

    def relevant_tweet(self, tweet, dictionary):
        found_words = []
        for word in tweet.split():
            if word in dictionary:
                found_words.append(word)

        return len(found_words) > 0

    def clean_tweet(self, tweet, dictionary):
        """
        This method thakes a single tweet and removes everything that
        I considered unnecessary (this might change in future).
        """
        min_len = DictionaryManager.shortest_len_in_dictionary(dictionary)

        parsed_tweet = tweet
        parsed_tweet = rgx_link.sub('LINK', parsed_tweet)
        parsed_tweet = rgx_punctuation.sub(' ', parsed_tweet)
        parsed_tweet = rgx_whitespace.sub(' ', parsed_tweet)
        parsed_tweet = parsed_tweet.lower()

        final_parsed_tweet = []
        for word in parsed_tweet.split():
            if len(word) >= min_len:
                final_parsed_tweet.append(word)

        return ' '.join(final_parsed_tweet)

    def find_tweet(self, tweet):
        matches = rgx_interstate.finditer(tweet)

        found = []
        for match in matches:
            found.append(match)

        if len(found) > 0:
            return found

        return None

class Tweet():

    def __init__(self,tweet):
        self.original_tweet = tweet
        self.hashtags = []
        self.height = False

    def parse_tweet(self):
        height = rgx_inches.search(self.original_tweet)
        if height:
            self.height = True
