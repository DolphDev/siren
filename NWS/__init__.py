import request
import toolbelt


#Alert Object. Made to make using this module easier.
#Wraps around the module.
class alert(object):

	def __init__(self, **kwargs):
		#Sets up the arguments for the object
		self.args = self.arg_loader(kwargs)
		#gets the request object
		self.request_obj = request.nws(self.state, self.auto_load)
		self.set_limit(self.limit)
		#

	#Sets up the arguments for the object. Can be called independently.
	def arg_loader(self, args):

		#Auto_load, decides if this object should load data from NWS servers on creation
		self.auto_load = (False) if not bool(args.get("auto_load")) else bool(args.get("auto_load"))
		
		#Determines the state
		self.state = ("us") if not bool(args.get("state")) else args.get("state") #default is "us"
		
		#The limit on how much of the result should be processed
		self.limit = (None) if not bool(args.get("limit")) else args.get("limit") #default is 20

	
	def load(self):
		#Loads our request object
		return self.request_obj.load()
		
	def set_limit(self, limit):
		self.request_obj.limit = limit


	#GETS the request data.
	def get(self,**kwargs):
		_def_ = {"cap":self.get_cap,"summary":self.get_summary,"title":self.get_title, "id":self.get_id()}
		content = kwargs.get("content")
		print content
		for x in xrange(0,len(content)):
			try:
				print x
				content[x] = _def_[content[x]](self.limit)
			except:
				raise Exception(str(content[x])+ " is not a valid content option")
		return content



	#START REQUEST METHODS

	#Determine limit
	def decide_limit(self, limit):
		return limit if bool(limit) else self.limit

	#Get cap
	def get_cap(self,limit=None):
		limit = self.decide_limit(limit)
		return self.request_obj.get_cap(limit)

	def get_summary(self,limit=None):
		limit = self.decide_limit(limit)
		return self.request_obj.get_summary(limit)

	def get_title(self,limit=None):
		limit = self.decide_limit(limit)
		return self.request_obj.get_title(limit)

	def get_id(self,limit=None):
		limit = self.decide_limit(limit)
		return self.request_obj.get_id(limit)

	#END Request Methods

	def get_report(self, **kwargs):
		raw_id = (kwargs.get("id"))
		_id_ = raw_id if bool(raw_id) else self.request_obj.get_id(1)
		_bulk_ = bool(kwargs.get("bulk"))
		if _bulk_:
			def gen_report(_id_):
				for x in (_id_ if type(_id_) is list else list(_id_)):
					yield id2report(x)
			return list(gen_report(_id_))
		else:
			return toolbelt.id2report(_id_)



	#gets all. .Can optionly include reports or only reports.
	def get_all(self,**kwargs):
		include_report = bool(kwargs.get("reports"))
		only_reports = bool(kwargs.get("only_reports"))

		return toolbelt.get_all(self.request_obj, include_report, only_reports)
