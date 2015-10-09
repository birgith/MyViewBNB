######################################
Sentiment Analysis of Airbnb Listings
######################################

# import some modules:
import sys, os
import re
import requests

import numerical python, pandas and matplotlib:
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



# Dataframe built from postings with specific words, whose reviews are evaluated by sentiment analysis: 
def sent_df(word1, word2, df):
    
    r = range(len(df))

    #get listings with the words in "Aboutlisting":
    a = df_pattern(word1, word2, r, df)
    #get listings with the words in "Title":
    b = df_pattern_title(word1, word2, r, df)

    #get listings with the words in "Review":
    c = df_pattern_rev(word1, word2, r, df)

    # Merge without repetition:
    new =  merge(a, b,  how='outer').drop_duplicates()

    new =  merge(new, c, how='outer').drop_duplicates()
    new = new.reset_index(drop=True)

    d = sentiment(new, col)
    f = d.reset_index(drop=True)

    return f


    
# Cleanup and return final Dataframe:
def cleanup(df):
    img_col = df['ImageUrl'].apply(lambda x:x.split(" "))
    img_dict = {}
    for i in range(len(img_col)):
        img_dict[i] = []
        row = list(OrderedDict.fromkeys(img_col[i]))
        row = [row[x] for x in range(len(row)) if Find('profile', row[x]) != True]
        for j in range(len(row)):
            try:
                m4 = re.search(r'(http.*)\?',row[j])
                img_dict[i].append(m4.group(1))
            except:
                None
    final = df_final(df, img_dict)
    return final


def df_final(df, img_dict):
    final = df
    
    #remove old ImageUrl column:
    del final['ImageUrl']
    
    col = ['ImageUrl']
    index = range(len(df))
    
    #initialize dataframe to be filled with lists:
    new = pd.DataFrame(index=index, columns=col)
    new = new.fillna(0)
    
    #fill dataframe with lists from the dictionary img_dict
    for i in range(len(df)):
        new['ImageUrl'][i] = img_dict[i]
    
    final2 = concat([final, new], axis=1)
    final2['ImageUrl'][0]
    
    return final2
 

# Try only evaluating first (cover) image of listing
def get_firstimg2(df):
	urllist = []
	for i in range(len(df)):

		if df['Polarity'][i] >= 0:

			urllist.append(df['ImageUrl'][i][0])

    # remove duplicates:
	img_list = list(OrderedDict.fromkeys(urllist))
	return urllist

##########################################################################################
#####Download images:
##########################################################################################

# revtrieve urls with list input:
import urllib

def download(img_list, img_dir): 
    if not os.path.exists("images/" + img_dir):
        os.makedirs("images/" + img_dir)
    for i in range(len(img_list)):
        try:
            filename = "images/%s//data_%d.jpg"%(img_dir, i)
            urllib.urlretrieve(img_list[i], filename)
        except:
            None

##########################################################################################
##### Sentiment Analysis:
##########################################################################################

#packages for sentiment analysis:
import nltk
import nltk.data
import textblob
from nltk.corpus import stopwords
from collections import Counter, defaultdict
from sklearn import linear_model
import datetime
#import pickle

# evaluates sentiment polarity and subjectivity
"""
polarity is a float within [-1.0, 1.0]
subjectivity is float within [0.0, 1.0], where 0.0= very objective, 1.0=very subjective

input: list of reviews 
output: list of sentiment tuples
"""

# only infer sentiment per sentence if it contains some variation of "view": 
view_word = ['eiffel', 'vue', 'outlook', 'panorama', 'vista', 'aussicht', 'blick', 'perspectiva', 'veduta', 'widok', 'perspectywa', 'sicht', 'zicht', 'uitzicht', 'the', 'a']

view_word2 = ['a', 'the','eiffel', 'vue', 'outlook', 'panorama', 'vista', 'aussicht', 'blick', 'perspectiva', 'veduta', 'widok', 'perspectywa', 'sicht', 'zicht', 'uitzicht']

""" 
sent_review provides a sentiment score per review.
input: a review as string, 
output: [avr polarity, avr subjectivity] = avr(sentiment per each sentence for whole review) if there are "view" words 

for example:
sent_review(airbnb_paris['Review'][1]) --> [0.465, 0.755]

"""
def sent_review(review):
    pol = 0
    subj = 0
    sents = textblob.TextBlob(review).sentences
    
    #counts the number of sentences with "view" words
    count = 0
    
    #go through each sentence:
    for sent in sents:
        sent = str(sent)
        
        # only provide sentiment for sentences that contain a variation of the word "view":
        for w in view_word:
            if Find(w, sent.lower()):
                count += 1
                pol += textblob.TextBlob(sent).sentiment[0]
                subj += textblob.TextBlob(sent).sentiment[1]
        if count != 0:
            pol_avr = pol/count
            subj_avr = subj/count
        else:
            pol_avr = None
            subj_avr = None
    return [pol_avr, subj_avr]

# base Url for single airbnb posts: 
base_url = 'https://www.airbnb.com/rooms/'

# Sentiment analysis: make a complete df for airbnb after sentiment analysis:
"""
input:  a row number (int), a list of column names for the df, the dataframe itself
output: Dataframe
"""

def df_airbnb_tot(row, col, df, pol, subj):
    d = dict.fromkeys(col, 'None')
    d['ListingID'] = df.ix[row]['ListingID']
    d['Title'] = df.ix[row]['Title']
    d['Url'] = base_url + str(df.ix[row]['ListingID'])
    d['Price'] = df.ix[row]['Price']
    d['Lat'] = df.ix[row]['Lat']
    d['Lon'] = df.ix[row]['Lon']
    d['AboutListing'] = df.ix[row]['AboutListing']
    #d['ShortDesc'] = df.ix[row]['ShortDesc']
    d['Review'] = df.ix[row]['Review']
    d['Rating'] = df.ix[row]['Rating']
    d['ImageUrl'] = df.ix[row]['ImageUrl']
    d['Polarity'] = pol
    d['Subjectivity'] = subj
    b = DataFrame(d, index=[row])
    return b

col = ['ListingID', 'Title', 'Url', 'Price', 'Lat', 'Lon', 'AboutListing', 'Review', 'Rating','ImageUrl', 'Polarity', 'Subjectivity']

# sentiment for each review:
def sentiment(df, col):
    d = DataFrame(columns=col)
    for post in range(len(df)):
    	#print post
        a = sent_review(df['Review'][post])
        pol = a[0]
        subj = a[1]
        if pol >= 0:
        	d = d.append(df_airbnb_tot(post, col, df, pol, subj))
        #d = d.append(df_airbnb_tot(post, col, df, pol, subj))
    return d

def sentiment2(df, col):
    d = DataFrame(columns=col)
    for post in range(len(df)):
        a = sent_review2(df['Review'][post])
        pol = a[0]
        subj = a[1]
        d = d.append(df_airbnb_tot(post, col, df, pol, subj))
    return d
    
    

  
    
    