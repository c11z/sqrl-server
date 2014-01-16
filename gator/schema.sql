CREATE TABLE LinkBundle (
  ExpandedUrl TEXT NOT NULL,
  TwitterUrl TEXT NOT NULL,
  TwitterUserId INTEGER NOT NULL,
  CreatedAt DATETIME NOT NULL,
  ScreenName TEXT NULL,
  Name TEXT NULL,
  ProfileImageUrl TEXT NULL,
  TweetContent TEXT NULL,
  PRIMARY KEY (TwitterUrl, TwitterUserId)
);
CREATE INDEX CreatedAtIDX on LinkBundle(CreatedAt);