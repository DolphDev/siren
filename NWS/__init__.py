import request
import toolbelt


#Alert Object. Made to make using this module easier.
#Wraps around the module.
class alert(object):

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
		self.auto_load = (False) if not bool(args.get("auto_load")) else bool(args.get("auto_load"))
		
		#Determines the state
		self.state = ("us") if not bool(args.get("state")) else args.get("state") #default is "us"
		
		#Sets limit on how much of the result should be processed. Default is None
		self.limit = (None) if not bool(args.get("limit")) else args.get("limit") #default is 20

		#If this is zone/county id rather than a state, this must be set to true.
		self.loc = (False) if not bool(args.get("loc")) else True

	#requests the data for our object
	def load(self):
		#empty the cache system.
		self.cap = None 
		self.summary = None
		self.title = None
		self.id = None
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
		_def_ = {"cap":self.get_cap,"summary":self.get_summary,"title":self.get_title, "id":self.get_id()}
		content = kwargs.get("content")
		if not bool(content):
			raise Exception("No arguments supplied")
			
		for x in xrange(0,len(content)):
			try:
				content[x] = _def_[content[x]](self.limit)
			except:
				raise Exception(str(content[x])+ " is not a valid content option")
		return content

	#START REQUEST METHODS

	#Handles all limit handeling
	def decide_limit(self, limit):
		return limit if bool(limit) else self.limit

	#Get cap
	def get_cap(self,limit=None):
		limit = self.decide_limit(limit)
		if self.cap == None:
			self.cap = (self.request_obj.get_cap(limit),limit)
		elif type(self.cap) is tuple:
			if self.cap[1] != limit:
				self.cap = (self.request_obj.get_cap(limit),limit)
		return self.cap[0]

	#Get Summary
	def get_summary(self,limit=None):
		limit = self.decide_limit(limit)
		if self.summary == None:
			self.summary = (self.request_obj.get_summary(limit),limit)
		elif type(self.summary) is tuple:
			if self.summary[1] != limit:
				self.summary = (self.request_obj.get_summary(limit),limit)
		return self.summary[0]


	#Get Summary
	def get_title(self,limit=None):
		limit = self.decide_limit(limit)
		if self.title == None:
			self.title = (self.request_obj.get_title(limit),limit)
		elif type(self.title) is tuple:
			if self.title[1] != limit:
				self.title = (self.request_obj.get_title(limit),limit)
		return self.title[0]


	#
	def get_id(self,limit=None):
		if self.id == None:
			self.id = (self.request_obj.get_id(limit), limit) #Creates a 
		elif type(self.id) is tuple:
			if self.id[1] != limit:
				self.id = (self.request_obj.get_id(limit),limit)
		return self.id[0]

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
			return toolbelt.id2report(_id_)



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
