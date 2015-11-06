#!/usr/bin/python
import sqlite3
import datapop
import sys
import codecs
import re
import time

current_milli_time = lambda: int(round(time.time() * 1000))

outfilename = 'index.html'
interval = 3 * 60 * 60 * 1000
start_time = current_milli_time() - interval

sys.stdout = codecs.getwriter('utf8')(sys.stdout)

databasefile = 'links.db'
# Connect to local database
conn = sqlite3.connect(databasefile)
c = conn.cursor()
urls = []
query = 'SELECT url, count(url), sum(retweets), sum(favorites), sum(followers) FROM twitterlinks where timestamp_ms > ' + str(start_time)+ ' group by url ORDER BY count(url) desc limit 50'
print query
for row in c.execute(query):
        (url, count, retweets, favorites, followers) = row
        urls.append({'url': url, 'count': count, 'retweets': retweets, 'favorites': favorites, 'followers': followers})
conn.close()
content = []
for url in urls:
        title = datapop.fetch_title(url['url'])
        if title:
            print url['count'], url['retweets'], url['favorites'], url['followers'], "\t", title, url['url']
            title = re.sub('\|','',title)
            content.append(str(url['count']) + ' | ' + title + ' | ' + "<a href='" + url['url'] + "'>" + url['url'] + "</a>")

print "\n\nWriting to file..."
outfile = codecs.open(outfilename,'w',encoding='utf8')
outfile.write("<html><h2>What's Popular in the Data World</h2><br>\n")
outfile.write("<br>\n".join(content))
outfile.write("</html>")
