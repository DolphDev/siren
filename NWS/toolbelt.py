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

