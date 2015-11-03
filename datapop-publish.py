#!/usr/bin/python
import sqlite3
import datapop
import sys
import codecs
import re

sys.stdout = codecs.getwriter('utf8')(sys.stdout)

databasefile = 'links.db'
# Connect to local database
conn = sqlite3.connect(databasefile)
c = conn.cursor()
urls = []
for row in c.execute('SELECT url, count(url), sum(retweets), sum(favorites), sum(followers) FROM twitterlinks group by url ORDER BY count(url) desc limit 30'):
        (url, count, retweets, favorites, followers) = row
        urls.append({'url': url, 'count': count, 'retweets': retweets, 'favorites': favorites, 'followers': followers})
conn.close()
for url in urls:
        title = datapop.fetch_title(url['url'])
        if title:
            print url['count'], url['retweets'], url['favorites'], url['followers'], "\t", title, url['url']
