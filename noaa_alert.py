from bs4 import BeautifulSoup
import requests
import json



class alert:

	def __init__(self):

		self.limit = 5
		self.alert_raw = requests.get("http://alerts.weather.gov/cap/us.php?x=1").text
		self.soup = BeautifulSoup(self.alert_raw)
		self.entries = (self.soup.find_all("entry"))
		self.cap = ["event", "effective","expires","status","msgtype","category","urgency","severity","areadesc","polygon","geocode"] #All the cap elements
	
	def refresh(self):                #Refreshes the data

		self.alert_raw = requests.get("http://alerts.weather.gov/cap/us.php?x=1").text
		self.soup = BeautifulSoup(self.alert_raw)
		self.entries = (self.soup.find_all("entry"))

	def get_summary_raw(self,limit): #generator for summary 
		
		for x in self.entries:
			yield {"summary":x.summary.text}
			limit = limit - 1 if limit is not None else None 
			if type(limit) is int:
				if limit == 0:
					break

	def get_summary(self,limit=None):
		
		limit = self.limit if limit is None else limit
		return list(self.get_summary_raw(limit))

	def get_title(self):            #To be moved to a generator

		for x in self.entries:
			yield x.title.text

	def get_id(self):				#To be moved to a generator


		for x in self.entries:
			yield x.id.text

	def get_cap_raw(self,limit):    #Generator for cap content

		store = {}
		for x in self.entries:
			for y in self.cap:
				store = dict(store.items() + {y:x.find("cap:"+y).text}.items()) 
			yield([store])
			limit = limit - 1 if limit is not None else None 
			if type(limit) is int:
				if limit == 0:
					break

	def get_cap(self,limit=None):   #
		limit = self.limit if limit is None else limit
		lst = []
		for x in self.get_cap_raw(limit):
			lst = lst + list(x)
		return lst



