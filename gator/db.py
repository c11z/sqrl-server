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
    title = db.Column('Title', db.String(255), nullable=True)
    description = db.Column('Description', db.String(255), nullable=True)
    heroImageUrl = db.Column('HeroImageUrl', db.String(1024), nullable=True)
    excerpt = db.Column('Excerpt', db.Text, nullable=True)
    createdAt = db.Column('CreatedAt', db.DateTime, index=True)
    # user_id is twitter id for the user subscribing to the service
    userId = db.Column('UserId', db.BigInteger, index=True)
    tweets = db.relationship('Tweet', secondary=tweet_link_conn,
        backref=db.backref('links', lazy='dynamic'))

    def __init__(self, url, twitter_url, user_id, tweets):
        self.url = url
        self.twitterUrl = twitter_url
        self.userId = user_id
        self.createdAt = datetime.utcnow()
        self.tweets = tweets
        
    # def __repr__(self):
    #     return 'Link {0}:{1}'.format(self.url, self.user_id)

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
        self.profileImage_Url = profile_image_url
        self.text = text
        self.createdAt = parser.parse(created_at)
        # self.created_at = parser.parse(created_at, '%a %b %d %H:%M:%S %z %Y')

    # def __repr__(self):
    #     return 'Tweet {0}:{1}'.format(self.tweet_id, self.screen_name)
      
##### Serializers #####

class TweetSerializer(Serializer):
    tweetId = fields.Integer()
    tweetUserId = fields.Integer()
    screenName = fields.String()
    name = fields.String()
    profileImageUrl = fields.String()
    text = fields.String()
    createdAt = fields.DateTime()

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
    userId = fields.Integer()
    tweets = fields.Nested(TweetSerializer, many=True)








