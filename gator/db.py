import logging
import requests
import sys
from HTMLParser import HTMLParser
from datetime import datetime
from dateutil import parser
from BeautifulSoup import BeautifulSoup

from gator import gator
import secret as s
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import exc
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

    def __init__(self):
        self.createdAt = datetime.utcnow()


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


def process_link(data, user_id):
    user = data.get('user')
    tweet = Tweet(data['id'], user['id'], user['screen_name'],
                  user['name'], user['profile_image_url'],
                  data['text'], data['created_at'])
    logging.info('Tweet Id: {0} -> {1}'.format(data.get('id_str'), tweet))

    for l in data['entities']['urls']:
        url = l['expanded_url']
        link = Link.query.filter_by(userId=user_id, url=url).first()
        if link: 
            logging.info('\nFound existing link: {0}\n'.format(link.linkId))
            if tweet not in link.tweets:
                link.tweets.append(tweet)
                link.createdAt = datetime.utcnow()
        else:
            logging.info('\nMaking new Link {0}\n'.format(url))
            link = Link()
            try:
                resp = requests.get(url)
                if resp.status_code >= 400:
                    raise requests.exceptions.ConnectionError
                link.url = resp.url if resp.url else url
                link.domain = '.'.join(link.url.split('/')[2].split('.')[-2:])                    
            except requests.exceptions.ConnectionError:
                logging.error('\nConnectionError for url {0}\n'.format(url))
            else:
                link.twitterUrl = l['url']
                link.userId = user_id
                link.tweets = [tweet]
                headers = resp.headers if resp.headers else {'content-type': ''}       
                if 'text/html' in headers.get('content-type'):     
                    soup = BeautifulSoup(resp.text, convertEntities=BeautifulSoup.HTML_ENTITIES)
                    t = soup.find('title')
                    link.title = parse_html(t.text) if t else None
                    # logging.info('Yeah found a title: {0}'.format(link.title))
                    d = soup.find('meta', {'name':'description'})
                    link.description = parse_html(d.get('content')) if d else None
                    # logging.info('Yeah found a Description: {0}'.format(link.description))
                elif headers.get('content-type') == 'application/pdf':
                    link.title = url
                elif 'image' in headers.get('content-type'):
                    link.title = link.url
                    link.description = ''
                    link.heroImageUrl = url
                if not link.title and link.description:
                    link.title = link.description
                    link.description = None
                elif not link.title and not link.description:
                    link.title = url
                    link.description = None           
        if link:
            logging.info('Successfull link -> {0}'.format(tweet))
            db.session.add(link)
            try:
                db.session.commit()
            except exc.SQLAlchemyError:
                db.session.rollback()
                logging.error('SQLAlchemyError {0}'.format(data))


def parse_html(tag):
    h = HTMLParser()
    return h.unescape(' '.join(tag.split()))

