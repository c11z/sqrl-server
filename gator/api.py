import logging
import subprocess
from gator import gator
from gator.db import db, Link, Tweet, LinkSerializer
from flask import render_template, abort
from flask.ext.restful import Resource, Api
import json

api = Api(gator)

@gator.route('/')
def index():
    return render_template('index.html')

class LinkBundle(Resource):
    def get(self, user_id, date):
        logging.info('calling linkbundle')
        links = Link.query.filter(Link.userId == user_id, Link.createdAt > date).all()
        logging.info("{0}".format(links))
        serialized = LinkSerializer(links, many=True)
        # if not user_id or not date:
            # abort(404, message='Please include twitter id and date')
        return serialized.data

class StartStream(Resource):
    def get(self, user_id):
        s = Secret()
        logging.info('Calling Start Stream for UserId:{0}'.format(user_id))
        subprocess.Popen(['python', 'streamer.py', '&'])
        return True

class StopStream(Resource):
    def get(self):
        logging.info('Calling Stop Stream')
        pid = subprocess.call(["ps aux | awk '/[s]treamer.py/{print $2}'"], shell=True)
        subprocess.call(['kill', pid], shell=True)
        return str(pid)

class CheckStream(Resource):
    def get(self):
        logging.info('Calling Check Stream')


##
## Actually setup the Api resource routing here
##
api.add_resource(LinkBundle, 
                 '/linkbundle/<int:user_id>/<string:date>')
# operating stream is not really ready from the app yet
# api.add_resource(StartStream, '/stream/start/<int:user_id>')
# api.add_resource(StopStream, '/stream/stop/')
# api.add_resource(CheckStream, '/stream/check')
