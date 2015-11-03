import goose
import urllib2
from goose import Goose
from bs4 import BeautifulSoup
import sys
import re

def fetch_web_data(url, headers = { 'User-Agent' : 'Magic Browser' }):
    '''
     Fetches data from a url. Prints message and returns False if failed.
     If successful returns dict data
     data['raw_html']
     data['content_type']
     data['page_links']
     data['title']
     data['cleaned_text']
    '''
    #print "Fetching web page: " + url
    data = {}
    try:
      req = urllib2.Request(url, None, headers)
      response = urllib2.urlopen(req)
      data['raw_html'] = unicode(response.read(), errors='replace')
      data['content_type'] = response.info().getheader('Content-Type')
      if 'text' not in data['content_type']:
        #print "Content type is not text, skipping." + data['content_type']
        return False
      soup = BeautifulSoup(data['raw_html'], "lxml")
      #print data['raw_html']
    except:
      #print "Failed to fetch page ", sys.exc_info()[0]
      return False
    #print "Extracting links..."
    data['page_links'] = []
    for link in soup.find_all('a'):
      data['page_links'].append(link.get('href'))
    #print "Extracting main text... "
    try:
      g = Goose()
      goose_data = g.extract(raw_html=data['raw_html'])
      #print "goose:", goose_data
      data['title'] = goose_data.title
      data['cleaned_text'] = goose_data.cleaned_text
    except:
      #print "Failed to extract text. ", sys.exc_info()[0]
      return False
    return data

def fetch_title(url, headers = { 'User-Agent' : 'Magic Browser' }):
    data = {}
    try:
      req = urllib2.Request(url, None, headers)
      response = urllib2.urlopen(req)
      data['raw_html'] = unicode(response.read(), errors='replace')
      data['content_type'] = response.info().getheader('Content-Type')
      if 'text' not in data['content_type']:
        #print "Content type is not text, skipping." + data['content_type']
        return False
      soup = BeautifulSoup(data['raw_html'], "lxml")
      data['title'] = re.sub('\n','', soup.title.string)
    except:
        return False
    return data['title']
