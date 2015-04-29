import urllib2

#Handles all fetching of data.

def get(url):
	response = urllib2.urlopen(url)
	return response.read()
