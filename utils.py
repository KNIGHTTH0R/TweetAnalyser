import re
from nltk import FreqDist

# REGEX
rgx_link = re.compile(r'https?://[\w\d.-/]+')
rgx_punctuation = re.compile(r'[^\w\d\s#]')
rgx_whitespace = re.compile(r'\s+')

rgx_hashtag = re.compile(r'\B#\w*[a-zA-Z]+\w*')
rgx_mention = re.compile(r'\B@\w*[a-zA-Z]+\w*')
rgx_rt = re.compile(r'RT\s')

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

def collocates(sentences_list, target_word, top_n):
    """
    This function performs a frequency distribution of the words
    appearing to the left and to the right of the target_word.
    """
    target_word = target_word.lower()
    num_left_right = 1

    words_on_left = []
    words_on_right = []

    for sentence in sentences_list:
        parsed_sentence = rgx_punctuation.sub(' ', sentence)
        parsed_sentence = rgx_whitespace.sub(' ', parsed_sentence)

        tweet_tokens = parsed_sentence.lower().split(' ')
        max_index = len(tweet_tokens) - 1

        for index,token in enumerate(tweet_tokens):
            if token and token == target_word:
                center_word_index = index
                
                left_index = center_word_index - num_left_right
                right_index = center_word_index + num_left_right

                if not (left_index < 0):
                    left_word = tweet_tokens[left_index]
                    words_on_left.append(left_word)

                if not (right_index > max_index):
                    right_word = tweet_tokens[right_index]
                    words_on_right.append(right_word)

    left_freqdist = FreqDist(words_on_left)
    right_freqdist = FreqDist(words_on_right)

    #left_freqdist_sorted = [key for (key,val) in left_freqdist.most_common(top_n)]
    #right_freqdist_sorted = [key for (key,val) in right_freqdist.most_common(top_n)]

    return { 'left': left_freqdist.most_common(top_n), 'right': right_freqdist.most_common(top_n) }