import os

from flask import Flask, url_for

gator = Flask(__name__)

# Determines the destination of the build. Only usefull if you're using Frozen-Flask
gator.config['FREEZER_DESTINATION'] = os.path.dirname(os.path.abspath(__file__))+'/../build'

# Function to easily find your assets
# In your template use <link rel=stylesheet href="{{ static('filename') }}">
gator.jinja_env.globals['static'] = (
    lambda filename: url_for('static', filename = filename)
)
import logging
logging.basicConfig(filename='/var/www/html/gator-server/logs/api.log',level=logging.DEBUG)
# logging.basicConfig(filename='logs/api.log',level=logging.DEBUG)
logging.info("Starting up Server!")
from gator import api
from gator import db
from gator import secret
