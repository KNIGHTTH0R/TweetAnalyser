import re
from dictionary_manager import DictionaryManager

# Regex
# TO-DO: Create regex for xx inches of snow
# Regex for location

rgx_link = re.compile(r'https?://[\w\d.-/]+')
rgx_punctuation = re.compile(r'[^\w\d\s#]')
rgx_whitespace = re.compile(r'\s+')

rgx_hashtag = re.compile(r'\B#\w*[a-zA-Z]+\w*')

# Fails on: 6-12 inches
rgx_inches = re.compile(r'(\d{1-2}["”]*\s?(-|to)\s?)?\d{1,2}\w*("|”|inches)')
rgx_interstate = re.compile(r'[iI]-[0-9]+')

class TweetManager():

    def find_dictionary_words(self, tweet, dictionary):
        found_words = set()
        for word in tweet.split():
            if word in dictionary:
                found_words.add(word)

        return list(found_words)

    def find_hashtags(self, tweet):
        matches = rgx_hashtag.finditer(tweet)

        hashtags = []
        for match in matches:
            hashtags.append(match.group(0))

        return hashtags

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
        """
        Temporary method to tell if a tweet contains required Regex.
        """
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
