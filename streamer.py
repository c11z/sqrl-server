import logging
import argparse
import requests
import gator.secret as s
from gator.db import db, Link, Tweet
from twython import TwythonStreamer
from BeautifulSoup import BeautifulSoup
from datetime import datetime

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
        if data.get('id') is not None:
            logging.info('Tweet Id: {0}'.format(data.get('id_str')))
            if len(data.get('entities').get('urls')) > 0:
                user = data.get('user')
                tweet = Tweet(data['id'], user['id'], user['screen_name'],
                              user['name'], user['profile_image_url'],
                              data['text'], data['created_at'])
                logging.info('{0}'.format(tweet))
                for l in data['entities']['urls']:
                    url = l['expanded_url']
                    link = Link.query.filter_by(userId=self.user_id, url=url).first()
                    if link and (tweet not in link.tweets):
                        link.tweets.append(tweet)
                        link.createdAt = datetime.utcnow()
                        db.session.add(link)
                    else:
                        link = self.getPageInfo(url, l['url'], self.user_id, [tweet])
                        # if title ends up being None then the Link has failed
                        if link:
                            db.session.add(link)
                try:
                    db.session.commit()
                except IntegrityError:
                    db.session.rollback()
                    logger.error('IntegrityError {0}'.format(link))
            

    # def on_error(self, status_code, data):
        # logging.error('Streaming Error Status Code: {0}'.format(status_code)
        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        # self.disconnect()
    def getPageInfo(self, url, tweet_url, user_id, tweets):
        link = Link(tweet_url, user_id, tweets)
        resp = None
        try:
            resp = requests.get(url)
            if resp.url:
                url = resp.url
            link.url = url
            link.domain = url.split('/')[2]
        except requests.exceptions.ConnectionError:
            logging.error('ConnectionError for url {0}'.format(url))
        if resp and resp.status_code < 400:
            headers = resp.headers
            if not headers:
                headers = {'content-type': ''}          
            if 'text/html' in headers.get('content-type'):     
                soup = BeautifulSoup(resp.text, convertEntities=BeautifulSoup.HTML_ENTITIES)
                t = soup.find('title')
                if t is not None:
                    link.title = ' '.join(t.renderContents().split())
                d = soup.find('meta', {'name':'description'})
                if d is not None:
                    link.description = ' '.join(d.get('content').split())
            elif headers.get('content-type') == 'application/pdf':
                link.title = url
            elif 'image' in headers.get('content-type'):
                link.title = url
                link.description = ''
                link.heroImageUrl = url
            if not link.title and link.description:
                link.title = description
                link.description = ''
            elif not link.title and not link.description:
                link.title = url
                link.description = ''
        else:
            link = None

        return link



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
