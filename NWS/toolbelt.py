import request

def id2report(id_url):
	#takes an id and requests the report for it.
	if not id_url is str:
		raise ValueError("Argument must be str, Not dict or list")
	return request.report(id_url)

