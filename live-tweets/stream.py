from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import tweepy
import twitter_credentials

from langdetect import detect

import json

# Searching Natural disaster by name.
# Need one of 2 things:
# 1. Stream tweets by specific keyword. #
# 2. Search tweets by specific keyword. # 180 requests per 15 minutes

class TwitterStreamer():

    def stream_tweets(self, output_filename, amount, keyword_list, tweet_mode):
        listener = TheListener(output_filename, amount)

        # Authentication
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)

        myStream = Stream(auth=auth,listener=listener,tweet_mode=tweet_mode)
        myStream.filter(track=keyword_list)

# Goal 1: Print tweets
class TheListener(StreamListener):

    def __init__(self, output_filename, amount):
        self.output_filename = output_filename
        self.amount = amount
        self.collected_data = []

    def on_data(self, data):
        response = self.process_data(data)

        return response

    def on_error(self, status):
        if status == 420:
            return False

        print(status)

    def process_data(self, data):
        json_data = json.loads(data)

        if len(self.collected_data) < self.amount:
            self.collected_data.append(json_data)
            print('Tweet added. Length: {}/{}'.format(len(self.collected_data), self.amount))
            return True
        else:
            self.save_collected_to_file()
            self.collected_data = []
            print('Collected data saved to file.')
            return False

    def save_collected_to_file(self):
        with open(self.output_filename, 'w') as f:
            f.write(json.dumps(self.collected_data))

if __name__ == '__main__':
    """
    Right now twitter_stream will keep grabbing tweets until it reaches 'amount',
    then it will save them to a file.
    """

    print('Script running...')

    desc = 'snow'
    amount = 100

    twitter_stream = TwitterStreamer()
    twitter_stream.stream_tweets(output_filename='{}-{}-tweets-test.json'.format(amount,desc),
                                 amount=amount,
                                 keyword_list=['snow'],
                                 tweet_mode="extended")
