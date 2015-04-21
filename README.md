# nws-alert V 0.0.1

A Python library for the National Weather Service Public Alerts.




# Documentation
---

Create an alert instance.

  `weather = alert()`

The Library current supports the following methods.
    
     weather.refresh()  #refreshs the page
     weather.get_cap()  #Gets collects all of the Cap feed, and returns a list of dictionaries that contain each of the cap feed elements.
     weather.get_summary()  #gets the summary. Returns a list of dictionaries 
     weather.get_title() #gets the titles.  Returns a list of dictionaries 
     weather.get_id() #Gets an alerts page. Returns a list of dictionaries 
     
     
