# importing geopy library and Nominatim class
from geopy.geocoders import Nominatim

def getLatLong(street, region, postalcode):
    """This function returns the latitude and longitude of an address"""
    # calling the Nominatim tool and create Nominatim class
    loc = Nominatim(user_agent="Geopy Library")

    # entering the location name
    getLoc = loc.geocode(street + " " + region + " " + postalcode)

    return getLoc.latitude, getLoc.longitude