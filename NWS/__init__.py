import request
import toolbelt


#Alert Object. Made to make using this module easier.
#Wraps around the module.
class alert(object):

	def __init__(self, **kwargs):
		#Sets up the arguments for the object
		self.args = self.arg_loader(kwargs)
		
		#Creates a request instance with our arguments supplied
		self.request_obj = request.nws(self.state, self.auto_load, self.loc)

		# Match up this object's limit with out request instances limit
		self.set_limit(self.limit) 

		if self.auto_load:
			self.load()

		#

	#Sets up the arguments for the object. Can be called independently.
	def arg_loader(self, args):

		#Auto_load, decides if this object should load data from NWS servers on creation
		self.auto_load = (False) if not bool(args.get("auto_load")) else bool(args.get("auto_load"))
		
		#Determines the state
		self.state = ("us") if not bool(args.get("state")) else args.get("state") #default is "us"
		
		#The limit on how much of the result should be processed
		self.limit = (None) if not bool(args.get("limit")) else args.get("limit") #default is 20

		#If the area supplied is not a state, rather area code, this is set to True.
		self.loc = (False) if not bool(args.get("loc")) else True

	#Tells our object to get the data.
	def load(self):
		return self.request_obj.load()

	#Changes area
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
		_def_ = {"cap":self.get_cap,"summary":self.get_summary,"title":self.get_title, "id":self.get_id()}
		content = kwargs.get("content")
		if not bool(content):
			raise Exception("No arguments supplied")
		for x in xrange(0,len(content)):
			try:
				print x
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
		return self.request_obj.get_cap(limit)

	#Get Summary
	def get_summary(self,limit=None):
		limit = self.decide_limit(limit)
		return self.request_obj.get_summary(limit)

	#Get Summary
	def get_title(self,limit=None):
		limit = self.decide_limit(limit)
		return self.request_obj.get_title(limit)

	#Get Id
	def get_id(self,limit=None):
		limit = self.decide_limit(limit)
		return self.request_obj.get_id(limit)

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



	#gets all. .Can optionly include reports or only reports.
	def get_all(self,**kwargs):

		include_report = bool(kwargs.get("reports"))
		only_reports = bool(kwargs.get("only_reports"))
		limit = self.decide_limit(kwargs.get("limit"))
		return toolbelt.get_all(self.request_obj, limit, include_report, only_reports)

	#Returns true if request returned back any warnings, false if not. (Only returns False Valid states with no current warnings, 404 errors will still raise an error)
	def warnings(self):
		return self.request_obj.has_warnings
		