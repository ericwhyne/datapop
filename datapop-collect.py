#!/usr/bin/python
import yaml
import os
from birdy.twitter import StreamClient
import json
import sqlite3

databasefile = 'links.db'
# Connect to local database
conn = sqlite3.connect(databasefile)
c = conn.cursor()
# Create table
c.execute('''CREATE TABLE IF NOT EXISTS twitterlinks (timestamp_ms integer, followers integer, retweets integer, url text)''')
c.close()
conn.close()
conn = sqlite3.connect(databasefile)
c = conn.cursor()

# Connect to Twitter
tokens = yaml.safe_load(open(os.path.expanduser("~") + "/.twitterapi/datapop.yml"))
client = StreamClient(tokens['consumer_key'],tokens['consumer_secret'],tokens['access_token'],tokens['access_secret'])
resource = client.stream.statuses.filter.post(track='data science')

for data in resource.stream():
   print json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
   print "Followers:", data['user']['followers_count']
   print "Retweets:", data['retweet_count']
   print "Timestamp:", data['timestamp_ms']
   for url in data['entities']['urls']:
     c.execute("INSERT INTO twitterlinks VALUES (?,?,?,?)",
        (int(data['timestamp_ms']), int(data['user']['followers_count']), int(data['retweet_count']), url['expanded_url']))
     print "url:", url['expanded_url']
   conn.commit()
