import request
import toolbelt

class alert(object):

	def __init__(self, **kwargs):
		#Sets up the arguments for the object
		self.args = self.arg_loader(kwargs)
		#gets the request object
		self.request_obj = request.nws(self.state, self.auto_load)


	def arg_loader(self, args):

		#Auto_load, decides if this object should load data from NWS servers on creation
		self.auto_load = (False) if not bool(args.get("auto_load")) else bool(args.get("auto_load"))
		
		#Determines the state
		self.state = ("us") if not bool(args.get("state")) else args.get("state") #default is "us"
		
		#The limit on how much of the result should be processed
		self.limit = (None) if not bool(args.get("limit")) else args.get("limit") #default is 20
		
		
	def set_limit(self, limit):
		request_obj.limit = limit

	def get(**kwargs):
		_def_ = {"cap":self.request_obj.get_cap,"summary":self.request_obj.get_summary}
		for x in xrange(0,kwargs.get(content)):
			try:
				content[x] = _def_[content[x]](self.limit)
			except:
				raise Exception(str(content[x])+ " is not a valid content option")
		return content


	def get_all(self,**kwargs):
		include_report = bool(kwargs.get("reports"))
		only_reports = bool(kwargs.get("only_reports"))

		return toolbelt.get_all(self.request_obj, include_report, only_reports)
