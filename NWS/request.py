from bs4 import BeautifulSoup
import requests
import json

class report:							#Handles reports
	def __init__(self,id_url,gdata=True):

		self.id  = id_url
		self.meta = ["identifier","sender","sent","status","msgType","scope","note"]
		self.infolist = ["category","event","urgency","severity","certainty","effective","expires","senderName","headline","description","instruction"]
		if gdata:
			self.report_raw = requests.get(self.id).text
			self.soup = BeautifulSoup(self.report_raw)
			self.info = self.soup.alert.info

	def refresh(self):
		self.report_raw = requests.get(self.id).text
		self.soup = BeautifulSoup(self.report_raw)
		self.info = self.soup.info

	def get_meta(self):
		store = {}
		for y in self.meta:
			try:
				store = dict(store.items() + {y:self.soup.find(y).text}.items()) 
			except:
				store = dict(store.items() + {y:None}.items()) 
		return store

	def get_info(self):
		store = {}
		for y in self.infolist:
			try:
				store = dict(store.items() + {y:self.info.find(y).text}.items()) 
			except:
				store = dict(store.items() + {y:None}.items() )
		return store
		

class nws:

	def __init__(self,state="usa", gdata=True):

		self.limit = 5
		if gdata:
			self.alert_raw = requests.get("http://alerts.weather.gov/cap/us.php?x=1").text
			self.soup = BeautifulSoup(self.alert_raw)
			self.entries = (self.soup.find_all("entry"))
		self.cap = ["event", "effective","expires","status","msgtype","category","urgency","severity","areadesc","polygon","geocode"] #All the cap elements
	
	def refresh(self):                #Refreshes the data
		try:
			self.alert_raw = requests.get("http://alerts.weather.gov/cap/us.php?x=1").text
			self.soup = BeautifulSoup(self.alert_raw)
			self.entries = (self.soup.find_all("entry"))
			return True
		except:
			return False

	def load_entry(self, entry):	#Loads entries
		if not type(entry) is list:
			self.entries = [entry]
		else:
			self.entries = entry


	def get_summary_raw(self, limit): #generator for summary 
		
		for x in self.entries:
			yield {"summary":x.summary.text}
			limit = limit - 1 if limit is not None else None 
			if type(limit) is int:
				if limit == 0:
					break

	def get_summary(self, limit=None):
		
		limit = self.limit if limit is None else limit
		return list(self.get_summary_raw(limit))

	def get_title_raw(self, limit):            #To be moved to a generator

		for x in self.entries:
			yield {"title":x.title.text}
			if type(limit) is int:
				if limit == 0:
					break

	def get_title(self, limit=None):
		limit = self.limit if limit is None else limit
		return list(self.get_title_raw(limit))

	def get_id_raw(self, limit):				#To be moved to a generator
		for x in self.entries:
			yield {"id":x.id.text}
			limit = limit - 1 if limit is not None else None 
			if type(limit) is int:
				if limit == 0:
					break
	def get_id(self, limit=None):
		limit = self.limit if limit is None else limit
		return list(self.get_id_raw(limit))


	def get_cap_raw(self, limit):    #Generator for cap content

		store = {}
		for x in self.entries:
			for y in self.cap:
				store = dict(store.items() + {y:x.find("cap:"+y).text}.items()) 
			yield([store])
			limit = limit - 1 if limit is not None else None 
			if type(limit) is int:
				if limit == 0:
					break

	def get_cap(self, limit=None):   #
		limit = self.limit if limit is None else limit
		lst = []
		for x in self.get_cap_raw(limit):
			lst = lst + list(x)
		return lst





