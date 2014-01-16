from gator import gator
from flask import render_template
from flask.ext.restful import Resource, Api
from secret import Secret

api = Api(gator)

@gator.route('/')
def index():
    return render_template('index.html')

s = Secret()

link_bundle_list = [
{
    'expandedUrl': 'http://google.com',
    'twitterUrl': 'http://t.co/KJHSKDJHF',
    'twitterUserId': 131886354,
    'createdAt': '2014-12-00 12:00:00',
    'screenName': 'corydominguez',
    'name': 'Cory Dominguez',
    'profileImageUrl': 'http://a0.twimg.com/profile_images/2284174872/7df3h38zabcvjylnyfe3_normal.png',
    'tweetContent': 'This is a tweet',
},
{
    'expandedUrl': 'http://google.com',
    'twitterUrl': 'http://t.co/KJHSKDJHF',
    'twitterUserId': 131886354,
    'createdAt': '2014-12-00 12:00:00',
    'screenName': 'corydominguez',
    'name': 'Cory Dominguez',
    'profileImageUrl': 'http://a0.twimg.com/profile_images/2284174872/7df3h38zabcvjylnyfe3_normal.png',
    'tweetContent': 'This is a tweet',  
},
{
    'expandedUrl': 'http://google.com',
    'twitterUrl': 'http://t.co/KJHSKDJHF',
    'twitterUserId': 131886354,
    'createdAt': '2014-12-00 12:00:00',
    'screenName': 'corydominguez',
    'name': 'Cory Dominguez',
    'profileImageUrl': 'http://a0.twimg.com/profile_images/2284174872/7df3h38zabcvjylnyfe3_normal.png',
    'tweetContent': 'This is a tweet',
}]     

class LinkBundle(Resource):
    def get(self, twitter_user_id, date):
        if not twitter_user_id or not date:
            abort(404, message='Please include twitter id and date')
        return link_bundle_list


def startStream():
    stream = LinkStreamer(s.CONSUMER_KEY, s.CONSUMER_SECRET, 
                          s.ACCESS_TOKEN, s.ACCESS_TOKEN_SECRET)
    stream.user(_with='followings')


##
## Actually setup the Api resource routing here
##
api.add_resource(LinkBundle, 
                 '/linkbundle/<int:twitter_user_id>/<string:date>')
