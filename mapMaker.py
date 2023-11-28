import geopandas as gpd
import folium
from folium.plugins import *

def makeMap(myState, myPlace):
    """This function makes a map based on the zip code entered"""
    statesBase = gpd.read_file("States.shp")

    # create a map
    m = folium.Map(location=[myPlace['LAT'], myPlace['LONG']], zoom_start=12)

    # add the statesBase layer
    folium.GeoJson(statesBase).add_to(m)

    # add the zip code layer
    folium.GeoJson(myState).add_to(m)

    zipTooltip = folium.features.GeoJsonTooltip(fields=['ZIP', 'PRIMECITY', 'COUNTY'],
                                                aliases=['Zip Code: ', 'Prime City: ', 'County: '])
    
    myState['color'] = 'yellow'
    myState['area'] = myState['geometry'].area

    # create a temporary dataframe to hold one row of data based on the zip parameter
    temp = myState.loc[myState['ZIP'] == myPlace['ZIP']]

    # create a pin for myPlace
    folium.Marker([myPlace['LAT'], myPlace['LONG']], popup=myPlace['STREET'] + " " 
                  + myPlace['CITY'] + ", " + myPlace['STATE'] + " " + myPlace['ZIP']).add_to(m)

    # change the value of myState['color'] by comparing the area of each row to the area of the temp dataframe
    for i in myState.index:
        if myState.loc[i, 'area'] > temp.loc[temp.index[0], 'area']:
            myState.loc[i, 'color'] = 'red'
        elif myState.loc[i, 'area'] < temp.loc[temp.index[0], 'area']:
            myState.loc[i, 'color'] = 'green'
        else:
            myState.loc[i, 'color'] = 'yellow'

    # color the zip code layer based on the color column and set opacity to 0.9
    zipMap = folium.features.GeoJson(myState,
                                        tooltip=zipTooltip,
                                        style_function=lambda x: {'fillColor': x['properties']['color'], 
                                                                  'fillOpacity': 0.9, 
                                                                  'color': 'black',
                                                                  'weight': 0.5},
                                        zoom_on_click=True)
    zipMap.add_to(m)

    # save the map
    m.save("map.html")
    
    #open the map
    import webbrowser
    webbrowser.open("map.html")