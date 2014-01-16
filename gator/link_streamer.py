from twython import TwythonStreamer


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
    stream = LinkStreamer('18AOSvTnaIzUyNz1uneJLw', '6ekavRAtc2zdsKUfUPCO53me5vUl62gIBhDUjKpQ', '164865735-kTLKnFba74NGwHmlSWoVt1EA9jW7FpB1H0zranPC', 'l3xdqtTDgkHGT4qb2I8GXqHHXsxG9HzpChuD8KQAknAyN')
    stream.user(_with='followings')