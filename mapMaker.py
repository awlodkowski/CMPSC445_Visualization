import geopandas as gpd
import folium
from folium.plugins import *

def printTest(state):
    print("From mapMaker.py")
    print(state.head())

def makeMap(myState, zip):
    states = gpd.read_file("IndexSHPfiles/States.shp")

    # get the LAT and LONG of the zip code
    zipLat = myState.loc[myState['ZIP'] == zip, 'LAT'].iloc[0]
    zipLong = myState.loc[myState['ZIP'] == zip, 'LONG'].iloc[0]

    # create a map
    m = folium.Map(location=[zipLat, zipLong], zoom_start=12)

    # add the states layer
    folium.GeoJson(states).add_to(m)

    # add the zip code layer
    folium.GeoJson(myState).add_to(m)

    zipTooltip = folium.features.GeoJsonTooltip(fields=['ZIP'],
                                                aliases=['Zip Code: '])
    
    zipMap = folium.features.GeoJson(myState,
                                        tooltip=zipTooltip,
                                        style_function=lambda x: {'fillColor': 'red'})
    zipMap.add_to(m)

    # save the map
    m.save("map.html")
    
    #open the map
    import webbrowser
    webbrowser.open("map.html")