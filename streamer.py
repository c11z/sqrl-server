import logging
import argparse

import gator.secret as s
import gator.db as db
from twython import TwythonStreamer



class LinkStreamer(TwythonStreamer):
    """docstring for LinkStreamer"""
    def __init__(self, user_id, app_key, app_secret, oauth_token, 
                 oauth_token_secret, timeout=300, retry_count=None, retry_in=10,
                 client_args=None, handlers=None, chunk_size=1):
        self.user_id = user_id
        super(LinkStreamer, self).__init__(app_key, app_secret, oauth_token, 
                                           oauth_token_secret, timeout=300, 
                                           retry_count=None, retry_in=10, 
                                           client_args=None, handlers=None, 
                                           chunk_size=1)

    def on_success(self, data):
        if data.get('id') and len(data.get('entities').get('urls')) > 0:
            try:
                db.process_link(data, self.user_id)

            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                logging.error("{0}, {1}, {2}".format(exc_type, exc_value, exc_traceback))

    # def on_error(self, status_code, data):
        # logging.error('Streaming Error Status Code: {0}'.format(status_code)
        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        # self.disconnect()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Script for streaming tweets into the database')
    parser.add_argument('user_id', action='store', type=int,
        help='Specify one store id so that things go quickly.')
    parser.add_argument('access_token', action='store', type=str)
    parser.add_argument('access_token_secret', action='store', type=str)
    parser.add_argument('consumer_key', action='store', type=str)
    parser.add_argument('consumer_secret', action='store', type=str)

    args = parser.parse_args([s.USER_ID, s.ACCESS_TOKEN, s.ACCESS_TOKEN_SECRET, 
                             s.CONSUMER_KEY, s.CONSUMER_SECRET])

    stream = LinkStreamer(args.user_id, args.consumer_key, args.consumer_secret,
                          args.access_token, args.access_token_secret)
    
    stream.user(_with='followings')
