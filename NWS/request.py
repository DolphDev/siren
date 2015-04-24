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

	def url_formatter(self):
		return ("http://alerts.weather.gov/cap/%s.php?x=0" % (self.state))

	def __init__(self,state="us", gdata=True):
		self.state = state
		self.limit = 5
		if gdata:
			self.alert_raw = requests.get(self.url_formatter()).text
			self.soup = BeautifulSoup(self.alert_raw)
			self.entries = (self.soup.find_all("entry"))
			self.updated = self.soup.find("updated")
		self.cap = ["event", "effective","expires","status","msgtype","category","urgency","severity","areadesc","polygon","geocode"] #All the cap elements
	
	def refresh(self):                #Refreshes the data
		try:
			self.alert_raw = requests.get(self.url_formatter()).text
			self.soup = BeautifulSoup(self.alert_raw)
			self.entries = (self.soup.find_all("entry"))
			self.update = self.soup.find("updated").text
			return True
		except:
			return False

	def change_state(self,state):
		self.state = state

	def load_entry(self, entry):	#Loads entries
		if not type(entry) is list:
			self.entries = [entry]
		else:
			self.entries = entry

	def get_summary(self, limit=None):
		
		def summary_gen(limit): #generator for summary 
		
			for x in self.entries:
				yield {"summary":x.summary.text}
				limit = limit - 1 if limit is not None else None 
				if type(limit) is int:
					if limit == 0:
						break

		limit = self.limit if limit is None else limit
		return list(self.summary_gen(limit))


	def get_title(self, limit=None):

		def title_gen(limit):            #To be moved to a generator

			for x in self.entries:
				yield {"title":x.title.text}
				if type(limit) is int:
					if limit == 0:
						break

		limit = self.limit if limit is None else limit
		return list(title_gen(limit))

	def get_id(self, limit=None):

		def id_gen(limit):				#id generator
			for x in self.entries:
				yield {"id":x.id.text}
				limit = limit - 1 if limit is not None else None 
				if type(limit) is int:
					if limit == 0:
						break
			limit = self.limit if limit is None else limit

		return list(id_gen(limit))


	def get_cap(self, limit=None):   #

		def cap_gen(limit):    #Generator for cap content

			store = {}
			for x in self.entries:
				for y in self.cap:
					store = dict(store.items() + {y:x.find("cap:"+y).text}.items()) 
				yield([store])
				limit = limit - 1 if limit is not None else None 
				if type(limit) is int:
					if limit == 0:
						break

		limit = self.limit if limit is None else limit
		lst = []
		for x in cap_gen(limit):
			lst = lst + list(x)
		return lst





