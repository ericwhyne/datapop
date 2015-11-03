#!/usr/bin/python
import sqlite3
import datapop

databasefile = 'links.db'
# Connect to local database
conn = sqlite3.connect(databasefile)
c = conn.cursor()

for row in c.execute('SELECT count(url), url FROM twitterlinks group by url ORDER BY count(url) desc limit 3'):
        print row
        url = row[1]
        data = datapop.fetch_web_data(url)
        print "############################"
        print data['title']
