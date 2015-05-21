import urllib2

#Handles all fetching of data.

#Gets data, currently returns the CAP feed (Basically XML from the alert.)

def get(url):
	response = urllib2.urlopen(url)
	return response.read()
