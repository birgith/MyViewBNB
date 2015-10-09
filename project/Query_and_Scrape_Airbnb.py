# -*- coding: utf-8 -*-

import mechanize
import cookielib
from lxml import html
import csv
import re
import json
from random import randint
from time import sleep
from lxml.etree import tostring
import bs4
import pandas as pd

"""
The scrape file has been downloaded from the source below and then modified for personal use by Birgit Hausmann 
(extended to scrape for reviews, rating, images, etc).


@author: Hamel Husain, TODO: Name Everyone In Group
CS109 Harvard Intro To Data Science
Scraping Airbnb
"""

# Browser
br = mechanize.Browser()


#learned necessary configuration from 
#http://stockrt.github.io/p/emulating-a-browser-in-python-with-mechanize/

# Allow cookies
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
#specify browser to emulate
br.addheaders = [('User-agent', 
'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

#######################################
#  Wrapper Functions    ###############
#######################################

def IterateMainPage(location_string, loop_limit): 
    MainResults = []
    """
    input: 
        location_string (string) - this is a location string that conforms to the 
                                   pattern on airbnb for example, 
                                   Cambridge, MA is "Cambridge--MA"
        loop_limit (integer) -    this is the maximum number of pages you want to parse.
        
    output:
        list of dictionaries, with each list element corresponding to a unique listing
        
    This function iterates through the main listing pages where different properties
    are listed and there is a map, and collects the list of properties available along
    with the limited amount of information that is available in that page.  This function
    returns a list of dictionaries with each list element corresponding to a unique listing. 
    Other functions will take the output from this function and iterate over them to explore
    the details of individual listings.  
    """  
        
    base_url = 'https://www.airbnb.com/s/'
    page_url = '?page='
    
    
    try:
        for n in range(1, loop_limit+1):
            print 'Processing Main Page %s out of %s' % (str(n), str(loop_limit))
            #Implement random time delay for scraping
            sleep(randint(1,3))
            current_url = ''.join([base_url, location_string, page_url, str(n)])
            MainResults += ParseMainXML(current_url, n)
        
            
    except:
        print 'This URL did not return results: %s ' % current_url
    
    print 'Done Processing Main Page'
    return MainResults



    
#######################################
#  Main Page    #######################
#######################################


def ParseMainXML(url= 'https://www.airbnb.com/s/Cambridge--MA--United-States', pg = 0):
    
    """
    input: url (string )
            
            this is the url for the type of listings you want to search. 
            default is to use the generic url to search for listings 
            in Cambridge, MA
    input: pg (integer)
        
            this is an integer corresponding to the page number, this is meant
            to be passed in by the wrapper function and collected in the dictionary.
            
    output: dict
    ------
    This funciton parses the main page with mulitple airbnb listings, and 
    returns a list of dictionaries corresponding to the attributes found
    """   
    n = 1
    ListingDB = []
           
    try:
        
        tree = html.fromstring(br.open(url).get_data())
        listings = tree.xpath('//div[@class="listing"]')

        #TODO: add error handling    
        for listing in listings:
            dat = {}
            dat['baseurl'] = url
            dat['Lat'] = listing.attrib.get('data-lat', 'Unknown')
            dat['Long'] = listing.attrib.get('data-lng', 'Unknown')
            dat['Title'] = listing.attrib.get('data-name', 'Unknown').encode('utf8')
            dat['ListingID'] = listing.attrib.get('data-id', 'Unknown')
            dat['UserID'] = listing.attrib.get('data-user', 'Unknown')
            dat['Price'] = ''.join(listing.xpath('div//span[@class="h3 text-contrast price-amount"]/text()'))
            dat['PageCounter'] = n
            dat['OverallCounter'] = n * pg
            dat['PageNumber'] = pg
            
            
            
            ShortDesc = listing.xpath('div//div[@class="media"]/div/a')
            
            if len(ShortDesc) > 0:
                dat['ShortDesc'] = ShortDesc[0].text.encode('utf8')
            
            if len(listing.xpath('div/div//span/i')) > 0:
                dat['BookInstantly'] = 'Yes'
            
            else:
                dat['BookInstantly']  = 'No'
                
            ListingDB.append(dat)
            n += 1
        
        print ListingDB
        return ListingDB   # there seems no problem up to this point
        
    except:
        print 'Error Parsing Page - Skipping: %s' % url
        #if there is an error, just return an empty list
        return ListingDB
        
    

#######################################
#  Detail Pages #######################
#######################################

def iterateDetail(mainResults):
    """
    This function takes the list of dictionaries returned by the
    IterateMainPage, and "enriches" the data with detailed data
    from the particular listing's info - if there is an error
    with getting that particular listing's info, the dictionary
    will be populated with default values of "Not Found"
    """
    finalResults = []
    counter = 0
    baseURL = 'https://www.airbnb.com/rooms/'   
       
    for listing in mainResults:    # listing is a dict
        counter += 1      
        print 'Processing Listing %s out of %s' % (str(counter), str(len(mainResults)))
        
        #Construct URL
        currentURL = ''.join([baseURL, str(listing['ListingID'])])
        
        #Get the tree         
        tree = getTree(currentURL) 
        
        #Parse the data out of the tree      
        DetailResults = collectDetail(tree, listing['ListingID'])
        
        #Collect Data
        newListing = dict(listing.items() + DetailResults.items())
        
        #Append To Final Results
        finalResults.append(newListing)
        
    return finalResults

        
        
def getTree(url):
    """
    input
        url (string): this is a url string.  example: "http://www.google.com"
    
    output
        tree object:  will return a tree object if the url is found, 
        otherwise will return a blank string
    """
    try:
        #Implement random time delay for scraping
        sleep(randint(0,1))
        tree = html.fromstring(br.open(url).get_data())
        return tree
        
    except:
        #Pass An Empty String And Error Handling Of Children Functions Will Do 
        #Appropriate Things
        print 'Was not able to fetch data from %s' % url
        return ''


def collectDetail(treeObject, ListingID):
    Results = {'AboutListing': 'Not Found', 
    			'ImageUrl': 'Not Found',
    			'Rating': 'Not Found',
    			'Review': 'Not Found'
                     }   
                     
    try:               
    	soup = TreeToSoup(treeObject)     
        Results['AboutListing'] = getAboutListing(treeObject, ListingID)
        Results['ImageUrl'] = getImageUrl(soup, ListingID)
        Results['Rating'] = getRating(soup, ListingID)
        Results['Review'] = getReview(soup, ListingID)
        return Results
        
    except:
        #Just Return Initialized Dictionary
        return Results


def TreeToSoup(treeObject):
    """
    input: HTML element tree
    output: soup object (Beautiful Soup)
    This function converts an HTML element tree to a soup object
    """
    source = tostring(treeObject)
    soup = bs4.BeautifulSoup(source)
    return soup
    
#############################################
### Birgit's Functions #########################   

def getImageUrl(soup, ListingID):
	ImageUrl = []
	
	try:
		img = soup.findAll("div", {"class": "slideshow-preload hide"})
		ImageUrl = [link.get('src') for link in soup.findAll('img')]
		return ImageUrl
		
	except:
		print 'Unable to parse image URLs for listing id: \s' % str(ListingID)
		return ImageUrl

def getRating(soup, ListingID):
	try:
		Rating = soup.findAll('meta', {"itemprop": "ratingValue"})[0]['content']
		return Rating
	except:
		print 'Rating not existing / Unable to parse Rating for listing id: \s' % str(ListingID)
		return Rating

def getReview(soup, ListingID):

	Review = []
	try:
		t = soup.findAll('div', {"data-key": "p3reviewsbundlejs_0"})
		obj = json.loads(t[1]['data-state'])
		Review = [obj['reviews'][i]['comments'] for i in range(len(obj['reviews']))]
		return Review
		
	except:
		print 'Review not existing / Unable to parse Review for listing id: \s' % str(ListingID)
		return Review

#########################################
## Hamel's Functions ####################     

def getAboutListing(tree, ListingID):
    """
    input: xmltree object
    output: string
    -----------------
    This function parses an individual listing's page to find 
    the "About This Listing" and extracts the associated text
    """  
    try:
    #Go To The Panel-Body
        elements = tree.xpath('//div[@class="row-space-8 row-space-top-8"]/h4')

        #Search For "About This Listing" In Elements    
        for element in elements:
            if element.text.find('About this listing') >= 0:
                #When You Find, it returns the text that comes afterwards
                return element.getnext().text.encode('utf8')

    except:
        print 'Error finding *About Listing* for listing ID: %s' % ListingID
        return 'No Description Found'

        
######################################
#### Save Results ####################
def writeToCSV(resultDict, outfile):
    
    colnames = [ 'ListingID', 'Title','UserID','baseurl',  'Price', 'ImageUrl', \
        'AboutListing', 'Lat','Long','BookInstantly', \
        'OverallCounter','PageCounter','PageNumber', \
        'ShortDesc', 'Rating', 'Review']
    
    with open(outfile, 'wb') as f:
        w = csv.DictWriter(f, fieldnames=colnames)
        w.writeheader()
        w.writerows(resultDict)     
        
#######################################
#  Testing ############################
#######################################

if __name__ == '__main__':   
    
    #towns = pd.read_csv('list_of_towns_bay.csv')
    #list_towns = towns['name']
    #Iterate Through Main Page To Get Results
    MainResults = IterateMainPage('paris-eiffel', 1)
    
    #Take The Main Results From Previous Step and Iterate Through Each Listing
    #To add more detail
    DetailResults = iterateDetail(MainResults)
    
    #Write Out Results To CSV File, using function I defined
    writeToCSV(DetailResults, 'test3.csv')
    #writeToCSV(MainResults, 'Notre-Dame--Paris--France-main.csv')
    
