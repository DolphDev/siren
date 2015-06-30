import urllib2

#Handles all fetching of data.

#Gets data, currently returns the CAP feed (XML from the alert.weather.gov server) 
def get(url):
    response = urllib2.urlopen(url)
    return response.read()

