import secret as s
from gator import gator
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from dateutil import parser
from marshmallow import Serializer, fields

gator.config['SQLALCHEMY_DATABASE_URI'] = s.DATABASE_URI
db = SQLAlchemy(gator)

tweet_link_conn = db.Table('TweetLinkConn',
                           db.Column('LinkId', db.BigInteger, db.ForeignKey('Link.LinkId')),
                           db.Column('TweetId', db.BigInteger, db.ForeignKey('Tweet.TweetId')))  

##### Models #####

class Link(db.Model):
    __tablename__ = 'Link'
    __table_args__ = (db.UniqueConstraint('Url', 'UserId'), {})
    linkId = db.Column('LinkId', db.BigInteger, primary_key=True, autoincrement=True)
    url = db.Column('Url', db.String(255), index=True)
    twitterUrl = db.Column('TwitterUrl', db.String(255))
    domain = db.Column('Domain', db.String(255), nullable=True)
    title = db.Column('Title', db.String(1024), nullable=True)
    description = db.Column('Description', db.String(1024), nullable=True)
    heroImageUrl = db.Column('HeroImageUrl', db.String(1024), nullable=True)
    excerpt = db.Column('Excerpt', db.Text, nullable=True)
    createdAt = db.Column('CreatedAt', db.DateTime, index=True)
    # user_id is twitter id for the user subscribing to the service
    userId = db.Column('UserId', db.BigInteger, index=True)
    tweets = db.relationship('Tweet', secondary=tweet_link_conn,
        backref=db.backref('links', lazy='dynamic'))

    def __init__(self, twitter_url, user_id, tweets):
        self.twitterUrl = twitter_url
        self.userId = user_id
        self.createdAt = datetime.utcnow()
        self.tweets = tweets


class Tweet(db.Model):
    __tablename__ = 'Tweet'
    tweetId = db.Column('TweetId', db.BigInteger, primary_key=True)
    # user information for the tweeting user
    tweetUserId = db.Column('TweetUserId', db.BigInteger)
    screenName = db.Column('ScreenName', db.String(64))
    name = db.Column('Name', db.String(64))
    profileImageUrl = db.Column('ProfileImageUrl', db.String(255))
    text = db.Column('Text', db.Text)
    # created date of the tweet
    createdAt = db.Column('CreatedAt', db.DateTime)

    def __init__(self, tweet_id, tweet_user_id, screen_name, name, 
                 profile_image_url, text, created_at):
        self.tweetId = tweet_id
        self.tweetUserId = tweet_user_id
        self.screenName = screen_name
        self.name = name
        self.profileImageUrl = profile_image_url
        self.text = text
        self.createdAt = parser.parse(created_at)
      
##### Serializers #####

class TweetSerializer(Serializer):
    tweetId = fields.Integer()
    tweetUserId = fields.Integer()
    screenName = fields.String()
    name = fields.String()
    profileImageUrl = fields.String()
    text = fields.String()

class LinkSerializer(Serializer):
    linkId = fields.Integer()
    url = fields.String()
    twitterUrl = fields.String()
    domain = fields.String()
    title = fields.String()
    description = fields.String()
    heroImageUrl = fields.String()
    excerpt = fields.String()
    createdAt = fields.DateTime()
    tweets = fields.Nested(TweetSerializer, many=True)








