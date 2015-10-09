import re
import requests

#  import numerical python, pandas:
import numpy as np
import pandas as pd
from pandas import DataFrame



"""

GOOGPLE MAPS ELEVATION API & GOOGLE STREET VIEW IMAGE API & GOOGLE MAPS GEOCODING API

Limits:
elevation:
streetview: Free until exceeding 25,000 map loads per 24 hours for 90 consecutive days
640 x 640 maximum image resolution
geocoding: 2,500 free requests per day

"""

gmaps_key = 'here is the key for...'
gstreet_key = 'here is the key for...'
ggeo_key = 'here is the key for...'




"""
Use Google Maps geocoding to get lat, lon for a given address and save it in a list.

User can enter address in following format: 1600 Amphitheatre Parkway, Mountain View, CA 
address wneeds to be converted into google conform url-string: 1600+Amphitheatre+Parkway,+Mountain+View,+CA
"""

# converts for example 1600 Amphitheatre Parkway, Mountain View, CA to 1600+Amphitheatre+Parkway,+Mountain+View,+CA
def address_convert(address):
    return re.sub('\s', '+', address, flags=re.IGNORECASE)

# returns dictionary with keys lat, lon and their values for a given address given as 1600 Amphitheatre Parkway, Mountain View, CA 
def geo(address):
    address_key = address_convert(address)
    latlon = {}
    ggeo_url = 'https://maps.googleapis.com/maps/api/geocode/json?address={address_key}&key={key}'.format(address_key=address_key,key=ggeo_key)
    ggeo_inital = requests.get(ggeo_url)
    ggeo_json = ggeo_inital.json()
    test_ggeo = DataFrame(ggeo_json['results'])
    latlon['lat'] = test_ggeo['geometry'][0].get('location')['lat']
    latlon['lon'] = test_ggeo['geometry'][0].get('location')['lng']
    return latlon


