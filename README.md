# nws-alert V 0.0.2

A Python library for the National Weather Service Public Alerts.




# Documentation
---

import the module

    import NWS

Create  NWS.request() instance.

    weather = NWS.request("us") #us is statecode. you can add a true-false to the argument to set if it should immedialetly request data on this instance (True = Get Data), False = Dont get data)

To get new alert date use .refresh()

    weather.refresh() #Will return True if successful. If not it will return False.

The Library current supports the following methods.
    

     weather.get_cap()  #Gets collects all of the Cap feed, and returns a list of dictionaries that contain each of the cap feed elements per entry.
     weather.get_summary() #gets the summary of an report. Returns a list of dictionaries 
     weather.get_title() #gets the titles.  Returns a list of dictionaries 
     weather.get_id() #Gets the id of an entry (the string of the id can be used for reports). Returns a list of dictionaries 
	
To get an report

     rep = NWS.toolbelt.id2report(weather.get_id()[0]["id"]) # 0 is the first entry, "id" is the key for the dict.
	
report currently supports the following

     rep.get_meta() #returns the meta information of the report (dict)
     rep.get_info() #returns the info about the report (dict)
     

     
