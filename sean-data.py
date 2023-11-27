# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 10:16:25 2023

@author: seanw
"""

###
#  Final Project.py
#
# Created on: Wed. November 08, 18:35:00 2023
# 
# Author: Jerod Bond (Penn State email: jqb6425@psu.edu)
###

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import requests
from torchvision import transforms
import numpy as np
import pandas as pd

###
#
# Step 1 - Get API loaded in
#
###

# API endpoint URL

# Small Set
# api_endpoint = "https://api.apify.com/v2/datasets/i90HzOMmb8L3L3WMm/items?token=apify_api_GGaoEhwAXmcBPAO16uIgXh6OPfdEKT4Df3Ub"

#Large Set
# api_endpoint = "https://api.apify.com/v2/datasets/vkP4kAXzvaeiD1s6e/items?token=apify_api_GGaoEhwAXmcBPAO16uIgXh6OPfdEKT4Df3Ub"

#Large Large Set
api_endpoint = "https://api.apify.com/v2/datasets/caJlY6CbOmbEzBUtJ/items?token=apify_api_GGaoEhwAXmcBPAO16uIgXh6OPfdEKT4Df3Ub"

# Download data from the API endpoint
response = requests.get(api_endpoint)
data = response.json()

###
#
# Step 2 - Convert API dataset into desired properties
#
###

# Create a new list with items containing only the desired properties
new_data = []
for item in data:
    address_info = item.get("address", None)
    
    #Get last sold price from history instead
    history_info = item.get("history", None)
    listing_price = item.get("listPrice", None)
    
    if history_info is not None:
        # Find the first history item with event_name "Sold"
        sold_event = next((history_item for history_item in history_info if history_item.get("event_name") == "Sold"), None)
    else:
        sold_event = None
    
    if sold_event is not None:
        listing = sold_event.get("listing", None)
        
        if listing is not None:
            list_price = listing.get("list_price", None) if listing.get("list_price") is not None else 0
        else:
            list_price = item.get("listPrice", None) if item.get("listPrice", None) is not None else 0
    else:
        list_price = item.get("listPrice", None) if item.get("listPrice", None) is not None else 0
    
    new_item = {
        "region": address_info.get("region", None) if address_info is not None else None,
        "postalCode": address_info.get("postalCode", None) if address_info is not None else None,
        "street": address_info.get("street", None) if address_info is not None else None,
        "lot_sqft": item.get("lot_sqft", 0) if item.get("lot_sqft") is not None else 0,
        "sqft": item.get("sqft", 0) if item.get("sqft") is not None else 0,
        "beds": item.get("beds", 0) if item.get("beds") is not None else 0,
        "baths": item.get("baths", 0) if item.get("baths") is not None else 0,
        "garage": item.get("garage", 0) if item.get("garage") is not None else 0,
        "pool": item.get("pool", 0) if item.get("pool") is not None else 0,
        "lastSoldPrice": list_price
    }
    new_data.append(new_item)

# Convert to array for training
dataset = pd.DataFrame(new_data)


print(dataset)

dataset.drop(dataset[(dataset['lastSoldPrice'] <= 0)].index, inplace=True)

dataset = dataset.sort_values(by=['region', 'postalCode'])

print(dataset)
print(dataset.info())

#Convert the dataset to a numpy array
new_data_array = dataset.to_numpy()

# Create a comma separated list into a file called data.txt
header = "region\tpostalCode\tstreet\tlot_sqft\tsqft\tbeds\tbaths\tgarage\tpool\tlastSoldPrice\n"

with open("sean-data-large.txt", "w") as file:
    file.write(header)
    np.savetxt(file, new_data_array, fmt='%s', delimiter="\t")
    file.close()