import request
import toolbelt

#This Object handles Cache
class cache(object):

	def __init__(self):
		
		self.data = None
		self.limit = None
		
	def set_dat(self, data, limit):

		self.data = data
		self.limit = limit

	def read(self, amount=None): 
		if bool(amount):
			return (self.data[:amount])
		else:
			return self.data

	def check(self, nLimit):
		#Returns True if cache needes to be updates, false if otherwise.
		if bool(self.limit) and bool(nLimit):
			return (nLimit <= self.limit)
		elif nLimit == nLimit and self.data != None:
			return True
		else: 
			return False

	def clean_out(self):
		#Needed for check()
		self.data = None
		self.limit = None


#Alert Object. Made to make using this module easier.
#Wraps around the module.
class siren(object):

	def __init__(self, **kwargs):

		#Sets up the arguments for the object
		self.arg_loader(kwargs)
		
		#Creates a request instance.
		self.request_obj = request.nws(self.state, self.auto_load, self.loc)

		# Match up this object's limit with out request instances limit
		self.set_limit(self.limit) 

		if self.auto_load:
			self.load()
		

	#Sets up the arguments for the object. Can be called independently.
	def arg_loader(self, args):

		#Auto_load, decides if this object should load data from NWS servers on creation
		self.auto_load = args.get("state", False)
		
		#Determines the state
		self.state = args.get("state", "us") #default is "us"
		
		#Sets limit on how much of the result should be processed. Default is None
		self.limit = args.get("limit", None) #default is 20

		#If this is zone/county id rather than a state, this must be set to true.
		self.loc = args.get("loc", False)

		#Cache System
		self.cap = cache()
		self.summary = cache()
		self.title = cache()
		self.id = cache()

	#requests the data for our object
	def load(self):
		#empty the cache system.
		self.cap.clean_out() 
		self.summary.clean_out()
		self.title.clean_out()
		self.id.clean_out()
		return self.request_obj.load()

	def parse(self,limit=None): #If called, it will parse the entire feed.
		limit = self.decide_limit(limit)
		self.get_cap(limit)
		self.get_summary(limit)
		self.get_title(limit)
		self.get_id(limit)
		return True

	#Changes area request info
	def change_area(self, **kwargs):
		area = kwargs.get("area")
		self.loc = bool(kwargs.get("is_loc"))
		onload = kwargs.get("onload")
		self.request_obj.change_state(loc)

	#Alllows you to set the limit
	def set_limit(self, limit):
		self.request_obj.limit = limit

	#GETS the request data.
	def get(self,**kwargs):
		#Dictionary for  valid content request
		_func_ = {"cap":self.get_cap,"summary":self.get_summary,"title":self.get_title, "id":self.get_id()}
		_limit_ = kwargs.get("limit")
		content = kwargs.get("content")
		if not bool(content):
			raise Exception("No arguments supplied")
			
		for x in xrange(0,len(content)):
			try:
				content[x] = _func_[content[x]](self.limit if not bool(_limit_) else _limit_)
			except:
				raise Exception(str(content[x])+ " is not a valid content option")
		return content

	#START REQUEST METHODS

	#Handles all limit handeling
	def decide_limit(self, limit):
		return limit if bool(limit) else self.limit
	
	def get_entries():
		return self.request_obj.entries

	def get_raw_xml():
		return self.request_obj.alert_raw
	#Get cap
	def get_cap(self,limit=None):
		limit = self.decide_limit(limit)
		if self.cap.check(limit):
			return self.cap.read(limit)
		else:
			self.cap.set_dat(self.request_obj.get_cap(limit),limit)
			return self.cap.read(limit)
		

	#Get Summary
	def get_summary(self,limit=None):
		limit = self.decide_limit(limit)
		if self.summary.check(limit):
			return self.summary.read(limit)
		else:
			self.summary.set_dat(self.request_obj.get_summary(limit),limit)
			return self.summary.read(limit)


	#Get Summary
	def get_title(self,limit=None):
		limit = self.decide_limit(limit)
		if self.title.check(limit):
			return self.title.read(limit)
		else:
			self.title.set_dat(self.request_obj.get_title(limit),limit)
			return self.title.read(limit)


	
	def get_id(self,limit=None):
		limit = self.decide_limit(limit)
		if self.id.check(limit):
			return self.id.read(limit)
		else:
			self.id.set_dat(self.request_obj.get_id(limit),limit)
			return self.id.read(limit)

	#END Request Methods

	#Parse reports.
	def get_report(self, **kwargs):
		raw_id = (kwargs.get("id"))
		limit = (self.decide_limit(kwargs.get("limit")))
		_id_ = raw_id if bool(raw_id) else self.request_obj.get_id(limit)
		_bulk_ = bool(kwargs.get("bulk"))
		if _bulk_:
			def gen_report(_id_):
				for x in (_id_ if type(_id_) is list else list(_id_)):
					yield toolbelt.id2report(x)
			return list(gen_report(_id_))
		else:
			return [toolbelt.id2report(_id_)]



	#gets all data. Can optionly include reports or only reports.
	def get_all(self,**kwargs):

		include_report = bool(kwargs.get("reports"))
		only_reports = bool(kwargs.get("only_reports"))
		limit = self.decide_limit(kwargs.get("limit"))
		return toolbelt.get_all(self, limit, include_report, only_reports)

	#Returns True if request returned back any warnings, False if not. (Only returns False Valid states with no current warnings, 404 errors will still raise an error)
	def warnings(self):
		try:
			return self.request_obj.has_warnings
		except:
			print("Warning: Server returned 404")
			return False		
 