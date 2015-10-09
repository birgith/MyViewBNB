# import some modules:
import sys, os
import re
import requests

#  import numerical python, pandas and matplotlib:
import numpy as np
import pandas as pd
from pandas import *
import matplotlib
import matplotlib.pyplot as plt
from collections import OrderedDict
from generate_maps import *
from geographic_locations import *
from image_recognition_analysis import *
from download_url import *
from Sentiment_Analysis import *

# build dataframe form csv data:
def build_df(filename):
    return DataFrame(read_csv(filename))

def run_prep(city, view):
	#if city == 'Paris':
	#	avr_price_map()
	# Paris view options:
	if city == "Paris" and view == 'Eiffel':
		img_list, df = run_all('Paris-airbnb_ny2.csv', 'eiffel', 'view', 'test2ny')
		maps2(img_list, df, 'eiffel tower, Paris', 14, 'Paris')
	if city == "Paris" and view == 'Notre Dame':
		img_list, df = run_all('Paris-airbnb_ny2.csv', 'notre', 'view', 'test2ny')
		maps2(img_list, df, 'notre dame, Paris', 14, 'Paris')
	if city == "Paris" and view == 'Montmartre':
		img_list, df = run_all('Paris-airbnb_ny2.csv', 'montmartre', 'view', 'test2ny')
		maps2(img_list, df, 'montmartre, Paris', 15, 'Paris')
	if city == "Paris" and view == 'Sacre Coeur':
		img_list, df = run_all('Paris-airbnb_ny2.csv', 'coeur', 'view', 'test2ny')
		maps2(img_list, df, 'sacre coeur, Paris', 14, 'Paris')	
	
	# San Francisco/Bay Area view options:
	if city == "SF" and view == 'GGB':
		img_list, df = run_all('Bay-Area-airbnb.csv', 'golden', 'view', 'test2ba')
		download_dict = get_all_img(df)
		final2 = run_img_analysis("golden", download_dict)
		dict_map(final2, df, 'San Francisco', 11)
	if city == "SF" and view == 'Bay View':
		img_list, df = run_all('Bay-Area-airbnb.csv', 'view', 'view', 'test2ba')
		download_dict = get_all_img(df)
		final2 = run_img_analysis("bay", download_dict)
		dict_map(final2, df, 'San Francisco', 11)	


def run_all(file_name, word1, word2, img_dir):
    #read airbnb data for Paris, 200 pages:
    initial_df = build_df(file_name)
    
    #filter for words and perform sentiment analysis:
    df = sent_df(word1, word2, initial_df)
    dfclean = cleanup(df)

    # get only the first images:
    img_list = get_firstimg2(dfclean)
    
    # uncomment to download:
    #download(img_list, img_dir)
    
    return img_list, dfclean

##########################################################################################
#######	Airbnb functions 
##########################################################################################

# base Url for single airbnb posts: 
base_url = 'https://www.airbnb.com/rooms/'

# make Dataframe for airbnb: 
"""
input:  a row number (int), a list of column names for the df, the dataframe itself
output: Dataframe
"""
def make_df_airbnb(row, col, df):
    d = dict.fromkeys(col, 'None')
    d['ListingID'] = df.ix[row]['ListingID']
    d['Title'] = df.ix[row]['Title']
    d['Url'] = base_url + str(df.ix[row]['ListingID'])
    d['Price'] = df.ix[row]['Price']
    d['Lat'] = df.ix[row]['Lat']
    d['Lon'] = df.ix[row]['Long']
    d['AboutListing'] = df.ix[row]['AboutListing']
    #d['ShortDesc'] = df.ix[row]['ShortDesc']
    d['Review'] = df.ix[row]['Review']
    d['Rating'] = df.ix[row]['Rating']
    d['ImageUrl'] = df.ix[row]['ImageUrl']
    b = DataFrame(d, index=[row])
    return b
    
    
 
# Find a phrase within a text:
"""
input:  a string
output: True or False
example: Find("the", "the world is beautiful") --> returns True
"""
def Find(pat, text):
    if re.search(pat, text):
        return True

# Column names for Airbnb Dataframes:
col = ['ListingID', 'Title', 'Url', 'Price', 'Lat', 'Lon', 'AboutListing', 'ImageUrl', 'Review', 'Rating']



"""
Next three functions build dataframes that contain specific words in airbnb posting sections:
input:  string1, string2, int for row number, a dataframe 
output: a dataframe that contains both strings in the "AboutListing" text
example: df("view", "eiffel", row#, df) --> returns dataframe that appends rows with phrases in "AboutListing"
"""
# returns a new dataframe of airbnb listings that have specific words in "AboutListing":
def df_pattern(pat1, pat2, row, df_in):
    df = DataFrame(columns=col)
    for i in row:
    	#print i
    	#print df_in['AboutListing'][i].lower()
        p1 = Find(pat1, df_in['AboutListing'][i].lower())
        p2 = Find(pat2, df_in['AboutListing'][i].lower())
    
        if p1 and p2:
            df = df.append(make_df_airbnb(i, col, df_in))
    return df
    
# find listings in airbnb_paris that have specifc words "Title":
def df_pattern_title(pat1, pat2, row, df_in):
    df = DataFrame(columns=col)
    for i in row:
		
        p1 = Find(pat1, df_in['Title'][i].lower())
        p2 = Find(pat2, df_in['Title'][i].lower())
    
        if p1 and p2:
        	#print 'check check check'
        	df = df.append(make_df_airbnb(i, col, df_in))
    return df

def df_pattern_rev(pat1, pat2, row, df_in):
    df = DataFrame(columns=col)
    for i in row:
        p1 = Find(pat1, df_in['Review'][i].lower())
        p2 = Find(pat2, df_in['Review'][i].lower())
    
        if p1 and p2:
            df = df.append(make_df_airbnb(i, col, df_in))
    return df

