import request


def id2report(id_url,entryint=0):
	#takes an id and requests the report for it.
	if type(id_url) is list:
		return request.report(id_url[entryint]["id"])
	if type(id_url) is dict:
		return request.report(id_url["id"])
	return request.report(id_url)

def city2list(c):
	if type(c) is str:
		raise ValueError("Arugment was "+str(type(c)))
	return c.split("; ")

def pretty_time(t):
	pass

def get_all(nws,limit=100):

	def all_gen(nws,limit):
		_cap_ = nws.get_cap()
		_id_ = nws.get_id()
		_title_ = nws.get_title()
		_summary_ = nws.get_summary()

		for x in xrange(0,limit if len(_cap_) > limit else len(_cap_)):
			yield {"id":_id_[x]["id"],"title":_title_[x]["title"],"summary":_summary_[x]["summary"],"cap":_cap_[x]}

	return list(all_gen(nws,limit))


