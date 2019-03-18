import re
from dictionary_manager import DictionaryManager
from utils import *

class TweetManager():

    def find_keywords_in_tweet(self, tweet, keywords):
        found_words = set()
        for word in tweet.split():
            if word in keywords:
                found_words.add(word)

        return list(found_words)

    def find_hashtags_with_keywords(self, hashtags, keywords):
        """
        This method takes a list of hashtags belogning to a single tweet.
        Returns a list of hashtags that contain keywords.
        """

        hashtags_with_keywords = []

        for hashtag in hashtags:

            hashtag_words = self.__hashtag_to_words(hashtag)    

            if len(hashtag_words):
                for word in hashtag_words:
                    if word.lower() in keywords:
                        hashtags_with_keywords.append(hashtag)
                        continue

        return hashtags_with_keywords

    def __hashtag_to_words(self, hashtag):
        """
        This method extracts words from a list of hashtags,
        and returns a list of extracted words.
        """
        
        found_words = re.findall('[a-zA-Z][^A-Z]*', hashtag[1:])
        
        return list(set(found_words))
    
    def find_hashtags(self, tweet):
        matches = rgx_hashtag.finditer(tweet)

        hashtags = []
        for match in matches:
            hashtags.append(match.group(0))

        return hashtags

    def clean_tweet(self, text):
        """
        This method thakes a single tweet and removes everything that
        I considered unnecessary (this might change in future).
        """
        
        parsed_text = text
        # Links can be extracted or substituted with something that indicates found link.

        parsed_text = rgx_link.sub(' ', parsed_text)
        parsed_text = rgx_hashtag.sub(' ', parsed_text)
        parsed_text = rgx_mention.sub(' ', parsed_text)

        parsed_text = rgx_rt.sub(' ', parsed_text)

        parsed_text = rgx_punctuation.sub(' ', parsed_text)
        parsed_text = rgx_whitespace.sub(' ', parsed_text)
        #parsed_text = parsed_text.lower()

        return parsed_text

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