# import some modules:
import sys, os
import re
import requests

#  import numerical python, pandas and matplotlib:
import numpy as np
import pandas as pd
from pandas import *
from pandas import DataFrame
import matplotlib
import matplotlib.pyplot as plt
from collections import OrderedDict
#from sentiment_analysis import *
#from maps import *
from geo_loc import *
import operator



"""
This is to obtain a dictionary where each key corresponds to a ListingID, and the entries are lists of ImageUrls. 
Returns that dictionary so that it can be downloaded distinctively.
"""

def get_all_img(df):
    urldict = {}
    
    for i in range(len(df)):

        urllist = []
        if df['Polarity'][i] >= 0:
            
            for j in range(len(df['ImageUrl'][i])):
                lengthbefore = len(urllist)
                urllist.append(df['ImageUrl'][i][j])
                lengthafter = len(urllist)
            urldict[int(df['ListingID'][i])] = urllist
                    
        else:
            print i
            
    img_list = list(OrderedDict.fromkeys(urllist))
    
    return urldict

