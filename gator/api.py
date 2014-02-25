import logging
import subprocess
from gator import gator
import gator.secret as s
from gator.db import process_link, db, Link, Tweet, LinkSerializer
from flask import render_template, request, abort
from flask.ext.restful import Resource, Api
from twython import Twython, TwythonError


api = Api(gator)

@gator.route('/')
def index():
    return render_template('index.html')

class LinkBundle(Resource):
    def get(self):
        params = request.args
        # return str(params.get('startDate'))
        if not params.get('limit'):
            limit = 200
        if not params.get('startDate'):
            links = Link.query.order_by(Link.createdAt.desc()).limit(limit).all()
        else:    
            # links = Link.query.filter(Link.userId == s.USER_ID, Link.createdAt > params['startDate']).all()
            links = Link.query.filter(Link.userId == s.USER_ID, Link.createdAt > params['startDate']).order_by(Link.createdAt.desc()).all()
        logging.info('calling linkbundle')
        logging.info("{0}".format(links))
        serialized = LinkSerializer(links, many=True)
        # if not user_id or not date:
            # abort(404, message='Please include twitter id and date')
        return serialized.data

class GetPast(Resource):
    def get(self):
        tweets = Tweet.query.order_by(Tweet.tweetId.asc()).limit(1).all()
        oldest = tweets[0] if len(tweets) > 0 else None
        twitter = Twython(s.CONSUMER_KEY, s.CONSUMER_SECRET, 
                          s.ACCESS_TOKEN, s.ACCESS_TOKEN_SECRET)
        data = []
        try:
            if oldest:
                logging.info('\n\nOldest tweetId = {0}\n\n'.format(oldest.tweetId))
                data = twitter.get_home_timeline(count=50, max_id=oldest.tweetId)
            else:
                data = twitter.get_home_timeline(count=200)
        except TwythonError as e:
            logging.error('{0}'.format(e))
        else:
            logging.info(str(data))
            for tweet in data:
                if len(tweet.get('entities').get('urls')) > 0:
                    logging.info("\n\nFound urls!\n\n")
                    process_link(tweet, s.USER_ID)
                else:
                    logging.info("\n\nNo urls :(\n\n")

                
            return "OK"
        # finally:
        #     abort(404, message='Sorry the server blew up')

# class StartStream(Resource):
#     def get(self, user_id):
#         s = Secret()
#         logging.info('Calling Start Stream for UserId:{0}'.format(user_id))
#         subprocess.Popen(['python', 'streamer.py', '&'])
#         return True

# class StopStream(Resource):
#     def get(self):
#         logging.info('Calling Stop Stream')
#         pid = subprocess.call(["ps aux | awk '/[s]treamer.py/{print $2}'"], shell=True)
#         subprocess.call(['kill', pid], shell=True)
#         return str(pid)

# class CheckStream(Resource):
#     def get(self):
#         logging.info('Calling Check Stream')


##
## Actually setup the Api resource routing here
##
api.add_resource(LinkBundle, 
                 '/linkbundle/')
# operating stream is not really ready from the app yet
api.add_resource(GetPast, '/getpast')
# api.add_resource(StopStream, '/stream/stop/')
# api.add_resource(CheckStream, '/stream/check')
