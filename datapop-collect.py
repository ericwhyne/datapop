#!/usr/bin/python
import yaml
import os
from birdy.twitter import StreamClient
import json
import sqlite3
import sys
from time import strftime

databasefile = 'links.db'
keywordsfile = 'keywords.txt'
tweetlogfile = 'tweets-' + strftime("%Y-%m-%d") + '.log'

try:
    tweetlog = open(tweetlogfile, "a")
except:
    print "Unable to open tweet log file."
    sys.exit()

with open(keywordsfile) as f:
    keywords = f.read().splitlines()

keywords_string = ','.join(set(keywords))

print "Tracking tweets with these keywords:", keywords_string

# Connect to local database
conn = sqlite3.connect(databasefile, timeout=100)
c = conn.cursor()
# Create table
c.execute('''CREATE TABLE IF NOT EXISTS twitterlinks (timestamp_ms integer, followers integer, retweets integer, favorites integer, tweetid text, url text)''')
c.execute('PRAGMA journal_mode=wal') # with write ahead log, reads don't lock
c.close()
conn.close()
conn = sqlite3.connect(databasefile)
c = conn.cursor()

# Connect to Twitter
tokens = yaml.safe_load(open(os.path.expanduser("~") + "/.twitterapi/datapop.yml"))
client = StreamClient(tokens['consumer_key'],tokens['consumer_secret'],tokens['access_token'],tokens['access_secret'])
resource = client.stream.statuses.filter.post(track=keywords_string)

for data in resource.stream():
   tweetlog.write(json.dumps(data) + '\n')
   print json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
   for url in data['entities']['urls']:
     c.execute("INSERT INTO twitterlinks VALUES (?,?,?,?,?,?)",
        (int(data['timestamp_ms']), int(data['user']['followers_count']), int(data['retweet_count']), int(data['favorite_count']), data['id_str'], url['expanded_url']))
   conn.commit()
