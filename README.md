gator-server
============

Simple python rest server that gets tweets from the twitter api, extracts, dedups and harvests information to bundle up and serve to the gator-android client.

### Deploying this server

1) Create a logs directory in the main app directory

2) Create a secret.py file with the following constants specified:

```python
USER_ID = '164865735'
DATABASE_URI = 'mysql://root:@localhost:3306/gator'
CONSUMER_KEY = 'XXX'
CONSUMER_SECRET = 'XXX'
ACCESS_TOKEN = 'XXX'
ACCESS_TOKEN_SECRET = 'XXX'
```

3) Install mysql and setup database with uri as in secret.py

```
yum install mysql
mysqld
```

4)