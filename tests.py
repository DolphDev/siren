#    Siren Module Tests    
#    Calls all methods in Siren() object
#     Calls all methods in request() object
import siren

alert = siren.Siren() #Create the object and assigns it to `alert`


if alert.load(): #Loads the data from the server
    alert.get_raw_xml() #Gets raw XML
    alert.get_entries() #
    alert.parse()
    alert.get_all()
