# nws-alert V 0.0.4.77

A Python library for the National Weather Service Public Alerts. 




# Documentation
---

import the module

    import NWS

(NWS is the Devolpment name of this module)   



# Alert Object

This module includes the object `NWS.alert()`. The Object wraps the entire module for easy and more consistant use. The Alert object includes most (and soon to be all_ of the modules uses. The only real reason you wouldnt want to use is if you want somewhat unparsed data or you need data in way that this object doesn't provide very well.

To the create the object

    alert = NWS.alert()

This also accepts keyword arguments for more advanced customization. 

* `state` - Default is `"us"` (Which is the entire country). Accepts either state abbreviations or county/zone code.
* `loc` - Default is `False`. Must be `True` if `state` is a country/zone code. Leave `False` if your using a state abbreviation.
* `auto_load` - Default is `False`. If set to `True` the Object will load the data on its creation.
* `limit` - Default is None. Sets a universal limit for the object. It will be used if you call a method without specifiying a limit.

## Methods

###Getting data

You most use `alert.load()` if you did not set `auto_load` to `True` when creating the object.

`alert.load()` loads the data. Returns `True` if successful and `False`

### Checking data

Sometimes the data will contain no alerts. The module includes one function to help with this

`alert.warnings` - Returns ``True`` if request was successful. ``False`` if not

### Parsing data.

#### get()

'alert.get()' - accepts the keyword argument `content` with an list of valid requests in it. for example, if you want `get_cap()`, `get_title()`, `get_id()`, and `get_summary()` in that exact order, simply make this call.

    alert.get(content=["cap","title","id","summary"])

It returns an list with the specified data where you want it (I.E `"cap"` is replaced with the result of `get_cap()`)

Note: this does not support reports.

#### get_title()

`alert.get_title(5)` - accepts 1 argument, an Integer representing a limit how on much of the data you want to parse. 

Example 

`alert.get_title(5)` -  the title of the warning



#### get_id()

`alert.get_id()` - accepts 1 argument, an Integer representing a limit how on much of the data you want to parse. Returns the id of the warnings. Needed request the full reports

Example 

    alert.get_id(5) # Five is the limit I have decided to use.

Limit must be larger than 0. (If its 0 it defaults to None, which means you have **no limit**). If limit goes over the actual amount of warnings, it just returns all of the warnings.


#### get_summary()

`alert.get_summary()` - accepts 1 argument, an Integer representing a limit how on much of the data you want to parse. Returns the id of the warnings. Cap fee

Example 

    alert.get_summary(5) # Five is the limit I have decided to use.

Returns the summaries of the warnings.



#### get_cap()

`alert.get_cap(5)` - accepts 1 argument, an Integer representing a limit how on much of the data you want to parse. Returns the id of the warnings. Cap fee

Example 

    alert.get_cap(5) # Five is the limit I have decided to use.

Cap returns most of the data about the warning. 

###### Note:

5 is arbitrary example. It can be any int above 0.



#Old Documentation

These methods still work, but they are older and now wraped around the Alert Method. they still may be used if you want more flexible use of the data

Create `NWS.request.nws()` instance.

    weather = NWS.request.nws("us") #us is statecode. you can add a `True`-`False` to the argument to set if it should immedialetly request data on this instance (`True` = Get Data), `False` = Dont get data)

To actually get the data use `weather.load()`

    weather.load() #Will return `True` if successful. If not it will return `False`.

The Library current supports the following methods.
    

     weather.get_cap()  #collects all of the data from the cap feed, and returns a list of dictionaries that contain each of the cap feed elements per entry.
     weather.get_summary() #gets the summary of an report. Returns a list of dictionaries 
     weather.get_title() #gets the titles.  Returns a list of dictionaries 
     weather.get_id() #Gets the id of an entry (the string of the id can be used for reports). Returns a list of dictionaries 
     NWS.toolbelt.get_all(weather) #returns a merged version of the above methods. Toolbelt, see below for details
    
To get a report. 

     rep = NWS.toolbelt.id2report(weather.get_id(),0) # 0 is the first entry. Uses toolbelt (see below)

report currently supports the following

     rep.load() #Gets the data. must be called before the below are used.
     rep.get_meta() #returns the meta information of the report (dict)
     rep.get_info() #returns the info about the report (dict)

You can also create a report instance by calling NWS.request.report(_id_) (_id_ is str or unicode) but it's not recommended due to possible future modifications and security issues.

### Toolbelt

This library includes some extra tools for handeling data. For various reasons that are not listed, it is faster (or more reasonable) to include a toolset rather than actually having the library itself extensively handling the data. The toolbelt includes functions that would be useful in the usage of this library.

Current uses of the toolbelt.
     
     NWS.toolbelt.id2report(_id_) # _id_ is the url of the page (string). Alternatively It accepts a dict with the "id" key in it. 
     #It also accepts list with the said dict in it, 
     #but you must specify which entry to use (defualt is the first). 
     #Returns a NWS.request.report() instance of the _id_
     #Automatically converts the id to https (note: urllib2 doesnt check for a valid cert)

     NWS.toolbelt.city2list(city) # where city is a str. get_cap() will give you the string of affected areas, this just makes them into a list.

     NWS.toolbelt.get_all(request) # request is a NWS.request.nws() instance. Merges NWS.request.nws() instance methods.
     #get_all() will return an error is the nws() instance has no data yet.

# Other Info

## DISCLAIMER

THIS LIBRARY SHOULD NOT BE USED TO ACTIVATE (OR EVEN WORK WITH) ANY KIND OF PRIVATE EMERGENCY SYSTEM/ALARM. IT WAS NEVER INTENDED TO BE USED AS SUCH. THIS LIBRARY SHOULD ONLY BE USED AS (INCLUDING, BUT NOT LIMITED TO) AN RESPONSIBLE NOTIFICATION SERVICE OR PERSONAL USE.

## Resources

Rules and Regulations - http://www.ecfr.gov/cgi-bin/text-idx?rgn=div5;node=47%3A1.0.1.1.12#se47.1.11_153
