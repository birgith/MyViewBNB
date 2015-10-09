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
from generate_maps import *
from geo_loc import *
import operator

""" 
Makes a dataframe from the image recognition output csv file for those rows that contain a value 
corresponding to the specified categories.
"""


def run_img_analysis(view, d):
	if view == "bay":
		values = [128, 47, 31, 90, 156, 163]
		df_rec = prep_df('205CNN_bay_view_view.csv', values)
	
		dtest = find_most_prob(df_rec, values)
		final = make_final_dict(dtest, d)
		
	elif view == "golden":
		values = [128, 47, 31, 90]
		df_rec = prep_df('205CNN_bay_golden_view.csv', values)
	
		dtest = find_most_prob(df_rec, values)
		final = make_final_dict(dtest, d)
	
	return final
	


def prep_df(filename, values):
    cnn_ba = DataFrame(read_csv(filename))
    col = cnn_ba.columns
    df_rec = DataFrame(columns=col)
    for i in range(len(cnn_ba)):
        if cnn_ba['style1'][i] in values or cnn_ba['style2'][i] in values or cnn_ba['style3'][i] in values or cnn_ba['style4'][i] in values or cnn_ba['style5'][i] in values:

            row = cnn_ba.ix[i]
            df_rec = df_rec.append(row)


    # add column with bare ID:
    baseID = []
    a = df_rec['ID'].reset_index()

    for i in range(len(df_rec)):
        b = re.search(r'\w+\_', a['ID'][i])
        c =b.group().strip("_")
        baseID.append(c)

    df_rec['baseID']= baseID
    return df_rec


"""
returns dictionary with baseID as key, and image ID as value for the images with highest probability.
remaining to fix: when probablility in for example styl2 is larger than that in style1
"""


def find_most_prob(df, values):
    #print values
    all_dict = {}
    for i in df.baseID:
        temp_out = df[(df.baseID == i)]
        temp_out = temp_out.reset_index() 

        df_select = DataFrame(columns=df.columns)
        if len(temp_out) <= 1:
            
            all_dict[temp_out.baseID[0]] = temp_out.ID[0]
        else:
            temp_dict={}
            for j in range(len(temp_out['style1'])):
                #print temp_out['style1']
                if temp_out['style1'][j] in values:
                    prob = temp_out.sval1[j]
                    temp_dict[temp_out.ID[j]] = prob
                elif temp_out['style2'][j] in values:
                    prob = temp_out.sval2[j]
                    temp_dict[temp_out.ID[j]] = prob
                elif temp_out['style3'][j] in values:
                    prob = temp_out.sval3[j]
                    temp_dict[temp_out.ID[j]] = prob
                elif temp_out['style4'][j] in values:
                    prob = temp_out.sval4[j]
                    temp_dict[temp_out.ID[j]] = prob
                elif temp_out['style5'][j] in values:
                    prob = temp_out.sval5[j]
                    temp_dict[temp_out.ID[j]] = prob

            max_temp = max(temp_dict.iteritems(), key=operator.itemgetter(1))[0]
        
            all_dict[temp_out.baseID[0]] = max_temp 
    
    return all_dict
    
"""
Compare list with dictionary that was fed into image recognition to retrieve the final image-url-list
"""
def make_final_dict(all_dict, d):
    final_dict = {}
    for key in all_dict:
        temp = all_dict[key]
        temp = re.search(r'\_\w+\.', temp)
        temp = temp.group().strip("_")
        temp = temp.strip(".")
        final_dict[int(key)]=d[int(key)][int(temp)]
    return final_dict