import geopandas as gpd
import pandas as pd
import mapMaker as mm
import LatLongGetter as llg



def getAddr():
    """This function gets the address, state, and zip code from the user"""

    street = str(input("Enter Street Address: "))
    city = str(input("Enter City: "))
    state = str(input("Enter State (abbrevation): "))
    zip = str(input("Enter Zip Code: "))

    return street, city, state, zip

def loadShapefile(state):
    """This function loads the shapefile data based on the state"""

    # read in the shapefile data
    shapefile = gpd.read_file("ZIP_states/ZIPs_" + state + ".shp")
    return shapefile

def main():

    street, city, state, zip = getAddr()
    myState = loadShapefile(state)
    pinLat, pinLong = llg.getLatLong(street, city, zip)
    myPlace = {'STREET': street, 'CITY': city, 'STATE': state, 'ZIP': zip, 'LAT': pinLat, 'LONG': pinLong}

    mm.makeMap(myState, myPlace)

if __name__ == "__main__":
    main()