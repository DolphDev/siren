import request


def id2report(id_url,entryint=0):
	#takes an id and requests the report for it.\
	entryint = entryint if bool(entryint) else 0
	if type(id_url) is list:
		_id_ = (id_url[entryint]["id"])
	elif type(id_url) is dict:
		_id_ =  (id_url["id"])
	elif type(id_url) is unicode or type(id_url) is str:
		_id_ = id_url
	else: 
		raise ValueError("id2report() only accepts str, list, and dict")
	return request.report(_id_.replace("http://","https://"))

def city2list(c):
	if not type(c) is str:
		raise ValueError("Argument was "+str(type(c))+" , instead of str")
	return c.split("; ")

def pretty_time(t): 
	if not type(t) is str:
		raise ValueError("Argument was "+str(type(t))+" instead of str")
	time = t.split("T")
	return {"date":time[0],"time":""}

def get_all(nws, limit=5, greport=False, only_report=False):

	def all_gen(nws,limit=None):
		limit = nws.limit if limit == None else limit+1
		_cap_ = nws.get_cap()
		_id_ = nws.get_id()
		_title_ = nws.get_title()
		_summary_ = nws.get_summary()
		if greport and not only_report:
			for x in xrange(0,limit if len(_cap_) > limit else len(_cap_)):
				report = id2report(_id_,x)
				report.load()
				yield {"report":{"meta":report.get_meta(),"info":report.get_info()}, "id":_id_[x]["id"],"title":_title_[x]["title"],"summary":_summary_[x]["summary"],"cap":_cap_[x]}
		elif greport and only_report:
				for x in xrange(0,limit if len(_cap_) > limit else len(_cap_)):
					report = id2report(_id_,x)
					report.load()
				yield {"report":{"meta":report.get_meta(),"info":report.get_info()}, "id":_id_[x]["id"]}
		else:
			for x in xrange(0,limit if len(_cap_) > limit else len(_cap_)):
				yield {"id":_id_[x]["id"],"title":_title_[x]["title"],"summary":_summary_[x]["summary"],"cap":_cap_[x]}

	return list(all_gen(nws, limit))


