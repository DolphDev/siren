#!!! Warning !!!#

This is one of my earlier projects. I knew very little then and made odd design decsions. This library was built poorly and is not usable for any use case outside of re-writing it. I plan to revist this in the future, however my work on other libraries are currently being focuses on. If you wish to see more of my work, checkout [nationstates](https://github.com/Dolphman/pynationstates) or [ezurl](https://github.com/Dolphman/ezurl)

# siren V 0.1.0.0

A Python library for the National Weather Service Public Alerts. 


# Documentation
---

import the module

    import siren

# Siren Object

This module includes the object `siren.Siren()`. This object wraps around the entire package for easy and more consistent use. 

To the create the object

    alert = siren.Siren()

This also accepts keyword arguments for more advanced usage. 

* `state` - Default is `"us"` (Which is the entire country, including territories). Accepts either a state abbreviations or a county/zone code.
* `loc` - Default is `False`. Must be `True` if `state` is a country/zone code. Dont include it or leave `False` if your using a state abbreviation.
* `auto_load` - Default is `False`. If set to `True` the object will request the data on its creation. Note - You cannot check if the request was successful if done.
* `limit` - Default is `None`. Sets a universal limit for the object. It will be used if you call a method without specifying a limit.


###### Note: `alert` is a arbitrary variable name

## Methods

###Getting data

You must use `alert.load()` if you did not set `auto_load` to `True` when creating the object.

`alert.load()` requests and sets up the module for parsing. returns `True` if successful and `False` if otherwise. 



## Parsing 


There is two ways this module parses the data:

##### On Demand.

A simple approach is to simply parse your data as you need it. Simply use the functions outlined in the Parsing Data section below.

This module keeps a cache the last request for each of parsing functions. The cache is cleared when either `alert.load()` is called or the said functions are called with larger parameters than what is in the cache.

##### Pre-processing

Another approach is to pre-process your data. To do this you call `alert.parse()`. It calls the parsing methods and store the result. `alert.parse` accepts one optional argument, and integer representing the limit, default is None (it will parse all warnings if argument is None) .

That the cache system will re-parse if the argument supplied is greater than what it was when parsed.  For example: if you call 'alert.parse(5)', if you want use the cache data stored by that method, the argument for the limit must be equal to or less than when it was cached (so for the given example it must be less than or equal to 5).

##### On-Demand or Pre-Processing?

This isn't this authors decision, but  is instead is up to the developer using it. That said On-Demand should be used when you don't need all of the data parsed or in circumstances where you want to limit amount of the data parsed. If you plan on using all of the data (especially if you want all current warnings parsed), it may be better to pre-process it.

Speed wise, their is no perceived difference that has been discovered during development. (As in if you use all the parsing methods for on-demand use, it will be the same speed of pre-processing it.)

Occasionally the data will contain no alerts. The module includes one function to help with this.


`alert.warnings` - Returns `True` if request has active alerts. ``False`` if not. **DOES NOT check for 404**, if the server returns a 404, the program will raise an error.

### Parsing data.



|   Method Name   | Example             | Result                                                                                    |
|:---------------:|---------------------|-------------------------------------------------------------------------------------------|
| `get_raw_xml()` | `alert.get_raw_xml()`| Returns the raw XML                                                                      |
| `get_entries()` | `alert.get_entries()`| returns the entries (XML that has been seperated, but not processed)                     |
| `parse()`       | `alert.parse()`     | Preprocess the CAP/XML data. Caches the result                                            |
| `get_cap()`     | `alert.get_cap()`   | Processes/Loads from cache the CAP data for the active warning(s). Returns the CAP feeds. |
| `get_summary()` | `alert.get_summary` | Processes/Loads from cache the summaries for the active warning(s). Returns the summaries |
| `get_title()`   | `alert.get_title()` | Processes/Loads from cache the title(s) of the active warning(s). Returns the titles      |
| `get_id()`      | `alert.get_title()` | Processes/Loads from cache the id(s) of the active warning(s). Returns the ids            |

All methods accept one optional argument, an interger representing a limit on how much you want to parse.

### Reports.

The `NWS.siren()` object includes the `get_reports()` method, which handles getting the extended reports that the NWS generates. 

It accepts the following keyword arguments.

* `id` - If supplied (and valid), the method will return supplied id's report.

the report instance has 3 methods (rep is representing the report instance)

* `rep.load()` - Requests the data. Required for use. Returns `True` if server returned valid content, `False` if otherwise.
* `rep.get_info()` - returns most of the info about an particular report.
* `rep.get_meta()` - returns the meta information about the report.

# More Siren object info

####Before load() method
	
`len()` will return the current limit.

######Note: If you dont have a limit, you may obtain unexpected results depending on your arguments when creating a Siren object.

####After load() method

`len()` will return the current limit. If the limit is `None`, it will return the amount of entries the server returns.

The Siren objects data can be accessed via keys. Currently, only 4 are supported (`"cap"`,`"title"`,`"id"`, `"summary"`)

Example Usage:

    cap = alert["cap"]

This is equivalent to calling alert.get_cap()


####The Toolbelt

#Old Documentation

These methods still work, but they are older and now wrapped around the alert object. they still may be used if you want more flexible use of the data.

You can view the old documentation [here](https://github.com/Dolphman/siren/blob/master/OldDoc.md)

#Requirements

This module requires the BeautifulSoup module, and only supports 2.x python (3.x support is in progress). 

# Other Info

## DISCLAIMER

THIS LIBRARY SHOULD NOT BE USED TO ACTIVATE (OR EVEN WORK WITH) ANY KIND OF PRIVATE EMERGENCY SYSTEM/ALARM. IT WAS NEVER INTENDED TO BE USED AS SUCH. 

## Resources

Rules and Regulations - http://www.ecfr.gov/cgi-bin/text-idx?rgn=div5;node=47%3A1.0.1.1.12#se47.1.11_153
