from twython import TwythonStreamer
<<<<<<< HEAD
from secret import Secret

=======
<<<<<<< HEAD
from secret import Secret
=======

>>>>>>> 25b37ba4c19bca5167263629a7d9f91da61ee91e
>>>>>>> 1f0a16a9b02b9c429b5e0ae27cebfea2d67b4653

class LinkStreamer(TwythonStreamer):
    """docstring for LinkStreamer"""
    def on_success(self, data):
        if 'text' in data:
            print data['text'].encode('utf-8')
            for k,v in data.items():
                print k, data[k]

    def on_error(self, status_code, data):
        print status_code

        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        # self.disconnect()

if __name__ == '__main__':
    s = Secret()
    stream = LinkStreamer(s.CONSUMER_KEY, s.CONSUMER_SECRET, 
                          s.ACCESS_TOKEN, s.ACCESS_TOKEN_SECRET)
    stream.user(_with='followings')