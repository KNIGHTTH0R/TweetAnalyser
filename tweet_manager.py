import re
from dictionary_manager import DictionaryManager
from utils import *

class TweetManager():

    def tweets_analysis_phase_one(self, tweets, dictionary):
        """
        This function is the first phase of filtering incoming tweets.
        It takes an original tweet, cleans it using 'clean_tweet' function,
        extracts hashtags and looks for features (from dictionary) within
        the tweet itself and hashtags.
        If it finds any features, the tweet is accepted and added to the retured list.
        """

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
        dm = DictionaryManager()
        min_len = dm.shortest_len_in_dictionary(dictionary)

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

    def save_to_file(self, analysed_tweets, filename):
        """
        This method takes 'analysed_tweets' from 'tweets_analysis_phase_one()'
        """
        with open(filename, 'w') as f:
            for tweet in analysed_tweets:
                tweet_text = tweet['tweet']
                f.write(tweet_text + "\n")

class SnowTweet():

    def __init__(self,original_tweet,hashtags):
        self.original_tweet = original_tweet
        self.hashtags = hashtags
        self.retweet_from = None

    def extract_links(self):
        matches = rgx_link.finditer(self.original_tweet)

        links = []
        for match in matches:
            links.append(match.group(0))

        self.links = links

    def get_tweet(self):
        return self.original_tweet

    def get_hashtags(self):
        return self.hashtags

    def local_grammar(self, center_word, left_list, right_list, num_left_right=1):
        """
        Parameters.
        center_word: the base word that we're looking for,
        left_list, right_list: lists of words that can appear to the left/right
        of the center word,
        num_left_right: how many words to the left/right of the center word to consider
        """
        parsed_tweet = rgx_punctuation.sub(' ', self.original_tweet)
        parsed_tweet = rgx_whitespace.sub(' ', parsed_tweet)
        
        tweet_tokens = parsed_tweet.lower().split(' ')
        max_index = len(tweet_tokens) - 1

        local_grammar = { 'left': '', 'right': '' }
        for index,token in enumerate(tweet_tokens):
            if token and token == center_word:
                center_word_index = index
                
                left_index = center_word_index - num_left_right
                right_index = center_word_index + num_left_right

                if left_index < 0: left_index = 0
                if right_index > max_index: right_index = max_index

                left_word = tweet_tokens[left_index]
                right_word = tweet_tokens[right_index]

                if left_word in left_list:
                    local_grammar['left'] = left_word

                if right_word in right_list:
                    local_grammar['right'] = right_word

        return local_grammar