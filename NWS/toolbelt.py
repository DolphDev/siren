import request

def id2report(id_url):
	#takes an id and requests the report for it.
	return request.report(id_url)

