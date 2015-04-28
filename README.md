# nws-alert V 0.0.3.08

A Python library for the National Weather Service Public Alerts. 




# Documentation
---

import the module

    import NWS

Create `NWS.request.nws()` instance.

    weather = NWS.request.nws("us") #us is statecode. you can add a true-false to the argument to set if it should immedialetly request data on this instance (True = Get Data), False = Dont get data)

To actually get the data use `weather.load()`

    weather.load() #Will return True if successful. If not it will return False.

The Library current supports the following methods.
    

     weather.get_cap()  #collects all of the data from the cap feed, and returns a list of dictionaries that contain each of the cap feed elements per entry.
     weather.get_summary() #gets the summary of an report. Returns a list of dictionaries 
     weather.get_title() #gets the titles.  Returns a list of dictionaries 
     weather.get_id() #Gets the id of an entry (the string of the id can be used for reports). Returns a list of dictionaries 
     NWS.toolbelt.get_all(weather) #returns a merged version of the above methods. Toolbelt, see below for details
	
To get a report. 

     rep = NWS.toolbelt.id2report(weather.get_id()[0]["id"]) # 0 is the first entry, "id" is the key for the dict. Uses toolbelt (see below)
report currently supports the following

     rep.load() #Gets the data. must be called before the below are used.
     rep.get_meta() #returns the meta information of the report (dict)
     rep.get_info() #returns the info about the report (dict)

You can also create a report instance by calling NWS.request.report(_id_) but its not recommended due to possible future modifications

### Toolbelt

This library includes some extra tools for handeling data. For various reasons that are not listed, it is faster (or more reasonable) to include a toolset rather than actually having the library itself extensively handling the data. The toolbelt includes functions that would be useful in the usage of this library.

Current uses of the toolbelt.
     
     NWS.toolbelt.id2report(_id_) # _id_ is the url of the page (string). Alternatively It accepts a dict with the "id" key in it. 
     #It also accepts list with the said dict in it, 
     #but you must specify which entry to use (defualt is the first). 
     #Returns a NWS.request.report() instance of the _id_

     NWS.toolbelt.city2list(city) # where city is a str. get_cap() will give you the string of affected areas, this just makes them into a list.

     NWS.toolbelt.get_all(request) # request is a NWS.request.nws() instance. Merges NWS.request.nws() instance methods.
