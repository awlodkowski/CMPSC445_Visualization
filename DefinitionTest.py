import geopandas as gpd
import pandas as pd
import mapMaker as mm

# We are to write a program that asks the user for a zipcode, and returns the state that zipcode is in.
# The state returned will be used to load the shapefile for that state.

# read in the zip code data
zipData = pd.read_csv("ZIPindex.csv")
zipData = zipData[['ZIP', 'STATEABV']]
zipData['ZIP'] = zipData['ZIP'].astype(str)

# define a function to get the state from the zip code
def getState():
    zipExists = False

    # loop until a valid zip is entered
    while zipExists == False:
        x1 = getZip()

        # check if zip code exists in the data
        if x1 in zipData['ZIP'].values:
            zipExists = True
            state = zipData.loc[zipData['ZIP'] == x1, 'STATEABV'].iloc[0]
            print("State: " + state)
            return state, x1
        else:
            print("Error: Zip Code not found")

# define a function that gets the zip code from the user
def getZip():
    x1 = str(input("Enter Zip Code: "))
    print("Zip Code: " + x1)
    return x1

# define a function that loads the shapefile data based on the state
def loadShapefile(state):
    # read in the shapefile data
    shapefile = gpd.read_file("IndexSHPfiles/" + state + "zips.shp")
    return shapefile

# define a main function
def main():
    state, zip = getState()
    myState = loadShapefile(state)
    # print(myState.head())
    mm.makeMap(myState, zip)

# call main function
if __name__ == "__main__":
    main()