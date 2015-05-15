import urllib2

#Handles all fetching of data.

#Gets data, currently returns the CAP (Basically XML from the server)

def get(url):
	response = urllib2.urlopen(url)
	return response.read()
