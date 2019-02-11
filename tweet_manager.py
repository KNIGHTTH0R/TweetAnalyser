import re
from dictionary_manager import DictionaryManager

# Regex
# TO-DO: Create regex for xx inches of snow
# Regex for location

rgx_link = re.compile(r'https?://[\w\d.-/]+')
rgx_punctuation = re.compile(r'[^\w\d\s#]')
rgx_whitespace = re.compile(r'\s+')

rgx_hashtag = re.compile(r'\B#\w*[a-zA-Z]+\w*')

# Inches range
"""
\d{1,2}
["'`]?
\s+
(-|to)
\s+
\d{1,2}
["'`]?
\s*
inches?
"""
#\d{1,2}[\"\'\`]?\s?(-|to)\s?\d{1,2}[\"\'\`]?\s?inches? <-- worked
#\d{1,2}[\"\'\`]?\s*(-|to)\s*\d{1,2}[\"\'\`]?\s*inches?
rgx_inches_range = re.compile(r'\d{1,2}[\"\'\`]?\s?(-|to)\s?\d{1,2}[\"\'\`]?\s?(inches)?')

# Fails on: 6-12 inches
rgx_inches = re.compile(r'(\d{1-2}["”]*\s?(-|to)\s?)?\d{1,2}\w*("|”|inches)')
rgx_interstate = re.compile(r'[iI]-[0-9]+')

class TweetManager():

    def tweets_analysis_phase_one(self, tweets, dictionary):
        analysed_tweets = []
        for tweet in tweets:
            clean_tweet = self.clean_tweet(tweet, dictionary)
            hashtags = self.find_hashtags(tweet)
            parsed_hashtags = self.hashtags_to_words(hashtags)
            features_in_tweet = self.find_features_tweet(clean_tweet, dictionary)
            features_in_hashtags = self.find_features_hashtags(parsed_hashtags, dictionary)

            accepted = len(features_in_hashtags) > 0 or len(features_in_tweet) > 0

            analysed_tweets.append({
                'tweet': tweet,
                'clean_tweet': clean_tweet,
                'hashtags': hashtags,
                'parsed_hashtags': parsed_hashtags,
                'features_in_tweet': features_in_tweet,
                'features_in_hashtags': features_in_hashtags,
                'accepted': accepted
            })

        return analysed_tweets

    def find_features_tweet(self, tweet, dictionary):
        found_words = set()
        for word in tweet.split():
            if word in dictionary:
                found_words.add(word)

        return list(found_words)

    def find_features_hashtags(self, hashtags, dictionary):
        """
        This method takes a list of hashtags and checks if they exist
        in the passed in dictionary of words.
        """
        found_words = set()
        for hashtag in hashtags:
            hashtag_lower = hashtag.lower()
            if hashtag_lower in dictionary:
                found_words.add(hashtag_lower)
        
        return list(found_words)

    def find_hashtags(self, tweet):
        matches = rgx_hashtag.finditer(tweet)

        hashtags = []
        for match in matches:
            hashtags.append(match.group(0))

        return hashtags

    def hashtags_to_words(self, hashtags):
        """
        This method extracts words from a list of hashtags,
        and returns a list of extracted words.
        """
        words = []
        for hashtag in hashtags:
            found_words = re.findall('[A-Z][^A-Z]*', hashtag[1:])
            words += found_words
        
        return list(set(words))

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
        matches = rgx_inches_range.finditer(tweet)

        found = []
        for match in matches:
            found.append(match)

        if len(found) > 0:
            return found

        return None

class SnowTweet():

    def __init__(self,original_tweet,hashtags):
        self.original_tweet = original_tweet
        self.hashtags = hashtags

    def parse_tweet(self):
        # Clean up the tweet first, so there are less terms to search.
        snow_height = rgx_inches.search(self.original_tweet)
        if snow_height:
            self.snow_height = True

    def get_tweet(self):
        return self.original_tweet
